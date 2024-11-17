import pandas as pd
import streamlit as st
import plotly.express as px

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

    # Paso 5: Renombrar las columnas repetidas
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

    # Paso 6: Filtrar por columnas adicionales en la barra lateral
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

    # Paso 7: Gráfica del total de columnas seleccionadas
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


# Llamada principal a la función en Streamlit
if __name__ == "__main__":
    cargar_procesar_archivo()

