import numpy as np
import cv2

cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
while True:
    ret,frame=cap.read()
    edges=cv2.Canny(frame,100,200)
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(gray,(5,5),0)
    cv2.imshow('Edges',edges)
    cv2.imshow('video',blur)
    cv2.imshow('video_gray',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
