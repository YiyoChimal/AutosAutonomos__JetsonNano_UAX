import cv2
import numpy as np

# -------------------------------
# Función para detectar los dos objetos amarillos principales
# -------------------------------
def detectar_lineas_amarillas(frame):
    # Convertimos la imagen de BGR a HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Leer valores actuales de los trackbars
    h_min = cv2.getTrackbarPos("H Min", "Control HSV")
    h_max = cv2.getTrackbarPos("H Max", "Control HSV")
    s_min = cv2.getTrackbarPos("S Min", "Control HSV")
    s_max = cv2.getTrackbarPos("S Max", "Control HSV")
    v_min = cv2.getTrackbarPos("V Min", "Control HSV")
    v_max = cv2.getTrackbarPos("V Max", "Control HSV")
    
    lower_yellow = np.array([h_min, s_min, v_min])
    upper_yellow = np.array([h_max, s_max, v_max])
    
    # Crear máscara para color amarillo
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Encontrar contornos
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filtrar contornos por área mínima
    contours_selected = []
    for cnt in contours:
        area_contour = cv2.contourArea(cnt)
        if area_contour > 700:
            contours_selected.append(cnt)

    # Ordenar y quedarnos con los 2 contornos más grandes
    contours_selected = sorted(contours_selected, key=cv2.contourArea, reverse=True)[:2]

    centers = []
    for cnt in contours_selected:
        area_line = cv2.contourArea(cnt)
        M = cv2.moments(cnt)
        if M["m00"] > 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            centers.append((cx, cy))
            cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 2)
            cv2.putText(frame, f"Area: {int(area_line)}", (cx - 40, cy - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

    # Dibujar línea central con margen
    height, width, _ = frame.shape
    mid_x_line = width // 2
    margen = 30

    cv2.line(frame, (mid_x_line, 0), (mid_x_line, height), (0, 255, 0), 2)
    cv2.line(frame, (mid_x_line - margen, 0), (mid_x_line - margen, height), (0, 0, 255), 1)
    cv2.line(frame, (mid_x_line + margen, 0), (mid_x_line + margen, height), (0, 0, 255), 1)

    if len(centers) == 2:
        (x1, y1), (x2, y2) = centers
        mid_x = (x1 + x2) // 2
        mid_y = (y1 + y2) // 2
        distancia = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
        
        if distancia > 50:
            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.circle(frame, (mid_x, mid_y), 6, (0, 255, 255), -1)
            cv2.putText(frame, f"Dist: {distancia}px", (mid_x - 40, mid_y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            if mid_x_line - margen < mid_x < mid_x_line + margen:
                print("⚠ Punto medio cruzó la línea central")

    return frame


def nothing(x): pass


# Valores iniciales para el color amarillo HSV
PRESET = {
    "H Min": 18,
    "H Max": 35,
    "S Min": 80,
    "S Max": 255,
    "V Min": 50,
    "V Max": 255
}

# Crear ventana para controles HSV solo UNA VEZ
cv2.namedWindow("Control HSV")
cv2.createTrackbar("H Min", "Control HSV", PRESET["H Min"], 179, nothing)
cv2.createTrackbar("H Max", "Control HSV", PRESET["H Max"], 179, nothing)
cv2.createTrackbar("S Min", "Control HSV", PRESET["S Min"], 255, nothing)
cv2.createTrackbar("S Max", "Control HSV", PRESET["S Max"], 255, nothing)
cv2.createTrackbar("V Min", "Control HSV", PRESET["V Min"], 255, nothing)
cv2.createTrackbar("V Max", "Control HSV", PRESET["V Max"], 255, nothing)

# Crear ventana para mostrar resultado solo UNA VEZ
cv2.namedWindow("Carro autonomo - detección de carril")

# Captura de video
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    resultado = detectar_lineas_amarillas(frame)

    # Mostrar resultado en la ventana creada
    cv2.imshow("Carro autonomo - detección de carril", resultado)

    # Esperar tecla 'q' para salir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos y cerrar ventanas al salir
cap.release()
cv2.destroyAllWindows()
