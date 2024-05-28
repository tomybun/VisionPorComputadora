#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import cv2

xy_iniciales = -1, -1
drawing = False
k = None
ban = False
callback = False
blue = (255, 0, 0)
red = (0, 0, 255)
xybutton_down = 0, 0

###############################################################################################################################

# mouse callback
def draw_line(event, x, y, flags, param):
    global xybutton_down, img_rectificada, img_rectificada_copy
    if event == cv2.EVENT_LBUTTONDOWN:
        print("cv2.EVENT_LBUTTONDOWN", event)
        xybutton_down = x, y
        cv2.circle(img_rectificada_copy, xybutton_down, 9, red, 2)
    elif event == cv2.EVENT_LBUTTONUP:
        print("cv2.EVENT_LBUTTONUP", event)
        cv2.line(img_rectificada_copy, xybutton_down, (x, y), blue, 3)
        # Actualizar la ventana con la imagen modificada
        cv2.imshow('imagen rectificada', img_rectificada_copy)

###############################################################################################################################

def calcular_homografia(puntos_origen, puntos_destino):
    # Convertir los puntos a formato adecuado para cv2.getPerspectiveTransform
    pts_origen = np.array(puntos_origen, dtype=np.float32)
    pts_destino = np.array(puntos_destino, dtype=np.float32)

    # Calcular la homografía entre los puntos correspondientes
    homografia = cv2.getPerspectiveTransform(pts_origen, pts_destino)

    return homografia

###############################################################################################################################

# obtiene el tamaño de la imagen y adapta la ventana
def tamIMG(img, nombreVentana):
    # Obtener el ancho y alto de la imagen
    alto, ancho, canales = img.shape
    # Crear una ventana con el nombre "Imagen Completa"
    cv2.namedWindow(nombreVentana, cv2.WINDOW_NORMAL)
    # Ajustar el tamaño de la ventana de acuerdo al ancho y alto de la imagen
    cv2.resizeWindow(nombreVentana, ancho, alto)

###############################################################################################################################

def dibuja(event, x, y, flags, param):
    global xy_iniciales, drawing, img, puntos_seleccionados, contador_puntos, puntos_destino

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        xy_iniciales = x, y

        puntos_seleccionados.append([x, y])
        contador_puntos += 1
        cv2.circle(img, (x, y), 5, (0, 255, 0), -1)

        if contador_puntos == 4:
            # Convertir los puntos seleccionados a un formato adecuado para la función de transformación afín
            puntos_destino = np.array(puntos_seleccionados, dtype=np.float32)
            # Deshabilitar el manejo de eventos de ratón
            cv2.setMouseCallback('imagen', lambda *args: None)

###############################################################################################################################

# Lectura de la imagen
img = cv2.imread('i_cancha.png', 1)

# Crear una copia de la imagen de fondo para mostrar los puntos seleccionados
img_aux = img.copy()

# Obtiene el tamaño de la imagen y adapta la ventana
tamIMG(img, 'imagen')

# Inicializar variables para la selección de puntos
puntos_seleccionados = []
contador_puntos = 0
puntos_destino = []

# Bandera que indica si se destruyo la primer ventana
ventana_destruida = False

cv2.setMouseCallback('imagen', dibuja)

while True:
    if ventana_destruida == False:
        cv2.imshow('imagen', img)
        k = cv2.waitKey(1) & 0xFF

    # Elimina los puntos dibujados
    if(k == ord('r')):
        img = img_aux.copy()
        contador_puntos = 0
        puntos_seleccionados.clear()

    if k == 27:
        break

    # Homografia
    if contador_puntos == 4:
        if ventana_destruida == False:
            cv2.destroyWindow('imagen')
            ventana_destruida = True

        alto, ancho, _ = img_aux.shape

        # Calcular la matriz de homografia
        # Arma las 4 esquinas de la imagen a que será rectificada
        puntos_destino = np.array([[0, 0],
                                   [ancho - 1, 0],
                                   [0, alto - 1],
                                   [ancho - 1, alto - 1]]).astype(np.float32)

        homografia = calcular_homografia(puntos_seleccionados, puntos_destino)

        # Aplicar la homografía a la imagen
        img_rectificada = cv2.warpPerspective(img_aux, homografia, (ancho, alto))
        img_rectificada_copy = img_rectificada.copy()  # Crear una copia para dibujar las líneas

        if callback == False:
            cv2.namedWindow('imagen rectificada')
            cv2.setMouseCallback('imagen rectificada', draw_line)
            callback = True

        cv2.imshow('imagen rectificada', img_rectificada_copy)
        k = cv2.waitKey(1) & 0xFF

cv2.destroyAllWindows()

