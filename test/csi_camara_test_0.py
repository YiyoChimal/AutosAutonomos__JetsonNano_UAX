import cv2

# Ajusta width/height/framerate/flip-method a tu necesidad
gst = (
    "nvarguscamerasrc ! "
    "video/x-raw(memory:NVMM), width=1280, height=720, framerate=30/1, format=NV12 ! "
    "nvvidconv flip-method=0 ! "
    "video/x-raw, format=BGRx ! "
    "videoconvert ! "
    "video/x-raw, format=BGR ! "
    "appsink drop=true max-buffers=1 sync=false"
)

cap = cv2.VideoCapture(gst, cv2.CAP_GSTREAMER)
if not cap.isOpened():
    raise RuntimeError("No pude abrir la CSI con GStreamer. Revisa soporte GStreamer en OpenCV y la cámara.")

while True:
    ok, frame = cap.read()
    if not ok:
        print("Frame perdido"); break
    # ... usa el frame (mostrar, procesar, etc.)
    cv2.imshow("CSI", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC para salir
        break

cap.release()
cv2.destroyAllWindows()
