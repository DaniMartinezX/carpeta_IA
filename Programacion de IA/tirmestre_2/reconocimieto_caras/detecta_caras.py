import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

import pylab

imagenes = []

individuos = {"messi": 0, "einstein": 1, "topuria": 2, "kiko": 3}

def nombre_sujeto(numero):
    nombre = ''
    if numero == 0: nombre = "messi"
    elif numero == 1: nombre = "einstein"
    elif numero == 2: nombre = "topuria"
    else: nombre = "kiko"
    return nombre

def cargar_imagenes():
    imagenes = []
    tipos = []

    # MESSI
    for i in range(5):
        # JPG
        ruta = f"C:\\Users\\daniel.martinezcarre\\Desktop\\Repositorios\\ia_repositorio\\Programacion de IA\\tirmestre_2\\reconocimieto_caras\\imagenes\\messi\\messi({i+1}).jpg"
        foto = cv.imread(ruta)
        img = cv.cvtColor(foto, cv.COLOR_BGR2RGB)
        imagenes.append(img)
        tipos.append(individuos["messi"])

    # EINSTEIN
    for i in range(6):
        ruta = f"C:\\Users\\daniel.martinezcarre\\Desktop\\Repositorios\\ia_repositorio\\Programacion de IA\\tirmestre_2\\reconocimieto_caras\\imagenes\\einstein\\einstein({i+1}).jpg"
        foto = cv.imread(ruta)
        img = cv.cvtColor(foto, cv.COLOR_BGR2RGB)
        imagenes.append(img)
        tipos.append(individuos["einstein"])
    # ILIA TOPURIA
    for i in range(7):
        if i == 0:
            # PNG
            ruta = f"C:\\Users\\daniel.martinezcarre\\Desktop\\Repositorios\\ia_repositorio\\Programacion de IA\\tirmestre_2\\reconocimieto_caras\\imagenes\\ilia_topuria\\topuria({i+1}).png"
            foto = cv.imread(ruta)
            img = cv.cvtColor(foto, cv.COLOR_BGR2RGB)
            imagenes.append(img)
            tipos.append(individuos["topuria"])
        else:
            # JPG
            ruta = f"C:\\Users\\daniel.martinezcarre\\Desktop\\Repositorios\\ia_repositorio\\Programacion de IA\\tirmestre_2\\reconocimieto_caras\\imagenes\\ilia_topuria\\topuria({i+1}).jpg"
            foto = cv.imread(ruta)
            img = cv.cvtColor(foto, cv.COLOR_BGR2RGB)
            imagenes.append(img)
            tipos.append(individuos["topuria"])
    # KIKO RIVERA
    for i in range(7):
        ruta = f"C:\\Users\\daniel.martinezcarre\\Desktop\\Repositorios\\ia_repositorio\\Programacion de IA\\tirmestre_2\\reconocimieto_caras\\imagenes\\kiko_rivera\\kiko_rivera({i+1}).jpg"
        foto = cv.imread(ruta)
        img = cv.cvtColor(foto, cv.COLOR_BGR2RGB)
        imagenes.append(img)
        tipos.append(individuos["kiko"])
    return imagenes, tipos

def detectar_caras(imagenes):
    list_rois = []
    for i in imagenes:
        face_cascade = cv.CascadeClassifier(cv.data.haarcascades + \
                                        'haarcascade_frontalface_default.xml')

        gris = cv.cvtColor(i, cv.COLOR_BGR2GRAY)
        caras = face_cascade.detectMultiScale(gris, 1.2, 3)
        img2 = i.copy()
        for (x,y,w,h) in caras:
            cv.rectangle(img2, (x,y), (x+w, y+h), (0,0,255), 4)
            roi = gris[y:y+h, x:x+w]
            list_rois.append(roi)
            break
        plt.imshow(img2)
        #plt.show()
    return list_rois
plt.show()
imagenes, individuos = cargar_imagenes()
rois = detectar_caras(imagenes)

# Creación del modelo
modelo = cv.face.LBPHFaceRecognizer_create()
modelo.train(rois, np.array(individuos))


#------------------------ PREDICCIÓN ------------------------

# Se saca la FOTO
path_messi = "C:\\Users\\daniel.martinezcarre\\Desktop\\Repositorios\\ia_repositorio\\Programacion de IA\\tirmestre_2\\reconocimieto_caras\\imagenes\\messi\\MESSI.jpg"
foto_messi = cv.imread(path_messi)
img_pru = cv.cvtColor(foto_messi, cv.COLOR_BGR2RGB)
plt.imshow(img_pru)
plt.show()


# Se saca el ROI
face_cascade = cv.CascadeClassifier(cv.data.haarcascades + \
                                    'haarcascade_frontalface_default.xml')
gris = cv.cvtColor(img_pru, cv.COLOR_BGR2GRAY)
caras = face_cascade.detectMultiScale(gris, 1.2, 3)
img2 = img_pru.copy()
for (x,y,w,h) in caras:
    cv.rectangle(img2, (x,y), (x+w, y+h), (0,0,255), 4)
    roi_pru = gris[y:y+h, x:x+w]


# Cuanto menos sea el parámetro de 'confidence' mejor
prediccion, confidence = modelo.predict(roi_pru)

# Saco nombre del sujeto
prediccion = nombre_sujeto(prediccion)

print(f"Predicción: { prediccion }\n Confidence: {confidence}")

