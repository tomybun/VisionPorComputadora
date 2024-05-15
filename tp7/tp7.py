#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import cv2

blue = (255, 0, 0); green = (0, 255, 0); red = (0, 0, 255)
dibuja = False  # true si el botón está presionado
xy_iniciales = -1, -1
drawing = False
k = None

###############################################################################################################################

def calcular_transformacion_afin(puntos_origen, puntos_destino):
	# Convertir los puntos a formato adecuado para cv2.getAffineTransform
	pts_origen = np.array(puntos_origen, dtype=np.float32)
	pts_destino = np.array(puntos_destino, dtype=np.float32)

	# Obtener la transformación afín a partir de los puntos correspondientes
	return cv2.getAffineTransform(puntos_origen, puntos_destino)

###############################################################################################################################

def insertar_imagen(img_fondo, img_insertar, puntos_destino):

	# Obtener las dimensiones de la imagen de fondo
	altura, ancho, canales = img_fondo.shape
	
	# Calcular la matriz de transformación afín
	puntos_origen = np.float32([[0, 0], [img_insertar.shape[1], 0], [img_insertar.shape[1], img_insertar.shape[0]]])
	matriz_transformacion = calcular_transformacion_afin(	puntos_origen=np.float32([[0, 0], [img_insertar.shape[1], 0], [img_insertar.shape[1],
								img_insertar.shape[0]]]),
								
								puntos_destino = puntos_destino)

	# Aplicar la transformación a la imagen a insertar
	imagen_transformada = cv2.warpAffine(img_insertar, matriz_transformacion, (ancho, altura))
	
	# Cálculo del cuarto punto del paralelogramo
	x4 = -(puntos_destino[1][0] - puntos_destino[0][0]) + puntos_destino[2][0] 
	y4 = -(puntos_destino[1][1] - puntos_destino[0][1]) + puntos_destino[2][1] 
	puntos_destino = np.append(puntos_destino, [[x4, y4]], axis=0).astype(np.float32)
    	
	#Listas que guardan los puntos para hacer los dos triangulos que forman el paralelogramo
	puntos_para_mascara1 = puntos_destino[[0, 1, 2]].astype(int)
	puntos_para_mascara2 = puntos_destino[[0, 2, 3]].astype(int)
	
	# Generar una máscara para la imagen insertada
	mascara = np.ones((altura, ancho), dtype=np.uint8) * 255 
	
	# Genera la máscara mediante dos triángulos
	cv2.fillPoly(mascara, [puntos_para_mascara1], 0)
	cv2.fillPoly(mascara, [puntos_para_mascara2], 0)

    	# Combinar las imágenes utilizando la máscara
	img_fondo_con_insertada = cv2.bitwise_and(img_fondo, img_fondo, mask=mascara)
	img_fondo_con_insertada += imagen_transformada


	return img_fondo_con_insertada
    

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
	global xy_iniciales, drawing, mode, img, foto_recortada, img_copia, imagen_transformada, k, puntos_seleccionados, contador_puntos, puntos_destino, afin_trans
	
	if event == cv2.EVENT_LBUTTONDOWN:
		drawing = True
		xy_iniciales = x, y
		
		#Si esta en modo transformacion afin
		if afin_trans is True:
				
			puntos_seleccionados.append([x, y])
			contador_puntos += 1
			cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
				
			if contador_puntos == 3:
				
				# Convertir los puntos seleccionados a un formato adecuado para la función de transformación afín
				puntos_destino = np.array(puntos_seleccionados, dtype=np.float32)
								
				# Deshabilitar el manejo de eventos de ratón	
				cv2.setMouseCallback('imagen', lambda *args: None)
								
		
	#Modo default, el que dibuja el rectangulo	
	elif event == cv2.EVENT_MOUSEMOVE and afin_trans is False:
		if drawing is True:
		
			img = img_copia.copy()
			
			#Para el rectangulo pintado de gris
			overlay = img.copy()  
			cv2.rectangle(overlay, xy_iniciales, (x, y), (128, 128, 128), -1)
			img = cv2.addWeighted(overlay, 0.4, img, 0.6, 0) 
			#Borde del rectangulo
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
	
#Bandera que indica si se está en modo afin, ya que cambia el dibujo
afin_trans= False 

#Lectura de la imagen
img = cv2.imread('messi.png' , 1)

# Crear una copia de la imagen de fondo para mostrar los puntos seleccionados
img_copia = img.copy()
img_aux = img.copy()

#Obtiene el tamaño de la imagen y adapta la ventana
tamIMG(img, 'imagen')

# Inicializar variables para la selección de puntos
puntos_seleccionados = []
contador_puntos = 0
puntos_destino = []

cv2.setMouseCallback('imagen', dibuja)

while True:
	cv2.imshow('imagen', img)
	k = cv2.waitKey(1) & 0xFF

	if(k == ord('r')):   # elimina el rectángulo dibujado
        	img = img_aux.copy()
        	
	if k == 27:
		break 
		
	#Guarda recorte selccionado
	elif(k == ord('g')): 
        	cv2.imwrite('foto_recortada.png', foto_recortada)
	
	#Transformacion ecuclidiana
	elif k == ord('e'):	
		imagen_transformada = transformacion_euclidiana(foto_recortada, angulo, x, y, escala)
		cv2.imwrite('trans_euclidiana.png', imagen_transformada)
		break 
	
	#Transformacion afin
	elif k == ord('a') or afin_trans:
		
		if contador_puntos <= 3:
			img = img_aux
		
		#Lectura de la imagen que se va a insertar
		imagen_insertar = cv2.imread('copa.png',1)
		
		#Se setea el modo de transformacion afin
		afin_trans = True
		
		
		#Una vez seleccionados los 3 puntos se llama a la funcion que transforma	
		if contador_puntos == 3:
			
			print(puntos_destino)
    			
    			# Insertar la imagen en la imagen de fondo
			imagen_resultante = insertar_imagen(img, imagen_insertar, puntos_destino)
			
			#Para pegar la imagen insertada en la imagen de abajo
			overlay = imagen_resultante.copy()  
			img = cv2.addWeighted(overlay, 1, img, 0, 0)	
			
			#Para que no vuelva a entrar al if
			contador_puntos = contador_puntos + 1	
		
		       
        
cv2.destroyAllWindows()










