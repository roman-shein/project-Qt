from math import sin

from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QPainter, QColor, QPen, QImage, QPixmap
from PyQt6.QtCore import QPoint, QTimer


class Julia(QWidget):
    def __init__(self, main_window: "MainWindow"):
        super().__init__()
        self.setFixedSize(600, 500)
        self.setWindowTitle("Множество Жюлиа")
        self.max_iter = 255
        self.m_w = main_window
        self.c = eval(self.m_w.choise_c.currentText())
        if self.m_w.choice_mandelbrot.currentText() == "Черно-белое множество":
            self.palette = [
                (255, 255, 255) for i in range(self.max_iter - 1)
            ]
        elif self.m_w.choice_mandelbrot.currentText() == "Серое множество":
            self.palette = [
                (i, i, i) for i in range(self.max_iter - 1)
            ]
        elif self.m_w.choice_mandelbrot.currentText() == "Цветное множество":
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
        xa, ya, xb, yb = [-2.0, -1.8, 2.0, 1.8]
        img_x, img_y = self.width(), self.height()
        for y in range(img_y):
            zy = y * (yb - ya) / img_y + ya
            for x in range(img_x):
                zx = x * (xb - xa) / img_x + xa
                c, z = self.c, zx + zy * 1j
                # 0.27334 + 0.00742 * 1j
                # -0.765 + 0.12 * 1j
                # 0.99 + 0.14 * 1j     z = z * z + c * z
                # 0.1103 + 0.6703 * 1j
                # 0.005 + 0.655 * 1j
                # -0.1 + 0.655 * 1j
                # -0.07 + 0.655 * 1j
                # -0.09 + 0.655 * 1j
                # -0.0875 + 0.655 * 1j
                # 0.992 + 0.135 * 1j   z = z * z + c * z
                for count in range(self.max_iter):
                    if abs(z) > 2.0:
                        break
                    z = z * z + c
                pen = QPen(QColor(*self.palette[count]), 1)
                painter.setPen(pen)
                painter.drawPoint(QPoint(x, y))
            yield True
        painter.end()


