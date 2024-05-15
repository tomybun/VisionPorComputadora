import cv2
import numpy as np

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

def seleccionar_puntos(event, x, y, flags, param):
	global puntos_seleccionados, contador_puntos, puntos_destino
	if event == cv2.EVENT_LBUTTONDOWN:
		puntos_seleccionados.append([x, y])
		contador_puntos += 1
		cv2.circle(imagen, (x, y), 5, (0, 255, 0), -1)
	if contador_puntos == 3:
	
		# Convertir los puntos seleccionados a un formato adecuado para la función de transformación afín
		puntos_destino = np.array(puntos_seleccionados, dtype=np.float32)
		
		# Deshabilitar el manejo de eventos de ratón	
		cv2.setMouseCallback('imagen', lambda *args: None)  
            
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

# Cargar la imagen de fondo y la imagen a insertar
imagen_fondo = cv2.imread('messi.png',1)
imagen_insertar = cv2.imread('copa.png',1)


#Obtiene el tamaño de la imagen y adapta la ventana
tamIMG(imagen_fondo, 'imagen')

# Crear una copia de la imagen de fondo para mostrar los puntos seleccionados
imagen = imagen_fondo.copy()

# Inicializar variables para la selección de puntos
puntos_seleccionados = []
contador_puntos = 0
puntos_destino = []

# Configurar el manejo de eventos de ratón
cv2.namedWindow('imagen')
cv2.setMouseCallback('imagen', seleccionar_puntos)

# Mostrar la imagen y esperar a que se seleccionen los puntos
while True:
	cv2.imshow('imagen', imagen)
	k = cv2.waitKey(1) & 0xFF
	if k == 27:  # Salir con la tecla 'Esc'
		break
	if contador_puntos == 3:
		# Insertar la imagen en la imagen de fondo
		imagen_resultante = insertar_imagen(imagen_fondo, imagen_insertar, puntos_destino)
		
		overlay = imagen_resultante.copy()  # Copia de la imagen original para usar como capa de fondo
		imagen = cv2.addWeighted(overlay, 1, imagen, 0, 0)	# Combinación de la capa overlay con la imagen original,
            								# overlay es la primera imagen, 1 es el peso de esa imagen en la mezcla
            								# img es la otra imagen a mezclar y 0 es su peso en la mezcla, lo ultimo es un 
            								# parametro opcional
		
		contador_puntos = contador_puntos + 1	#Para que no vuelva a entrar al if
		

cv2.destroyAllWindows()

