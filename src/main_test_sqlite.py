from PyQt6.QtWidgets import QApplication, QSplashScreen, QLabel, QMainWindow
from PyQt6.QtGui import QPixmap, QFont, QColor, QPainter
from PyQt6.QtCore import Qt, QTimer
import sys

class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__()

        # Crear fondo azul del splash
        pixmap = QPixmap(600, 300)
        pixmap.fill(QColor("#2B579A"))  # Color similar al azul de Word
        self.setPixmap(pixmap)

        # Dibujar elementos con QPainter
        self.setFont(QFont("Segoe UI", 30, QFont.Weight.Bold))

        painter = QPainter(pixmap)
        painter.setPen(Qt.GlobalColor.white)
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "Word")

        font_small = QFont("Segoe UI", 10)
        painter.setFont(font_small)
        painter.drawText(20, pixmap.height() - 20, "Iniciando...")
        painter.end()

        self.setPixmap(pixmap)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplicación Principal")
        self.setGeometry(100, 100, 800, 600)

app = QApplication(sys.argv)

splash = SplashScreen()
splash.show()

# Simular carga de la aplicación
QTimer.singleShot(3000, splash.close)  # Cierra el splash después de 3 segundos
QTimer.singleShot(3000, lambda: MainWindow().show())

sys.exit(app.exec())