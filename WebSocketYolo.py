import socket
import cv2
import numpy as np

# Set up server
server_ip = '192.168.159.114'  # '192.168.159.117' # HoloLens Marlon 192.168.159.104
server_port = 8889
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(5)  # Maximum number of queued connections

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

            print(image_data)
            #print(image_data)

            # Assuming 'imageData' is the byte array received from Unity
            # Decode the JPEG byte array into an image (assuming it's already in RGB format)
            #image = cv2.imdecode(np.frombuffer(image_data, dtype=np.uint8), cv2.IMREAD_COLOR)

            # Convert from BGRA to RGB
            #image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)

            # Now, 'image' should be in RGB format, proceed with saving it or any further processing
            # For example, saving the image
            #cv2.imwrite('output.jpg', image)


            # Save the received image data to a file (e.g., "received_photo.jpg")
            with open("received_photo.jpg", "wb") as file:
                file.write(image_data)
            print("Received and saved image data to 'received_photo.jpg'.")

            # Process the received image data as needed
            # You can use image processing libraries like OpenCV to analyze or manipulate the image

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
