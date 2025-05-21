import os
from PyQt6.QtWidgets import QMainWindow,QTabWidget
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QTimer
from features.home.widgets.main_menu import MainMenu
from features.capture_rfid.presentation.screens.capture_rfid_screen import CaptureRfidScreen

base_path = os.getcwd()

class MainScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DEMO ARCO CDH")
        self.setWindowIcon(QIcon(os.path.join(os.getcwd(),'assets','icons', "logo.png")))
        self.setGeometry(0, 0, 1280, 720)
        self.menu_bar = MainMenu()

        # self.tabs = QTabWidget()
        
        currentScreen = CaptureRfidScreen()
        self.setCentralWidget(currentScreen)

        
        self.apply_styles(os.path.join(base_path, "assets", "styles", "styles.qss"))
        # self.setMenuBar(self.menu_bar)
        self.showMaximized()
        # QTimer.singleShot(100,self.add_tabs)



    def apply_styles(self, qss_file):
        with open(qss_file, "r") as f:
            self.setStyleSheet(f.read())

    # def add_tabs(self):
      
    #     capture_tab = CaptureRfidScreen()
    #     self.tabs.addTab(capture_tab, "ESCANEO RFID")
       










