import sys

from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class VentanaJuego(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tres en Raya")
        self.resize(400, 400)
        self.ganador = QMessageBox(self)
        self.texto = QLabel(self)
        self.texto.setStyleSheet("font-size: 18px;")
        self.turno = "Player 1"
        self.texto.setText(f"Turno de: {self.turno}")
        self.boton = QPushButton("")
        self.ubicacion()

    def crear_turno(self):
        self.turno = "Player 1"
        return self.turno

    def ubicacion(self):
        self.orden = QVBoxLayout()
        self.setLayout(self.orden)
        self.orden.addWidget(self.texto)
        self.orden.addWidget(self.boton)


app = QApplication(sys.argv)
ventana = VentanaJuego()


ventana.show()
app.exec()
