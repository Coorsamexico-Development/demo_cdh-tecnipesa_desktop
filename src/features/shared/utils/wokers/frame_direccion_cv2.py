from PyQt6.QtCore import  pyqtSignal, QThread

import numpy as np
import cv2
from enum import Enum
from services.camara_service import CamaraInfo, ResolutionInfo


fondo = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40, detectShadows=True) # sustractor de fondo que sirve para detectar movimiento
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)) 

class StateDirection(Enum):
        
        ENTRADA = "Salida"
        SALIDA = "Entrada"
class FrameCv2(QThread):

    frames = pyqtSignal((np.ndarray, object))
    directions = pyqtSignal(StateDirection)




    def __init__(self, 
                 camara:CamaraInfo, 
                 resolution:ResolutionInfo | None = None, 
                 with_direction:bool = False):
        super().__init__()
        self.camara = camara
        self.resolution = resolution
        self.videoCapture = None
        
        self.running = False
        self.with_direction = with_direction
        self.current_direction:StateDirection = None


    def run(self):
        if self.resolution is None:
            self.resolution = self.camara.resolutions[0]

        
        if self.videoCapture is None or not self.videoCapture.isOpened():
            self.videoCapture =  cv2.VideoCapture(self.camara.camera_index)
        
        self.videoCapture.set(cv2.CAP_PROP_FPS, 30)
        self.videoCapture.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution.width)
        self.videoCapture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution.height)
        
        self.running = True
       
        # #de declaran incluso cuando no se usan
        estaba_dentro = False
        width = self.resolution.width
        height = self.resolution.height
        min_area = int(width * height * 0.005)
        start_x_dectect = int( width *  0.05)
        end_x_dectect = int(width * 0.95)
        start_y_dectect = int(height * 0.1)
        end_y_dectect = int(height * 0.9)
        

        while self.running:

            ret, frame = self.videoCapture.read()
            if not ret:
                print("Error al capturar el frame")
                break
            
            # print("Capturando el frame")

            # para que se detecte el movimiento siempre que se mueva el objeto dentro del rectangulo
            frame_mask = None
            if self.with_direction:
                frame_mask = frame.copy()
                # crea el segundo frame negro0 que muestra solo los pixeles del objeto dentro del rectsangulo
                mascara = np.zeros(shape=(frame_mask.shape[:2]), dtype = np.uint8) 
                cv2.rectangle(mascara, (start_x_dectect, start_y_dectect), (end_x_dectect, end_y_dectect), 255, -1)
                imagen_area = cv2.bitwise_and(frame_mask, frame_mask, mask=mascara) 

                # detecta el movimiento del objeto
                fg = fondo.apply(imagen_area)
                fg = cv2.morphologyEx(fg, cv2.MORPH_OPEN, kernel)
                fg = cv2.morphologyEx(fg, cv2.MORPH_CLOSE, kernel)
                fg = cv2.dilate(fg, None, iterations=5)
                # cv2.imshow('fg', fg)
                contornos, _ = cv2.findContours(fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                if contornos:
                    contorno_mayor = max(contornos, key=cv2.contourArea)
                    if cv2.contourArea(contorno_mayor) > min_area:
                        x, y, w, h = cv2.boundingRect(contorno_mayor)
                        centro_x = x + w // 2
                        centro_y = y + h // 2
                        cv2.rectangle(frame_mask, (x, y), (x + w, y + h), (0, 255, 255), 2)
                        cv2.circle(frame_mask, (centro_x, centro_y), 2, (0, 0, 255), -1)

                        # ver si el objeto (todo el rectngulo) esta dentro del limite
                        dentro = (x > start_x_dectect and x + w  < end_x_dectect)
                        if estaba_dentro and not dentro:

                            if x + w >= end_x_dectect:
                                self.current_direction = StateDirection.SALIDA
                              
                            elif x <= start_x_dectect:
                                self.current_direction = StateDirection.ENTRADA
                            print(f"Direccion was dectected: {self.current_direction}")
                            self.directions.emit(self.current_direction)
                        estaba_dentro = dentro
            
                # dibuja las zonas y muestra texto
                # cv2.drawContours(frame_mask, [area], -1, (255, 0, 255), 2)
                cv2.rectangle(frame_mask, (start_x_dectect, start_y_dectect), (end_x_dectect, end_y_dectect), (0, 255, 255), 2)
                cv2.line(frame_mask, (end_x_dectect, start_y_dectect), (end_x_dectect, end_y_dectect), (0, 255, 255), 2)
                cv2.line(frame_mask, (start_x_dectect, start_y_dectect), (start_x_dectect, end_y_dectect), (0, 255, 255), 2)
                if self.current_direction is not None:  
                    cv2.putText(frame_mask, f"Direccion: {self.current_direction.value}", (20, 40), cv2.FONT_ITALIC, 0.7, (0, 0, 255), 2)
                    if self.current_direction == StateDirection.ENTRADA:
                        cv2.line(frame_mask, (start_x_dectect, start_y_dectect), (start_x_dectect, end_y_dectect), (0, 255, 0), 7)    
                    else:     
                        cv2.line(frame_mask, (end_x_dectect, start_y_dectect), (end_x_dectect, end_y_dectect), (0, 255, 0), 7) # el color es (0, 255, 0) y el grosor es el ultimo numero
                        

            self.frames.emit(frame, frame_mask)
            self.msleep(100)



    def stop(self):
        if self.running and self.videoCapture is not None:
            self.running = False
            self.wait()
            self.videoCapture.release()