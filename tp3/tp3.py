#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import cv2

if(len(sys.argv)>1):
    filename=sys.argv[1]
else:
    print('Pass a filename as first argument')
    sys.exit(0)
    
cap=cv2.VideoCapture(filename)

fourcc=cv2.VideoWriter_fourcc('X','V','I','D')

# Lee el fps de la cámara para no harcodear el retardo de la funcion waitKey
fps = cap.get(cv2.CAP_PROP_FPS)

# Lee el ancho y alto de la imagen capturada para no harcodear el anchoalto del video generado (no elegirlo al azar)
ancho = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
alto = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)


framesize=(int(ancho), int(alto))
out=cv2.VideoWriter('output.mkv',fourcc,fps,framesize)

delay = 1/fps *1000 #x1000 pq la funcion waitkey espera un valor en ms

while(cap.isOpened()):
    ret,frame=cap.read()
    if ret is True:
        #gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        out.write(frame)
        cv2.imshow('Image gray',frame)
        if cv2.waitKey(int(delay)) & 0xFF==ord('q'):
            break
    else:
        break
        
cap.release()
out.release()
cv2.destroyAllWindows()

