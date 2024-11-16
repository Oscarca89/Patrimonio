import pandas as pd
import streamlit as st
from io import BytesIO

def cargar_procesar_archivo():
    # Paso 1: Título de la app
    st.title("Automatización de patrimonio mensual 🍺")

    # Paso 2: Subir el archivo semanal "Patrimonio mensual"
    archivo_subido = st.file_uploader("Sube el archivo", type=["xlsx"])

    if archivo_subido is None:
        st.info("Sube el archivo para continuar")
        st.stop()

    # Paso 3: Verificar que el archivo contenga las hojas específicas
    try:
        with pd.ExcelFile(archivo_subido) as xls:
            hojas_requeridas = ['OCT 2024 PT1', 'OCT 2024 PT2']
            if not all(hoja in xls.sheet_names for hoja in hojas_requeridas):
                st.error(f"El archivo debe contener las hojas: {hojas_requeridas}")
                st.stop()

            # Leer ambas hojas comenzando desde la fila 2 (índice 1 en pandas)
            df_hoja1 = pd.read_excel(xls, sheet_name='OCT 2024 PT1', header=1)
            df_hoja2 = pd.read_excel(xls, sheet_name='OCT 2024 PT2', header=1)
            st.success("Hojas cargadas correctamente.")

    except Exception as e:
        st.error(f"Error al cargar el archivo: {e}")
        st.stop()

    # Paso 4: Unir los dos dataframes
    try:
        df_unido = pd.concat([df_hoja1, df_hoja2], ignore_index=True)
        st.write("Los datos han sido unidos exitosamente.")
    except Exception as e:
        st.error(f"Error al unir los datos: {e}")
        st.stop()

    # Paso 5: Filtrar por las columnas relevantes
    columnas_interes = ["Amo acum.", "Val.cont.", "Val.adq."]
    df_filtrado = df_unido[[col for col in columnas_interes if col in df_unido.columns]]

    # Mostrar datos y opciones de filtrado
    st.write("Datos filtrados por las columnas de interés:")
    st.dataframe(df_filtrado)

    # Filtros por columnas específicas
    for columna in columnas_interes:
        if columna in df_filtrado.columns:
            valores_unicos = df_filtrado[columna].dropna().unique()
            seleccionados = st.multiselect(f"Filtrar por {columna}", valores_unicos)
            if seleccionados:
                df_filtrado = df_filtrado[df_filtrado[columna].isin(seleccionados)]

    # Mostrar datos finales filtrados
    st.write("Datos finales después del filtrado:")
    st.dataframe(df_filtrado)

# Llamada principal a la función en Streamlit
if __name__ == "__main__":
    cargar_procesar_archivo()
