import sys
import os
from PyQt6.QtWidgets import QApplication
from features.home.screens.main_screen import MainScreen


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        #implement menu draw dataset
        self.main_window = MainScreen()


if __name__ == '__main__':
    app = App(sys.argv)
    #set window full screen
    app.main_window.show()
    sys.exit(app.exec())

