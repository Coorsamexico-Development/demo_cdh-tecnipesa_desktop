import json
import sys
import threading
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout

from services.websocket_service import WebsocketService, communicator
from services.web_service import run_flask
from features.capture_rfid.infrastructure.adapters.scaneo_adapter import ScaneoAdapter

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

    def update_label(self, messageData):
        dataJson = json.loads(messageData)

        for scaneJson in dataJson:
            scaneo = ScaneoAdapter.fromJson(scaneJson)
            self.label.setText(f"EPC: {scaneo.tag_inventory_event.epc}")
          
        




class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        #implement menu draw dataset
        self.main_window = MainWindow()


# --- Main ---
if True:
    # Iniciar Flask y WebSocket en hilos
    threading.Thread(target=run_flask, daemon=True).start()
    threading.Thread(target=WebsocketService.run_websocket_server, daemon=True).start()

    # Iniciar PyQt en el hilo principal
    app = App(sys.argv)
    #set window full screen
    app.main_window.show()
    sys.exit(app.exec())