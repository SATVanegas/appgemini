import streamlit as st
import re
import random

# Título de la aplicación
st.title('Generador de Poemas Aleatorios con Regex por Santiago Vanegas')

# Explicación del funcionamiento
st.write("""
Esta aplicación genera un poema aleatorio basado en las palabras que ingreses. 
Utilizamos expresiones regulares para buscar patrones en tu entrada y jugar con ellos de manera creativa.
""")

# Entrada de texto
entrada = st.text_area('Escribe algo que te inspire (pueden ser palabras o frases):')

# Función para generar un poema basado en la entrada
def generar_poema(texto):
    # Usamos expresiones regulares para encontrar palabras que empiecen con una letra mayúscula
    palabras_mayus = re.findall(r'\b[A-Z][a-z]*\b', texto)
    # Encontramos las palabras que terminan en "o" o "a"
    palabras_terminadas = re.findall(r'\b\w+[oa]\b', texto)
    # Generamos algunas frases aleatorias con patrones
    lineas_poeticas = [
        f"El viento susurra sobre {random.choice(palabras_mayus)}.",
        f"{random.choice(palabras_terminadas)} florecen a la luz de la luna.",
        f"¿Quién puede comprender el suspiro de {random.choice(palabras_terminadas)}?",
        f"La sombra de {random.choice(palabras_mayus)} danza en el atardecer.",
        f"Y así, {random.choice(palabras_terminadas)} van cayendo como estrellas perdidas."
    ]
    # Combinamos las líneas generadas en un poema
    poema = "\n".join(lineas_poeticas)
    return poema

# Si hay entrada de texto, generamos un poema
if entrada:
    poema_generado = generar_poema(entrada)
    st.write("### Tu poema aleatorio:")
    st.text(poema_generado)
else:
    st.write("¡Escribe algo para generar tu poema!")

