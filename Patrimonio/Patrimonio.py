import pandas as pd
import openpyxl
import streamlit as st
from io import BytesIO
import plotly.express as px


def leer_hoja_excel_optimizadamente(archivo, hoja, max_filas=None):
    """
    Lee una hoja de Excel en fragmentos utilizando openpyxl para optimizar memoria.
    Maneja encabezados y celdas vacías.
    """
    wb = openpyxl.load_workbook(archivo, read_only=True)
    ws = wb[hoja]

    # Leer encabezados (primera fila)
    encabezados = [
        cell.value if cell.value is not None else f"Columna_{idx+1}"
        for idx, cell in enumerate(ws[1])
    ]

    # Leer datos de filas (excluyendo encabezados)
    filas = []
    for row in ws.iter_rows(min_row=2, max_row=max_filas, values_only=True):
        if any(cell is not None for cell in row):  # Ignorar filas completamente vacías
            filas.append(row)

    # Convertir a DataFrame
    df = pd.DataFrame(filas, columns=encabezados)
    return df


def cargar_datos_optimizado(archivo, hojas):
    """
    Carga y concatena múltiples hojas de Excel usando una carga optimizada.
    """
    df_list = [leer_hoja_excel_optimizadamente(archivo, hoja) for hoja in hojas]
    return pd.concat(df_list, ignore_index=True)


def cargar_procesar_archivo():
    # Título de la app
    st.title("Automatización de patrimonio mensual 🍺")

    # Subir el archivo
    archivo_subido = st.file_uploader("Sube el archivo (Máx 200MB)", type=["xlsx"])

    if archivo_subido is None:
        st.info("Sube el archivo para continuar")
        st.stop()

    hojas_requeridas = ['OCT 2024 PT1', 'OCT 2024 PT2']

    # Cargar datos optimizadamente
    try:
        st.info("Cargando datos, por favor espera...")
        df_unido = cargar_datos_optimizado(archivo_subido, hojas_requeridas)
        st.success("Datos cargados correctamente.")
    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
        st.stop()

    # Mostrar un resumen de los datos
    st.write("Resumen de los datos cargados:")
    st.dataframe(df_unido.head(10))

    # Filtros dinámicos en la barra lateral
    st.sidebar.header("Filtros dinámicos")
    columnas_filtro = ["Soc.", "Clase", "Supranumero", "GZ"]

    for columna in columnas_filtro:
        if columna in df_unido.columns:
            valores_unicos = df_unido[columna].dropna().unique()
            seleccionados = st.sidebar.multiselect(f"Filtrar por {columna}", valores_unicos, default=valores_unicos)
            if seleccionados:
                df_unido = df_unido[df_unido[columna].isin(seleccionados)]

    # Mostrar los datos filtrados
    st.write("Datos después de aplicar los filtros dinámicos:")
    st.dataframe(df_unido)

    # Gráfica del total de columnas seleccionadas
    columnas_totales = ["Val.adq.", "Amo acum.", "Val.cont."]
    if all(col in df_unido.columns for col in columnas_totales):
        df_totales = df_unido[columnas_totales].sum().reset_index()
        df_totales.columns = ["Columna", "Total"]

        # Crear la gráfica
        fig = px.bar(df_totales, x="Columna", y="Total", title="Totales por columna", labels={"Total": "Total", "Columna": "Columna"})
        st.plotly_chart(fig)
    else:
        st.warning("No se encontraron todas las columnas necesarias para la gráfica.")

# Llamada principal a la función en Streamlit
if __name__ == "__main__":
    cargar_procesar_archivo()



