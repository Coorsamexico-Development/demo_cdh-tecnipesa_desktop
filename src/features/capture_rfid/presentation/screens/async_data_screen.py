from PyQt6.QtWidgets import  QWidget,QLabel,QHBoxLayout
from PyQt6.QtCore import QTimer,Qt
from features.capture_rfid.domain.workers.tarimas_sync_worker import TarimasSyncWorker


class AsyncDataScreen(QWidget):
    def __init__(self):
        super().__init__()

        layout= QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)


        self.message_label = QLabel("Bienvenido")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.message_label)

        self.setLayout(layout)


        self.tarimas_sync_worker = TarimasSyncWorker()
        self.tarimas_sync_worker.task_complete.connect(self._result_tarimas_worker)

        QTimer.singleShot(800, self.start_async_tarimas)

    def start_async_tarimas(self):
        self.message_label.setText("Actualizado tarimas...")
        self.tarimas_sync_worker.start()

    def _result_tarimas_worker(self, success:bool):

        if success:
            
            self.message_label.setText("Actualizado Exitosamente.")
            QTimer.singleShot(800, self.to_capture_rfid)
        else: 
            print(self.tarimas_sync_worker.error)
            if isinstance(self.tarimas_sync_worker.error, Exception):
                self.message_label.setText(self.tarimas_sync_worker.error.message)
            else:
                self.message_label.setText("Error al syncronizar la información")


    

    
    def to_capture_rfid(self):
        screen =self.parent()
        screen.toGo("capture_rfid")