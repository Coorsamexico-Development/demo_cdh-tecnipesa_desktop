
from PyQt6.QtCore import QThread, pyqtSignal
from services.camara_service import CamaraInfo, get_camera_info



class CamerasWorker(QThread):
    was_chenged = pyqtSignal(bool)

    
    def __init__(self, filter_index_camera: int, cameras):
        super().__init__()
        self.filter_index_camera = filter_index_camera
        self.cameras = cameras
       

    def run(self):
        cameras: list[CamaraInfo]  = [camera for camera in get_camera_info() if camera.camera_index > self.filter_index_camera]
        was_chenged = cameras != self.cameras
        if was_chenged:
            self.cameras = cameras
            # Emit signal to notify that the cameras have changed
        self.was_chenged.emit(was_chenged)
# class ResponseGpos: 
#     def __init__(self):
#         self.resp:str = ""
#         self.has_error = False
#         self.error = RequestError()

    
