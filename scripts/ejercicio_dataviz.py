import pandas as pd
import matplotlib.pyplot as plt

data = df = pd.read_csv("datos_inscripcion.csv", index_col="Ciudad")
df_filtrado = df.drop(columns=["Mejora Preescolar"])

plt.figure()
df_filtrado.plot(kind="bar", figsize=(12, 6), colormap="viridis")
plt.title("Estadísticas de inscripción por ciudad")
plt.xlabel("Ciudad")
plt.ylabel("Número de inscritos (miles)")
plt.legend()
plt.grid(alpha=0.7)
plt.show()

df_filtrado2 = df[["Preescolar A1", "Preescolar A2"]]

plt.figure()
df_filtrado2.plot(kind="bar", figsize=(12, 6), colormap="cool")
plt.title("Estadísticas de inscripción por ciudad")
plt.xlabel("Ciudad")
plt.ylabel("Número de inscritos (miles)")
plt.legend()
plt.grid(alpha=0.7)
plt.show()

# opcion 2
plt.figure()
df_filtrado3 = df[["Mejora Preescolar"]]
df_ordenado = df_filtrado3.sort_values(by="Mejora Preescolar", ascending=False)
df_ordenado.plot(kind="bar", figsize=(12, 6), colormap="cool")
plt.title("Mejora de inscritos (miles) por ciudad")
plt.xlabel("Ciudad")
plt.grid(alpha=0.7)
plt.show()
