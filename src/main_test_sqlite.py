from PyQt6.QtWidgets import QApplication, QSplashScreen, QMainWindow
from PyQt6.QtGui import QPixmap, QFont, QColor, QPainter, QGuiApplication
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, pyqtProperty, QObject
import sys

class FadeSplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__()
        pixmap = QPixmap(600, 300)
        pixmap.fill(QColor("#BF2626"))
        self.setFont(QFont("Segoe UI", 30, QFont.Weight.Bold))
        self.setPixmap(pixmap)


        # Draw "Word"
        painter = QPainter(pixmap)
        painter.setPen(Qt.GlobalColor.white)
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "Coorsamexico")

        font_small = QFont("Segoe UI", 22)
        painter.setFont(font_small)



        self.message_base = "Iniciando"
        self.dot_count = 0
        self.max_dots = 5

        self.setFont(QFont("Segoe UI", 12))
        self.setStyleSheet("color: white")

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_message)
        self.timer.start(500)

        # Para controlar la opacidad
        self._opacity = 1.0
        self.setWindowOpacity(self._opacity)

        painter.end()

        self.setPixmap(pixmap)


    def update_message(self):
        self.dot_count = (self.dot_count + 1) % (self.max_dots + 1)
        dots = "." * self.dot_count
        self.showMessage(f"{self.message_base}{dots}", Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft, Qt.GlobalColor.white)

    def fade_and_close(self, on_finished):
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(800)  # 1 segundo
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.finished.connect(lambda: [self.close(), on_finished()])
        self.animation.start()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplicación Principal")
        self.setGeometry(100, 100, 800, 600)

# App setup
app = QApplication(sys.argv)

splash = FadeSplashScreen()
splash.show()

# Mostrar ventana principal con desvanecimiento
def show_main_window():
    window = MainWindow()
    window.show()

QTimer.singleShot(4000, lambda: splash.fade_and_close(show_main_window))

sys.exit(app.exec())