from PyQt6.QtWidgets import QFrame,QHBoxLayout,QLabel,QPushButton
from features.capture_rfid.infrastructure.models.scaneo_model import ScaneoModel

class ScaneoItem(QFrame):
    def __init__(self,parent, scaneo:ScaneoModel, onAdd= lambda x:None):
        super().__init__()
        self._parent =parent
        self._scaneo = scaneo
        layout = QHBoxLayout()
        self.label_c = QLabel(f"{scaneo.count} ")
        self.label_epc = QLabel(f"EPC: {scaneo.tag_inventory_event.epc} ")
        self.label_antenna = QLabel(f"Antenna: {scaneo.tag_inventory_event.antenna_port}")
        # botton = QPushButton("Añadir")
        # botton.setProperty('class', 'btn_add')
        layout.addWidget(self.label_c, 1)
        layout.addWidget(self.label_epc, 5)
        layout.addWidget(self.label_antenna,2)
        # layout.addWidget(botton,2)
        self.setLayout(layout)

    @property
    def scaneo(self):
        return self._scaneo
    
    @scaneo.setter
    def scaneo(self, scaneo:ScaneoModel):
        self._scaneo = scaneo
        self.updateInfo()
    

    def updateInfo(self):
        self.label_c.setText(f"{self._scaneo.count} ")
        self.label_epc.setText(f"EPC: {self._scaneo.tag_inventory_event.epc} ")
        self.label_antenna.setText(f"Antenna: {self._scaneo.tag_inventory_event.antenna_port}")

    def updateColor(self,color:str):
        if color == 'red':
            self.setStyleSheet('background-color:#e55959')
            return
        self.setStyleSheet(f'background-color:light{color};')