import streamlit as st
import re

def validar_nombre(nombre):
    patron = r"^[A-Z][a-zA-Z]*$"
    return re.match(patron, nombre)

def validar_email(email):
    patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(patron, email)

def validar_telefono(telefono):
    # Adapta el patrón según el formato de teléfono que desees validar
    patron = r"^\d{3}-\d{3}-\d{4}$"  # Ejemplo: 123-456-7890
    return re.match(patron, telefono)

def validar_fecha(fecha):
    # Adapta el patrón según el formato de fecha que desees validar
    patron = r"^\d{4}-\d{2}-\d{2}$"  # Ejemplo: 2023-11-22
    return re.match(patron, fecha)

# Interfaz de usuario
st.title("Formulario de Validación")

nombre = st.text_input("Nombre:")
email = st.text_input("Correo electrónico:")
telefono = st.text_input("Teléfono:")
fecha = st.text_input("Fecha (AAAA-MM-DD):")

if st.button("Enviar"):
    if not validar_nombre(nombre):
        st.error("El nombre debe comenzar con mayúscula y contener solo letras.")
    if not validar_email(email):
        st.error("El correo electrónico no es válido.")
    if not validar_telefono(telefono):
        st.error("El número de teléfono no es válido.")
    if not validar_fecha(fecha):
        st.error("La fecha no es válida.")
    else:
        st.success("¡Datos válidos!")
