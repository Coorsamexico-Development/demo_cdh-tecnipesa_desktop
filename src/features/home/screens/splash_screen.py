from PyQt6.QtWidgets import QSplashScreen
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation
from PyQt6.QtGui import QPixmap, QFont, QColor, QPainter
from features.database.managers.sqlite_manager import SqliteManager
from features.database.migrations.creates_tables import CreateTables
from features.capture_rfid.domain.workers.tarimas_sync_worker import TarimasSyncWorker
from features.home.workers.impinj_start_worker import ImpinjStartWoker
import os

class FadeSplashScreen(QSplashScreen):
    def __init__(self, on_finished):
        super().__init__()
        self.on_finished = on_finished
        width, height = 600, 300
        pixmap = QPixmap(width, height)
        pixmap.fill(QColor("#BF2626"))
        self.setPixmap(pixmap)


        self.logo = QPixmap(os.path.join(os.getcwd(),'assets','images', "logo_coorsa_white.png"))  # Tu logo PNG
        self.logo = self.logo.scaled(400, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

        # Pintar el logo y texto en el splash
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.drawPixmap((width - self.logo.width()) // 2, 50, self.logo)  # Centrado horizontal arriba
      
        # painter.setPen(Qt.GlobalColor.white)
        # painter.drawText(pixmap.rect().adjusted(0, 130, 0, 0), Qt.AlignmentFlag.AlignHCenter, "Word")

        # font_small = QFont("Segoe UI", 12)
        # painter.setFont(font_small)
        
        painter.end()
        


        self.message_base = "Iniciando"
        self.dot_count = 0
        self.max_dots = 5

        self.setFont(QFont("Segoe UI", 10))
        self.setStyleSheet("color: white")

        self.setPixmap(pixmap)

        # Animar puntos
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_message)
        self.timer.start(400)

        # Para controlar la opacidad
        self._opacity = 1.0
        self.setWindowOpacity(self._opacity)




        self.tarimas_sync_worker = TarimasSyncWorker()
        self.tarimas_sync_worker.task_complete.connect(self.result_tarimas_worker)

        self.impinj_start_worker = ImpinjStartWoker()
        #alfinalizar el prendido de las antenas intentamos syncronizar la data
        self.impinj_start_worker.task_complete.connect(self.start_async_tarimas)

        QTimer.singleShot(200,self.load_data)

    def load_data(self):
        self.load_sqlite()
        self.message_base = "Iniciando antenas"
        self.impinj_start_worker.start()


    def load_sqlite(self):
        db_manager = SqliteManager()
        if db_manager.required_migration:
            CreateTables().up()
            self.message_base = "Creando base de datos"
        db_manager.close_connection()
    
    def start_async_tarimas(self):
        if self.impinj_start_worker.has_error:
            print(self.impinj_start_worker.error)
        self.message_base = "Sincronizando Información"
        self.tarimas_sync_worker.start()



    def result_tarimas_worker(self,success:bool):
        if success:
            self.message_base = "Sincronización Exitosamente."
        else: 
            self.message_base = "Error al sincronizar la información"
        self.fade_and_close()
        
    


    def update_message(self):
        self.dot_count = (self.dot_count + 1) % (self.max_dots + 1)
        dots = "." * self.dot_count
        self.showMessage(f"{self.message_base}{dots}", Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft, Qt.GlobalColor.white)

    def fade_and_close(self):
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(800)  # 1 segundo
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.finished.connect(lambda: [self.close(),self.on_finished()])
        self.animation.start()

