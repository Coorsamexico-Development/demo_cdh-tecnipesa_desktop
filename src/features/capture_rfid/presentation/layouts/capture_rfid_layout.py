import os
from typing import Union
from PyQt6.QtWidgets import  QWidget,QLabel,QVBoxLayout,QSizePolicy
from PyQt6.QtCore import QTimer, Qt
from features.shared.presentation.layouts.app_layout import AppLayout
from features.capture_rfid.presentation.partials.list_scaneos import ListScaneos
from features.capture_rfid.presentation.partials.panels_video import PanelsVideo





class CaptureRfidLayout(QWidget):
    def __init__(self):
        super().__init__()

        self.message_label = QLabel("Camaras")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        sidebar = ListScaneos()
        self.content = PanelsVideo()

        app_layout = AppLayout(
            sidebar=sidebar,
            content=self.content
        )

        self.setLayout(app_layout)
       


        

    

    



         














