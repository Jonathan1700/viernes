"""
Paso 3: Detección en tiempo real usando un clasificador Haar Cascade.

Por defecto usa el detector de caras que ya viene incluido con
opencv-python (no requiere entrenar ni descargar nada). Si en vez de caras
quieres detectar tu propio objeto, entrena un 'cascade.xml' (ver README.md,
sección de entrenamiento), colócalo junto a este script y cambia
CASCADE_PATH para que apunte a ese archivo. Puedes cambiar libremente:
  - CASCADE_PATH -> qué clasificador (=qué objeto) usar
  - LABEL         -> el texto que se dibuja sobre la detección
  - scaleFactor / minNeighbors / minSize -> sensibilidad de la detección
"""

import os
import sys

import cv2

# Detector de caras incluido con opencv-python. Para usar tu propio
# cascade.xml entrenado, cambia esta línea por: CASCADE_PATH = 'cascade.xml'
CASCADE_PATH = os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml')
LABEL = 'Cara'

if not os.path.exists(CASCADE_PATH):
    sys.exit(
        f"No se encontró '{CASCADE_PATH}'. Si usas tu propio clasificador, "
        "primero entrénalo (ver README.md) y colócalo junto a este script."
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
