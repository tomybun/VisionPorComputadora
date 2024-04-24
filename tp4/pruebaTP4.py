import cv2

blue = (255, 0, 0)
green = (0, 255, 0)
red = (0, 0, 255)
drawing = False  # true si el botón está presionado
mode = True  # si True, rectángulo, sino línea, cambia con ’m’
xybutton_down = -1, -1
img = None
img_copia = None

def dibuja(event, x, y, flags, param):
    global xybutton_down, drawing, mode, img
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        xybutton_down = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing is True:
            img = img_copia.copy()
            if mode is True:
                cv2.rectangle(img, xybutton_down, (x, y), blue, -1)
            else:
                cv2.line(img, xybutton_down, (x, y), red, 2)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False


img = cv2.imread('hoja.png', 1)
img_copia = img.copy()
cv2.namedWindow('image')
cv2.setMouseCallback('image', dibuja)

while True:
    cv2.imshow('image', img)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('m'):
        mode = not mode
    elif k == 27:
        break
        
cv2.destroyAllWindows()

