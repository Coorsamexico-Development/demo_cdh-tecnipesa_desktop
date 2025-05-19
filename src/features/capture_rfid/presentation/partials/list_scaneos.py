import json
from typing import Callable 
from typing import Union
from PyQt6.QtWidgets import QFrame,QSizePolicy,QListWidget,QListWidgetItem,QVBoxLayout,QMessageBox,QLabel
from PyQt6.QtCore import QTimer

from features.capture_rfid.infrastructure.models.scaneo_model import ScaneoModel
from features.capture_rfid.presentation.widgets.scaneo_item import ScaneoItem
from services.websocket_service import communicator
from features.capture_rfid.infrastructure.adapters.scaneo_adapter import ScaneoAdapter


class ListScaneos(QFrame):
    def __init__(self,on_finish_scan: Callable[[list[ScaneoModel]],None] = lambda x:None):
        super().__init__()
        self.list_scaneos:list[ScaneoModel] =  []
        self.on_finish_scan= on_finish_scan
        self.item_seleted = None
        self.scaneo_selected:Union[ ScaneoModel, None ] = None
        self.captured_scaneos = True
        self._init_ui()

    def _init_ui(self):
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setProperty('class', 'card')
        layout = QVBoxLayout()
        label_title = QLabel("Lista de Escaneos")
        label_title.setProperty("class", 'title')
        layout.addWidget(label_title)
        
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)
        self.setLayout(layout)
        #proviene del servicio web socket
        communicator.message_received.connect(self.on_receive_scan)

    
    def _finish_scan(self):
        self.captured_scaneos = False
        self.on_finish_scan(self.list_scaneos)
        self.clear_scaneos()


    def clear_scaneos(self):
        self.list_widget.clear()
        self.list_scaneos.clear()

    def on_receive_scan(self, messageData):
        
        
        dataJson = json.loads(messageData)
        if len(dataJson) > 0 and len(self.list_scaneos) == 0:
             self.captured_scaneos = True
             QTimer.singleShot(5000, self._finish_scan)

        if self.captured_scaneos:
            for scaneJson in dataJson:
                scaneo = ScaneoAdapter.fromJson(scaneJson)
                self.add_scaneo_item(scaneo)

    def add_scaneo_item(self, scaneo:ScaneoModel):
        if scaneo in self.list_scaneos: #no agrega duplicados
            return
        # Crear un QListWidgetItem
        item = QListWidgetItem(self.list_widget)
        # Crear un widget personalizado (un QLabel en este caso)
        datastItem = ScaneoItem(scaneo)
        # Establecer el tamaño del item
        item.setSizeHint(datastItem.sizeHint())
        # Añadir el widget personalizado al QListWidgetItem
        self.list_widget.setItemWidget(item, datastItem)

    def remove_scaneo_item(self ):
        try:
            row = self.list_widget.row(self.item_seleted)
            self.list_widget.takeItem(row)
            self.item_seleted = None

        except ValueError:
            pass
       


      