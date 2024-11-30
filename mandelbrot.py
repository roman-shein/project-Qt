from math import sin

from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QPainter, QColor, QPen, QImage, QPixmap
from PyQt6.QtCore import QPoint, QTimer


class Mandelbrot(QWidget):
    def __init__(self, type):
        super().__init__()
        self.setFixedSize(600, 400)
        self.setWindowTitle("Множество Мандельброта")
        self.max_iter = 255
        if type == "Черно-белое множество":
            self.palette = [
                (255, 255, 255) for i in range(self.max_iter - 1)
            ]
        elif type == "Серое множество":
            self.palette = [
                (i, i, i) for i in range(self.max_iter - 1)
            ]
        elif type == "Цветное множество":
            self.palette = [
                (
                    int(255 * sin(i / 30.0 + 0.3) ** 2),
                    int(255 * sin(i / 30.0 + 1.0) ** 2),
                    int(255 * sin(i / 30.0 + 1.8) ** 2)
                ) for i in range(self.max_iter - 1)
            ]
        self.palette.append((0, 0, 0))

        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(self.width(), self.height())

        self.images = {'params': (-2.0, -1.0, 1.0, 1.0), 'image': None}
        self.images['image'] = QImage(self.width(), self.height(), QImage.Format.Format_ARGB32_Premultiplied)

        self.mand_timer = QTimer(self)
        self.mand_timer.setInterval(10)
        self.mand_timer.timeout.connect(self.build_mand_line)

        self.start_build_mand()

    def start_build_mand(self):
        self.image_generator = self.paint_mand_color()
        self.mand_timer.start()

    def build_mand_line(self):
        try:
            next(self.image_generator)
            self.image.setPixmap(QPixmap.fromImage(self.images["image"]))
        except StopIteration:
            self.mand_timer.stop()

    def paint_mand_color(self):
        painter = QPainter()
        painter.begin(self.images["image"])
        xa, ya, xb, yb = [-2.0, -1.0, 1.0, 1.0]
        img_x, img_y = self.width(), self.height()
        for y in range(img_y):
            zy = y * (yb - ya) / img_y + ya
            for x in range(img_x):
                zx = x * (xb - xa) / img_x + xa
                c, z = zx + zy * 1j, 0
                for count in range(self.max_iter):
                    if abs(z) > 2.0:
                        break
                    z = z * z + c
                pen = QPen(QColor(*self.palette[count]), 1)
                painter.setPen(pen)
                painter.drawPoint(QPoint(x, y))
            yield True
        painter.end()
