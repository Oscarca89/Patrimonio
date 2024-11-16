import pandas as pd
import streamlit as st

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

    # Mostrar el DataFrame unido con los nuevos nombres
    st.write("Vista previa del DataFrame con columnas renombradas:")
    st.dataframe(df_unido)

    # Paso 6: Filtrar por las columnas de interés
    columnas_interes = ["Val.adq. 01", "Amo acum. 01", "Val.cont. 01"]
    df_filtrado = df_unido[[col for col in columnas_interes if col in df_unido.columns]]

    # Mostrar datos finales
    st.write("Datos finales después del procesamiento:")
    st.dataframe(df_filtrado)

# Llamada principal a la función en Streamlit
if __name__ == "__main__":
    cargar_procesar_archivo()

