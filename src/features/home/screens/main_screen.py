import os
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QIcon
from features.home.widgets.main_menu import MainMenu
from features.capture_rfid.presentation.screens.home_screen import HomeScreen
from features.capture_rfid.infrastructure.datasource.api_impinj_gpos_datasource import (
    ApiImpinjGposDatasource)
from features.capture_rfid.infrastructure.models.gpo_configuration_model import (
    GpoConfigurationModel)
from features.database.managers.sqlite_manager import SqliteManager

base_path = os.getcwd()

class MainScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DEMO ARCO CDH")
        self.setWindowIcon(QIcon(os.path.join(os.getcwd(),'assets','icons', "logo.png")))
        self.setGeometry(0, 0, 1280, 720)
        self.menu_bar = MainMenu()

        # self.tabs = QTabWidget()
        
        currentScreen = HomeScreen()
        self.setCentralWidget(currentScreen)

        
        self.apply_styles(os.path.join(base_path, "assets", "styles", "styles.qss"))
        # self.setMenuBar(self.menu_bar)
        self.showMaximized()
        # QTimer.singleShot(100,self.add_tabs)



    def apply_styles(self, qss_file):
        with open(qss_file, "r") as f:
            self.setStyleSheet(f.read())

    def closeEvent(self, event):
        SqliteManager().close_connection()
        print("apagando luces....")
        datasource = ApiImpinjGposDatasource()
        datasource.update_gpos(gpo_configurations=self.offLeds())
        print("luces apagadas")


    def offLeds(self):
        bin_numers = list("000")
        leds = [GpoConfigurationModel(
                gpo=index+1,
                state=GpoConfigurationModel.StateGeo.HIGH if bin_numer == '1' else GpoConfigurationModel.StateGeo.LOW
            )  for index,bin_numer  in enumerate(bin_numers)]
        
        return leds
        

    # def add_tabs(self):
      
    #     capture_tab = CaptureRfidScreen()
    #     self.tabs.addTab(capture_tab, "ESCANEO RFID")
       










