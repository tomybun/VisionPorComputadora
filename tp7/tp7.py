import sys
import numpy as np
import cv2

blue = (255, 0, 0); green = (0, 255, 0); red = (0, 0, 255)
dibuja = False  # true si el botón está presionado
xy_iniciales = -1, -1
drawing = False

#puntos = []  # Lista para almacenar los puntos seleccionados por el usuario

x1 = None
y1 = None
x2 = None
y2 = None
x3 = None
y3 = None

###############################################################################################################################

# Función para calcular la transformación afín entre 3 pares de puntos correspondientes
def calcular_transformacion_afin(puntos_originales, puntos_destino):

    # Convertir los puntos a formato adecuado para cv2.getAffineTransform
    pts_origen = np.array(puntos_originales, dtype=np.float32)
    pts_destino = np.array(puntos_destino, dtype=np.float32)

    return cv2.getAffineTransform(pts_origen, pts_destino)

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
    global img, x1, y1, x2, y2, x3, y3 # puntos
    
    if x3 != None:  # Si se han seleccionado 3 puntos
        pass
    elif event == cv2.EVENT_LBUTTONDOWN:
        #puntos.append((x, y))  # Agregar el punto seleccionado a la lista
        if x1 == None:
        	x1 = x.copy()
        	y1 = y.copy()
        elif x2 == None:
        	x2 = x.copy()
        	y2 = y.copy()
        elif x3 == None:
        	x3 = x.copy()
        	y3 = y.copy()
        	
        cv2.circle(img, (x, y), 3, (0, 255, 0), -1)  # Dibujar un círculo en el punto seleccionado
        
     
###############################################################################################################################    

def insertar_imagen_entre_puntos(img, img_insertar, x1, y1, x2, y2, x3, y3):

	# Calcular la transformación afín entre los puntos de la imagen principal y los puntos de la imagen a insertar
	M = calcular_transformacion_afin([x1, y1,x2, y2,x3, y3], [(0, 0), (img_insertar.shape[1], 0), (0, img_insertar.shape[0])])


	# Aplicar la transformación afín a la imagen a insertar
	img_insertar_transformada = cv2.warpAffine(img_insertar, M, (img.shape[1], img.shape[0]))
	cv2.imwrite('copa_transformada.png', img_insertar_transformada)

	# Crear una máscara para la imagen a insertar
	mascara = np.ones_like(img_insertar_transformada) * 255

	# Aplicar la transformación afín a la máscara
	mascara_transformada = cv2.warpAffine(mascara, M, (img.shape[1], img.shape[0]), flags=cv2.INTER_NEAREST)

	# Invertir la máscara
	mascara_invertida = cv2.bitwise_not(mascara_transformada)

	# Combinar las imágenes utilizando la máscara
	imagen_final = cv2.bitwise_and(img, mascara_invertida)
	imagen_final = cv2.add(imagen_final, img_insertar_transformada)
      
    

	return imagen_final


    

###############################################################################################################################   

#Lectura de la imagen
img		= cv2.imread('messi.png' , 1)
img_insertar    = cv2.imread('copa.png' , 1)

#Obtiene el tamaño de la imagen y adapta la ventana
tamIMG(img, 'imagen')

cv2.setMouseCallback('imagen', dibuja)

while True:
    cv2.imshow('imagen', img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break    
    if k == ord('a'):
        img = insertar_imagen_entre_puntos(img, img_insertar, x1, y1, x2, y2, x3, y3)
               
        
cv2.destroyAllWindows()

