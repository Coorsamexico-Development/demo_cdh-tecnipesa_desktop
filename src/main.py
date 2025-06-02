import sys
from PyQt6.QtWidgets import QApplication
from features.home.screens.main_screen import MainScreen
from PyQt6.QtCore import QTimer

import threading
from services.websocket_service import WebsocketService
from services.web_service import run_flask
from features.database.managers.sqlite_manager import SqlliteManager
from features.database.migrations.creates_tables import CreateTables 



db_manager = SqlliteManager()

if db_manager.required_migration:
    CreateTables().up()

db_manager.close_connection()


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        #implement menu draw dataset
        self.main_window = MainScreen()
        #only for test local witout lector r700
        # QTimer.singleShot(1000,self.start_webserver)

    
    def start_webserver(self):
        threading.Thread(target=run_flask, daemon=True).start()
        threading.Thread(target=WebsocketService.run_websocket_server, daemon=True).start()
    


if __name__ == '__main__':
    
    
    app = App(sys.argv)
    #set window full screen
    app.main_window.show()
    sys.exit(app.exec())
    print("exit")

