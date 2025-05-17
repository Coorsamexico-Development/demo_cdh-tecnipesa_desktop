
from PyQt6.QtWidgets import QWidget, QVBoxLayout,QSizePolicy
from features.capture_rfid.presentation.layouts.capture_rfid_layout import CaptureRfidLayout

class CaptureRfidScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.layout_body = QVBoxLayout()
        self.toGo('capture_video')
        self.setLayout(self.layout_body)
        
    def toGo(self, route_name:str, **params):
        body = self.layout_body.itemAt(0)
        if body is not None:
            body = body.widget()
            body.deleteLater()
        #layout change    
        if route_name == 'capture_video':
            body = CaptureRfidLayout()
        # elif route_name == 'producto_dataset':
        #     body = ProductoDatasetLayout(**params)

        body.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.layout_body.addWidget(body)