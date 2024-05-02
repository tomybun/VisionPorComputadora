#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import cv2

def transformacion_euclidiana(img, angulo, x, y):
    (h, w) = img.shape[:2]
    centro = (w/2, h/2)
    escala= 1.0

    # Definir la matriz de transformación euclidiana
    M = cv2.getRotationMatrix2D(centro, angulo, escala)
    M[:, 2] += np.array([x, y])
       
    # M[:, 2] selecciona la tercera columna de la matriz M.
    # El índice : significa que selecciona todas las filas de la matriz, y 2 selecciona la tercera columna.
    # np.array([tx, ty]) crea un arreglo NumPy que contiene los valores de traslación en x e y proporcionados como argumentos (x, y).
    # += es un operador de asignación que agrega los valores de traslación proporcionados a la tercera columna de la matriz M.
    

    # Aplicar la transformación euclidiana
    transformada = cv2.warpAffine(img, M, (w, h))

    return transformada
 
#obtiene el tamaño de la imagen y adapta la ventana   
def tamIMG(img, nombreVentana):
	# Obtener el ancho y alto de la imagen
	alto, ancho, canales = img.shape
	# Crear una ventana con el nombre "Imagen Completa"
	cv2.namedWindow(nombreVentana, cv2.WINDOW_NORMAL)
	# Ajustar el tamaño de la ventana de acuerdo al ancho y alto de la imagen
	cv2.resizeWindow(nombreVentana, ancho, alto)
	
      
    
img = cv2.imread('messi.png' , 1)

# Obtener el angulo y las coordenadas de traslacion
if len(sys.argv) > 3:
	angulo 	= float(sys.argv[1])
	x	= float(sys.argv[2])
	y	= float(sys.argv[3])
else:
	angulo	= 30  # Modo predeterminado si no se proporciona ningún argumento
	x	= 4
	y	= 4

imagen_transformada = transformacion_euclidiana(img, angulo, x, y)

#obtiene el tamaño de la imagen y adapta la ventana
tamIMG(img, 'imagen')

while True:
    cv2.imshow('imagen', img)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('k'):
        break
        
cv2.destroyAllWindows()

#obtiene el tamaño de la imagen y adapta la ventana
tamIMG(img, 'imagen transformada')

while True:
    cv2.imshow('imagen transformada', imagen_transformada)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('k'):
        break        
        


        
cv2.destroyAllWindows()










