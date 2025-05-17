import os
from typing import Union
from PyQt6.QtWidgets import  QWidget,QLabel,QVBoxLayout,QSizePolicy
from PyQt6.QtCore import QTimer, Qt
from features.shared.presentation.layouts.app_layout import AppLayout
from features.capture_rfid.presentation.partials.list_scaneos import ListScaneos





class CaptureRfidLayout(QWidget):
    def __init__(self):
        super().__init__()

        self.header_label = QLabel("Obteniendo productos")
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        sidebar = ListScaneos()

        app_layout = AppLayout(
            header=self.header_label,
            sidebar=sidebar,
            content=self.panel_video_dataset,
        )

        self.setLayout(app_layout)
       


        

    

    



         














