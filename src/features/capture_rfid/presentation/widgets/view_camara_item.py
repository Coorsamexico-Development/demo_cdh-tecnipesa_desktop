
from PyQt6.QtWidgets import   QVBoxLayout, QFrame,QSizePolicy
from PyQt6.QtCore import QTimer, Qt
from features.shared.presentation.widgets.capture_video_widget import CaptureVideoWidget
from services.camara_service import CamaraInfo

class ViewCamaraItem(QFrame):
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
        self._init_ui()
    

  

    def _init_ui(self):
        self.setFixedHeight(400)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)
        # self.clicked.connect(self._call_click)
        self.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        layout = QVBoxLayout()

        self.capture_video = CaptureVideoWidget(
                                                title="SIN SEÑAL",
                                                on_save_frame=self.on_save_frame
                                                )
        self.capture_video.setCamaraIndex(self.camara.camera_index)

        layout.addWidget(self.capture_video)
        self.setLayout(layout)


        QTimer.singleShot(0, self.capture_video.startCapture)
        

    def mousePressEvent(self, event):
        self.on_click(self.camara)
        return super().mousePressEvent(event)


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