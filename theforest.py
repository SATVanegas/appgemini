# Importar las bibliotecas necesarias
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage

# Cargar el archivo CSV
df = pd.read_csv('deforestacion.csv')

# Explorar las primeras filas del DataFrame
print("Primeras filas del DataFrame:")
print(df.head())

# Verificar la información general del DataFrame
print("\nInformación del DataFrame:")
print(df.info())

# Verificar valores nulos
print("\nValores nulos por columna:")
print(df.isnull().sum())

# Calcular la superficie deforestada total
superficie_total = df['Superficie_Deforestada'].sum()
print(f"\nSuperficie deforestada total: {superficie_total}")

# Calcular la tasa de deforestación promedio
tasa_promedio = df['Tasa_Deforestacion'].mean()
print(f"Tasa de deforestación promedio: {tasa_promedio}")

# Calcular la superficie deforestada por tipo de vegetación
superficie_por_vegetacion = df.groupby('Tipo_Vegetacion')['Superficie_Deforestada'].sum()
print("\nSuperficie deforestada por tipo de vegetación:")
print(superficie_por_vegetacion)

# Convertir el DataFrame en un GeoDataFrame
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitud, df.Latitud))

# Visualizar las zonas deforestadas en un mapa mundial
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
ax = world.plot(figsize=(10, 6), color='lightgray')
gdf.plot(ax=ax, color='red', markersize=5)
plt.title('Zonas Deforestadas')
plt.show()

# Función para crear mapas personalizados según variables seleccionadas
def mapa_personalizado(df, variables, rangos):
    filtro = np.ones(len(df), dtype=bool)
    for var, rango in zip(variables, rangos):
        filtro &= (df[var] >= rango[0]) & (df[var] <= rango[1])
    
    gdf_filtrado = gdf[filtro]
    
    ax = world.plot(figsize=(10, 6), color='lightgray')
    gdf_filtrado.plot(ax=ax, color='red', markersize=5)
    plt.title('Mapa Personalizado')
    plt.show()

# Ejemplo de uso de la función mapa_personalizado
variables = ['Latitud', 'Longitud', 'Altitud', 'Precipitacion']
rangos = [(-5, 5), (-80, -50), (0, 1000), (0, 2000)]
mapa_personalizado(df, variables, rangos)

# Análisis de clúster de superficies deforestadas
X = df[['Latitud', 'Longitud', 'Superficie_Deforestada']]
Z = linkage(X, method='ward')

# Graficar el dendrograma
plt.figure(figsize=(10, 6))
dendrogram(Z)
plt.title('Dendrograma de Clúster de Superficies Deforestadas')
plt.xlabel('Índice del Punto')
plt.ylabel('Distancia')
plt.show()

# Gráfico de torta según tipo de vegetación
plt.figure(figsize=(8, 8))
plt.pie(superficie_por_vegetacion, labels=superficie_por_vegetacion.index, autopct='%1.1f%%', startangle=140)
plt.title('Distribución de la Superficie Deforestada por Tipo de Vegetación')
plt.show()
