import cv2

# Cargar la imagen
imagen = cv2.imread("messi.png")

# Obtener el ancho y alto de la imagen
alto, ancho, _ = imagen.shape

# Crear una ventana con el nombre "Imagen Completa"
cv2.namedWindow("Imagen Completa", cv2.WINDOW_NORMAL)

# Ajustar el tamaño de la ventana de acuerdo al ancho y alto de la imagen
cv2.resizeWindow("Imagen Completa", ancho, alto)

# Mostrar la imagen completa
cv2.imshow("Imagen Completa", imagen)

# Esperar a que se presione una tecla y cerrar la ventana
cv2.waitKey(0)
cv2.destroyAllWindows()

