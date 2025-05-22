import json
from typing import Callable 
from typing import Union
from PyQt6.QtWidgets import QFrame,QSizePolicy,QListWidget,QListWidgetItem,QVBoxLayout,QMessageBox,QLabel
from PyQt6.QtCore import QTimer

from features.capture_rfid.infrastructure.models.scaneo_model import ScaneoModel
from features.capture_rfid.presentation.widgets.scaneo_item import ScaneoItem

from features.capture_rfid.infrastructure.adapters.scaneo_adapter import ScaneoAdapter
import numpy as np
from features.capture_rfid.domain.workers.impinj_stream_worker import ImpinjStreamWorker

class ListScaneos(QFrame):
    def __init__(self,
                 
                 get_image: Callable[[], np.ndarray],
                 on_add_scaneo: Callable[[ScaneoModel],None] = lambda x:None 
                 ):
        super().__init__()
        self.list_scaneos:list[ScaneoModel] =  []
        self.on_add_scaneo= on_add_scaneo
        self.item_seleted = None
        self.scaneo_selected:Union[ ScaneoModel, None ] = None
        self.get_image = get_image
        self._init_ui()

    def _init_ui(self):
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setProperty('class', 'card')
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        label_title = QLabel("Lista de Escaneos")
        label_title.setProperty("class", 'title')
        layout.addWidget(label_title)
        
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)
        self.setLayout(layout)
        #proviene del servicio web socket

        self.impinj_stream_worker = ImpinjStreamWorker()
        self.impinj_stream_worker.new_data.connect(self.on_receive_scan)
        QTimer.singleShot(2000, self.start_stream)

    
    
    def start_stream(self):
        print("Iniciando el stream de Impinj")
        self.impinj_stream_worker.start()

    def clear_scaneos(self):
        self.list_widget.clear()
        self.list_scaneos.clear()

    def on_receive_scan(self, data):
        dataJson = json.loads(data)
        scaneo = ScaneoAdapter.fromJson(dataJson)
        self.add_scaneo_item(scaneo)

    def add_scaneo_item(self, scaneo:ScaneoModel):
        exists = any(s.tag_inventory_event.epc == scaneo.tag_inventory_event.epc
                    for s in self.list_scaneos)
        if exists: #no agrega duplicados
            return
        scaneo.image = self.get_image()
        if scaneo.image is None:
            return
            

        self.list_scaneos.append(scaneo)

        self.on_add_scaneo(scaneo)
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
       
