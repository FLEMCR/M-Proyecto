import sys

from cairo import STATUS_LAST_STATUS
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class Juego_Tres_Raya(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tres en Raya")


app = QApplication(sys.argv)
ventana = Juego_Tres_Raya()
