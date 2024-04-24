#A. Usando como base el programa anterior, escribir un programa que permita seleccionar
#una porción rectangular de una imagen, luego
#con la letra “g” guardar la porción de la imagen seleccionada como una nueva imagen,
#con la letra “r” restaurar la imagen original y permitir realizar una nueva selección,
#con la “q” finalizar.


#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np

blue = (255, 0, 0); green = (0, 255, 0); red = (0, 0, 255)
drawing = False  # true si el botón está presionado
xy_iniciales = -1, -1


def dibuja(event, x, y, flags, param):
    global xy_iniciales, drawing, mode, img, foto_recortada, img_copia
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        xy_iniciales = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing is True:
            img = img_copia.copy()
            cv2.rectangle(img, xy_iniciales, (x, y), (128, 128, 128), 2)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        x1, y1 = xy_iniciales
        x2, y2 = x, y
        foto_recortada = img[y1:y2, x1:x2]
        

#Esto es lo mad facil, para que abra una imagen asi nomas    
"""   
img = cv2.imread('messi.png' , 1)
img_copia = img.copy()
cv2.namedWindow('image')
cv2.setMouseCallback('image', dibuja)"""


img = cv2.imread('messi.png' , 1)
img_copia = img.copy()

#Como tenia problemas para abrir la foto completa hice esto:

# Obtener el ancho y alto de la imagen
alto, ancho, canales = img.shape
# Crear una ventana con el nombre "Imagen Completa"
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
# Ajustar el tamaño de la ventana de acuerdo al ancho y alto de la imagen
cv2.resizeWindow('image', ancho, alto)

cv2.setMouseCallback('image', dibuja)


while True:
    cv2.imshow('image', img)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('r'):
        img = img_copia.copy()
    elif k == 27:
    	break
    elif k == ord('g'):
    	cv2.imwrite('foto_recortada.png', foto_recortada)
    	break
    	
        
cv2.destroyAllWindows()

