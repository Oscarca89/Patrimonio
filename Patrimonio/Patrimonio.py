import pandas as pd
import streamlit as st
import traceback

# Paso 1: Título de la aplicación
st.title("Carga y proceso de centralizado BAT")

# Paso 2: Subir el archivo semanal "centralizado BAT" desde la interfaz de Streamlit
archivo_subido = st.file_uploader("Sube el archivo", type=["xlsx"])

if archivo_subido is None:
    st.info("Sube el archivo de centralizado")
    st.stop()

# Paso 3: Leer el archivo subido y manejar excepciones detalladamente
try:
    # Cargar el archivo Excel
    st.write("Cargando el archivo...")
    excel_data = pd.ExcelFile(archivo_subido)

    # Obtener los nombres de las hojas
    hojas = excel_data.sheet_names
    st.write("Hojas encontradas:", hojas)

    # Mostrar las primeras 3 hojas (si hay menos, mostrará todas las disponibles)
    hojas_a_previsualizar = hojas[:3]
    st.write(f"Previsualizando las primeras {len(hojas_a_previsualizar)} hojas:")

    # Crear una lista para almacenar los resúmenes
    resumenes = []
    hoja_1_2_unidas = None  # Variable para almacenar las hojas unidas

    # Iterar sobre las hojas a previsualizar
    for i, hoja in enumerate(hojas_a_previsualizar):
        st.write(f"### Leyendo hoja: {hoja}")
        
        # Leer la hoja
        df = pd.read_excel(excel_data, sheet_name=hoja)
        st.write(f"Dimensiones de la hoja '{hoja}': {df.shape}")

        # Generar el resumen de la hoja
        resumen = {
            "Hoja": hoja,
            "Filas": len(df),
            "Columnas": len(df.columns),
            "Columnas principales": list(df.columns[:5]) if len(df.columns) > 5 else list(df.columns)
        }
        resumenes.append(resumen)

        # Mostrar una tabla con las primeras filas de la hoja
        st.write(f"Resumen de la hoja '{hoja}':")
        st.write(resumen)
        st.write("Vista previa:")
        st.dataframe(df.head())

        # Si es la primera o segunda hoja, unirlas
        if i in [0, 1]:  # Índices de las hojas 1 y 2
            if hoja_1_2_unidas is None:
                hoja_1_2_unidas = df  # Inicializar con la primera hoja
            else:
                if list(hoja_1_2_unidas.columns) == list(df.columns):
                    hoja_1_2_unidas = pd.concat([hoja_1_2_unidas, df], ignore_index=True)
                    st.write(f"Unidas las filas de la hoja '{hoja}' con la anterior.")
                else:
                    st.warning(f"Las columnas de la hoja {hoja} no coinciden con la hoja anterior. No se unirán.")

    # Mostrar la hoja combinada
    if hoja_1_2_unidas is not None:
        st.write("### Hoja combinada (1 y 2 unidas):")
        st.dataframe(hoja_1_2_unidas)

except Exception as e:
    st.error("Se produjo un error al leer el archivo:")
    error_message = traceback.format_exc()
    st.code(error_message, language="plaintext")

