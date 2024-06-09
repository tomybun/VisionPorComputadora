import cv2 as cv
import numpy as np

# Cargamos el diccionario.
dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_6X6_250)
parameters = cv.aruco.DetectorParameters_create()
cap = cv.VideoCapture(0)

# Cargamos la imagen que queremos insertar
image_to_insert = cv.imread("WorkSpace4.jpeg")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Detectamos los marcadores en la imagen
    (corners, ids, rejected) = cv.aruco.detectMarkers(frame, dictionary, parameters=parameters)
    if ids is not None:
        print("")
        print("esquinas: {}".format(corners))
        print("ids: {}".format(ids))
        
        for corner in corners:
            # Definimos los puntos de destino (las esquinas del marcador)
            pts_dst = np.array(corner[0], dtype="float32")
            
            # Definimos los puntos de origen (las esquinas de la imagen a insertar)
            h, w = image_to_insert.shape[:2]
            pts_src = np.array([
                [0, 0],
                [w - 1, 0],
                [w - 1, h - 1],
                [0, h - 1]
            ], dtype="float32")
            
            # Calculamos la matriz de transformación de perspectiva
            M = cv.getPerspectiveTransform(pts_src, pts_dst)
            
            # Aplicamos la transformación de perspectiva a la imagen
            warped_image = cv.warpPerspective(image_to_insert, M, (frame.shape[1], frame.shape[0]))
            
            # Creamos una máscara para combinar la imagen insertada con el frame
            mask = np.zeros_like(frame, dtype=np.uint8)
            cv.fillConvexPoly(mask, pts_dst.astype(int), (255, 255, 255))
            mask = cv.bitwise_not(mask)
            
            # Combinamos el frame y la imagen insertada usando la máscara
            frame = cv.bitwise_and(frame, mask)
            frame = cv.bitwise_or(frame, warped_image)
    
    # Dibujamos los marcadores detectados en la imagen
    frame = cv.aruco.drawDetectedMarkers(frame, corners, ids)
    cv.imshow("ventana", frame)
    key = cv.waitKey(50)
    if key == 27:
        break

cap.release()
cv.destroyAllWindows()

