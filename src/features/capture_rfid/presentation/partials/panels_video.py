from PyQt6.QtCore import QTimer
import os
from datetime import datetime
from PyQt6.QtWidgets import   QHBoxLayout, QFrame,QSizePolicy
from features.capture_rfid.presentation.partials.list_view_camaras import ListViewCamaras
from services.camara_service import CamaraInfo,get_camera_info
from features.shared.utils.capture_camara_cv2 import CaptureCamera
from features.shared.presentation.widgets.camera_viewer_widget import CameraViewerWidget
from features.capture_rfid.presentation.widgets.view_camara_item import ViewCamaraItem
import numpy as np

from pygrabber.dshow_graph import FilterGraph
from features.capture_rfid.domain.workers.cameras_worker import CamerasWorker


global start_time 
start_time = datetime.now()
FILTER_INDEX_CAMERA = 0

class PanelsVideo(QFrame):
    def __init__(self, onSave= lambda x,y:None):
        super().__init__()

        self.onSave = onSave
        
        self.principal_camera_index =0
        # Esctrura  dataset _json
        self._dataset_json = {}
        self._init_ui()
        self.image_id = 1
        self.annotations = []
        self.record_path = None

    def _init_ui(self):
        # UI layout
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setContentsMargins(0, 0, 0, 0)
      
        horizontal_layout = QHBoxLayout()
        horizontal_layout.setContentsMargins(0, 0, 0, 0)
        horizontal_layout.setSpacing(0)

        
        self.cameras: list[CamaraInfo]  = [camera for camera in get_camera_info() if camera.camera_index > FILTER_INDEX_CAMERA]


        
        self.capture_camara_times= [CaptureCamera(camera=camera) for camera in self.cameras]

      

        self.principal_camera_viewer = CameraViewerWidget()
        
       
        self.list_view_camaras = ListViewCamaras(
            camaras=self.cameras,
            on_click=self._start_camaras_time
        )
        horizontal_layout.addWidget(self.principal_camera_viewer,15)
        horizontal_layout.addWidget(self.list_view_camaras,5)

        
        self.cameras_worker = CamerasWorker(filter_index_camera=FILTER_INDEX_CAMERA, cameras=self.cameras)
        
        self.cameras_worker.was_chenged.connect(self.restart_cameras)
    
        
        self.setLayout(horizontal_layout)
        QTimer.singleShot(150, lambda: self._stop_camaras(start_camaras=True))
        QTimer.singleShot(250, lambda: self.cameras_worker.start())
        
        



        

        
    # Inicia las camaras y asigna la funcion de actualizacion de imagenes a cada camara
    def _start_camaras_time(self, principal_index=0):
        self.principal_camera_index  = principal_index
        for index,camara_time in enumerate(self.capture_camara_times):

            if index > len(self.list_view_camaras.camaras_layout):
                return
       
            camara_viewer_in_list:ViewCamaraItem =  self.list_view_camaras.camaras_layout.itemAt(index).widget()
            camara_viewer:CameraViewerWidget = camara_viewer_in_list.camera_viewer

            camara_viewers = [camara_viewer]
            # para mostrarlo en la principal le indicampos donde deberia mostrarse
            if index == principal_index:
                camara_viewers.append(self.principal_camera_viewer)

            camara_time.on_update_frame = lambda frame, camara_viewers=camara_viewers: update_images_viewer(frame=frame, camara_viewers=camara_viewers)
            camara_time.startCapture()

    
    # Detiene todas las camaras y las reinicia si start_camaras es True
    def _stop_camaras(self,start_camaras=False):
       
        for camara in self.cameras:
            graph = FilterGraph()
            graph.add_video_input_device(camara.camera_index)
            graph.stop()
            graph.remove_filters()
        if start_camaras:
            QTimer.singleShot(100, self._start_camaras_time)
       


    

    # Guarda los frames de las camaras activas
    def save_frames(self)->list[np.ndarray]:
        resp = []
        for camara_time in self.capture_camara_times:
            frame = camara_time.takeFoto()
            if frame is None:
                continue
            resp.append(frame)
            

        return resp
    

    # revisa las camaras conectadas y si hay cambios en los indices o nombres de las camaras
    # reinicia las camaras y actualiza la lista de camaras
    # si hay cambios en las camaras
    def restart_cameras(self, was_chenged:bool = False):
        if was_chenged:
            print("Camaras cambiaron, reiniciando camaras...")
           
            # Detener las camaras actuales
            
            for camara_time in self.capture_camara_times:
                camara_time.stopCapture()
        
            
            #Reiniciar las camaras con las nuevas camaras
            self.cameras = self.cameras_worker.cameras
            self.capture_camara_times= [CaptureCamera(camera=camera) for camera in self.cameras]

            
            self.list_view_camaras.camaras = self.cameras
            principal_camera_index =  self.principal_camera_index if self.principal_camera_index < len(self.cameras) else 0
            if len(self.cameras) > 0: 
                self._start_camaras_time(principal_index= principal_camera_index)

            # Reinicamos el worker para detectar camaras
            QTimer.singleShot(500, self.cameras_worker.start)

   
# Actualiza las vistas de las camaras con el frame recibido
def update_images_viewer(frame, camara_viewers:list[CameraViewerWidget]= []):
    
    for camara_viewer in camara_viewers:
        camara_viewer.update_image(frame=frame)




    



        