
from PyQt6.QtWidgets import QWidget, QVBoxLayout,QSizePolicy
from features.capture_rfid.presentation.screens.capture_rfid_screen import CaptureRfidScreen
from features.capture_rfid.presentation.screens.async_data_screen import AsyncDataScreen

class HomeScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout_body = QVBoxLayout()
        layout_body.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout_body)
        self.toGo('async_data')
        
    def toGo(self, route_name:str, **params):
        layout = self.layout()
        body = layout.itemAt(0)
        if body is not None:
            body = body.widget()
            body.deleteLater()
        #layout change    
        if route_name == 'async_data':
            body = AsyncDataScreen()
        elif route_name == 'capture_rfid':
            body = CaptureRfidScreen()

        body.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(body)