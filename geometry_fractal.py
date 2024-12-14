from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QPainter, QPen, QImage, QPixmap

from math import pi, cos, sin
from PyQt6.QtCore import QPointF, QTimer, Qt


class GeometryFractal(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.m_v = main_window
        self.setWindowTitle("Геометрический фрактал")
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.old_pos = None
        self.c = 0
        # self.my_init()

        self.timer = QTimer(self)
        self.timer.setInterval(1)
        self.timer.timeout.connect(self.build_gf)

        self.statusbar = QLabel(self)

        # self.start_build_gf()

    def my_init(self):
        self.image.move(0, 0)
        self.images = {"image": None}
        self.s = self.m_v.cur_string
        self.rec = self.m_v.cur_rec
        self.len_line = self.m_v.len_line
        self.cur_color = self.m_v.cur_color
        self.alpha = self.m_v.cur_angle
        self.max_x = 0
        self.min_x = 0
        self.max_y = 0
        self.min_y = 0
        self.check = self.m_v.delay_checkbox.isChecked()
        self.define_coord()
        self.x_0 = 20 - (self.min_x if self.min_x < 0 else 0)
        self.y_0 = 20 - (self.min_y if self.min_y < 0 else 0)
        self.len_x = abs(self.min_x - self.max_x) + 40
        self.len_y = abs(self.min_y - self.max_y) + 40
        self.setGeometry(100, 100, min(800, int(self.len_x)), min(600, int(self.len_y)))
        self.images['image'] = QImage(int(self.len_x), int(self.len_y), QImage.Format.Format_ARGB32_Premultiplied)
        self.image.resize(int(self.len_x), int(self.len_y))
        self.statusbar.move(20, self.height() - 20)
        self.statusbar.resize(100, 20)
        self.statusbar.setText("Process 0%")
        self.start_build_gf()

    def start_build_gf(self):
        self.image_generator = self.draw_fractal()
        self.timer.start()

    def build_gf(self):
        try:
            next(self.image_generator)
            self.image.setPixmap(QPixmap.fromImage(self.images["image"]))
        except StopIteration:
            self.timer.stop()

    def define_coord(self):
        stored_coord = []
        x_0 = 0
        y_0 = 0
        cur_alpha = 0
        k = (self.rec + 1) ** 2
        for el in self.s:
            if el == 'F':
                cur_x = x_0 + self.len_line * cos(cur_alpha * pi / 180) / k
                cur_y = y_0 + self.len_line * sin(cur_alpha * pi / 180) / k
                x_0 = cur_x
                y_0 = cur_y
            elif el == 'f':
                cur_x = x_0 + self.len_line * cos(cur_alpha * pi / 180) / k
                cur_y = y_0 + self.len_line * sin(cur_alpha * pi / 180) / k
                x_0 = cur_x
                y_0 = cur_y
            elif el == '+':
                cur_alpha = (cur_alpha + self.alpha) % 360
            elif el == '-':
                cur_alpha = (cur_alpha - self.alpha) % 360
            elif el == '[':
                stored_coord.append((x_0, y_0, cur_alpha))
            elif el == ']':
                x_0, y_0, cur_alpha = stored_coord[-1]
                stored_coord.pop()
            elif el == '|':
                cur_alpha = (cur_alpha + 180) % 360
            if x_0 > self.max_x:
                self.max_x = x_0
            if x_0 < self.min_x:
                self.min_x = x_0
            if y_0 > self.max_y:
                self.max_y = y_0
            if y_0 < self.min_y:
                self.min_y = y_0
            # print(self.min_x, self.max_x, self.min_y, self.max_y)

    def draw_fractal(self):
        painter = QPainter()
        painter.begin(self.images["image"])
        cur_alpha = 0
        stored_coord = []
        x_0 = self.x_0
        y_0 = self.y_0
        pen = QPen(self.cur_color, 1)
        painter.setPen(pen)
        k = (self.rec + 1) ** 2
        q = len(str(len(self.s)))
        c = 0
        for el in self.s:
            if el == 'F':
                cur_x = x_0 + self.len_line * cos(cur_alpha * pi / 180) / k
                cur_y = y_0 + self.len_line * sin(cur_alpha * pi / 180) / k
                p1 = QPointF(x_0, y_0)
                p2 = QPointF(cur_x, cur_y)
                painter.drawLine(p1, p2)
                x_0 = cur_x
                y_0 = cur_y
                c += 1
                if self.check:
                    if c % 10 ** (q - 3) == 0:
                        self.statusbar.setText(f"Process {c * 100 // self.s.count('F')}%")
                        yield True
                else:
                    if c % 10 ** (q - 1) == 0:
                        self.statusbar.setText(f"Process {c * 100 // self.s.count('F')}%")
                        yield True
            elif el == 'f':
                cur_x = x_0 + self.len_line * cos(cur_alpha * pi / 180) / k
                cur_y = y_0 + self.len_line * sin(cur_alpha * pi / 180) / k
                x_0 = cur_x
                y_0 = cur_y
            elif el == '+':
                cur_alpha = (cur_alpha + self.alpha) % 360
            elif el == '-':
                cur_alpha = (cur_alpha - self.alpha) % 360
            elif el == '[':
                stored_coord.append((self.x_0, self.y_0, cur_alpha))
            elif el == ']':
                x_0, y_0, cur_alpha = stored_coord[-1]
                stored_coord.pop()
            elif el == '|':
                cur_alpha = (cur_alpha + 180) % 360
        yield True
        painter.end()
        self.statusbar.setText("Successfully")

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
                new_width = self.images["image"].width() // 2 ** abs(self.c)
                new_height = self.images["image"].height() // 2 ** abs(self.c)
            elif self.c >= 0:
                new_width = self.images["image"].width() * 2 ** abs(self.c)
                new_height = self.images["image"].height() * 2 ** abs(self.c)

            new_image = self.images["image"].scaled(new_width, new_height,
                                                    transformMode=Qt.TransformationMode.SmoothTransformation)
            self.image.setPixmap(QPixmap.fromImage(new_image))
            self.image.move(0, 0)
            self.image.resize(new_image.width(), new_image.height())
