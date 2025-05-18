from PyQt6.QtCore import QTimer
import os
from datetime import datetime
from PyQt6.QtWidgets import   QHBoxLayout, QFrame,QSizePolicy
from features.shared.presentation.widgets.capture_video_widget import CaptureVideoWidget
from features.capture_rfid.presentation.partials.list_view_camaras import ListViewCamaras
from services.camara_service import CamaraInfo,get_camera_info
from features.shared.utils.capture_camara_time import CaptureCameraTime
from features.shared.presentation.widgets.camera_viewer_widget import CameraViewerWidget
from features.capture_rfid.presentation.widgets.view_camara_item import ViewCamaraItem



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

        self.cameras: list[CamaraInfo] = get_camera_info()

        self.capture_camara_times= [CaptureCameraTime(camera=camera) for camera in self.cameras]

      

        self.principal_camera_viewer = CameraViewerWidget()
        
       
        self.list_view_camaras = ListViewCamaras(
            camaras=self.cameras
        )
        horizontal_layout.addWidget(self.principal_camera_viewer,15)
        horizontal_layout.addWidget(self.list_view_camaras,5)

        self.setLayout(horizontal_layout)
        QTimer.singleShot(150, self._start_camaras_time)
        
  
    def _start_camaras_time(self, principal_index=0):
        for index,camara_time in enumerate(self.capture_camara_times):

            if index > len(self.list_view_camaras.scroll_layout):
                return
       
            camara_viewer_in_list:ViewCamaraItem =  self.list_view_camaras.scroll_layout.itemAt(index).widget()
            camara_viewer:CameraViewerWidget = camara_viewer_in_list.camera_viewer

            camara_viewers = [camara_viewer]
            if index == principal_index:
                camara_viewers.append(self.principal_camera_viewer)
            camara_time.on_update_frame = lambda frame: self.update_images_viewer(frame,camara_viewers)
            camara_time.startCapture()

    
    def save_frame(self):
        pass

    def set_principal_camara(self,index:int, camara:CamaraInfo):
        if index > len(self.list_view_camaras.scroll_layout):
            return
       
        camara_viewer_in_list:ViewCamaraItem =  self.list_view_camaras.scroll_layout.itemAt(index).widget()
        camara_viewer:CameraViewerWidget = camara_viewer_in_list.camera_viewer


        self.capture_camara_times[index].on_update_frame = lambda frame: self.update_images_viewer(frame,[
        #    camara_viewer,
        #    self.principal_camera_viewer,
        ])

    
    def update_images_viewer(self,frame, camara_viewers:list[CameraViewerWidget]= []):
        
        for camara_viewer in camara_viewers:
            camara_viewer.update_image(frame=frame)




    



        