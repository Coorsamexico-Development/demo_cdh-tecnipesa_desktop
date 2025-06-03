
from PyQt6.QtCore import QThread, QTimer
from PyQt6.QtWidgets import QWidget, QVBoxLayout,QSizePolicy
from features.capture_rfid.presentation.screens.capture_rfid_screen import CaptureRfidScreen
from features.capture_rfid.presentation.screens.async_data_screen import AsyncDataScreen
from features.capture_rfid.domain.workers.pusher_worker import PusherWorker

class HomeScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout_body = QVBoxLayout()
        layout_body.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout_body)
        self.toGo('capture_rfid')
        self.pusher_worker = PusherWorker()
        self.thread_pusher = QThread()
        self.pusher_worker.moveToThread(self.thread_pusher)
        self.thread_pusher.started.connect(self.pusher_worker.start)
        QTimer.singleShot(100,self.thread_pusher.start)
        
    def toGo(self, route_name:str, **params):
        layout = self.layout()
        body = layout.itemAt(0)
        if body is not None:
            body = body.widget()
            body.deleteLater()
        #layout change    
        if  route_name == 'capture_rfid':
            body = CaptureRfidScreen()

        body.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(body)