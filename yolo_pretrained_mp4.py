import cv2
from ultralytics import YOLO
import numpy as np
import os
import gpu_availablility

gpu = gpu_availablility.checkgpu()

def gentxt(class_list):
    print("generating classes.txt")
    with open('classes.txt', 'w') as f:
        for item in class_list.items():
            f.write(str(item)+"\n")

model = YOLO("yolov8m.pt")

class_list = model.model.names

if not os.path.isfile("classes.txt"):
    gentxt(class_list)

cap = cv2.VideoCapture("catsdogs.mp4")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    results = model(frame, device=gpu)
    result = results[0]

    bboxes = np.array(result.boxes.xyxy.cpu(), dtype="int")
    classes = np.array(result.boxes.cls.cpu(), dtype="int")
    confidences = np.array(result.boxes.conf.cpu(), dtype="double")
    
    for bbox, cls, conf in zip(bboxes, classes, confidences) :

        (x, y, x2, y2) = bbox
        print("x", x, "; y", y)
        cv2.rectangle(frame, (x,y), (x2, y2), (0, 0, 225), 3)
        print(str(cls))
        cls_name = class_list[cls]
        cv2.putText(frame, str(cls) + "; " + str(cls_name) + "; " + str("%.2f" % round(conf, 2)), (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 225), 3)

    cv2.imshow("Img", frame)
    key = cv2.waitKey(0)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
