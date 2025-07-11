from datetime import datetime
from PyQt6.QtWidgets import   QVBoxLayout, QLabel, QFrame,QSizePolicy
from PyQt6.QtCore import Qt
import cv2
from PyQt6.QtGui import QImage, QPixmap

import numpy as np


class CameraViewerWidget(QFrame):
    def __init__(self, 
                 title:str = "SIN SEÑAL",
                 add_custome_mask= lambda frame: None,
                 with_mask_camara:bool = False
                 ):
        super().__init__()


        self.add_custome_mask = add_custome_mask
        self.capture_started = False

        self.with_mask_camara = with_mask_camara

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

        


    def update_image(self, frame:np.ndarray):
       
        original_height, original_width, ch = frame.shape
        size = self.video_label.size()
        container_width = size.width() -20
        container_height = size.height() -10

        # print(f"Size Width: {container_width},height: {container_height} ")

        frame_show = frame.copy()
        self.add_custome_mask(frame_show)
         
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
        
        
        self.last_qimage = QImage(frame_show.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(self.last_qimage))
       

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
        

