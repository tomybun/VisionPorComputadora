#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import cv2

blue = (255, 0, 0); green = (0, 255, 0); red = (0, 0, 255)
dibuja = False  # true si el botón está presionado
xy_iniciales = -1, -1
drawing = False



###############################################################################################################################
def transformacion_euclidiana(img, angulo, x, y, escala):
    (h, w) = img.shape[:2]
    centro = (w/2, h/2)

    # Definir la matriz de transformación euclidiana
    M = cv2.getRotationMatrix2D(centro, angulo, escala)
    M[:, 2] += np.array([x, y])
    
    # Aplicar la transformación euclidiana
    transformada = cv2.warpAffine(img, M, (w, h))

    return transformada

###############################################################################################################################

#obtiene el tamaño de la imagen y adapta la ventana   
def tamIMG(img, nombreVentana):
	# Obtener el ancho y alto de la imagen
	alto, ancho, canales = img.shape
	# Crear una ventana con el nombre "Imagen Completa"
	cv2.namedWindow(nombreVentana, cv2.WINDOW_NORMAL)
	# Ajustar el tamaño de la ventana de acuerdo al ancho y alto de la imagen
	cv2.resizeWindow(nombreVentana, ancho, alto)
	
###############################################################################################################################
	
def dibuja(event, x, y, flags, param):
    global xy_iniciales, drawing, mode, img, foto_recortada, img_copia, imagen_transformada
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        xy_iniciales = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing is True:
            img = img_copia.copy()
            overlay = img.copy()  # Copia de la imagen original para usar como capa de fondo
            cv2.rectangle(overlay, xy_iniciales, (x, y), (128, 128, 128), -1)  # Rectángulo relleno con color gris transparente en la capa overlay
            img = cv2.addWeighted(overlay, 0.4, img, 0.6, 0)  	# Combinación de la capa overlay con la imagen original,
            							# overlay es la primera imagen, 0.4 es el peso de esa imagen en la mezcla
            							# img es la otra imagen a mezclar y 0.6 es su peso en la mezcla, lo ultimo es un 
            							# parametro opcional
            cv2.rectangle(img, xy_iniciales, (x, y), (128, 128, 128), 2)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        x1, y1 = xy_iniciales
        x2, y2 = x, y
        foto_recortada = img_copia[y1:y2, x1:x2]
      
###############################################################################################################################    
    
       

#Obtener el angulo y las coordenadas de traslacion
if len(sys.argv) > 4:
	angulo 	= float(sys.argv[1])
	x	= float(sys.argv[2])
	y	= float(sys.argv[3])
	escala	= float(sys.argv[4])
else:
	angulo	= 90.0  # Modo predeterminado si no se proporciona ningún argumento
	x	= 0.0
	y	= 0.0
	escala	= 1.0
	

#Lectura de la imagen
img = cv2.imread('messi.png' , 1)
img_copia = img.copy()

#Obtiene el tamaño de la imagen y adapta la ventana
tamIMG(img, 'imagen')

cv2.setMouseCallback('imagen', dibuja)

while True:
    cv2.imshow('imagen', img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break 
    if k == ord('e'):
    	imagen_transformada = transformacion_euclidiana(foto_recortada, angulo, x, y, escala)
    	cv2.imwrite('foto_recortada.png', imagen_transformada)
    	break          
        
cv2.destroyAllWindows()










