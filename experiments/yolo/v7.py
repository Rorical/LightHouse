# -*- coding: utf-8 -*-
import cv2
import numpy as np
import time
import pyttsx3
from PIL import Image
import matplotlib.pyplot as plt

CONFIDENCE_THRESHOLD = 0.4
NMS_THRESHOLD = 0.4

engine = pyttsx3.init()

net = cv2.dnn.readNet('yolov4-tiny.cfg', 'yolov4-tiny.weights')

model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(416, 416), scale=1/255)

with open("coco.txt", "r", encoding="utf-8") as f:
    labels = f.read().split("\n")

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)

def counter(classids):
    ct = {}
    for i in classids:
        if i in ct:
            ct[i] += 1
        else:
            ct[i] = 1
    return ct

while cap.isOpened():
    start = time.time()
    ret, frame = cap.read()
    #cv2.imshow("cam", frame)
    #if cv2.waitKey(1) == 27:
    #    break
    

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    start = time.time()
    classids, confidences, boxes = model.detect(frame, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
    print("detect time", time.time() - start)    
    
    for box in boxes:
        x, y, w, h = box
        frame = cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 5)
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    plt.imshow(image)
    plt.show()

    objects = counter(classids)
    text = ""
    for index, class_id in enumerate(objects):
        
        count = objects[class_id]
        if text != "":
            text += "和"
        
        if count > 1:
            text += str(count) + "个" + labels[class_id]
        else:
            text +=  labels[class_id]
        
    if text != "":
        engine.say(text)
        engine.runAndWait()


cap.release()
