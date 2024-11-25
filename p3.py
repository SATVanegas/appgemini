import re
import pandas as pd
import streamlit as st
from io import BytesIO

# Función para procesar el archivo CSV y extraer información con regex
def procesar_archivo(csv_data):
    # Leer el archivo como texto
    text = csv_data.decode('utf-8')
    
    # Definir patrones regex
    patron_producto = re.compile(r"(?P<codigo>\d{5,6}),.*?,.*?(?P<precio>\d+\.\d+),.*?(?P<fecha>\d{2}/\d{2}/\d{2})")
    patron_contacto = re.compile(r"(?P<nombre>[A-Za-z\s]+),.*?(?P<email>[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+),.*?(?P<telefono>\+\d{1,3}\s\d{7,15})")

    # Buscar coincidencias para productos y contactos
    productos = patron_producto.findall(text)
    contactos = patron_contacto.findall(text)

    # Crear DataFrame combinado
    datos_combinados = []
    max_filas = max(len(productos), len(contactos))

    for i in range(max_filas):
        fila = {
            "Código del Producto": productos[i][0] if i < len(productos) else None,
            "Precio": productos[i][1] if i < len(productos) else None,
            "Fecha de Compra": productos[i][2] if i < len(productos) else None,
            "Nombre": contactos[i][0] if i < len(contactos) else None,
            "Correo Electrónico": contactos[i][1] if i < len(contactos) else None,
            "Teléfono": contactos[i][2] if i < len(contactos) else None,
        }
        datos_combinados.append(fila)

    df_combinado = pd.DataFrame(datos_combinados)
    
    return df_combinado

# Función para convertir DataFrame a archivo Excel
def convertir_a_excel(df_combinado):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df_combinado.to_excel(writer, sheet_name="Datos Extraídos", index=False)
    return output.getvalue()

# Interfaz de Streamlit
st.title("Procesador de archivo CSV con Regex")
st.write("Sube un archivo CSV para procesar la información.")

# Subida de archivo
archivo_subido = st.file_uploader("Sube tu archivo CSV", type=["csv"])

if archivo_subido is not None:
    # Procesar el archivo
    try:
        df_combinado = procesar_archivo(archivo_subido.read())

        # Mostrar DataFrame combinado
        st.subheader("Datos extraídos")
        st.dataframe(df_combinado)

        # Botón para descargar archivo Excel
        if st.button("Generar archivo Excel"):
            archivo_excel = convertir_a_excel(df_combinado)
            st.download_button(
                label="Descargar archivo Excel",
                data=archivo_excel,
                file_name="datos_extraidos.xls",
                mime="application/vnd.ms-excel"
            )
    except Exception as e:
        st.error(f"Error procesando el archivo: {e}")
