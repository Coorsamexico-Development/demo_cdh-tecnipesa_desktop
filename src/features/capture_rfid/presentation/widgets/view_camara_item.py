
from PyQt6.QtWidgets import   QVBoxLayout, QFrame,QSizePolicy
from PyQt6.QtCore import QTimer, Qt
from features.shared.presentation.widgets.capture_video_widget import CaptureVideoWidget
from services.camara_service import CamaraInfo
from features.shared.presentation.widgets.camera_viewer_widget import CameraViewerWidget

class ViewCamaraItem(QFrame):
    def __init__(self, 
                 index:int,
                 camara:CamaraInfo, 
                 on_click= lambda index:None,                 
                 ):
        super().__init__()
        self.index = index
        self.camara = camara
        self.on_click = on_click
        self.is_active = False
        self._init_ui()
    

  

    def _init_ui(self):
        # print(self.camara.resolutions)
        self.setFixedHeight(150)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)
        # self.clicked.connect(self._call_click)
        self.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.camera_viewer = CameraViewerWidget(
                                                title="SIN SEÑAL",
                                                )

        layout.addWidget(self.camera_viewer)
        self.setLayout(layout)


        

    def mousePressEvent(self, event):
        self._call_click()
        return super().mousePressEvent(event)


    def _call_click(self):
        self.toggleActive()
        self.on_click(self.index)


    def toggleActive(self):
        self.is_active = not self.is_active
        # current_class = self.property('class')
        # if not self.is_active:
        #     current_class  = current_class.replace(' active', '')
        # else:
        #     current_class += ' active'
            
        # self.setProperty('class', current_class)
        # #self.style().unpolish(self)
        # self.style().polish(self)
        # self.update()