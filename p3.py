import re
import pandas as pd
import streamlit as st
from io import BytesIO

# Función para procesar el archivo CSV y extraer información con regex
def procesar_archivo(csv_data):
    # Leer el archivo como texto
    text = csv_data.decode('utf-8')
    filas = text.split("\n")

    # Definir patrones regex
    patron_producto = re.compile(
        r"(?P<codigo_producto>\d{5,6}),\s*\$(?P<precio>\d+\.\d+),\s*(?P<fecha_compra>\d{2}/\d{2}/\d{2})"
    )
    patron_contacto = re.compile(
        r"(?P<nombre>[A-Za-z\s]+),\s*(?P<email>[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+),\s*(?P<telefono>\+57\s\d{10})"
    )

    registros = []

    for fila in filas:
        # Buscar información de productos
        producto = patron_producto.search(fila)
        contacto = patron_contacto.search(fila)
        
        # Construir un registro con datos disponibles
        registro = {
            "Código del Producto": producto.group("codigo_producto") if producto else "",
            "Precio": producto.group("precio") if producto else "",
            "Fecha de Compra": producto.group("fecha_compra") if producto else "",
            "Nombre": contacto.group("nombre") if contacto else "",
            "Correo Electrónico": contacto.group("email") if contacto else "",
            "Teléfono": contacto.group("telefono") if contacto else "",
        }
        registros.append(registro)

    # Crear un DataFrame con los registros
    df = pd.DataFrame(registros)
    return df

# Función para convertir DataFrame a archivo Excel
def convertir_a_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Datos Extraídos", index=False)
    output.seek(0)
    return output.getvalue()

# Interfaz de Streamlit
st.title("Procesador de archivo CSV con Regex")
st.write("Sube un archivo CSV para procesar la información.")

# Subida de archivo
archivo_subido = st.file_uploader("Sube tu archivo CSV", type=["csv"])

if archivo_subido is not None:
    # Procesar el archivo
    try:
        df_datos = procesar_archivo(archivo_subido.read())

        # Mostrar DataFrame
        st.subheader("Datos extraídos")
        st.dataframe(df_datos)

        # Botón para descargar archivo Excel
        if st.button("Generar archivo Excel"):
            archivo_excel = convertir_a_excel(df_datos)
            st.download_button(
                label="Descargar archivo Excel",
                data=archivo_excel,
                file_name="datos_extraidos.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    except Exception as e:
        st.error(f"Error procesando el archivo: {e}")
