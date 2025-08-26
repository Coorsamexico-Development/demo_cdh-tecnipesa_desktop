
import sys
from PyQt6.QtWidgets import QApplication
from features.home.screens.main_screen import MainScreen
from PyQt6.QtCore import QTimer

import threading
# from services.websocket_service import WebsocketService
from services.web_service import run_flask
from features.home.screens.splash_screen import FadeSplashScreen


app = QApplication(sys.argv)

def show_main():
    app.main_window = MainScreen()
    #set window full screen
    QTimer.singleShot(1000,start_webserver)
    app.main_window.show()
    

def start_webserver():
    """
    Inicia el servidor web y el servidor websocket en segundo plano,
    este m todo es llamado desde el splash screen, y una vez iniciado
    el servidor web, se muestra la pantalla principal de la aplicaci n.
    """
    
    threading.Thread(target=run_flask, daemon=True).start()
    # threading.Thread(target=WebsocketService.run_websocket_server, daemon=True).start()

if __name__ == '__main__':
    splash = FadeSplashScreen(
        on_finished=show_main
    )
    splash.show()
    sys.exit(app.exec())
    

