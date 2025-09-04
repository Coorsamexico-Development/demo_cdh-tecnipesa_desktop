from PyQt6.QtCore import  pyqtSignal, QThread

import numpy as np
from collections import deque

import cv2
from enum import Enum
from services.camara_service import CamaraInfo, ResolutionInfo


fondo = cv2.createBackgroundSubtractorMOG2(history=200, varThreshold=40, detectShadows=True)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

historial = deque(maxlen=10)  # guardamos últimos 10 centros detectados


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
        width = self.resolution.width
        height = self.resolution.height
        min_area = int(width * height * 0.005)
        linea_x = int(width * 0.5)
        tolerancia = 10  # margen para el cruce
        entradas = 0
        salidas = 0

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
                # detecta el movimiento del objeto
                # Preprocesamiento con MOG2
                fg = fondo.apply(frame_mask)
                # Limpiar la máscara
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
                fg = cv2.morphologyEx(fg, cv2.MORPH_OPEN, kernel, iterations=2)
                fg = cv2.morphologyEx(fg, cv2.MORPH_CLOSE, kernel, iterations=2)
                fg = cv2.dilate(fg, None, iterations=2)
                # cv2.imshow('fg', fg)
                # Buscar contornos
                contornos, _ = cv2.findContours(fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                if contornos:
                    contorno_mayor = max(contornos, key=cv2.contourArea)
                    if cv2.contourArea(contorno_mayor) > min_area:  # área mínima para evitar ruido
                        x, y, w, h = cv2.boundingRect(contorno_mayor)
                        centro = (x + w // 2, y + h // 2)
                        historial.append(centro)

                        # Dibujar rectángulo y centro
                        cv2.rectangle(frame_mask, (x, y), (x + w, y + h), (0, 255, 255), 2)
                        cv2.circle(frame_mask, centro, 5, (0, 0, 255), -1)

                        # Verificar cruce de línea con historial
                        if len(historial) >= 2:
                            x_prev = historial[0][0]
                            x_act = historial[-1][0]

                            if x_prev < linea_x - tolerancia and x_act > linea_x + tolerancia:
                                self.directions.emit(StateDirection.ENTRADA)
                                entradas += 1
                                historial.clear()  # evitar contar dos veces
                            elif x_prev > linea_x + tolerancia and x_act < linea_x - tolerancia:
                                self.directions.emit(StateDirection.SALIDA  )
                                salidas += 1
                                historial.clear()

                 # Dibujar línea y contadores
                
                cv2.line(frame_mask, (linea_x, 0), (linea_x, frame_mask.shape[0]), (0, 255, 255), 2)
                cv2.putText(frame_mask, f"Entradas: {entradas}", (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                cv2.putText(frame_mask, f"Salidas: {salidas}", (10, 70),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            
                

            self.frames.emit(frame, frame_mask)
            self.msleep(100)



    def stop(self):
        if self.running and self.videoCapture is not None:
            self.running = False
            self.wait()
            self.videoCapture.release()