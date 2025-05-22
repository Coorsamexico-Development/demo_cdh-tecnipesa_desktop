from services.camara_service import CamaraInfo
from PyQt6.QtCore import QTimer
from pygrabber.dshow_graph import FilterGraph
import numpy as np
from datetime import datetime
from typing import Tuple

global start_time 
start_time = datetime.now()

class CaptureCameraTime:
    def __init__(self, camera: CamaraInfo,
                 on_update_frame = lambda frame:None, 
                 on_save_frame= lambda frame,image_name:None,
                 on_stop_record= lambda: None,
                 auto_start:bool = False,
                 ):
        super().__init__()
        self.frame = None
        self.camera = camera
        self.on_stop_record = on_stop_record
        self.on_update_frame = on_update_frame
        self.on_save_frame = on_save_frame
        self.graph = FilterGraph()
        self.is_recording = False
        self.capture_started = False

        if len(self.camera.resolutions) > 0:
            self.setResolutionIndex(self.camera.resolutions[0].index)

        self.timer = QTimer()

        self.timer.timeout.connect(self.graph.grab_frame)

        if auto_start:
            self.startCapture()

   

    def startCapture(self):
        QTimer.singleShot(150, self._startCapture)

    def _startCapture(self):
        if self.capture_started:
            return

        if self.camera is not None and self.resolution_index is not None:
            self.setSettings()
            self.capture_started = True
            self.timer.start(120)

    def stopCapture(self):
        if self.capture_started:
                self.graph.stop()
                self.graph.remove_filters()
                self.timer.stop()
                self.capture_started = False
        self._stopRecord()


    def setResolutionIndex(self, index:int):
        self.resolution_index = index
        if self.capture_started:
            self.setSettings()


    def setSettings(self):
        if self.is_recording:
            self._stopRecord()
        self.graph.stop()
        self.graph.remove_filters()

        self.graph.add_video_input_device(self.camera.camera_index)
            
        self.graph.get_input_device().set_format(self.resolution_index)
        self.graph.add_sample_grabber(self.update_frame)
        self.graph.add_null_render()
        self.graph.prepare_preview_graph()
        self.graph.run()

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
        
        self.frame = frame
        self.on_update_frame(self.frame)

        if self.is_recording:
            image_time = self.getImageTime()
            self.on_save_frame(frame,image_time)
       