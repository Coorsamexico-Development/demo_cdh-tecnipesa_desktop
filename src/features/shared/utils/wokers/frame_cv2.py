from PyQt6.QtCore import  pyqtSignal, QThread

import numpy as np
import cv2
from services.camara_service import CamaraInfo, ResolutionInfo
class FrameCv2(QThread):

    frames = pyqtSignal(np.ndarray)

    def __init__(self, 
                 camara:CamaraInfo, 
                 resolution:ResolutionInfo | None = None,):
        super().__init__()
        self.camara = camara
        self.resolution = resolution
        self.videoCapture = None
        
        self.running = False



    def run(self):
        
        if self.resolution is None:
                    self.resolution = self.camara.resolutions[0]

                
        if self.videoCapture is None or not self.videoCapture.isOpened():
            print("Camara")
            self.videoCapture =  cv2.VideoCapture(self.camara.camera_index)
        
        self.videoCapture.set(cv2.CAP_PROP_FPS, 30)
        self.videoCapture.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution.width)
        self.videoCapture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution.height)
        
        self.running = True
        while self.running:
            ret, frame = self.videoCapture.read()
            if not ret:
                break

            self.frames.emit(frame)
            self.msleep(100)



    def stop(self):
        if self.running and self.videoCapture is not None:
            self.running = False
            self.wait()
            self.videoCapture.release()
        
        

  
