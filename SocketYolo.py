import socket
import cv2
import numpy as np
from ultralytics import YOLO
import gpu_availablility
import base64


def convert_image_to_byte_array(img):
    # Convert the OpenCV image to a byte array
    _, buffer = cv2.imencode('.jpg', img)
    byte_array = base64.b64encode(buffer)
    return byte_array


# Set up server
server_ip = '127.0.0.1' # 192.168.159.116 # Computer IP
server_port = 8889
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(5)  # Maximum number of queued connections
# check for gpu
gpu = gpu_availablility.checkgpu()

model = YOLO("runs/detect/train5/weights/best.pt")
print('Model loaded.')
class_list = model.model.names
print('Class List:', class_list)
print('==============================================================================')

try:
    while True:
        # Accept connection
        print("Waiting for connection...")
        client_socket, client_address = server_socket.accept()
        print("Connected to:", client_address)

        try:
            # Send confirmation to client
            #client_socket.sendall(b"Connected to server.")

            # Receive image data from client
            image_data = b""
            while True:
                chunk = client_socket.recv(4096)  # Adjust buffer size as needed
                if not chunk:
                    break
                image_data += chunk

            print(image_data, "  ;  ", type(image_data))

            # Save the received image data to a file (e.g., "received_photo.jpg")
            with open("HoloLens2Prediction/recieved/SDC-received_photo.png", "wb") as file:
                file.write(image_data)

            image = cv2.imread("HoloLens2Prediction/recieved/SDC-received_photo.png")

            # Run inference with the YOLOv8n model on an image
            results = model(image, device=gpu)
            # Extract bounding boxes, classes and confidence scores0
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
            cv2.imwrite('HoloLens2Prediction/predicted/SDC-predictionImage.jpg', image)
            print('Image prediction saved.')
            print('=========================================================')

            # Convert the image to a byte array
            byte_array = convert_image_to_byte_array(image)
            # Send response to client
            client_socket.sendall(byte_array)

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
