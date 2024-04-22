import asyncio
import websockets


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
    # This is just a placeholder
    processed_data = "Data processed successfully"
    return processed_data


start_server = websockets.serve(websocket_server, "192.168.159.116", 8880)
print('WebSocketServer started.')
print('Waiting for Client to connect.')
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
