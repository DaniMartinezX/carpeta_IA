import os
import cv2 as cv
import numpy as np

def click_raton(event, x, y, flags, param):
    # Para sobreescribir la variable
    global color_punto
    if event == cv.EVENT_LBUTTONDBLCLK:
        b,g,r = frame[y, x]
        color_punto = np.uint8([[[b, g, r]]])
        color_punto = cv.cvtColor(color_punto, cv.COLOR_BGR2HSV)
        print(f"Click en {x}, {y}, color = {color_punto}")


def croma(img1, video):
    b,g,r = img1
    color_punto = np.uint8([[[b, g, r]]])
    color_punto = cv.cvtColor(color_punto, cv.COLOR_BGR2HSV)
    # Se definen los rangos de color a reemplazar
    color_minimo = np.array([color_punto[0,0,0] - 10,10,10])
    color_maximo = np.array([color_punto[0,0,0] + 10,255,255])

    while True:
        # Lee un frame del video
        ret, frame = video.read()

        # Comprueba si se ha leído un frame válido
        if ret == False:
            break

        # Convierte el frame a escala de grises
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # Crea una máscara con los píxeles del color a reemplazar
        mascara = cv.inRange(gray, color_minimo, color_maximo)
        # Aplica la máscara al video
        frame = cv.bitwise_and(frame, frame, mask=mascara)
        # Pega la foto de fondo al video
        frame = cv.bitwise_or(frame, img1, mask=mascara)
        # Muestra el frame
        cv.imshow("Video", frame)


#video = cv.VideoCapture(0)
fichero = "Programacion de IA\\tirmestre_2\\imagenes\\video_chapa.mp4"
video = cv.VideoCapture(0)
cv.namedWindow("Frame")
cv.setMouseCallback("Frame", click_raton)



 
color_punto = None
todo_preparado = False

while(True): 
    ret, frame = video.read()
    if color_punto is not None:
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        color_minimo = np.array([color_punto[0,0,0] - 10,10,10])
        color_maximo = np.array([color_punto[0,0,0] + 10,255,255])

        click_raton

        mascara = cv.inRange(hsv, color_minimo, color_maximo)
        cv.namedWindow("Mascara")
        cv.setMouseCallback("Mascara", click_raton)
        
        cv.imshow("Mascara", mascara)
    if ret == True:
        frame = cv.flip(frame, 1)
        cv.imshow("Frame", frame)
    if cv.waitKey(10) & 0xFF == 32:
        # Captura el frame actual
        captura = frame.copy()
        cv.namedWindow("Cap")
        cv.imshow("Cap", captura)
        todo_preparado = True
        print("Debería de haber sacado a captura ")
    if todo_preparado:                
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        color_minimo = np.array([color_punto[0,0,0] - 10,10,10])
        color_maximo = np.array([color_punto[0,0,0] + 10,255,255])

        mascara1 = cv.inRange(gray, color_minimo, color_maximo)
        mascara2 = cv.inRange(gray, color_minimo, color_maximo)
        mascara3 = cv.inRange(gray, color_minimo, color_maximo)

        mascara_final = cv.merge(mascara1, mascara2, mascara3)
        
        fondo_mascara = cv.bitwise_and(captura, mascara_final)
        no_mask = cv.bitwise_not(mascara_final)
        frame_nomask = cv.bitwise_and(frame, no_mask, mask=mascara)
        final = cv.bitwise_or(frame_nomask, fondo_mascara, mask=mascara)
        cv.imshow("Final", final)   

    if cv.waitKey(10) & 0xFF == 27: break
video.release()
cv.destroyAllWindows()
       