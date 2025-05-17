from datetime import datetime
from PyQt6.QtWidgets import   QVBoxLayout, QLabel, QFrame,QSizePolicy
from PyQt6.QtCore import QTimer,Qt
import cv2
from pygrabber.dshow_graph import FilterGraph
from PyQt6.QtGui import QImage, QPixmap

from services.camara_service import CamaraInfo, get_camera_info
import numpy as np

global start_time 
start_time = datetime.now()


class CaptureVideoWidget(QFrame):
    def __init__(self, 
                 title:str = "Abrir Camará",
                 on_stop_record= lambda: None, 
                 add_custome_mask= lambda x,y: None, 
                 on_save_frame=lambda x,y,z,w:None,
                 with_mask_camara:bool = True
                 ):
        super().__init__()


        self.on_stop_record = on_stop_record
        self.add_custome_mask = add_custome_mask
        self.on_save_frame = on_save_frame
        self.is_recording = False
        self.capture_started = False

        self.with_mask_camara = with_mask_camara
        self.graph = None
        self.frame =None
        self.cameras: list[CamaraInfo] = get_camera_info()

        self.camara_index = None
        self.resolution_index = None
        if self.cameras:
            self.setCamaraIndex(0)
        self._init_ui(title)

    def _init_ui(self,title):
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameShadow(QFrame.Shadow.Raised)

        layout_video = QVBoxLayout()
        layout_video.setContentsMargins(0, 0, 0, 0)
        layout_video.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.video_label = QLabel(title)
        self.video_label.setContentsMargins(0, 0, 0, 0)
        
        self.video_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setProperty("class", "labe_capture")


        layout_video.addWidget(self.video_label)

        self.setLayout(layout_video)

        
        self.timer = QTimer()
        self.timer.timeout.connect(self.capture_loop)


    
    def setCamaraIndex(self, camara_index:int):
        self.camara_index = camara_index
        if self.camara_index < len(self.cameras):
            if self.cameras[self.camara_index].resolutions:
                self.setResolutionIndex(0)
        
   
    
    def setResolutionIndex(self, index:int):
        self.resolution_index = index
        if self.capture_started:
            self.setSettings()

    

    def capture_loop(self):
        self.graph.grab_frame()
        
    def startCapture(self):
        QTimer.singleShot(150, self._startCapture)
    
    def _startCapture(self):
        if self.capture_started:
            return

        if self.camara_index is not None and self.resolution_index is not None:
            self.setSettings()
            self.capture_started = True
            self.timer.start(120)


    def setSettings(self):
        if self.graph is None:
            self.graph = FilterGraph()
        else:
            if self.is_recording:
                self.stopRecord()
            self.graph.stop()
            self.graph.remove_filters()

        self.graph.add_video_input_device(self.camara_index)
            
        self.graph.get_input_device().set_format(self.resolution_index)
        self.graph.add_sample_grabber(self.update_frame)
        self.graph.add_null_render()
        self.graph.prepare_preview_graph()
        self.graph.run()

    
    def update_frame(self, frame:np.ndarray):
        self.frame = frame
        image_time = self.getImageTime()
       
        original_height, original_width, ch = self.frame.shape
        size = self.video_label.size()
        container_width = size.width() -20
        container_height = size.height() -10

        # print(f"Size Width: {container_width},height: {container_height} ")

        frame_show = self.frame.copy()
        self.add_custome_mask(frame_show,image_time)
        if self.is_recording:
            self.on_save_frame(self.frame,image_time,original_width,original_height)
        
        if self.with_mask_camara:
            self.mask_camara(frame_show, original_width, original_height)

        reduce_percent = (container_width)/original_width
        reduce_percent_h = (container_height)/original_height


        if reduce_percent > reduce_percent_h:
            reduce_percent = reduce_percent_h
        
        frame_show = cv2.cvtColor(frame_show, cv2.COLOR_BGR2RGB)
        
        h  = int(original_height * reduce_percent)
        w = int(original_width* reduce_percent)

        frame_show = cv2.resize(frame_show, (w, h))
        bytes_per_line = ch * w
        
        convert_to_Qt_format = QImage(frame_show.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(convert_to_Qt_format))
       


    def getImageTime(self)->str:
        global start_time
        capture_time = datetime.now() - start_time
        return str(capture_time.seconds * 1000 + int(capture_time.microseconds / 1000))

    def stopRecord(self):
        if self.is_recording:
            self.is_recording = False
            self.on_stop_record()

    def startRecord(self):
        self.is_recording = True


    def takeFoto(self):
        return self.frame, self.getImageTime()

    def stopCapture(self):
        self.stopRecord()
        if self.graph is not None:
                self.graph.stop()
                self.graph.remove_filters()
        if self.capture_started:
                self.timer.stop()
                self.capture_started = False
        self.video_label.setPixmap(QPixmap(""))

    
    def mask_camara(self, frame:np.ndarray, 
                    w:int = 320, 
                    h:int = 480):
        center_x = int(w/2)
        center_y = int(h/2)
        #partiendo como base una resolucion  320x
        scale_resolution = int(w/320)

        line_size = int(scale_resolution * 5)
        thickness =  round((scale_resolution/2) + 0.6)

        cv2.line(frame, (center_x -line_size, center_y), (center_x +line_size, center_y), color=(255, 255, 255), thickness=thickness)
        cv2.line(frame, (center_x, center_y-line_size), (center_x, center_y+line_size), color=(255, 255, 255), thickness=thickness)
        #lines camara cortonos

        maring = int(scale_resolution* 10)
        line_size=line_size*3
        margins_trbl = [(maring,maring), (w-maring,maring), (maring,h-maring), (w-maring,h-maring)]
        for margin in margins_trbl:
            margin_x = margin[0]
            margin_y = margin[1]
            if margin_x == maring:
                line_x =   margin_x + line_size
            else:
                line_x = margin_x-line_size
            
            if margin_y == maring:
                line_y =    margin_y  + line_size
            else:
                line_y = margin_y-line_size

            cv2.line(frame, margin, ( line_x,margin_y), color=(255, 255, 255), thickness=thickness)
            cv2.line(frame, margin, (margin_x, line_y), color=(255, 255, 255), thickness=thickness)
        

