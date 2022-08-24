# -*- coding: utf-8 -*-
import cv2
from PIL import Image
import time
import matplotlib.pyplot as plt

CAMWIDTH = 2560
CAMHEIGHT = 720

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,CAMWIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,CAMHEIGHT)

index = 0

while cap.isOpened():
    ret, frame = cap.read()
    left_img = frame[:, 0:1280]
    right_img = frame[:, 1280:2560]
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    plt.imshow(image)
    plt.show()
    cv2.imwrite("left_calib/left_%d.png"%index, left_img)
    cv2.imwrite("right_calib/right_%d.png"%index, right_img)
    index += 1
    if index > 40:
        break
    time.sleep(2)
    
cap.release()