import cv2 as cv
import numpy as np

def click_raton(event, x, y, flags, param):
    # Para sobreescribir la variable
    global color_punto
    if event == cv.EVENT_LBUTTONDBLCLK:
        b,g,r = img1[y, x]
        color_punto = np.uint8([[[b, g, r]]])
        color_punto = cv.cvtColor(color_punto, cv.COLOR_BGR2HSV)
        print(f"Click en {x}, {y}, color = {color_punto}")

scr1 = cv.imread("Programacion de IA\\tirmestre_2\\imagenes\\nemo.jpg")
cv.namedWindow("Imagen")
cv.setMouseCallback("Imagen", click_raton)


img1 = scr1
hsv = cv.cvtColor(img1, cv.COLOR_BGR2HSV)
color_punto = None

cv.imshow("Imagen", img1)


while True:
    if color_punto is not None:
        color_minimo = np.array([color_punto[0,0,0] - 10,10,10])
        color_maximo = np.array([color_punto[0,0,0] + 10,255,255])

        mascara = cv.inRange(hsv, color_minimo, color_maximo)
        cv.namedWindow("Mascara")
        cv.imshow("Mascara", mascara)
        color_punto = None
    if cv.waitKey(10) & 0xFF == 27: break   # Si pulsa escape sale del bucle, lo de 0xFF es para coger el byte bajo de la imagen.
