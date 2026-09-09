# Detector de objetos con Haar Cascade (Python + OpenCV)

Implementación del tutorial ["9 DETECTOR DE OBJETOS con Haar Cascade"](https://github.com/GabySol/OmesTutorials2020/tree/master/9%20DETECTOR%20DE%20OBJETOS%20con%20Haar%20Cascade)
de OmesTutorials2020. Detecta en tiempo real, con la webcam, cualquier
objeto para el que hayas entrenado un clasificador Haar Cascade propio.

## ¿Puedo elegir qué detectar?

Sí. Un Haar Cascade no viene "sabiendo" detectar nada en particular: tú lo
entrenas mostrándole muchas fotos del objeto que quieres reconocer (positivas)
y fotos sin ese objeto (negativas/fondo). El resultado del entrenamiento es un
archivo `cascade.xml`, y ese archivo es literalmente "qué se detecta". Cambiar
de objeto = entrenar un `cascade.xml` distinto, sin tocar el código de
detección.

Funciona mejor con objetos **rígidos y con textura/patrón definido** (logos,
cajas, juguetes, señales, caras, etc.). No es la mejor técnica para objetos
deformables o con apariencia muy variable (para eso conviene un modelo de
deep learning tipo YOLO).

## Estructura

```
capturandoObjetos.py   # Paso 1: captura fotos del objeto (positivas) con la webcam
detectando.py           # Paso 3: detecta el objeto en vivo usando cascade.xml
requirements.txt
n/                       # se crea sola, aquí caen las fotos capturadas
cascade.xml              # tú lo generas en el paso 2 (no incluido)
```

## Instalación

```bash
pip install -r requirements.txt
```

## Paso 1 — Capturar imágenes positivas

```bash
python capturandoObjetos.py
```

- Se abre la webcam con un rectángulo azul guía.
- Coloca el objeto que quieres detectar dentro del rectángulo.
- Presiona **s** para guardar una foto (carpeta `n/`), muévelo un poco y
  repite. Junta idealmente **cientos** de fotos variando ángulo, distancia,
  fondo e iluminación.
- **ESC** para salir.

También necesitas **imágenes negativas**: fotos variadas que *no* contengan
el objeto (habitaciones, calles, objetos distintos, etc.). Pueden ser fotos
sueltas que ya tengas o que captures con el mismo script apuntando a otra
cosa.

## Paso 2 — Entrenar el clasificador (fuera de este script)

Este paso no es un script de Python: se usa una herramienta externa que arma
el archivo `cascade.xml` a partir de tus imágenes positivas/negativas. Dos
opciones equivalentes:

- **Cascade Trainer GUI** (Windows, la que usa el tutorial original):
  https://amin-ahmadi.com/cascade-trainer-gui/
- **`opencv_traincascade`** por línea de comandos (Linux/Mac), que viene con
  `opencv` compilado con los módulos de `apps`, o vía el paquete
  `opencv-contrib-python` + binarios de OpenCV. Requiere primero generar el
  `.vec` de positivas con `opencv_createsamples`.

El proceso general, con cualquiera de las dos:

1. Cargar la carpeta de imágenes positivas (las de `n/`) y la de negativas.
2. Elegir el tamaño de muestra (por ejemplo 24x24 o similar al `width=38`
   usado al capturar).
3. Elegir número de "stages" (12–20 es un punto de partida típico) y lanzar
   el entrenamiento. Puede tardar de minutos a varias horas según cuántas
   imágenes y stages uses.
4. Al terminar obtienes `cascade.xml`. Cópialo a la raíz de este proyecto,
   junto a `detectando.py`.

## Paso 3 — Detectar en vivo

```bash
python detectando.py
```

- Abre la webcam y dibuja un rectángulo verde + etiqueta sobre cada
  detección del objeto.
- **ESC** para salir.

Si las detecciones son muy pocas, muchas falsas, o parpadean, ajusta en
`detectando.py`:

- `scaleFactor`: qué tan finamente se reescala la imagen buscando el objeto
  (más cerca de 1.0 = más preciso pero más lento).
- `minNeighbors`: cuántas detecciones vecinas se necesitan para confirmar
  una — súbelo para reducir falsos positivos.
- `minSize`: tamaño mínimo (px) de detección — súbelo si detecta ruido
  pequeño que no es el objeto.
- `LABEL`: el texto que se muestra sobre la detección.
- `CASCADE_PATH`: qué archivo `cascade.xml` cargar (útil si tienes varios
  detectores y quieres alternar entre ellos).

## Créditos

Tutorial original y explicación en video/blog:
- Blog: https://omes-va.com/como-crear-tu-propio-detector-de-objetos-con-haar-cascade-python-y-opencv/
- Video: https://youtu.be/v_cwOq06g9E

---

# Bonus: Detector "¿Formal o informal?" (`formal_o_informal.html`)

Un segundo detector, aparte del de Haar Cascade, para el gag de la feria:
alguien se para frente a la cámara y la página dice si va **formal** o
**informal**. Esto NO usa Haar Cascade — usa un clasificador de imágenes
entrenado en [Teachable Machine](https://teachablemachine.withgoogle.com/),
que es la herramienta correcta para este tipo de tarea (clasificar un
"estilo" completo, no detectar un objeto rígido puntual).

## Cómo prepararlo

1. Entra a https://teachablemachine.withgoogle.com/ → **Get Started** →
   **Image Project** → **Standard image model**.
2. Crea dos clases: **Formal** e **Informal**.
3. En cada clase, usa **Webcam** para capturar fotos:
   - *Formal*: tu compañero con traje/vestido/gala, varios ángulos y poses.
   - *Informal*: ropa casual (playera, jeans, etc.), también varios ángulos
     y, si puedes, varias personas distintas para que generalice mejor.
   - Mientras más fotos y más variedad (distancia, luz, pose), mejor.
4. Click **Train Model** (tarda segundos/pocos minutos, corre en tu navegador).
5. Prueba en vivo con el preview de la misma página antes de exportar.
6. Click **Export Model** → pestaña **Upload (shareable link)** →
   **Upload my model** → copia el link que te da (algo como
   `https://teachablemachine.withgoogle.com/models/AbC123XyZ/`).
7. Abre `formal_o_informal.html` en un editor y reemplaza
   `PEGA_AQUI_TU_LINK_DE_TEACHABLE_MACHINE` por ese link, dentro de las
   comillas de `MODEL_URL`.

## Cómo correrlo

Simplemente abre `formal_o_informal.html` con doble clic (o
`xdg-open formal_o_informal.html`) en tu navegador. Dale permiso a la
cámara y presiona **Iniciar cámara**. El fondo cambia de color y muestra
**🎩 FORMAL** o **😅 INFORMAL** con el porcentaje de confianza según lo que
detecta.

No necesita Python, ni instalar nada — todo corre en el navegador vía
TensorFlow.js.
# viernes
