import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

df = pd.read_csv("../data/datasaurus.csv")
grupos = df.groupby("dataset")
print(len(grupos))
fig, axes = plt.subplots(3, 5, figsize=(15, 10))

for i, (nombre, grupo) in enumerate(grupos):
    print(f"Grupo: {nombre}, Cantidad de puntos: {len(grupo)}")
    print(grupo.describe()) 
    axes[i//5, i%5].scatter(grupo["x"], grupo["y"])
    axes[i//5, i%5].set_title(nombre)
    model = LinearRegression()
    model.fit(grupo[["x"]], grupo["y"])
    xmin, xmax = grupo["x"].min(), grupo["x"].max()
    x_line = np.array([xmin, xmax]).reshape(-1, 1)
    y_line = model.predict(x_line)
    axes[i//5, i%5].plot(x_line.flatten(), y_line, color="red")
    print(f"Pendiente: {model.coef_[0]:.2f}, Intercepto: {model.intercept_:.2f}")
plt.tight_layout()
plt.show()

df = pd.read_csv("../data/anscombes.csv")
grupos = df.groupby("dataset")
print(len(grupos))
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

for i, (nombre, grupo) in enumerate(grupos):
    print(f"Grupo: {nombre}, Cantidad de puntos: {len(grupo)}")
    print(grupo.describe()) 
    axes[i//2, i%2].scatter(grupo["x"], grupo["y"])
    axes[i//2, i%2].set_title(nombre)
    
    model = LinearRegression()
    model.fit(grupo[["x"]], grupo["y"])
    xmin, xmax = grupo["x"].min(), grupo["x"].max()
    x_line = np.array([xmin, xmax]).reshape(-1, 1)
    y_line = model.predict(x_line)
    axes[i//2, i%2].plot(x_line.flatten(), y_line, color="red")
    
plt.tight_layout()
plt.show()
