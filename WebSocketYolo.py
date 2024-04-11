import asyncio
import websockets

async def process_image(image):
    # Add your image processing logic here (e.g., using YOLOv8)
    processed_result = "Processed result"
    return processed_result

async def handle_client(websocket, path):
    while True:
        try:
            # Receive image from client
            image = await websocket.recv()

            # Process image
            processed_result = await process_image(image)

            # Send processed result back to client
            await websocket.send(processed_result)
        except websockets.exceptions.ConnectionClosedError:
            break

start_server = websockets.serve(handle_client, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
