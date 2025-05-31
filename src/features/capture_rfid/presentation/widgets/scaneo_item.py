from PyQt6.QtWidgets import QFrame,QHBoxLayout,QLabel,QPushButton
from features.capture_rfid.infrastructure.models.scaneo_model import ScaneoModel

class ScaneoItem(QFrame):
    def __init__(self, scaneo:ScaneoModel, onAdd= lambda x:None):
        super().__init__()
        self.scaneo = scaneo
        self.onAdd = onAdd
        layout = QHBoxLayout()
        label = QLabel(f"EPC: {scaneo.tag_inventory_event.epc}")
        label2 = QLabel(f"Antenna: {scaneo.tag_inventory_event.antenna_port}")
        # botton = QPushButton("Añadir")
        # botton.setProperty('class', 'btn_add')
        # botton.clicked.connect(lambda: self.onAdd(self.scaneo))
        layout.addWidget(label)
        layout.addWidget(label2)
        # layout.addWidget(botton,2)
        self.setLayout(layout)