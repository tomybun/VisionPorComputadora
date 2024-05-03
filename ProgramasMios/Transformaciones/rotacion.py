#!/usr/bin/env python
# -*- coding: utf-8 -*-


import cv2

def rotate(image, angle, center=None, scale=1.0):

    (h, w) = image.shape[:2]
    
    if center is None:
        center = (w/2, h/2)
        
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))
    
    return rotated


img = cv2.imread('hoja.png' , 1)

#Como tenia problemas para abrir la foto completa hice esto:

# Obtener el ancho y alto de la imagen
alto, ancho, canales = img.shape
# Crear una ventana con el nombre "Imagen Completa"
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
# Ajustar el tamaño de la ventana de acuerdo al ancho y alto de la imagen
cv2.resizeWindow('image', ancho, alto)

while True:
    cv2.imshow('image', img)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('k'):
        break
        
cv2.destroyAllWindows()

imagen_rotada = rotate(img,30)
     
while True:
    cv2.imshow('imagen transladada', imagen_rotada)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('k'):
        break        
        
        
cv2.destroyAllWindows()
