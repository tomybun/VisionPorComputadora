#!/usr/bin/envpython
#-*-coding:utf-8 -*-



import cv2

cap = cv2.VideoCapture(0)

while(True):
	#devuelve una tupla, en ret el estado en im la imagen
	ret, img = cap.read()
	
	cv2.imshow('img',img)
	
					# esta and con FF es para considerar sólo los primeros 8 bits
	key = cv2.waitKey(1) & 0xFF  	# Espera una tecla y almacena su valor 
	
	
	if(key == ord('q')):
		break
	
	if(key == ord('f')):
		cv2.imwrite('Fotito.png', img)
		break

cap.release()
cv2.destroyAllWindows()
