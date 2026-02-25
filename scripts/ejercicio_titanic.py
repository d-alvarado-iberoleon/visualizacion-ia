import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("titanic/train.csv")
print(df.shape)
df.head(10)

print("Reporte de atributos incompletos")
print(df.isnull().sum())
# los atributos de nombre, # ticket, cabina no nos sirven para construir gráficas
df_clean = df.drop(columns=["Name", "Ticket", "Cabin"])

# edad y puerto de embarque si podrían servir, 
# pero hay 177 y 2 registros faltantes, 
# tendríamos que quitarlas o sustituirlas por algun valor

# df_clean = df_clean.dropna() # Opcion 1
df_clean["Age"].fillna(df_clean["Age"].median(), inplace=True) # Opcion 2
df_clean["Embarked"].fillna(df_clean["Embarked"].mode().iloc[0], \
   inplace=True) # Opcion 2

print("\nDataset limpio")
print(df_clean.shape)
print(df_clean.isnull().sum())

# ¿Cómo se distribuyen las edades de los pasajeros?
edades = df_clean["Age"].values
fig, ax = plt.subplots()
intervalos = np.arange(0, 100, 10)
ax.hist(edades, bins=intervalos)
plt.show()

# ¿Qué relación hay entre la tarifa pagada y la clase del pasajero?
fig, ax = plt.subplots()
clases = df_clean["Pclass"].unique()
tarifas_por_clase = [df_clean[df_clean["Pclass"]==i]["Fare"] for i in clases]
ax.boxplot(tarifas_por_clase)
plt.show()

# ¿Cuántos pasajeros viajaban en cada clase?
fig, ax = plt.subplots()
pasajeros_por_clase = df_clean.groupby("Pclass")["Pclass"].count()
print(pasajeros_por_clase)
ax.bar(pasajeros_por_clase.index, pasajeros_por_clase.values)
plt.show()

# ¿Cuántos pasajeros sobrevivieron por clase?
fig, ax = plt.subplots()
conteo_sobrevivientes = df_clean.groupby("Pclass")["Survived"].agg(total="count", sobrevivientes="sum").reset_index()
#conteo_sobrevivientes["muertos"] = conteo_sobrevivientes["total"]-conteo_sobrevivientes["sobrevivientes"] 
print(conteo_sobrevivientes)
ax.bar(conteo_sobrevivientes['Pclass'], conteo_sobrevivientes['total'])
ax.bar(conteo_sobrevivientes['Pclass'], conteo_sobrevivientes['sobrevivientes'])
plt.show()


# ¿Cómo se distribuyen las edades de los pasajeros?
edades = df_clean["Age"].values
fig, ax = plt.subplots(figsize=(18,5))
intervalos = np.arange(0, 100, 10)
centros = (intervalos[:-1] + intervalos[1:]) / 2  # Calcula los puntos centrales de los bins
etiquetas = [f"[{intervalos[i]}, {intervalos[i+1]})" for i in range(len(intervalos)-1)]
ax.hist(edades, bins=intervalos, edgecolor='black', alpha=0.7, color='lightgray')
ax.set_xticks(centros)
ax.set_xticklabels(etiquetas)
ax.set_xlabel("Edad")
ax.set_ylabel("Frecuencia")
ax.grid(linestyle='--', alpha=0.7)
ax.set_title("Distribución de edades de los pasajeros")
plt.show()

# ¿Qué relación hay entre la tarifa pagada y la clase del pasajero?
fig, ax = plt.subplots()
clases = df_clean["Pclass"].unique()
tarifas_por_clase = [df_clean[df_clean["Pclass"]==i]["Fare"] for i in clases]
ax.boxplot(tarifas_por_clase, labels=["1ra Clase", "2da Clase", "3ra Clase"], patch_artist=True,
            boxprops=dict(facecolor="lightgray", alpha=0.7), medianprops=dict(color="black"))
ax.set_xlabel("Clase del boleto")
ax.set_ylabel("Tarifa pagada ($)")
ax.set_title("Distribución de tarifas por clase")
ax.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# ¿Cuántos pasajeros viajaban en cada clase?
fig, ax = plt.subplots(figsize=(8,5))
pasajeros_por_clase = df_clean.groupby("Pclass")["Pclass"].count()
print(pasajeros_por_clase)
colores = ['#a6cee3', '#1f78b4', '#0b3c5d']  # Azul claro a oscuro
ax.bar(pasajeros_por_clase.index, pasajeros_por_clase.values, color=colores, 
       tick_label=["1ra Clase", "2da Clase", "3ra Clase"])
ax.set_xlabel("Clase")
ax.set_ylabel("Cantidad de pasajeros")
ax.set_title("Número de pasajeros por clase")
ax.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# ¿Cuántos pasajeros sobrevivieron por clase?
fig, ax = plt.subplots()
conteo_sobrevivientes = df_clean.groupby("Pclass")["Survived"].agg(total="count", sobrevivientes="sum").reset_index()
#conteo_sobrevivientes["muertos"] = conteo_sobrevivientes["total"]-conteo_sobrevivientes["sobrevivientes"] 
print(conteo_sobrevivientes)
ax.bar(conteo_sobrevivientes['Pclass'], conteo_sobrevivientes['total'], label='Fallecidos', color='lightgray', 
      tick_label=["1ra Clase", "2da Clase", "3ra Clase"])
ax.bar(conteo_sobrevivientes['Pclass'], conteo_sobrevivientes['sobrevivientes'], label='Sobrevivientes', color='lightgreen')
ax.set_xlabel('Clase', fontsize=12)
ax.set_ylabel('Número de pasajeros', fontsize=12)
ax.set_title('Número de pasajeros fallecidos y sobrevivientes por clase', fontsize=14)
ax.legend()
ax.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()
