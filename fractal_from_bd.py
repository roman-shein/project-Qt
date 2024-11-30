from PyQt6.QtWidgets import QWidget, QLabel


class ReadyFractal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Готовый фрактал")
        self.label = QLabel(self)
        self.label.resize(200, 200)
        self.setGeometry(50, 50, 800, 700)
        self.label.move(10, 10)

    def draw(self, pixmap):
        self.label.setPixmap(pixmap)
        self.label.resize(pixmap.width(), pixmap.height())
