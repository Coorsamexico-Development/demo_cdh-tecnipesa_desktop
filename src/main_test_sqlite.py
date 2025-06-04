from PyQt6.QtWidgets import QApplication, QSplashScreen, QMainWindow
from PyQt6.QtGui import QPixmap, QFont, QColor, QPainter
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation
import os
import sys

class FadeSplashScreen(QSplashScreen):
    def __init__(self):

        super().__init__()
        width, height = 600, 300
        pixmap = QPixmap(width, height)
        pixmap.fill(QColor("#2B579A"))  # Fondo azul estilo Word
        # self.setPixmap(pixmap)

        self.logo = QPixmap(os.path.join(os.getcwd(),'assets','images', "logo_coorsa_white.png"))  # Tu logo PNG
        self.logo = self.logo.scaled(400, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

        # Pintar el logo y texto en el splash
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.drawPixmap((width - self.logo.width()) // 2, 50, self.logo)  # Centrado horizontal arriba
        # painter.setPen(Qt.GlobalColor.white)
        # painter.drawText(pixmap.rect().adjusted(0, 130, 0, 0), Qt.AlignmentFlag.AlignHCenter, "Word")
        painter.end()
        

        self.message_base = "Iniciando"
        self.dot_count = 0
        self.max_dots = 5

        self.setFont(QFont("Segoe UI", 12))
        self.setStyleSheet("color: white")
        self.setWindowOpacity(1.0)

        self.setPixmap(pixmap)
        # Animar puntos
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_message)
        self.timer.start(500)


    def update_message(self):
        self.dot_count = (self.dot_count + 1) % (self.max_dots + 1)
        dots = "." * self.dot_count
        self.showMessage(f"{self.message_base}{dots}", Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft, Qt.GlobalColor.white)

    def fade_and_close(self, on_finished):
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(1000)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.finished.connect(lambda: [self.close(), on_finished()])
        self.animation.start()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplicación Principal")
        self.setGeometry(100, 100, 800, 600)

app = QApplication(sys.argv)

splash = FadeSplashScreen()
splash.show()

def show_main():
    app.main_window = MainWindow()
    #set window full screen
    # QTimer.singleShot(1000,start_webserver)
    app.main_window.show()
    

# Después de 4 segundos, hace fade out y muestra la ventana principal
QTimer.singleShot(4000, lambda: splash.fade_and_close(show_main))

sys.exit(app.exec())