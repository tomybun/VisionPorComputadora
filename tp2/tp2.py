#!/usr/bin/envpython
#-*-coding:utf-8 -*-


import cv2


img = cv2.imread('hoja.png' , 0)

cv2.imshow('fotito', img)
cv2.waitKey(0)
cv2.destroyAllWindows()	

# Para resolverlo podemos usar dos for anidados
for i, row in enumerate(img) :
	for j, col in enumerate(row) :
		if col < 240:
			img[i][j] = 0
		else:
			img[i][j] = 255
	

cv2.imwrite('resultado.png', img)

cv2.imshow('fotito', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
