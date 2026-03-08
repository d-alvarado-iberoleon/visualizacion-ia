# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 17:53:21 2026

@author: alvaradocde
"""
import numpy as np

def funcion(x, y):
    return np.sin(x)*np.cos(y)

def muestrear_señal(xlims, ylims, ancho=128, alto=128):
    x = np.linspace(xlims[0], xlims[1], ancho)
    y = np.linspace(ylims[0], ylims[1], alto)
    xx, yy = np.meshgrid(x, y)
    zz = funcion(xx, yy)
    return zz

def cuantizar_señal(señal, L=32):
    z_min = np.min(señal)
    z_max = np.max(señal)
    return np.floor((señal-z_min)/(z_max-z_min)*(L-1))

xlims = [-3.14, 3.14]
ylims = [-3.14, 3.14]
s = muestrear_señal(xlims, ylims)
img = cuantizar_señal(s)



    
