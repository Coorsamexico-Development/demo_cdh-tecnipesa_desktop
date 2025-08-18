from PyQt6.QtCore import QObject, pyqtSignal, QThread

import numpy as np

from pygrabber.dshow_graph import FilterGraph
class FrameGrabber(QObject):

    def __init__(self, filter_graph:FilterGraph):
        super().__init__()
        self.filter_graph = filter_graph
        self.running = False


    def start(self):
        
        self.running = True
        while self.running:
            self.filter_graph.grab_frame()
            QThread.msleep(30) # 30 FPS
    def stop(self):
        self.running = False
  
