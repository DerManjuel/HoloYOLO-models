import asyncio
import websockets
import gpu_availablility
import cv2
import numpy as np
from ultralytics import YOLO
import base64
from PIL import Image
from io import BytesIO


async def websocket_server(websocket, path):
    while True:
        try:
            # Receive data from the WebSocket client (HoloLens 2)
            print('Waiting for incoming message.')
            data = await websocket.recv()

            # Process the received data (e.g., image processing)
            print('Processing incoming message.')
            processed_data = process_data(data)

            # Send response back to the WebSocket client
            print('Sending outgoing message.')
            await websocket.send(processed_data)
        except websockets.exceptions.ConnectionClosedError:
            break


def process_data(data):
    # Implement your image processing logic here

    print(type(data) , "  ;  ", data) # this is a string

    # Decode the base64 string to bytes
    image_bytes = base64.b64decode(data)
    print(type(image_bytes))  # , "  ", image_bytes)

    with open("HoloLens2Prediction/recieved/received_photoWebSocket1.png", "wb") as file:
        file.write(image_bytes)

    # Create a BytesIO object to wrap the bytes; can't save as image here
    image_stream = BytesIO(image_bytes)
    print(type(image_stream))  # , "   ", image_stream)

    # Open the image using PIL
    image = Image.open(image_stream)

    # Convert the PIL image to a cv2 image
    cv2_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    cv2.imwrite("HoloLens2Prediction/recieved/received_photoWebSocket2.png", cv2_image)

    '''image = cv2.imread("HoloLens2Prediction/recieved/received_photoWebSocket.png")

    # Run inference with the YOLOv8n model on an image
    results = model(image, device=gpu)
    # Extract bounding boxes, classes and confidence scores
    result = results[0]
    bboxes = np.array(result.boxes.xyxy.cpu(), dtype="int")
    classes = np.array(result.boxes.cls.cpu(), dtype="int")
    confidences = np.array(result.boxes.conf.cpu(), dtype="double")

    # Add bounding boxes, class names and confidence scores to image
    for bbox, cls, conf in zip(bboxes, classes, confidences):

        (x, y, x2, y2) = bbox
        cv2.rectangle(image, (x, y), (x2, y2), (0, 0, 225), 3)

        cls_name = class_list[cls]

        # print results on images
        if y <= 25:
            cv2.putText(image, str(cls) + "; " + str(cls_name) + "; " + str("%.2f" % round(conf, 2)),
                        (x, y2 - 5),
                        cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 225), 3)
        else:
            cv2.putText(image, str(cls) + "; " + str(cls_name) + "; " + str("%.2f" % round(conf, 2)),
                        (x, y + 35),
                        cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 225), 3)

        print('Found this in image:')
        print("x", x, "; y", y)
        print(str(cls), str(cls_name))

    # save .jpg
    cv2.imwrite('HoloLens2Prediction/predicted/predictionImageWebSocket.jpg', image)
    print('Image prediction saved.')
    print('=========================================================')'''

    processed_data = "Data processed successfully"
    return processed_data


# check for gpu
gpu = gpu_availablility.checkgpu()

model = YOLO("runs/detect/train5/weights/best.pt")
print('Model loaded.')
class_list = model.model.names
print('Class List:', class_list)
print('==============================================================================')

start_server = websockets.serve(websocket_server, "127.0.0.1", 8880)  # 192.168.159.116
print('WebSocketServer started.')
print('Waiting for Client to connect.')
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
