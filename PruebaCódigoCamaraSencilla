import cv2

cap = cv2.VideoCapture(0) #0 es para usar la camara

while True:
    ret, frame = cap.read()

    #gray = cv2.cvtColor(frame, cv2.COLOR_BAYER_BG2GRAY)

    cv2.imshow('Video', frame)
    #cv2.imshow('Grises', gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
