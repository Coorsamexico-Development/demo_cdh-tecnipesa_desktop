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
                 on_add_scaneo: Callable[[ScaneoItem],None] = lambda x:None,
                 send_scaneo: Callable[[ScaneoModel],None] = lambda x:None 
                 ):
        super().__init__()
        self.list_scaneos:list[ScaneoItem] =  []
        self.on_add_scaneo= on_add_scaneo
        self.send_scaneo= send_scaneo
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
        for scaneoItem in self.list_scaneos:
            if len(scaneoItem.scaneo.images) > 0:
                self.remove_scaneo_item(scaneoItem)

    def on_receive_scan(self, data):
        dataJson = json.loads(data)
        scaneo = ScaneoAdapter.fromJson(dataJson)
        self.add_scaneo_item(scaneo)

    def add_scaneo_item(self, scaneo:ScaneoModel):
        if scaneo.tag_inventory_event.epc == "E2801191A5030065E024AA03":
            return


        scaneoItemFind = next((scaneoItem for scaneoItem in self.list_scaneos \
                           if scaneoItem.scaneo.tag_inventory_event.epc == scaneoItem.scaneo.tag_inventory_event.epc), None)
       
        if scaneoItemFind is not None:
            scaneoItemFind.scaneo.count +=1
            scaneoItemFind.scaneo.tag_inventory_event.antenna_port =scaneo.tag_inventory_event.antenna_port

            if scaneoItemFind.scaneo.tag_inventory_event.scond_antenna is None and \
                GROUP_ANTENNA[scaneoItemFind.scaneo.tag_inventory_event.first_antenna] != GROUP_ANTENNA[scaneo.tag_inventory_event.antenna_port]:
                
                
                scaneoItemFind.scaneo.tag_inventory_event.scond_antenna = scaneo.tag_inventory_event.antenna_port


                

            scaneoItemFind.updateInfo()
            return 

        scaneoItem = self.add_scane_item(scaneo)
        self.on_add_scaneo(scaneoItem)
        #mandamos a llamar el scaneo
        QTimer.singleShot(1000, lambda s=scaneo:self.add_scaneo_images(s) )
        

       
    def add_scaneo_images(self,scaneo:ScaneoModel):
        scaneo.images = self.get_images()
        self.send_scaneo(scaneo)

    def add_scane_item(self, scaneo:ScaneoModel)->ScaneoItem:
        # Crear un QListWidgetItem
        item = QListWidgetItem(self.list_widget)
        # Crear un widget personalizado (un QLabel en este caso)
        scaneoItem = ScaneoItem(parent=item,scaneo=scaneo)
        # Establecer el tamaño del item
        item.setSizeHint(scaneoItem.sizeHint())
        # Añadir el widget personalizado al QListWidgetItem
        self.list_widget.setItemWidget(item, scaneoItem)

        self.list_scaneos.append(scaneoItem)
        return scaneoItem

    def remove_scaneo_item(self, scaneo_item:ScaneoItem ):
        try:
            row = self.list_widget.row(scaneo_item._parent)
            self.list_widget.takeItem(row)
            self.list_scaneos.remove(scaneo_item)

        except ValueError as e :
            print(e)
            pass
       
