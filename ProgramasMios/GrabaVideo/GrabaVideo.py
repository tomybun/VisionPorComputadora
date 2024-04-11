#!/usr/bin/envpython
#-*-coding:utf-8 -*-


import cv2
cap = cv2.VideoCapture(0)

# Lee el fps de la cámara para no harcodear el retardo de la funcion waitKey (igual en este programa no hace falta)
fps = cap.get(cv2.CAP_PROP_FPS)

# Lee el ancho y alto de la imagen capturada para no harcodear el anchoalto del video generado (no elegirlo al azar)
#ancho = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
#alto = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
#fps = 20.0
anchoalto = (640 ,480)

out = cv2.VideoWriter('mivideo.mkv', fourcc, fps, anchoalto)
while (cap.isOpened()):
	ret,img = cap.read()
	if ret is True :
		out.write(img)
		cv2.imshow('Mi Video',img)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	else:
		break
		
cap.release()
out.release()
cv2.destroyAllWindows()
