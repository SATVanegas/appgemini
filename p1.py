import streamlit as st
import re

def evaluar_contrasena(contrasena):
    """Evalúa la fortaleza de una contraseña utilizando expresiones regulares.

    Args:
        contrasena (str): La contraseña a evaluar.

    Returns:
        str: Un mensaje indicando la fortaleza de la contraseña y sugerencias.
    """

    # Expresiones regulares para cada criterio
    mayusculas = re.compile(r'[A-Z]')
    minusculas = re.compile(r'[a-z]')
    numeros = re.compile(r'\d')
    especiales = re.compile(r'[^a-zA-Z0-9]')

    # Verificar cada criterio
    longitud_valida = len(contrasena) >= 8
    tiene_mayusculas = mayusculas.search(contrasena)
    tiene_minusculas = minusculas.search(contrasena)
    tiene_numeros = numeros.search(contrasena)
    tiene_especiales = especiales.search(contrasena)

    # Mensaje y sugerencias
    if longitud_valida and tiene_mayusculas and tiene_minusculas and tiene_numeros and tiene_especiales:
        return "Excelente! Tu contraseña es muy segura."
    else:
        sugerencias = []
        if not longitud_valida:
            sugerencias.append("La contraseña debe tener al menos 8 caracteres.")
        if not tiene_mayusculas:
            sugerencias.append("Incluye al menos una letra mayúscula.")
        if not tiene_minusculas:
            sugerencias.append("Incluye al menos una letra minúscula.")
        if not tiene_numeros:
            sugerencias.append("Incluye al menos un número.")
        if not tiene_especiales:
            sugerencias.append("Incluye al menos un carácter especial (!, $, #, etc.).")
        return "Tu contraseña podría ser más segura. Sugerencias:\n" + "\n".join(sugerencias)

# Interfaz de usuario con Streamlit
st.title("Evaluador de Contraseñas")
contrasena = st.text_input("Ingrese su contraseña:")

st.write("Desarrollado por: Sebastián Rodríguez Suarez")

if contrasena:
    resultado = evaluar_contrasena(contrasena)
    st.write(resultado)
