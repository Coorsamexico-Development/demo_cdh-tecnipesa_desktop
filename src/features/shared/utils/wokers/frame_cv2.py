from PyQt6.QtCore import  pyqtSignal, QThread

import numpy as np
from cv2 import VideoCapture, typing
class FrameCv2(QThread):

    frames = pyqtSignal(np.ndarray)

    def __init__(self, videoCapture:VideoCapture | None = None):
        super().__init__()
        self.videoCapture = videoCapture
        self.running = False


    def run(self):
        
        self.running = True
        while self.running:
            ret, frame = self.videoCapture.read()
            if not ret:
                break

            self.frames.emit(frame)



    def stop(self):
        self.running = False
        if self.videoCapture is None:
            return
        self.videoCapture.release()
        self.videoCapture = None
        
        

  
