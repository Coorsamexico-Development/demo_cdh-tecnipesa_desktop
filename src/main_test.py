import sys
import threading
import asyncio
from websockets.asyncio.server import serve
from websockets.asyncio.client import connect
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout
from PyQt6.QtCore import pyqtSignal, QObject
from flask import Flask
from flask import request
import base64

# --- Señales para comunicar WebSocket con PyQt ---
class Communicator(QObject):
    message_received = pyqtSignal(str)

communicator = Communicator()

# --- PyQt6 GUI ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DEMO ARCO CDH")
        self.setWindowTitle("PyQt6 escucha WebSocket")
        self.label = QLabel("Esperando mensaje...")
        self.setCentralWidget(self.label)

        # Conectar señal
        communicator.message_received.connect(self.update_label)

    def update_label(self, message):
        self.label.setText(f"Mensaje recibido: {message}")

# --- WebSocket Server ---
connected_clients = set()

async def websocket_handler(websocket):
    print("Entra el websocket_handler")
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            await websocket.send(message)
            print("Mensaje recibido en WebSocket:", message)
            communicator.message_received.emit(message)
    except:
        pass
    finally:
        connected_clients.remove(websocket)

async def start_websocket_server():
    async with serve(websocket_handler, "localhost", 8765) as server:
        print("Entrada al future")
        await server.serve_forever()  # run forever
    print("run_websocket_server")

def run_websocket_server():
    
    asyncio.run(start_websocket_server())

# --- Flask App ---
flask_app = Flask(__name__)

@flask_app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # Enviar mensaje a todos los WebSocket conectados
    
    dataJson =request.get_json()

    if not dataJson:
        return "No se envio JSON válido"
    
    firstData = dataJson[0]
    tagInventory =  firstData.get('tagInventoryEvent')
    epc = base64.urlsafe_b64decode(tagInventory.get('epc')).hex().upper()
    print(epc)

    asyncio.run(send_ws_message(f"EPC{epc}"))
    return f"Mensaje enviado desde Flask al WebSocket {epc}."

async def send_ws_message(message):
    print("intento send ws message")
    async with connect("ws://localhost:8765") as websocket:
        await websocket.send(message)
    # disconnected = []
    # for ws in connected_clients:
    #     try:
    #         await ws.send(message)
    #     except:
    #         disconnected.append(ws)
    # for ws in disconnected:
    #     connected_clients.remove(ws)

def run_flask():
    flask_app.run(host="0.0.0.0",port=5000)


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        #implement menu draw dataset
        self.main_window = MainWindow()


# --- Main ---
if True:
    # Iniciar Flask y WebSocket en hilos
    threading.Thread(target=run_flask, daemon=True).start()
    threading.Thread(target=run_websocket_server, daemon=True).start()

    # Iniciar PyQt en el hilo principal
    app = App(sys.argv)
    #set window full screen
    app.main_window.show()
    sys.exit(app.exec())