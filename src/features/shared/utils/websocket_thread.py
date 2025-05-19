from PyQt6.QtCore import QThread
import asyncio
from typing import Callable
from src.services.websocket_service import WebsocketService

class WebSocketThread(QThread):
    def __init__(self, on_receive: Callable[[str], None]):
        super().__init__()
        self.on_receive = on_receive

    def run(self):
        asyncio.run(WebsocketService.receive_ws_messages(self.on_receive))