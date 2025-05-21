
from PyQt6.QtWidgets import QWidget, QVBoxLayout,QSizePolicy
from features.capture_rfid.presentation.layouts.capture_rfid_layout import CaptureRfidLayout

class CaptureRfidScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout_body = QVBoxLayout()
        layout_body.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout_body)
        self.toGo('capture_video')
        
    def toGo(self, route_name:str, **params):
        layout = self.layout()
        body = layout.itemAt(0)
        if body is not None:
            body = body.widget()
            body.deleteLater()
        #layout change    
        if route_name == 'capture_video':
            body = CaptureRfidLayout()
        # elif route_name == 'producto_dataset':
        #     body = ProductoDatasetLayout(**params)

        body.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(body)