import pandas as pd
import openpyxl
import csv
import streamlit as st
import os
import plotly.graph_objects as go
from io import BytesIO

# Paso 1: Importar las librerías necesarias
st.title("Automatización de patrimonio mensual 🍺")

# Paso 2: Subir el archivo semanal "centralizado BAT" desde la interfaz de Streamlit
archivo_subido = st.file_uploader("Sube el archivo", type=["xlsx"])

if archivo_subido is None:
    st.info("Sube el archivo")
    st.stop()

# Paso 3: Leer el archivo Excel cargado y generar un resumen
try:
    # Cargar el archivo Excel
    excel_data = pd.ExcelFile(archivo_subido)

    # Obtener los nombres de las hojas
    hojas = excel_data.sheet_names

    # Mostrar un resumen de las primeras tres hojas (o menos si no hay tantas)
    st.subheader("Resumen de las primeras hojas")
    num_hojas = min(3, len(hojas))  # Limitar a 3 hojas o el total disponible
    for i in range(num_hojas):
        hoja = hojas[i]
        st.write(f"**Hoja {i+1}: {hoja}**")
        
        # Leer los primeros 5 registros de la hoja
        df = excel_data.parse(sheet_name=hoja, nrows=5)
        st.dataframe(df)
except Exception as e:
    st.error(f"Error al procesar el archivo: {e}")
