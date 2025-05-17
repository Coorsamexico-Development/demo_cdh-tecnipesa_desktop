import os
from PyQt6.QtWidgets import  QPushButton,QHBoxLayout, QComboBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

from services.camara_service import CamaraInfo, ResolutionInfo


class ControlsVideoWidget(QHBoxLayout):
    def __init__(self, 
                 
                 camaras: list[CamaraInfo], 
                 with_play_record:bool = True,
                 with_take_photo:bool = True,
                 on_take_photo= lambda x:None,
                 on_change_record= lambda x:None,
                 on_change_camara= lambda x:None,
                 on_change_resolution= lambda x:None,
                 ):
        super().__init__()
        self.is_recording = False
        self.with_play_record = with_play_record
        self.with_take_photo = with_take_photo

        self.on_take_photo = on_take_photo
        self.on_change_record = on_change_record
        self.on_change_camara = on_change_camara
        self.on_change_resolution = on_change_resolution
        self._init_ui()
        self.camaras = camaras
        
    def _init_ui(self):
        base_icon_path = os.path.join(os.getcwd(),'assets','icons')
        self.icon_play = QIcon(os.path.join(base_icon_path, 'play-circle-outline.png'))
        self.icon_record = QIcon(os.path.join(base_icon_path, 'record-rec.png'))
        icon_camara = QIcon(os.path.join(base_icon_path, 'camera-outline.png'))
       
        # UI controls layout
        self.setContentsMargins(10, 20, 10, 20)
        self.setSpacing(10)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)


        # UI Elements
        self.record_button = QPushButton()
        self.record_button.setProperty("class", 'button_icon')
        self.record_button.setIcon(self.icon_play)
        self.record_button.setIconSize(self.record_button.sizeHint())
        self.record_button.clicked.connect(self.toggle_record)

        self.take_button = QPushButton()
        self.take_button.setProperty("class", 'button_icon')
        self.take_button.setIcon(icon_camara)
        self.take_button.setIconSize(self.take_button.sizeHint())
        self.take_button.clicked.connect(self.on_take_photo)



        #combox camaras
        self.camera_selector = QComboBox()
        self.camera_selector.currentIndexChanged.connect(self.change_camera)

        #combox resoluctions
        self.resoluctions_selector = QComboBox()
        self.resoluctions_selector.currentIndexChanged.connect(self.change_resolution)
        
        self.addWidget(self.camera_selector)
        self.addWidget(self.resoluctions_selector)
        if self.with_play_record:
            self.addWidget(self.record_button)
        if self.with_take_photo:
            self.addWidget(self.take_button)

    
    @property
    def camaras(self):
        return self._camaras
    
    @camaras.setter
    def camaras(self, camaras: list[CamaraInfo]):
        self._camaras = camaras
        for camara in self._camaras:
            self.camera_selector.addItem(f"Camara ({camara.name})", camara.camera_index)

       
        if len(self._camaras) > 0:
            self.resoluctions = self._camaras[0].resolutions

    @property
    def resoluctions(self):
        return self._resoluctions
    
    @resoluctions.setter
    def resoluctions(self, resoluctions: list[ResolutionInfo]):
        self._resoluctions = resoluctions
        self.resoluctions_selector.clear()
        for resolution in self._resoluctions:
            self.resoluctions_selector.addItem(f"Resolución ({resolution.width}x{resolution.height})", resolution.index)    

   
    def toggle_record(self):
        if not self.is_recording:
            self.record_button.setIcon(self.icon_record)
        
        else:
            self.record_button.setIcon(self.icon_play)

        self.is_recording = not self.is_recording
        self.on_change_record(self.is_recording)

   

    def change_camera(self):
        camara_index = self.camera_selector.currentData()
        

        if  camara_index is not None:
            self.resoluctions = self._camaras[camara_index].resolutions
            self.on_change_camara(camara_index)


    def change_resolution(self):
        resolution_index = self.resoluctions_selector.currentData()
        if  resolution_index is not None:
            self.on_change_resolution(resolution_index)
