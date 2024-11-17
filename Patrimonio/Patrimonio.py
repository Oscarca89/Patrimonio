import pandas as pd
import streamlit as st
import plotly.express as px

def cargar_datos_por_partes(archivo_subido, hojas, chunksize=50000):
    """
    Carga datos desde un archivo Excel por partes usando Pandas.
    """
    df_total = []
    for hoja in hojas:
        chunk_iterador = pd.read_excel(archivo_subido, sheet_name=hoja, header=1, chunksize=chunksize)
        for chunk in chunk_iterador:
            df_total.append(chunk)
    return pd.concat(df_total, ignore_index=True)


def optimizar_columnas(df):
    """
    Optimiza tipos de columnas para reducir uso de memoria.
    """
    for col in df.select_dtypes(include=["int64", "float64"]).columns:
        df[col] = pd.to_numeric(df[col], downcast="unsigned")
    for col in df.select_dtypes(include=["object"]).columns:
        if df[col].nunique() / len(df[col]) < 0.5:  # Si hay pocos valores únicos
            df[col] = df[col].astype("category")
    return df


def cargar_procesar_archivo():
    # Título de la app
    st.title("Automatización de patrimonio mensual 🍺")

    # Subir el archivo
    archivo_subido = st.file_uploader("Sube el archivo", type=["xlsx"])

    if archivo_subido is None:
        st.info("Sube el archivo para continuar")
        st.stop()

    hojas_requeridas = ['OCT 2024 PT1', 'OCT 2024 PT2']

    # Cargar datos por partes
    try:
        st.info("Cargando datos por partes... Esto puede tardar unos minutos.")
        df_unido = cargar_datos_por_partes(archivo_subido, hojas_requeridas)
        st.success("Datos cargados correctamente.")
    except Exception as e:
        st.error(f"Error al cargar el archivo: {e}")
        st.stop()

    # Renombrar columnas repetidas
    renombrar_columnas = {
        "Val.adq.": ["Val.adq. 01", "Val.adq. 03", "Val.adq. 50"],
        "Amo acum.": ["Amo acum. 01", "Amo acum. 03", "Amo acum. 50"],
        "Val.cont.": ["Val.cont. 01", "Val.cont. 03", "Val.cont. 50"],
    }

    nuevos_nombres = []
    contador = {"Val.adq.": 0, "Amo acum.": 0, "Val.cont.": 0}
    for col in df_unido.columns:
        if col in renombrar_columnas and contador[col] < len(renombrar_columnas[col]):
            nuevo_nombre = renombrar_columnas[col][contador[col]]
            nuevos_nombres.append(nuevo_nombre)
            contador[col] += 1
        else:
            nuevos_nombres.append(col)

    df_unido.columns = nuevos_nombres

    # Optimizar columnas
    df_unido = optimizar_columnas(df_unido)

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
    columnas_totales = ["Val.adq. 01", "Amo acum. 01", "Val.cont. 01"]
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

