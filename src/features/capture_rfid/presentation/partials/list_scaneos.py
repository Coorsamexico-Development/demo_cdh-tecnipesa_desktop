import os
from typing import Union
from PyQt6.QtWidgets import QFrame,QSizePolicy,QListWidget,QListWidgetItem,QVBoxLayout,QMessageBox,QLabel
from PyQt6.QtCore import QTimer

from features.capture_rfid.infrastructure.models.scaneo_model import ScaneoModel
from features.capture_rfid.presentation.components.scaneo_item import ScaneoItem



class ListScaneos(QFrame):
    def __init__(self,):
        super().__init__()
        self.item_seleted = None
        self.scaneo_selected:Union[ ScaneoModel, None ] = None
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

           



    def add_scaneo_item(self, scaneo:ScaneoModel):
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
       


      