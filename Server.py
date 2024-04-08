import socket

# Set up server
server_ip = '127.0.0.1'
server_port = 8888
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(1)

try:
    # Accept connection
    print("Waiting for connection...")
    client_socket, client_address = server_socket.accept()
    print("Connected to:", client_address)

    # Send confirmation to client
    client_socket.sendall(b"Connected to server.")

    # Close connection
    client_socket.close()
    print("Connection closed.")
except Exception as e:
    print("Error:", e)
finally:
    server_socket.close()
