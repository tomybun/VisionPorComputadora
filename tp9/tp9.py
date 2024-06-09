#INSTRUCCIONES DE USO:
#			Ejecutar el programa, una vez que se ve la imagen seleccionar las 4 esquinas de la mesa desde la esquina superior
#			izquierda y seguir con los puntos en sentido horario (para que la medicion sea lo mas precisa posible, tratar de seleccionar
#			los bordes externos de la mesa, los cuales son los de la medicion que se hizo para harcodear el programa).
#			Luego medir, usar de referencia la regla de 20cm y la cinta metrica. En el directorio hay varias imagenes de la mesa
#			en cuestion, se puede editar que imagen se quiere y todas funcionaran, siempre seleccionando la misma esquina primero.




#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import cv2
import math

xy_iniciales = 0, 0
xy_finales = 0, 0
drawing1 = False
drawing2 = False
k = None

#Bandera que controla el 2do callback
callback2 = False

#Bandera que indica si se destruyo la primer ventana
ventana_destruida = False

#Variables para la selección de puntos
puntos_seleccionados = []
contador_puntos = 0
puntos_destino = []

img_rect_ban = False

azul=(255,0,0)
verde = (34, 139, 34)

###############################################################################################################################
	
def dibuja(event, x, y, flags, param):
	global xy_iniciales, drawing1, img, puntos_seleccionados, contador_puntos, puntos_destino
	
	if event == cv2.EVENT_LBUTTONDOWN:
		drawing1 = True
		xy_iniciales = x, y
			
		puntos_seleccionados.append([x, y])
		contador_puntos += 1
		cv2.circle(img, (x, y), 5, azul, -1)
			
		if contador_puntos == 4:
			
			# Convertir los puntos seleccionados a un formato adecuado para la función de transformación afín
			puntos_destino = np.array(puntos_seleccionados, dtype=np.float32)
							
			# Deshabilitar el manejo de eventos de ratón	
			cv2.setMouseCallback('imagen', lambda *args: None)	
###############################################################################################################################

def draw_line1(event, x, y, flags, param):
	global xy_iniciales, xy_finales, drawing2, img, img_copia, h
   	
	if event == cv2.EVENT_LBUTTONDOWN:
		drawing2 = True
		xy_iniciales = x, y
		
	elif event == cv2.EVENT_MOUSEMOVE:
		if drawing2 is True:
			xy_finales = x, y
			img = img_copia.copy()
			cv2.line(img, xy_iniciales, xy_finales, verde,3)
			
	elif event == cv2.EVENT_LBUTTONUP:
		drawing2 = False
		
		#La mesa de trabajo es de 39cmx68cm por lo tanto sera de 600x1046 pixeles
		relacion_cm_pixel = math.sqrt( (39*39)/(600*600) + (68*68)/(1046*1046) )
	
		medicion = math.sqrt(	(xy_finales[0] - xy_iniciales[0]) * (xy_finales[0] - xy_iniciales[0]) +
					(xy_finales[1] - xy_iniciales[1]) * (xy_finales[1] - xy_iniciales[1])	) * 68/1046 
					#Lo multiplique por un factor que fui corrigiendo hasta que la medicion sobre el plano era correcta
		
		medicion = f"{medicion:.2f}" #Deja la medicion con 2 numeros despues de la coma
		
		#Inserta la medicion en la parte superior de la imagen
		cv2.putText(img, str(medicion) + "cm", [50,50], cv2.FONT_HERSHEY_SIMPLEX, 1, verde, 2, cv2.LINE_AA)			

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

#Lectura de la imagen
img = cv2.imread('WorkSpace3.jpeg',1)

# Crear una copia de la imagen de fondo para mostrar los puntos seleccionados
img_aux = img.copy()

#Obtiene el tamaño de la imagen y adapta la ventana
tamIMG(img, 'imagen')


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
        	
	if k == 27:
		break				
	
	#Si selecciona los 4 puntos del plano, lo rectifica
	if contador_puntos == 4:
	
		#Verifica si la ventana anterior no esta destruida y la destruye si es asi
		if ventana_destruida == False: 
			cv2.destroyWindow('imagen')
			ventana_destruida = True	

               	#La mesa de trabajo es de 39cmx68cm por lo tanto sera de 600x1046 pixeles				
		puntos_destino = np.array( 	[[200,200],
                				[800,200],
                				[800,1246],
               					[200,1246]]	).astype(np.float32)
               				               					
		homografia = calcular_homografia(puntos_seleccionados, puntos_destino)
		
		#Se rectifica la imagen una sola vez
		if img_rect_ban == False:
			img = cv2.warpPerspective(img_aux, homografia, (1000, 1300))
			img_rectificada_copia = img.copy()
			img_rect_ban = True
		
		#Se hace que el callback en la nueva ventana solo se llame una vez		
		if callback2 == False:
			tamIMG(img, 'imagen rectificada')
			img_copia = img.copy()
			cv2.setMouseCallback('imagen rectificada',draw_line1)
			callback2 = True				
		
		
		cv2.imshow('imagen rectificada', img)
		k = cv2.waitKey(1) & 0xFF 
	
		
		#Elimina las lineas dibujadas
		if(k == ord('r')):   
			img = img_rectificada_copia.copy()		
			     
cv2.destroyAllWindows()


#39x68

