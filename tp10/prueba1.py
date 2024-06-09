import cv2 as cv
import numpy as np

# Función para dibujar un recuadro azul alrededor del marcador detectado
def dibujar_recuadro_azul(imagen, contorno):
    x, y, w, h = cv.boundingRect(contorno)
    cv.rectangle(imagen, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Dibujar el recuadro azul
    #cv.rectangle(imagen, (int(ontorno[0][0][0]), int(contorno[0][0][1])), (int(contorno[0][3][0]), int(contorno[0][3][1])), (255, 0, 0), -2)

# Cargar el diccionario predefinido de ArUco
diccionario = cv.aruco.Dictionary_get(cv.aruco.DICT_6X6_250)

# Inicializar el detector de marcadores ArUco
detector = cv.aruco.DetectorParameters_create()

# Inicializar la captura de video desde la webcam
captura = cv.VideoCapture(0)

while True:
    # Capturar fotograma de la webcam
    ret, frame = captura.read()

    # Convertir el fotograma a escala de grises
    gris = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Detectar marcadores ArUco
    corners, ids, _ = cv.aruco.detectMarkers(gris, diccionario, parameters=detector)

    # Si se detecta el marcador 33, dibujar un recuadro azul alrededor de él
    if ids is not None and 33 in ids:
        indice = np.where(ids == 33)[0][0]  # Índice del marcador 33
        contorno = corners[indice]          # Obtener el contorno del marcador
        dibujar_recuadro_azul(frame, contorno)
        print(contorno)
        print()
        print(contorno[0][0][0])
        print(contorno[0][1][1])
        
    # Mostrar el fotograma con el recuadro azul alrededor del marcador 33
    cv.imshow('Marcador ArUco 33', frame)

    # Salir del bucle si se presiona la tecla 'q'
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar los recursos y cerrar la ventana
captura.release()
cv.destroyAllWindows()

