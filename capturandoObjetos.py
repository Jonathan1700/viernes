"""
Paso 1: Captura de imágenes para entrenar el detector.

Abre la webcam, dibuja un rectángulo guía en pantalla y guarda como imagen
todo lo que quede dentro de ese rectángulo cada vez que presionas 's'.
Usa esto para capturar decenas/cientos de fotos del OBJETO que quieres
detectar (muéstraselo a la cámara en distintos ángulos, distancias y luces).

Controles:
  s   -> guarda una imagen del recuadro actual en la carpeta 'n'
  ESC -> salir
"""

import cv2
import imutils
import os

Datos = 'n'
if not os.path.exists(Datos):
    print('Carpeta creada:', Datos)
    os.makedirs(Datos)

cap = cv2.VideoCapture(0)

# Coordenadas del rectángulo guía (ajústalas a tu gusto/tamaño de cámara)
x1, y1 = 190, 80
x2, y2 = 450, 398

count = 0
while True:

    ret, frame = cap.read()
    if ret == False:
        break

    imAux = frame.copy()
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

    objeto = imAux[y1:y2, x1:x2]
    objeto = imutils.resize(objeto, width=38)

    k = cv2.waitKey(1)
    if k == ord('s'):
        cv2.imwrite(Datos + '/objeto_{}.jpg'.format(count), objeto)
        print('Imagen almacenada:', 'objeto_{}.jpg'.format(count))
        count = count + 1
    if k == 27:
        break

    cv2.imshow('frame', frame)
    cv2.imshow('objeto', objeto)

cap.release()
cv2.destroyAllWindows()
