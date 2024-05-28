#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import cv2

xy_iniciales = 0, 0
xy_finales = 0, 0
drawing1 = False
drawing2 = False
k = None
ban = False

click = False

#Bandera que controla el 2do callback
callback2 = False

#Bandera que controla el 3er callback
callback3 = False

img_rect_ban = False

h = False
a = False

salir = False

blue=(255,0,0);red=(0,0,255)


###############################################################################################################################

def draw_line(event, x, y, flags, param):
	global xy_iniciales, drawing2, img, img_copia	
   	
	if event == cv2.EVENT_LBUTTONDOWN:
		drawing2 = True
		xy_iniciales = x, y
		
	elif event == cv2.EVENT_MOUSEMOVE:
		if drawing2 is True:
			xy_finales = x, y
			img = img_copia.copy()
			cv2.line(img, xy_iniciales, xy_finales, blue,3)
			
	elif event == cv2.EVENT_LBUTTONUP:
		drawing2 = False

	
###############################################################################################################################

def calcular_homografia(puntos_origen, puntos_destino):
	# Convertir los puntos a formato adecuado para cv2.getPerspectiveTransform
	pts_origen = np.array(puntos_origen, dtype=np.float32)
	pts_destino = np.array(puntos_destino, dtype=np.float32)

	# Calcular la homografía entre los puntos correspondientes
	homografia = cv2.getPerspectiveTransform(pts_origen, pts_destino)

	return homografia

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
	global xy_iniciales, drawing1, img, puntos_seleccionados, contador_puntos, puntos_destino
	
	if event == cv2.EVENT_LBUTTONDOWN:
		drawing1 = True
		xy_iniciales = x, y
			
		puntos_seleccionados.append([x, y])
		contador_puntos += 1
		cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
			
		if contador_puntos == 4:
			
			# Convertir los puntos seleccionados a un formato adecuado para la función de transformación afín
			puntos_destino = np.array(puntos_seleccionados, dtype=np.float32)
							
			# Deshabilitar el manejo de eventos de ratón	
			cv2.setMouseCallback('imagen', lambda *args: None)							
			
###############################################################################################################################      

#Lectura de la imagen
img = cv2.imread('mesaValu.jpeg',1)

# Crear una copia de la imagen de fondo para mostrar los puntos seleccionados
img_aux = img.copy()

#Obtiene el tamaño de la imagen y adapta la ventana
tamIMG(img, 'imagen')

# Inicializar variables para la selección de puntos
puntos_seleccionados = []
contador_puntos = 0
puntos_destino = []

#Bandera que indica si se destruyo la primer ventana
ventana_destruida = False

cv2.setMouseCallback('imagen', dibuja)



while True:

	if ventana_destruida == False:
		cv2.imshow('imagen', img)
		k = cv2.waitKey(1) & 0xFF
		
	#Elimina los puntos dibujados
	if(k == ord('r')):   
        	img = img_aux.copy()
        	contador_puntos = 0
        	puntos_seleccionados.clear()
        	
	if k == 27 or salir == True:
		break				
	
	#Si selecciona los 4 puntos del plano, lo rectifica
	if contador_puntos == 4:
	
		#Verifica si la ventana anterior no esta destruida y la destruye si es asi
		if ventana_destruida == False: 
			cv2.destroyWindow('imagen')
			ventana_destruida = True
			
		#print(contador_puntos)
		alto, ancho, _ = img_aux.shape		
	
		# Calcular la matriz de homografia	
		# Arma las 4 esquinas de la imagen a que será rectificada
		puntos_destino = np.array( 	[[0,0],
                				[ancho - 1, 0],
                				[0, alto - 1],
               					[ancho - 1, alto- 1]]	).astype(np.float32)				               					
		homografia = calcular_homografia(puntos_seleccionados, puntos_destino)
		
		#Se rectifica la imagen una sola vez
		if img_rect_ban == False:
			# Aplicar la homografía a la imagen
			print('RECTIFICACION')
			img = cv2.warpPerspective(img_aux, homografia, (ancho, alto))
			img_rectificada_copia = img.copy()
			img_rect_ban = True
		
		#Se hace que el callback en la nueva ventana solo se llame una vez		
		if callback2 == False:
			#Obtiene el tamaño de la imagen y adapta la ventana
			print('CALLBACK')
			tamIMG(img, 'imagen rectificada')
			img_copia = img.copy()
			cv2.setMouseCallback('imagen rectificada',draw_line)
			callback2 = True				
				
		cv2.imshow('imagen rectificada', img)
		k = cv2.waitKey(1) & 0xFF 
		
		
		#Elimina las lineas dibujadas
		if(k == ord('b')):   
			img = img_rectificada_copia.copy()
						
						
		if(k == ord('h')): 
			med1	= -xy_finales[1] + xy_iniciales[1]
			med1 = med1/40
			h = True
			
		if(k == ord('a')): 
			med2	= -xy_finales[0] + xy_iniciales[0]
			med2 = med2/45
			a = True

		if h == True and a == True:
			print('ENTRO AL IF')
			cv2.destroyWindow('imagen rectificada')
			new_width = int(img.shape[1] * med2)
			new_height = int(img.shape[0] * med1)
			img_final = cv2.resize(img_rectificada_copia, (new_width, new_height))
			
			#BUENO, VIENE POR ACA, TENGO QUE ARREGLAR EL HECHO DE QUE LA FUNCION DRAW_LINE PUEDA SER LLAMADA CON VARIABLES
			#GENERICAS PORQUE NO ME ESTA DIBUJANDO LA LIENA EN LA ULTIMA IMAGEN
			if callback3 == False:
				img = img_final.copy()
			
			while True:				
				
				
				
				if callback3 == False:
					tamIMG(img, 'imagen final')
					img_copia = img.copy()
					cv2.setMouseCallback('imagen final',draw_line)
					callback3 = True
				
				cv2.imshow('imagen final', img)
				k = cv2.waitKey(1) & 0xFF
				
				if k == 27:
					salir = True
					break
				
				
						
		
			#callback = False
			
		
			
		#Para que no vuelva a entrar al if
		#contador_puntos = contador_puntos + 1
		
		
		#PARA VOLVER ATRAS, LO DEJO PARA DESPUES
		#if(k == ord('s')):
		#	#contador_puntos = 0
		#	contador_puntos = contador_puntos + 1
		#	puntos_seleccionados.clear()
		#	cv2.destroyWindow('imagen rectificada')
		#	ventana_destruida = True
			
			#Quita los puntos de la primera imagen 			ESTO ES PARA CUANDO QUIERA VOLVER A LA IMAGEN PRINCIPAL
		#	img = img_aux.copy()
			
		#	print('SALIR')
			
			
	     
cv2.destroyAllWindows()










