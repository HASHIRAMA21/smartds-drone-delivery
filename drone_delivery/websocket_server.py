import asyncio
import websockets
import json
from dronekit import connect

async def send_coordinates(websocket, path):
    vehicle = connect('/dev/ttyAMA0', wait_ready=True, baud=57600)
    while True:
        try:
            location = vehicle.location.global_relative_frame
            data = {
                "lat": location.lat,
                "lon": location.lon,
                "alt": location.alt
            }
            await websocket.send(json.dumps(data))
            await asyncio.sleep(1)
        except Exception as e:
            print("Error sending coordinates:", e)

start_server = websockets.serve(send_coordinates, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

