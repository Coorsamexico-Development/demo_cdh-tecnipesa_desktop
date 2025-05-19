import sys
from PyQt6.QtWidgets import QApplication
from features.home.screens.main_screen import MainScreen

import threading
from services.websocket_service import WebsocketService
from services.web_service import run_flask

class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        #implement menu draw dataset
        self.main_window = MainScreen()


if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
    threading.Thread(target=WebsocketService.run_websocket_server, daemon=True).start()
    
    app = App(sys.argv)
    #set window full screen
    app.main_window.show()
    sys.exit(app.exec())

