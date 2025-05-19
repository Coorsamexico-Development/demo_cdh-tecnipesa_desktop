import asyncio
from websockets.asyncio.server import serve
from websockets.asyncio.client import connect
from websockets.exceptions import ConnectionClosed
import config.constants.enviroments as Enviroments
from typing import Callable
from PyQt6.QtCore import pyqtSignal, QObject


# --- Señales para comunicar WebSocket con PyQt ---
class Communicator(QObject):
    message_received = pyqtSignal(str)

communicator = Communicator()


class WebsocketService():

    host = Enviroments.websocket_host
    port = Enviroments.websocket_port

    @staticmethod
    async def websocket_handler(websocket):
        try:
            async for message in websocket:
                communicator.message_received.emit(message)
                await websocket.send(message)
        except:
            print("Error websocket")

    @staticmethod
    async def start_websocket_server():
        async with serve(WebsocketService.websocket_handler, WebsocketService.host, WebsocketService.port) as server:
            await server.serve_forever()  # run forever
      

    @staticmethod
    def run_websocket_server():
        asyncio.run(WebsocketService.start_websocket_server())

    @staticmethod
    async def send_ws_message(message):
        async with connect(f"ws://{WebsocketService.host}:{WebsocketService.port}") as websocket:
            await websocket.send(message)

    @staticmethod
    async def receive_ws_messages(on_receive: Callable[[str], None], retry_delay: float = 5.0):
        url = f"ws://{WebsocketService.host}:{WebsocketService.port}"
        while True:
            try:
                async with connect(url) as websocket:
                    async for message in websocket:
                        on_receive(message)
            except ConnectionClosed as e:
                print(f"Conexión cerrada: {e}. Reintentando en {retry_delay} segundos...")
            except Exception as e:
                print(f"Error en WebSocket: {e}. Reintentando en {retry_delay} segundos...")

            await asyncio.sleep(retry_delay)
        