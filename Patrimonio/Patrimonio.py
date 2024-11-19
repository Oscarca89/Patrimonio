import pandas as pd
import streamlit as st
import traceback

# Paso 1: Título de la aplicación
st.title("Automatización de patrimonio mensual 🍺")

# Paso 2: Subir el archivo semanal "centralizado BAT" desde la interfaz de Streamlit
archivo_subido = st.file_uploader("Sube el archivo", type=["xlsx"])

if archivo_subido is None:
    st.info("Sube el archivo de centralizado")
    st.stop()

# Paso 3: Leer el archivo subido
try:
    # Cargar el archivo Excel
    excel_data = pd.ExcelFile(archivo_subido)

    # Obtener los nombres de las hojas
    hojas = excel_data.sheet_names

    # Mostrar las primeras 3 hojas (si hay menos, mostrará todas las disponibles)
    hojas_a_previsualizar = hojas[:3]

    st.write("Hojas encontradas:", hojas)
    st.write(f"Previsualizando las primeras {len(hojas_a_previsualizar)} hojas:")

    # Crear una lista para almacenar los resúmenes
    hoja_1_2_unidas = None  # Variable para almacenar las hojas unidas

    # Iterar sobre las hojas a previsualizar
    for i, hoja in enumerate(hojas_a_previsualizar):
        st.write(f"### Hoja: {hoja}")
        
        # Leer la hoja
        df = pd.read_excel(excel_data, sheet_name=hoja)

        # Mostrar una tabla con las primeras filas de la hoja
        st.write(f"Vista previa de la hoja '{hoja}':")
        st.dataframe(df.head())

        # Si es la primera o segunda hoja, unirlas
        if i in [0, 1]:  # Índices de las hojas 1 y 2
            if hoja_1_2_unidas is None:
                hoja_1_2_unidas = df  # Inicializar con la primera hoja
            else:
                hoja_1_2_unidas = pd.concat([hoja_1_2_unidas, df], ignore_index=True)

    # Si se combinó exitosamente
    if hoja_1_2_unidas is not None:
        st.write("### Hoja combinada (1 y 2 unidas):")
        st.dataframe(hoja_1_2_unidas)

        # Calcular la suma total de las 3 primeras columnas
        try:
            columnas_suma = hoja_1_2_unidas.iloc[:, :3]  # Seleccionar las primeras 3 columnas
            suma_total = columnas_suma.sum(numeric_only=True)  # Sumar solo columnas numéricas
            st.write("### Suma total de las 3 primeras columnas:")
            st.write(suma_total)
        except Exception as e:
            st.error("No se pudieron calcular las sumas. Verifica que las primeras columnas sean numéricas.")
            st.error(str(e))

except Exception as e:
    st.error(f"Error al leer el archivo: {str(e)}")

