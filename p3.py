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

    productos = []
    contactos = []

    for fila in filas:
        # Buscar información de productos
        producto = patron_producto.search(fila)
        if producto:
            productos.append(producto.groupdict())

        # Buscar información de contacto
        contacto = patron_contacto.search(fila)
        if contacto:
            contactos.append(contacto.groupdict())

    # Crear DataFrames
    df_productos = pd.DataFrame(productos)
    df_contactos = pd.DataFrame(contactos)

    # Verificar DataFrames vacíos y devolver resultados
    if df_productos.empty:
        df_productos = pd.DataFrame(columns=["Código del producto", "Precio", "Fecha de compra"])
    if df_contactos.empty:
        df_contactos = pd.DataFrame(columns=["Nombre", "Correo Electrónico", "Teléfono"])

    return df_productos, df_contactos

# Función para convertir DataFrame a archivo Excel
def convertir_a_excel(df_productos, df_contactos):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df_productos.to_excel(writer, sheet_name="Productos", index=False)
        df_contactos.to_excel(writer, sheet_name="Contactos", index=False)
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
        df_productos, df_contactos = procesar_archivo(archivo_subido.read())

        # Mostrar DataFrames
        st.subheader("Productos extraídos")
        st.dataframe(df_productos)
        
        st.subheader("Contactos extraídos")
        st.dataframe(df_contactos)

        # Botón para descargar archivo Excel
        if st.button("Generar archivo Excel"):
            archivo_excel = convertir_a_excel(df_productos, df_contactos)
            st.download_button(
                label="Descargar archivo Excel",
                data=archivo_excel,
                file_name="productos_y_contactos.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    except Exception as e:
        st.error(f"Error procesando el archivo: {e}")
