from PyQt6.QtCore import QTimer
import os
from datetime import datetime
from PyQt6.QtWidgets import   QHBoxLayout, QFrame,QSizePolicy
from features.shared.presentation.widgets.capture_video_widget import CaptureVideoWidget



global start_time 
start_time = datetime.now()
base_path = os.getcwd()


class PanelsVideo(QFrame):
    def __init__(self, onSave= lambda x,y:None):
        super().__init__()

        self.onSave = onSave
        
       
        # Esctrura  dataset _json
        self._dataset_json = {}
        self._init_ui()
        self.image_id = 1
        self.annotations = []
        self.record_path = None

    def _init_ui(self):
        # UI layout
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        horizontal_layout = QHBoxLayout()
        horizontal_layout.setContentsMargins(0, 0, 0, 0)
        horizontal_layout.setSpacing(0)

        self.capture_video = CaptureVideoWidget(
                                                title="SIN SEÑAL",
                                                on_save_frame=self.saveFrame,

                                                )
        horizontal_layout.addWidget(self.capture_video)

        self.setLayout(horizontal_layout)

        QTimer.singleShot(0, self.capture_video.startCapture)
        
    
    @property
    def camara(self):
        return self._camara
    
    def saveFrame(self):
        pass
    
   




    



        