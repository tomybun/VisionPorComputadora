import cv2 as cv
import numpy as np

# Definimos el tamaño de la imagen y el tamaño de los marcadores
imagen_ancho = 800
imagen_alto = 800
marcador_tamaño = 200

# Creamos una imagen en blanco
imagen = np.ones((imagen_alto, imagen_ancho), dtype=np.uint8) * 255

# Cargamos el diccionario predefinido
diccionario = cv.aruco.Dictionary_get(cv.aruco.DICT_6X6_250)

# Generamos y colocamos los marcadores en las esquinas
posiciones = [(0, 0), (0, imagen_ancho - marcador_tamaño), 
              (imagen_alto - marcador_tamaño, 0), 
              (imagen_alto - marcador_tamaño, imagen_ancho - marcador_tamaño)]

for i, (y, x) in enumerate(posiciones):
    marcador = np.zeros((marcador_tamaño, marcador_tamaño), dtype=np.uint8)
    marcador = cv.aruco.drawMarker(diccionario, i, marcador_tamaño, marcador, 1)
    imagen[y:y + marcador_tamaño, x:x + marcador_tamaño] = marcador

# Guardamos e mostramos la imagen resultante
cv.imwrite("imagen_con_marcadores.png", imagen)
cv.imshow("Imagen con Marcadores", imagen)
cv.waitKey(0)
cv.destroyAllWindows()

