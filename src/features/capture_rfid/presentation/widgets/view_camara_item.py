import PyQt6.QtCore
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import QSize, Qt
from src.features.shared.presentation.widgets.capture_video_widget import CaptureVideoWidget
from src.services.camara_service import CamaraInfo

class ViewCamaraItem(QPushButton):
    def __init__(self, 
                 index:int,
                 camara:CamaraInfo, 
                 on_click= lambda x:None,
                 on_save_frame=lambda x,y,z,w:None
                 
                 
                 ):
        super().__init__()
        self.index = index
        self.camara = camara
        self.on_click = on_click
        self.is_active = False
        self.on_save_frame= on_save_frame
    

  

    def _init_ui(self):
        self.setSizePolicy(QSize(100,100))
        self.setContentsMargins(0, 0, 0, 0)
        self.setProperty('class', 'card')
        self.clicked.connect(self._call_click)
        self.setLayoutDirection(Qt.LayoutDirection.LeftToRight)


        self.capture_video = CaptureVideoWidget(
                                                title="SIN SEÑAL",
                                                on_save_frame=self.on_save_frame
                                                )
        self.capture_video.setCamaraIndex(self.camara.camera_index)

        self.capture_video
        




    def _call_click(self):
        self.toggleActive()
        self.on_click(self)


    def toggleActive(self):
        self.is_active = not self.is_active
        current_class = self.property('class')
        if not self.is_active:
            current_class  = current_class.replace(' active', '')
        else:
            current_class += ' active'
            
        self.setProperty('class', current_class)
        #self.style().unpolish(self)
        self.style().polish(self)
        self.update()