import socket

# Set up server
server_ip = '192.168.159.116'  # '192.168.159.117' # HoloLens Marlon
server_port = 8888
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

            # Wait for message from client
            message = client_socket.recv(1024)
            print("Received message from client:", message.decode())

            # Send response based on received message
            if message.strip() == b"Hello from HoloLens!":
                print("Sent TRUE")
                client_socket.sendall(b"TRUE")
            else:
                print("Sent FALSE")
                client_socket.sendall(b"FALSE")

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
