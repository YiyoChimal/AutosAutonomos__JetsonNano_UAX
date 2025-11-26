import cv2
import numpy as np
import matplotlib.pyplot as plt
from jetcam.csi_camera import CSICamera
import ipywidgets
from IPython.display import display
from jetcam.utils import bgr8_to_jpeg
import traitlets
import pandas as pd

# -------------------------------
# Función para detectar los dos objetos amarillos principales
# -------------------------------
def detectar_lineas_amarillas(frame):
    # Convertimos la imagen de BGR (por defecto en OpenCV) a HSV,
    # ya que HSV facilita la detección de colores
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Definimos el rango del color amarillo en HSV
    # (estos valores pueden ajustarse según la iluminación de la cámara)
    lower_yellow = np.array([h_min.value, s_min.value, v_min.value], dtype=np.uint8) 
    upper_yellow = np.array([h_max.value, s_max.value, v_max.value], dtype=np.uint8) # mantenemos límite superior

    # Creamos una máscara binaria donde solo quedan los píxeles amarillos
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Buscamos los contornos de las regiones amarillas detectadas
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #seleccionamos solo los contornos que esten es cierto intervalo
    contours_selected=[]
    for i in contours:
        area_contour=cv2.contourArea(i)
        if 700<area_contour:
            contours_selected.append(i)
            
        
    # Ordenamos los contornos encontrados de mayor a menor área
    # y nos quedamos solo con los dos más grandes (los carriles laterales)
    contours_selected = sorted(contours_selected , key=cv2.contourArea, reverse=True)[:2]

    centers = []  # Lista donde guardaremos los centros de los objetos detectados
    for cnt in contours_selected :
        area_line=cv2.contourArea(cnt)
        # Calculamos los momentos del contorno para hallar el centroide
        M = cv2.moments(cnt)
        if M["m00"] > 0:  # Verificamos que el área no sea cero (para evitar división por cero)
            cx = int(M["m10"] / M["m00"])  # Coordenada X del centro
            cy = int(M["m01"] / M["m00"])  # Coordenada Y del centro
            centers.append((cx, cy))       # Guardamos el centro detectado
            #.append() es un método de las listas en Python que agrega un elemento al final de la lista.
            # Dibujamos el contorno del objeto en verde
            cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 2)

            # Escribir el área encima del objeto
            cv2.putText(frame, f"Area: {int(area_line)}", (cx - 40, cy - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Dibujamos un círculo rojo en el centro del objeto
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

    # Dibujar línea central con margen
    height, width, _ = frame.shape
    mid_x_line = width // 2
    margen = 30  # ancho de la franja de tolerancia

    # Dibujar línea central (verde) y márgenes (rojos)
    cv2.line(frame, (mid_x_line, 0), (mid_x_line, height), (0, 255, 0), 2)
    cv2.line(frame, (mid_x_line - margen, 0), (mid_x_line - margen, height), (0, 0, 255), 1)
    cv2.line(frame, (mid_x_line + margen, 0), (mid_x_line + margen, height), (0, 0, 255), 1)
 
    # Si encontramos exactamente dos objetos amarillos, dibujamos la línea de unión
    if len(centers) == 2:
        (x1, y1), (x2, y2) = centers  # Extraemos las coordenadas de los dos centros

        # Calculamos el punto medio entre los dos objetos
        mid_x = (x1 + x2) // 2
        mid_y = (y1 + y2) // 2

        # Calcular la distancia entre los dos puntos
        distancia = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
        
        if distancia>50:
            # Dibujamos una línea azul que une los dos centros detectados
            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            # Dibujamos un círculo amarillo en el punto medio
            cv2.circle(frame, (mid_x, mid_y), 6, (0, 255, 255), -1)
            # Escribir la distancia en la imagen (en el punto medio de la línea)
            cv2.putText(frame, f"Dist: {distancia}px", (mid_x - 40, mid_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            # Verificar si el punto medio toca la franja central
            if mid_x_line - margen < mid_x < mid_x_line + margen:
                print("Punto medio cruzó la línea central")
            
        
    # Retornamos la imagen procesada
    return frame,mask

# ---- Funciones auxiliares ----
def clamp_ranges():
    """ Asegura que los valores min nunca superen a los max """
    if h_min.value > h_max.value: h_min.value = h_max.value
    if s_min.value > s_max.value: s_min.value = s_max.value
    if v_min.value > v_max.value: v_min.value = v_max.value

def on_reset_clicked(_):
    """ Cuando se hace clic en Reset, restablece valores iniciales """
    h_min.value, h_max.value = 18, 35
    s_min.value, s_max.value = 80, 255
    v_min.value, v_max.value = 50, 255
    status_lbl.value = "HSV reseteado a presets"


# -------------------------------
# Código principal: captura de video en vivo
# -------------------------------
print("program start")

# ---- Sliders HSV (OpenCV: H=0..179, S,V=0..255) ----
# Creamos sliders para controlar dinámicamente los rangos HSV
h_min = ipywidgets.IntSlider(description='H Min', min=0, max=179, value=18)    # Hue mínimo
h_max = ipywidgets.IntSlider(description='H Max', min=0, max=179, value=35)    # Hue máximo
s_min = ipywidgets.IntSlider(description='S Min', min=0, max=255, value=80)    # Saturación mínima
s_max = ipywidgets.IntSlider(description='S Max', min=0, max=255, value=255)   # Saturación máxima
v_min = ipywidgets.IntSlider(description='V Min', min=0, max=255, value=50)    # Brillo mínimo
v_max = ipywidgets.IntSlider(description='V Max', min=0, max=255, value=255)   # Brillo máximo

#Tabla en pandas test
datos = {"Min_val": [18, 80, 50],"Max_val": [35, 255, 255]}
df = pd.DataFrame(datos, columns=["Min_val","Max_val"])
df.index = ["Hue (H)", "Saturation (S)", "Value (V)"]


# Botón para resetear sliders y etiqueta de estado
reset_btn = ipywidgets.Button(description='Reset HSV')     # Botón "Reset HSV"
status_lbl = ipywidgets.HTML(value="Listo")                # Etiqueta de texto (estado)

# Organizamos sliders y botón en un panel vertical
controls = ipywidgets.VBox([ipywidgets.HBox([h_min, h_max]),   # Fila con H Min y H Max
                         ipywidgets.HBox([s_min, s_max]),   # Fila con S Min y S Max
                         ipywidgets.HBox([v_min, v_max]),   # Fila con V Min y V Max
                         reset_btn,                      # Botón Reset
                         status_lbl])  

# Conectamos el botón con la función de reset
reset_btn.on_click(on_reset_clicked)

#cap = cv2.VideoCapture(0)  # Capturamos desde la cámara (0 = cámara por defecto)
#cama dimension 3280x2464
camera = CSICamera(width=224, height=244)
image=camera.read()
#Areas para mostrar imagen
image_widget = ipywidgets.Image(format='jpeg')
image_mask_widget=ipywidgets.Image(format='fpeg')
#Panel que agruapa las dos imagenes
panel=ipywidgets.HBox([image_mask_widget,image_widget])

#Refrescar la camara
camera.running = True

#here is where the procesing of the image has to be done
def callback(change):
    new_image = change['new']
    # Procesamos el frame para detectar los objetos amarillos y dibujar la línea
    resultado,resultado_mask = detectar_lineas_amarillas(new_image)
    image_widget.value = bgr8_to_jpeg(resultado)
    image_mask_widget.value=bgr8_to_jpeg(resultado_mask)

camera.observe(callback, names='value')

display(df,controls,panel)
