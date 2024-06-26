#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import cv2

def translate(img, x, y):
    (h, w) = (img.shape[0], img.shape[1])
    M = np.float32([[1, 0, x],
                    [0, 1, y]])
    shifted = cv2.warpAffine(img, M, (w, h))
    return shifted
    
    
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

imagen_trasladada = translate(img, 50, 30)
     
while True:
    cv2.imshow('imagen transladada', imagen_trasladada)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('k'):
        break        
        


        
cv2.destroyAllWindows()










