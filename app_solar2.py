# -*- coding: utf-8 -*-
"""Despliegue Final — Energía Solar"""

# ======================
# 🔹 Importar librerías
# ======================
import numpy as np
import pandas as pd
import streamlit as st
import joblib

# ======================
# Cargar el modelo
# ======================
model = joblib.load("pipeline_modelo.pkl")

# ======================
#  Configuración de interfaz
# ======================
st.title(" Predicción de Energía Solar — Despliegue de Modelo")

st.markdown("""
Sube un archivo Excel con las **variables meteorológicas** para predecir la
**capacidad energética esperada (kW)** según el modelo entrenado.
""")

# ======================
#  Cargar archivo Excel
# ======================
uploaded_file = st.file_uploader(" Sube tu archivo Excel (.xlsx) con los datos futuros", type=["xlsx"])

if uploaded_file is not None:
    try:
        # Leer el archivo subido
        data = pd.read_excel(uploaded_file)
        st.success(" Archivo cargado exitosamente")
        
        # Mostrar vista previa
        st.write("### Vista previa de los datos:")
        st.dataframe(data.head())

        # ======================
        #  Realizar predicciones
        # ======================
        preds = model.predict(data)
        data["Predicción (kW)"] = preds

        # Mostrar resultados
        st.write("### Resultados de la predicción:")
        st.dataframe(data)

        # ======================
        #  Descargar resultados
        # ======================
        output_path = "predicciones_resultado.xlsx"
        data.to_excel(output_path, index=False)

        with open(output_path, "rb") as f:
            st.download_button(
                label=" Descargar archivo con predicciones",
                data=f,
                file_name="predicciones_resultado.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f" Error al procesar el archivo: {e}")

else:
    st.info("Por favor, sube un archivo Excel para generar predicciones.")
