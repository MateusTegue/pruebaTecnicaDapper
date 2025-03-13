import pandas as pd
import os 

# ruta donde se van a guardar los archivos generados despues del analisis 
os.makedirs('resultados', exist_ok=True)

# cargar cargamos el archivo donde  estan los datos a analizar
rutaArchivo = "./data/precios_combustibles_mensuales.csv"
df = pd.read_csv(rutaArchivo)

# Eliminar fechas duplicadas
df.drop_duplicates(subset='Fecha', keep='first', inplace=True)


#Eliminamos los valores nulos
df.dropna(inplace=True)

# convertir el formato de fecha 
df['Fecha'] =pd.to_datetime( df['Fecha'] )

# agrupar por mes y sacar el promedio
def calcular_promedio_nacional(df):
    return df.groupby('Fecha', as_index=False)[['Gasolina MC ($/gal)', 'ACPM ($/gal)']].mean()

# calcular variación mensual porcentual
def calcular_variacion_mensual(df):
    df = df.sort_values(by='Fecha' )
    df['var_gasolina'] = df['Gasolina MC ($/gal)'].pct_change() * 100
    df['var_acpm'] = df['ACPM ($/gal)'].pct_change() * 100
    return df

# calcular variación anual porcentual
def calcular_variacion_anual(df):
    df['anio'] = df['Fecha'].dt.year
    df['mes'] = df['Fecha'].dt.month

    # Agrupar por año y mes 
    df_agrupado = df.groupby(['anio', 'mes'], as_index= False)[['Gasolina MC ($/gal)', 'ACPM ($/gal)']].mean()

    # Crear la tabla  anual
    df_anual =df_agrupado.pivot(index= 'mes', columns='anio', values=['Gasolina MC ($/gal)', 'ACPM ($/gal)'])
    df_anual =df_anual.pct_change(axis= 'columns') * 100
    
    return df_anual.reset_index()


# calcular promedio móvil secuencial de 3 meses y creamos un archivo .csv
def calcular_promedio_movil_secuencial(df):
    df = df.sort_values(by='Fecha' )
    df['prom_movil_gasolina'] = df['Gasolina MC ($/gal)'].rolling(window=3, min_periods=1).mean()
    df['prom_movil_acpm'] =df['ACPM ($/gal)'].rolling(window=3, min_periods=1).mean()
    return df


# calcular promedio móvil anualizado de 3 años
def calcular_promedio_movil_anualizado(df):
    df['anio'] =df['Fecha'].dt.year
    df['mes'] =df['Fecha'].dt.month
    df_anualizado =df.groupby('mes')[['Gasolina MC ($/gal)', 'ACPM ($/gal)']].rolling(window=3, min_periods=1).mean().reset_index()
    return df_anualizado

# llamamos las funciones para hacer el respectivo calculo de cada una de la operaciones 
df_promedio=calcular_promedio_nacional(df)
df_variacion_mensual=calcular_variacion_mensual(df)
df_variacion_anual=calcular_variacion_anual(df)
df_promedio_movil_secuencial=calcular_promedio_movil_secuencial(df)
df_promedio_movil_anualizado=calcular_promedio_movil_anualizado(df)

# guardar los resultados en archivos csv
df_promedio.to_csv('resultados/promedio_nacional.csv ',index= False )
df_variacion_mensual.to_csv('resultados/variacion_mensual.csv ',index= False )
df_variacion_anual.to_csv('resultados/variacion_anual.csv ',index= False )
df_promedio_movil_secuencial.to_csv('resultados/promedio_movil_secuencial.csv ',index= False)
df_promedio_movil_anualizado.to_csv('resultados/promedio_movil_anualizado.csv ',index= False)