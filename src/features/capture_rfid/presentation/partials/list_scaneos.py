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

GROUP_ANTENNA = {
    1: 'group_1',
    2: 'group_1',
    3: 'group_2',
    4: 'group_2',
}


class ListScaneos(QFrame):
    def __init__(self,
                 
                 get_images: Callable[[], list[np.ndarray]],
                 on_add_scaneo: Callable[[ScaneoModel],None] = lambda x:None 
                 ):
        super().__init__()
        self.list_scaneos:list[ScaneoModel] =  []
        self.on_add_scaneo= on_add_scaneo
        self.item_seleted = None
        self.scaneo_selected:Union[ ScaneoModel, None ] = None
        self.get_images = get_images
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
        aux_scaneos = []
        for row,scaneo in enumerate(self.list_scaneos):
            if scaneo.tag_inventory_event.scond_antenna is None:
                aux_scaneos.append(scaneo)  

        self.list_scaneos = aux_scaneos

        for scaneo in self.list_scaneos:
            self.add_scane_item(scaneo)

        

    def on_receive_scan(self, data):
        dataJson = json.loads(data)
        scaneo = ScaneoAdapter.fromJson(dataJson)
        self.add_scaneo_item(scaneo)

    def add_scaneo_item(self, scaneo:ScaneoModel):
       


        scaneoFind = next((s for s in self.list_scaneos \
                           if s.tag_inventory_event.epc == scaneo.tag_inventory_event.epc), None)
       
        if scaneoFind is not None:
            if scaneoFind.tag_inventory_event.scond_antenna is None and \
                GROUP_ANTENNA[scaneoFind.tag_inventory_event.first_antenna] != GROUP_ANTENNA[scaneo.tag_inventory_event.antenna_port]:
                
                scaneoFind.tag_inventory_event.scond_antenna = scaneo.tag_inventory_event.antenna_port
                #mandamos a llamar el scaneo
                self.on_add_scaneo(scaneoFind)
            return 


        scaneo.images = self.get_images()
        if len(scaneo.images) == 0:
            return
            

        self.list_scaneos.append(scaneo)

        self.add_scane_item(scaneo)

    def add_scane_item(self, scaneo:ScaneoModel):
        print(f"addscane item: {scaneo}")
        # Crear un QListWidgetItem
        item = QListWidgetItem(self.list_widget)
        # Crear un widget personalizado (un QLabel en este caso)
        scaneoItem = ScaneoItem(scaneo)
        # Establecer el tamaño del item
        item.setSizeHint(scaneoItem.sizeHint())
        # Añadir el widget personalizado al QListWidgetItem
        self.list_widget.setItemWidget(item, scaneoItem)

    def remove_scaneo_item(self ):
        try:
            row = self.list_widget.row(self.item_seleted)
            self.list_widget.takeItem(row)
            self.item_seleted = None

        except ValueError:
            pass
       
