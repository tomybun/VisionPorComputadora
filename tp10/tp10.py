import cv2 as cv
import numpy as np

# Cargamos el diccionario.
diccionario = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_6X6_250)
parameters = cv.aruco.DetectorParameters_create()
cap = cv.VideoCapture(0)

# Cargamos la imagen que queremos insertar
img_a_insertar = cv.imread("TutorialADS(0).jpg")

num_diap = 0

# Obtener el ancho y alto del video de la cámara
width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

# Definir un factor de escalado para aumentar el tamaño de la ventana
scale_factor = 2

# Calcular el nuevo ancho y alto de la ventana
new_width = int(width * scale_factor)
new_height = int(height * scale_factor)

while True:
	ret, WebCam = cap.read()
	if not ret:
		break
	
	# Detectamos los marcadores en la imagen
	(esquinas, ids, pts_rechazados) = cv.aruco.detectMarkers(WebCam, diccionario, parameters=parameters)
	
	
	if ids is not None and len(ids) >= 4:
		# Suponemos que los IDs de los 4 marcadores son conocidos y consecutivos
		ids_esperados = [0, 1, 2, 3]
		#  		Realiza una compresion de diccionario
		esquinas_detectadas = {id[0]: esquina[0] for id, esquina in zip(ids, esquinas) if id[0] in ids_esperados}
		
		if len(esquinas_detectadas) == 4:
			# Ordenamos las esquinas en el orden correcto
			esquinas_detectadas = [esquinas_detectadas[i] for i in ids_esperados]

			# Definimos los puntos de destino (las esquinas de los 4 marcadores)
			pts_dest = np.array([
						esquinas_detectadas[0][0],  # Esquina superior izquierda del primer marcador
						esquinas_detectadas[1][1],  # Esquina superior derecha del segundo marcador
						esquinas_detectadas[3][2],  # Esquina inferior derecha del cuarto marcador
						esquinas_detectadas[2][3]   # Esquina inferior izquierda del tercer marcador
			], dtype="float32")
			
			# Definimos los puntos de origen (las esquinas de la imagen a insertar)
			h, w = img_a_insertar.shape[:2]
			pts_origen = np.array	([
						[0, 0],
						[w - 1, 0],
						[w - 1, h - 1],
						[0, h - 1]
			], dtype="float32")
			
			# Calculamos la matriz de transformación de perspectiva
			M = cv.getPerspectiveTransform(pts_origen, pts_dest)
			
			# Aplicamos la transformación de perspectiva a la imagen
			warped_image = cv.warpPerspective(img_a_insertar, M, (WebCam.shape[1], WebCam.shape[0]))
			
			# Creamos una máscara para combinar la imagen insertada con la WebCam
			mask = np.zeros_like(WebCam, dtype=np.uint8)
			cv.fillConvexPoly(mask, pts_dest.astype(int), (255, 255, 255))
			mask = cv.bitwise_not(mask)
			
			# Combinamos la WebCam y la imagen insertada usando la máscara
			WebCam = cv.bitwise_and(WebCam, mask)
			WebCam = cv.bitwise_or(WebCam, warped_image)
	
	# Dibujamos los marcadores detectados en la imagen
	#WebCam = cv.aruco.drawDetectedMarkers(WebCam, esquinas, ids)
	
	cv.namedWindow("ventana", cv.WINDOW_NORMAL)  # Definir una ventana redimensionable
	cv.resizeWindow("ventana", new_width, new_height)
	cv.imshow("ventana", WebCam)
	key = cv.waitKey(50)

	
	if key == 27:
		break
		
	if key == 83:
		if num_diap <= 27:
			num_diap += 1
			nombre_archivo = "TutorialADS({}).jpg".format(num_diap)
			img_a_insertar = cv.imread(nombre_archivo)
		
		
	if key == 81:
		if num_diap >= 0:
			if num_diap == 0:
				num_diap += 1
			num_diap -= 1
			nombre_archivo = "TutorialADS({}).jpg".format(num_diap)
			img_a_insertar = cv.imread(nombre_archivo)

cap.release()
cv.destroyAllWindows()












