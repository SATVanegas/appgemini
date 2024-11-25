import re
import pandas as pd
import streamlit as st
from io import BytesIO

# Función para procesar el archivo CSV y extraer información con regex
def procesar_archivo(csv_data):
    # Leer el archivo como texto
    text = csv_data.decode('utf-8')
    
    # Definir patrones regex
    patron_producto = re.compile(r"(?P<numero_serie>\w+-\d+),\s*(?P<nombre_producto>.+?),\s*\$(?P<valor>\d+\.\d{2}),\s*(?P<fecha_compra>\d{2}/\d{2}/\d{2})")
    patron_contacto = re.compile(r"(?P<nombre>[\w\s]+),\s*(?P<email>[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+),\s*(?P<telefono>\d{7,15})")

    # Buscar coincidencias para productos y contactos
    productos = patron_producto.findall(text)
    contactos = patron_contacto.findall(text)

    # Crear DataFrames
    df_productos = pd.DataFrame(productos, columns=["Número de serie", "Nombre del producto", "Valor", "Fecha de compra"])
    df_contactos = pd.DataFrame(contactos, columns=["Nombre", "Correo Electrónico", "Teléfono"])
    
    return df_productos, df_contactos

# Función para convertir DataFrame a archivo Excel
def convertir_a_excel(df_productos, df_contactos):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df_productos.to_excel(writer, sheet_name="Productos", index=False)
        df_contactos.to_excel(writer, sheet_name="Contactos", index=False)
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
                file_name="productos_y_contactos.xls",
                mime="application/vnd.ms-excel"
            )
    except Exception as e:
        st.error(f"Error procesando el archivo: {e}")
