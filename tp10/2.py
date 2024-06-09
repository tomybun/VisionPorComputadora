import cv2 as cv
import numpy as np

# Cargamos el diccionario.
dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_6X6_250)
parameters = cv.aruco.DetectorParameters_create()
cap = cv.VideoCapture(0)

while 1:
    ret, frame = cap.read()
    # Detectamos los marcadores en la imagen
    (corners, ids, rejected) = cv.aruco.detectMarkers(frame, dictionary, parameters=parameters)
    if ids is not None:
        print("")
        print("esquinas: {}".format(corners))
        print("ids: {}".format(ids))
    # Dibujamos los marcadores detectados en la imagen
    frame = cv.aruco.drawDetectedMarkers(frame, corners, ids)
    cv.imshow("ventana", frame)
    key = cv.waitKey(50)
    if key == 27:
        break

