from PyQt6.QtCore import  pyqtSignal, QThread

import numpy as np
import cv2
from enum import Enum


fondo = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40, detectShadows=True) # sustractor de fondo que sirve para detectar movimiento
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)) 

class StateDirection(Enum):
        
        ENTRADA = "Salida"
        SALIDA = "Entrada"
class FrameCv2(QThread):

    frames = pyqtSignal(np.ndarray)
    directions = pyqtSignal(StateDirection)




    def __init__(self, videoCapture:cv2.VideoCapture | None = None, with_direction:bool = False):
        super().__init__()
        self.videoCapture = videoCapture
        self.running = False
        self.with_direction = with_direction
        self.current_direction:StateDirection = None


    def run(self):
        
        self.running = True
       
        #de declaran incluso cuando no se usan
        estaba_dentro = False
        width = self.videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        min_area = int(width * height * 0.005)
        start_x_dectect = int( width *  0.1)
        end_x_dectect = int(width * 0.9)
        start_y_dectect = int(height * 0.1)
        end_y_dectect = int(height * 0.9)

        while self.running:
            ret, frame = self.videoCapture.read()
            if not ret:
                break
            # para que se detecte el movimiento siempre que se mueva el objeto dentro del rectangulo
            if self.with_direction:
                # crea el segundo frame negro0 que muestra solo los pixeles del objeto dentro del rectsangulo
                mascara = np.zeros(shape=(frame.shape[:2]), dtype = np.uint8) 
                cv2.rectangle(mascara, (start_x_dectect, start_y_dectect), (end_x_dectect, end_y_dectect), 255, -1)
                imagen_area = cv2.bitwise_and(frame, frame, mask=mascara) 

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
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                        cv2.circle(frame, (centro_x, centro_y), 2, (0, 0, 255), -1)

                        # ver si el objeto (todo el rectngulo) esta dentro del limite
                        dentro = (x > start_x_dectect + 10 and x + w  < end_x_dectect-10)
                        if estaba_dentro and not dentro:
                            if  x <= start_x_dectect:
                                self.current_direction = StateDirection.SALIDA
                            else:
                                self.current_direction = StateDirection.ENTRADA
                            
                            self.directions.emit(self.current_direction)
                        estaba_dentro = dentro
            
                # dibuja las zonas y muestra texto
                # cv2.drawContours(frame, [area], -1, (255, 0, 255), 2)
                cv2.rectangle(frame, (start_x_dectect, start_y_dectect), (end_x_dectect, end_y_dectect), (0, 255, 255), 2)
                cv2.line(frame, (end_x_dectect, start_y_dectect), (end_x_dectect, end_y_dectect), (0, 255, 255), 2)
                cv2.line(frame, (start_x_dectect, start_y_dectect), (start_x_dectect, end_y_dectect), (0, 255, 255), 2)
                if self.current_direction is not None:  
                    cv2.putText(frame, f"Direccion: {self.current_direction.value}", (20, 40), cv2.FONT_ITALIC, 0.7, (0, 0, 255), 2)
                    if self.current_direction == StateDirection.ENTRADA:
                        cv2.line(frame, (end_x_dectect, start_y_dectect), (end_x_dectect, end_y_dectect), (0, 255, 0), 7) # el color es (0, 255, 0) y el grosor es el ultimo numero
                    else:     
                        cv2.line(frame, (start_x_dectect, start_y_dectect), (start_x_dectect, end_y_dectect), (0, 255, 0), 7)    

            self.frames.emit(frame)
            self.msleep(100)



    def stop(self):
        self.running = False
        self.wait()
        if self.videoCapture is not None:
            self.videoCapture.release()
            self.videoCapture = None
        
        

  
