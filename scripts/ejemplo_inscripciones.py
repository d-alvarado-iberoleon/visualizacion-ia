# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 12:41:41 2026

@author: alvaradocde
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("../data/datos_inscripcion.csv", 
                 index_col='Ciudad')
print(df.info())
print(df.describe())

promedios = df.agg('mean')

grados = ['Preescolar', 'Primaria', 'Secundaria']
cols1 =['Preescolar A1', 'Primaria A1', 'Secundaria A1']
cols2 =['Preescolar A2', 'Primaria A2', 'Secundaria A2']
plt.figure()
plt.barh(grados, promedios[cols1].values)
plt.barh(grados, promedios[cols2].values, left=promedios[cols1].values)
plt.show()


# Seleccionar columnas del Año 2
datos = df[["Preescolar A2", "Primaria A2", "Secundaria A2"]]

# Establecer la ciudad como índice
#datos = datos.set_index("Ciudad")

# Crear gráfica de barras apiladas
datos.plot(kind="barh", stacked=True)

plt.title("Inscripción por nivel educativo y ciudad (Año 2)")
plt.xlabel("Ciudad")
plt.ylabel("Porcentaje de inscripción")
plt.legend(title="Nivel educativo")

plt.show()