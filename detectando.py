"""
Paso 3: Detección en tiempo real usando el clasificador Haar Cascade
entrenado (cascade.xml).

Este script SOLO funciona si ya tienes un archivo 'cascade.xml' entrenado
para el objeto que quieres detectar (ver README.md, sección de
entrenamiento). Puedes cambiar libremente:
  - CASCADE_PATH -> qué clasificador (=qué objeto) usar
  - LABEL         -> el texto que se dibuja sobre la detección
  - scaleFactor / minNeighbors / minSize -> sensibilidad de la detección
"""

import os
import sys

import cv2

CASCADE_PATH = 'cascade.xml'
LABEL = 'Objeto'

if not os.path.exists(CASCADE_PATH):
    sys.exit(
        f"No se encontró '{CASCADE_PATH}'. Primero debes entrenar tu propio "
        "clasificador (ver README.md) y colocarlo junto a este script."
    )

objetoClassif = cv2.CascadeClassifier(CASCADE_PATH)

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()
    if ret == False:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    objetos = objetoClassif.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(70, 78),
    )

    for (x, y, w, h) in objetos:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, LABEL, (x, y - 10), 2, 0.7, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
