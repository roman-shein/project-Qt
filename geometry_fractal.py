from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen

from math import pi, cos, sin
from PyQt6.QtCore import QPointF


class GeometryFractal(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.m_v = main_window
        self.setWindowTitle("Геометрический фрактал")
        self.my_init()

    def my_init(self):
        self.s = self.m_v.cur_string
        self.rec = self.m_v.cur_rec
        self.len_line = self.m_v.len_line
        self.cur_color = self.m_v.cur_color
        self.alpha = self.m_v.cur_angle
        self.max_x = 0
        self.min_x = 0
        self.max_y = 0
        self.min_y = 0
        self.define_coord()
        self.x_0 = 20 - (self.min_x if self.min_x < 0 else 0)
        self.y_0 = 20 - (self.min_y if self.min_y < 0 else 0)
        self.len_x = abs(self.min_x - self.max_x) + 40
        self.len_y = abs(self.min_y - self.max_y) + 40
        self.setGeometry(100, 100, max(400, int(self.len_x)), max(400, int(self.len_y)))

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

    def paintEvent(self, event):
        self.my_init()
        qp = QPainter()
        qp.begin(self)
        self.draw_fractal(qp)
        qp.end()

    def draw_fractal(self, qp):
        cur_alpha = 0
        stored_coord = []
        x_0 = self.x_0
        y_0 = self.y_0
        pen = QPen(self.cur_color, 1)
        qp.setPen(pen)
        k = (self.rec + 1) ** 2
        for el in self.s:
            if el == 'F':
                cur_x = x_0 + self.len_line * cos(cur_alpha * pi / 180) / k
                cur_y = y_0 + self.len_line * sin(cur_alpha * pi / 180) / k
                p1 = QPointF(x_0, y_0)
                p2 = QPointF(cur_x, cur_y)
                qp.drawLine(p1, p2)
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
                stored_coord.append((self.x_0, self.y_0, cur_alpha))
            elif el == ']':
                x_0, y_0, cur_alpha = stored_coord[-1]
                stored_coord.pop()
            elif el == '|':
                cur_alpha = (cur_alpha + 180) % 360

