from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage
from PyQt6.QtWidgets import QWidget, QLabel


class ReadyFractal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Готовый фрактал")
        self.image = QLabel(self)
        self.image.resize(200, 200)
        self.setGeometry(50, 50, 800, 700)
        self.image.move(10, 10)
        self.images = QImage()
        self.c = 0

    def draw(self, pixmap):
        self.image.setPixmap(pixmap)
        self.image.resize(pixmap.width(), pixmap.height())
        self.pixmap = pixmap

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = (event.pos() - self.old_pos)
            self.image.move(self.image.pos() + delta)
            if self.image.x() > 0:
                self.image.move(0, self.image.y())
            if self.image.x() + self.image.width() < self.width():
                self.image.move(self.width() - self.image.width(), self.image.y())
            if self.image.y() > 0:
                self.image.move(self.image.x(), 0)
            if self.image.y() + self.image.height() < self.height():
                self.image.move(self.image.x(), self.height() - self.image.height())
            if 0 <= self.image.x() and self.image.x() + self.image.width() <= self.width():
                self.image.move((self.width() - self.image.width()) // 2, self.image.y())
            if 0 <= self.image.y() and self.image.y() + self.image.height() <= self.height():
                self.image.move(self.image.x(), (self.height() - self.image.height()) // 2)
            self.old_pos = event.pos()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = None

    def mouseDoubleClickEvent(self, event):
        if abs(self.c) <= 3:
            if event.button() == Qt.MouseButton.LeftButton:
                self.c = max(self.c - 1, -3)
            elif event.button() == Qt.MouseButton.RightButton:
                self.c = min(self.c + 1, 3)

            if self.c < 0:
                new_width = self.pixmap.width() // 2 ** abs(self.c)
                new_height = self.pixmap.height() // 2 ** abs(self.c)
            elif self.c >= 0:
                new_width = self.pixmap.width() * 2 ** abs(self.c)
                new_height = self.pixmap.height() * 2 ** abs(self.c)

            new_image = self.pixmap.scaled(new_width, new_height,
                                           transformMode=Qt.TransformationMode.SmoothTransformation)
            self.image.setPixmap(new_image)
            self.image.move(0, 0)
            self.image.resize(new_image.width(), new_image.height())
