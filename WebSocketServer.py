import asyncio
import websockets


async def websocket_server(websocket, path):
    while True:
        try:
            # Receive data from the WebSocket client (HoloLens 2)
            data = await websocket.recv()

            # Process the received data (e.g., image processing)
            processed_data = process_data(data)

            # Send response back to the WebSocket client
            await websocket.send(processed_data)
        except websockets.exceptions.ConnectionClosedError:
            break


def process_data(data):
    # Implement your image processing logic here
    # This is just a placeholder
    processed_data = "Data processed successfully"
    return processed_data


start_server = websockets.serve(websocket_server, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
