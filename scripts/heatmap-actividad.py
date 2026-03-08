import pandas as pd
import plotly.express as px
import numpy as np

# -----------------------------
# 1. Parámetros del curso
# -----------------------------
inicio_curso = "2026-01-13"
fin_curso    = "2026-05-08"

# -----------------------------
# 2. Carga/Generación de Datos
# -----------------------------

df = pd.read_csv("data/actividad-curso.csv", parse_dates=["fecha"])
#print(df.head())
# -----------------------------
# 3. Calendario completo
# -----------------------------
calendario = pd.DataFrame({
    "fecha": pd.date_range(start=inicio_curso, end=fin_curso, freq="D")
})

# Unir datos reales con calendario
df = calendario.merge(df, on="fecha", how="left")
df["actividad"] = df["actividad"].fillna(0)

# -----------------------------
# 4. Variables temporales y orden
# -----------------------------
# Extraemos el nombre del día en inglés para ordenar y luego lo traducimos
df["dia_nombre"] = df["fecha"].dt.day_name()
df["semana"] = df["fecha"].dt.isocalendar().week
df["semana"] -=2 

# Definimos el orden lógico de la semana
orden_dias = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
mapa_espanol = {
    "Monday": "Lun", "Tuesday": "Mar", "Wednesday": "Mié", 
    "Thursday": "Jue", "Friday": "Vie", "Saturday": "Sáb", "Sunday": "Dom"
}

df["dia_nombre"] = pd.Categorical(df["dia_nombre"], categories=orden_dias, ordered=True)

# -----------------------------
# 5. Tabla para heatmap
# -----------------------------
tabla = df.pivot_table(
    index="dia_nombre",
    columns="semana",
    values="actividad",
    fill_value=0, 
    observed=False,
)

# Cambiamos los nombres de las filas a español justo antes de graficar
tabla.index = [mapa_espanol[dia] for dia in tabla.index]

# -----------------------------
# 6. Heatmap con Plotly Express
# -----------------------------
"""
        [0.0, "#ebedf0"], # Gris GitHub
        [0.33, "#9be9a8"], # Verde claro
        [0.66, "#40c463"], # Verde medio
        [1.0, "#216e39"]   # Verde oscuro
"""
        
fig = px.imshow(
    tabla,
    labels=dict(x="Semana", y="", color="Actividad"),
    color_continuous_scale=[
        
        [0.0, "#f2f0f7"],  # sin actividad
        [0.33, "#cbc9e2"],
        [0.66, "#9e9ac8"],
        [1.0, "#6a51a3"]
    ],
    range_color=[0, 3], # Define los límites de color
    aspect="equal"      # Obliga a que las celdas sean cuadradas
)

# Ajustes de diseño y estilo de "mosaico"
fig.update_traces(
    xgap=3, # Espacio horizontal entre cuadros
    ygap=3, # Espacio vertical entre cuadros
    hovertemplate="Semana %{x}<br>%{y}<br>Actividad: %{z}<extra></extra>"
)

fig.update_layout(
    title=None,
    height=280,
    plot_bgcolor="white",
    xaxis=dict(
        dtick=1,        # Muestra cada número de semana
        side="bottom",  # Títulos de semana abajo
        fixedrange=True # Desactiva zoom para que parezca una app
    ),
    yaxis=dict(
        autorange="reversed", # CRÍTICO: Pone el Lunes arriba
        fixedrange=True
    ),
    coloraxis_showscale=False # Oculta la barra lateral de escala (estilo GitHub)
)

fig.show()
#fig.write_html("heatmap-actividad.html")
