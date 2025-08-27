from services.camara_service import CamaraInfo
from PyQt6.QtCore import QTimer
import numpy as np
from datetime import datetime
import cv2
from features.shared.utils.wokers.frame_direccion_cv2 import FrameCv2


global start_time 
start_time = datetime.now()

class CaptureCamera:
    def __init__(self, camera: CamaraInfo,
                 on_update_frame = lambda frame:None, 
                 on_save_frame= lambda frame,image_name:None,
                 on_stop_record= lambda: None,
                 auto_start:bool = True,
                 min_resolution:int=1080,
                 on_change_direction= lambda direction:None
                 ):
        super().__init__()
        self.resolution_index = None
        self.frame = None
        self.camera = camera
        self.on_stop_record = on_stop_record
        self.on_update_frame = on_update_frame
        self.on_save_frame = on_save_frame
        self.is_recording = False

    
        self.on_change_direction = on_change_direction
        

        self.frame_cv2 = None
        for index,resolution in enumerate(self.camera.resolutions):
            if resolution.height >= min_resolution:
                self.resolution_index = index
                break

        self.frame_cv2 = FrameCv2(
            camara=self.camera, 
            resolution=self.camera.resolutions[self.resolution_index],
         )
        
        self.frame_cv2.frames.connect(self.update_frame)
        self.frame_cv2.directions.connect(self.on_change_direction)

        if auto_start:
            self.startCapture()


    @property
    def index_resolution(self):
        return self.resolution_index

    @index_resolution.setter
    def index_resolution(self, index:int):
        self.resolution_index = index
        if self.frame_cv2 is not None and self.frame_cv2.running:
            self.setSettings()

    @property
    def with_direction(self):
        return self.frame_cv2.with_direction
    @with_direction.setter
    def with_direction(self, value: bool):
        if not value:
            self.on_change_direction = lambda direction:None
        
        self.frame_cv2.with_direction = value   


   

    def startCapture(self):
        QTimer.singleShot(20, self._startCapture)

    def _startCapture(self):
        if self.frame_cv2.running:
            return

        if self.camera is not None and self.resolution_index is not None:
            self.frame_cv2.start()

    def setSettings(self):
        if self.is_recording:
            self._stopRecord()
        
        self.frame_cv2.stop()
        self.frame_cv2.resolution = self.camera.resolutions[self.resolution_index]
        self.startCapture()

    def stopCapture(self):
        if self.frame_cv2.running:
                self.frame_cv2.stop()
        self._stopRecord()


    


   

    def _stopRecord(self):
        if self.is_recording:
            self.is_recording = False
            self.on_stop_record()

    def startRecord(self):
        self.is_recording = True


    def takeFoto(self)->np.ndarray:
        return self.frame


    def getImageTime(self)->str:
        global start_time
        capture_time = datetime.now() - start_time
        return str(capture_time.seconds * 1000 + int(capture_time.microseconds / 1000))
    

   
    def update_frame(self, frame: np.ndarray,  frame_mask:object= None):
        self.frame = frame
        if frame_mask is not None:
            self.on_update_frame(frame_mask)
        else:
            self.on_update_frame(frame)

        if self.is_recording:
            image_time = self.getImageTime()
            self.on_save_frame(frame,image_time)
       