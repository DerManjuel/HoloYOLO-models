import socket
import cv2
import numpy as np
from ultralytics import YOLO
import os
import gpu_availablility

# Set up server
server_ip = '192.168.159.114'  # '192.168.159.117' # HoloLens Marlon 192.168.159.104
server_port = 8889
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(5)  # Maximum number of queued connections
# check for gpu
gpu = gpu_availablility.checkgpu()

try:
    while True:
        # Accept connection
        print("Waiting for connection...")
        client_socket, client_address = server_socket.accept()
        print("Connected to:", client_address)

        try:
            # Send confirmation to client
            client_socket.sendall(b"Connected to server.")

            # Receive image data from client
            image_data = b""
            while True:
                chunk = client_socket.recv(4096)  # Adjust buffer size as needed
                if not chunk:
                    break
                image_data += chunk

            print(type(image_data))

            # Save the received image data to a file (e.g., "received_photo.jpg")
            with open("HoloLens2Prediction/recieved/received_photo.png", "wb") as file:
                file.write(image_data)

            image = cv2.imread("HoloLens2Prediction/recieved/received_photo.png")

            # Assuming 'imageData' is the byte array received from Unity
            # Decode the JPEG byte array into an image (assuming it's already in RGB format)
            #image = cv2.imdecode(np.frombuffer(image_data, dtype=np.uint8), cv2.IMREAD_COLOR)

            # Convert from BGRA to RGB
            #image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)

            # Now, 'image' should be in RGB format, proceed with saving it or any further processing
            # For example, saving the image
            #cv2.imwrite('output.jpg', image)

            model = YOLO("runs/detect/train6/weights/best.pt")
            print('Model loaded.')
            class_list = model.model.names
            print('Class List:', class_list)
            print('==============================================================================')

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
            cv2.imwrite('HoloLens2Prediction/predicted/predictionImage.jpg', image)
            print('Image prediction saved.')
            print('=========================================================')

            # Send response to client
            client_socket.sendall(b"Image received successfully.")

        except Exception as e:
            print("Error during communication:", e)

        finally:
            # Close connection
            client_socket.close()
            print("Connection closed.")

except Exception as e:
    print("Error:", e)

finally:
    server_socket.close()
