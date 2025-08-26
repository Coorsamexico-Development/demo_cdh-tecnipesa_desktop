from services.camara_service import CamaraInfo
from PyQt6.QtCore import QTimer
import numpy as np
from datetime import datetime
import cv2
from features.shared.utils.wokers.frame_cv2 import FrameCv2

global start_time 
start_time = datetime.now()

class CaptureCamera:
    def __init__(self, camera: CamaraInfo,
                 on_update_frame = lambda frame:None, 
                 on_save_frame= lambda frame,image_name:None,
                 on_stop_record= lambda: None,
                 auto_start:bool = False,
                 min_resolution:int=720,
                 ):
        super().__init__()
        self.resolution_index = None
        self.frame = None
        self.camera = camera
        self.on_stop_record = on_stop_record
        self.on_update_frame = on_update_frame
        self.on_save_frame = on_save_frame
        self.is_recording = False
    
        cv2.VideoCapture()

        self.frame_cv2 = FrameCv2( )
        
        self.frame_cv2.frames.connect(self.update_frame)
       


        for index,resolution in enumerate(self.camera.resolutions):
            if resolution.height >= min_resolution:
                self.setResolutionIndex(index=index)
                break

        if auto_start:
            self.startCapture()

   

    def startCapture(self):
        QTimer.singleShot(20, self._startCapture)

    def _startCapture(self):
        if self.frame_cv2.running:
            return

        if self.camera is not None and self.resolution_index is not None:
            self.setSettings()

    def setSettings(self):
        if self.is_recording:
            self._stopRecord()
        
        self.frame_cv2.stop()
        self.frame_cv2.videoCapture = cv2.VideoCapture(self.camera.camera_index)
        self.frame_cv2.videoCapture.set(cv2.CAP_PROP_FPS, 30)
        self.frame_cv2.videoCapture.set(cv2.CAP_PROP_FRAME_WIDTH, self.camera.resolutions[self.resolution_index].width)
        self.frame_cv2.videoCapture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.camera.resolutions[self.resolution_index].height)
        self.frame_cv2.start()

    def stopCapture(self):
        if self.frame_cv2.running:
                self.frame_cv2.stop()
        self._stopRecord()


    def setResolutionIndex(self, index:int):
        self.resolution_index = index
        if self.frame_cv2.running:
            self.setSettings()


   

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
    

   
    def update_frame(self, frame:np.ndarray):
        
        self.frame = frame.copy()
        self.on_update_frame(self.frame)

        if self.is_recording:
            image_time = self.getImageTime()
            self.on_save_frame(frame,image_time)
       