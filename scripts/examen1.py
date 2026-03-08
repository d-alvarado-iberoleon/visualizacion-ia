# -*- coding: utf-8 -*-
"""
Created on Fri Feb  6 13:36:40 2026

@author: alvaradocde
"""

import matplotlib.pyplot as plt
import numpy as np

def modelo_a_pantalla(x, y, xlims, ylims, H, W):
    x_p = (x-xlims[0])/(xlims[1]-xlims[0])*(H-1)
    y_p = (1-(y-ylims[0])/(ylims[1]-ylims[0]))*(W-1)
    return round(x_p), round(y_p)

def dda(img, origen, dest):
    x0, y0 = origen
    x1, y1 = dest
    dx = x1-x0
    dy = y1-y0
    pasos = max(abs(dx), abs(dy))
    print(pasos)
    delta_x = dx/pasos
    delta_y = dy/pasos
    x, y = origen
    for i in range(pasos):
        img[round(y), round(x)]=1
        x+=delta_x
        y+=delta_y
    return img

p1 = (2, 3)
p2 = (7, 5)
p3 = (6, -2)
print(p1)
print(p2)
print(p3)
xlims = [-2, 10]
ylims = [-3, 7]
p1_p = modelo_a_pantalla(p1[0], p1[1], xlims, ylims, 800, 600)
p2_p = modelo_a_pantalla(p2[0], p2[1], xlims, ylims, 800, 600)
p3_p = modelo_a_pantalla(p3[0], p3[1], xlims, ylims, 800, 600)
print(p1_p)
print(p2_p)
print(p3_p)
img = np.zeros((600, 800))

img = dda(img, p1_p, p2_p)
img = dda(img, p2_p, p3_p)
img = dda(img, p3_p, p1_p)

plt.imshow(img, cmap="gray")
plt.show()
