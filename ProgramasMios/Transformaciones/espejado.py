#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import cv2

modes = {'x': 0, 'y': 1, 'b': -1}

def flip(img, mode):
    if (mode not in modes.keys()):
        return img
    flipped = cv2.flip(img, modes[mode])
    return flipped
    
img = cv2.imread('hoja.png' , 1)

#Como tenia problemas para abrir la foto completa hice esto:

# Obtener el ancho y alto de la imagen
alto, ancho, canales = img.shape
# Crear una ventana con el nombre "Imagen Completa"
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
# Ajustar el tamaño de la ventana de acuerdo al ancho y alto de la imagen
cv2.resizeWindow('image', ancho, alto)

while True:
    cv2.imshow('image', img)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('k'):
        break
        
cv2.destroyAllWindows()

# Obtener el modo de volteo de los argumentos de la línea de comandos
if len(sys.argv) > 1:
    modo_volteo = sys.argv[1]
else:
    modo_volteo = 'x'  # Modo predeterminado si no se proporciona ningún argumento

imagen_espejada = flip(img, modo_volteo)
     
while True:
    cv2.imshow('imagen transladada', imagen_espejada)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('k'):
        break        
        
        
cv2.destroyAllWindows()

