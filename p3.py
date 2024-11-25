import streamlit as st
import re
import pandas as pd
from io import BytesIO

def to_csv(dataframe):
    output = BytesIO()
    dataframe.to_csv(output, index=False, encoding="utf-8")
    processed_data = output.getvalue().decode("utf-8")  # Decode bytes to string
    return processed_data



def procesar_datos(content):
    # Regex para cada campo
    regex_serie = re.compile(r'\b\d{6}\b')  # 6 dígitos para el número de serie
    regex_correo = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')  # Correo electrónico válido
    regex_nombre = re.compile(r'[A-Z][a-z]+\s[A-Z][a-z]+')  # Nombre completo
    regex_telefono = re.compile(r'\+57\s?\d{10}')  # Número de teléfono
    regex_fecha = re.compile(r'\b\d{2}/\d{2}/\d{2}\b')  # Fecha en formato DD/MM/YY
    regex_valor = re.compile(r'\d+\.\d{2}')  # Valor en formato decimal
    
    # Lista para almacenar los datos procesados
    data = []

    # Procesar cada línea del archivo
    for linea in content.splitlines():
        # Buscar los campos en la línea
        serie = regex_serie.search(linea)
        correo = regex_correo.search(linea)
        nombre = regex_nombre.findall(linea)  # Puede haber más de un nombre
        telefono = regex_telefono.search(linea)
        fecha = regex_fecha.search(linea)
        valor = regex_valor.search(linea)
        
        # Validar y asignar los campos encontrados
        datos = {
            "Número de Serie": serie.group() if serie else "",
            "Nombre del Producto": nombre[1] if len(nombre) > 1 else "",
            "Valor": float(valor.group()) if valor else 0.0,
            "Fecha de Compra": fecha.group() if fecha else "",
            "Contacto (Nombre)": nombre[0] if len(nombre) > 0 else "",
            "Correo Electrónico": correo.group() if correo else "",
            "Teléfono": telefono.group() if telefono else "",
        }
        data.append(datos)
    return data
    
# Configuración de la app
st.title("Generador de archivo Excel con regex")
st.write(
    """
    Esta aplicación utiliza expresiones regulares para procesar un archivo 
    CSV y genera un archivo Excel estructurado con los datos encontrados.
    """
)

# Cargar el archivo CSV
uploaded_file = st.file_uploader("Sube tu archivo regex_productos.csv", type="csv")

if uploaded_file:
    # Leer el contenido del archivo
    content = uploaded_file.read().decode("utf-8")

    # Extraer los datos
    data = procesar_datos(content)
    if data:
        
        
        # Crear un DataFrame
        df = pd.DataFrame(data)

        # Mostrar la tabla en la app
        st.write("Datos procesados:")
        st.dataframe(df)

        #Convertir a Excel

        excel_data = to_csv(df)

        # Botón de descarga
        st.download_button(
            label="Descargar archivo Excel",
            data=excel_data,
            file_name="productos_procesados.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    else:
        st.error("No se encontraron coincidencias en el archivo. Verifica el formato.")
