import sys
import sqlite3
import time

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QPlainTextEdit, QGraphicsOpacityEffect
from PyQt6.QtWidgets import QPushButton, QColorDialog, QRadioButton, QWidget, QTableWidgetItem
from PyQt6.QtGui import QPainter, QColor, QPen, QAction, QPixmap
from PyQt6.QtCore import QByteArray
from documentation import Documentation
from geometry_fractal import GeometryFractal
from fractal_from_bd import ReadyFractal
from mandelbrot import Mandelbrot
from main_window_ui import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.setGeometry(50, 50, 500, 500)
        self.setFixedSize(1000, 500)

        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        button_act = QAction("&Документация", self)
        button_act.triggered.connect(self.documentation)
        file_menu.addAction(button_act)
        self.w = None

        self.error_mess: QLabel
        self.error_mess.hide()
        self.op_eff = QGraphicsOpacityEffect()
        self.op_eff.setOpacity(0.99)
        self.error_mess.setGraphicsEffect(self.op_eff)
        self.paint_btn.clicked.connect(self.paint)
        self.recursion_depth: QComboBox
        self.len_line = 200
        for i in range(5):
            self.recursion_depth.addItem(f"{i}")
        self.color_btn = QPushButton(self)
        self.color_btn.setText("Выбрать цвет")
        self.color_btn.resize(100, 30)
        self.color_btn.move(20, 450)
        self.color_btn.clicked.connect(self.new_color)
        self.paint_btn.resize(100, 30)
        self.paint_btn.move(130, 428)
        self.axiom.move(20, 45)
        self.label.move(20, 25)
        self.label_2.move(20, 80)
        self.theorems.move(20, 100)
        self.label_3.move(20, 300)
        self.recursion_depth.move(20, 320)
        self.label_4.setText("Угол поворота")
        self.label_4.move(20, 360)
        self.degrees.move(20, 380)
        self.cur_string = ''
        self.cur_angle = 1
        self.cur_rec = 0
        self.cur_color = QColor(0, 0, 0)
        self.new_color_for_pen = QColor(0, 0, 0)

        self.choice_btn = QPushButton("Рисовать", self)
        self.choice_btn.resize(100, 30)
        self.choice_btn.move(20, 450)
        self.choice_btn.hide()
        self.choice_btn.clicked.connect(self.choice_fractal)

        self.window_with_gf = None

        self.set_radio_button()  # Создаём флажки для выбора режима рисования
        self.set_ready_fractal()  # Создаём элементы для рисования готового фрактала
        self.set_mandelbrot()  # Создаём элементы для рисования множества Мандельброта

        # Показываем элементы по умолчанию и скрываем ненужные
        self.show_gf()
        self.hide_mandelbrot()
        self.hide_ready_gf()

    def set_radio_button(self):
        self.geom_fractal = QRadioButton("Геометрический фрактал", self)
        self.geom_fractal.move(250, 120)
        self.geom_fractal.resize(200, 20)
        self.geom_fractal.setChecked(True)

        self.ready_geom_fractal = QRadioButton("Готовый геометрический фрактал из Базы Данных", self)
        self.ready_geom_fractal.move(250, 150)
        self.ready_geom_fractal.resize(200, 20)

        self.mandelbrot_fractal = QRadioButton("Множество Мандельброта", self)
        self.mandelbrot_fractal.move(250, 180)
        self.mandelbrot_fractal.resize(200, 20)

        self.julia_fractal = QRadioButton("Множество Жюлиа", self)
        self.julia_fractal.move(250, 210)
        self.julia_fractal.resize(200, 20)

        self.geom_fractal.toggled.connect(self.type_of_fractal)
        self.ready_geom_fractal.toggled.connect(self.type_of_fractal)
        self.mandelbrot_fractal.toggled.connect(self.type_of_fractal)
        self.julia_fractal.toggled.connect(self.type_of_fractal)

    def set_ready_fractal(self):
        self.choice_fractal_from_bd = None

        self.tableWidget.resize(480, 450)
        self.tableWidget.move(510, 30)
        self.connection = sqlite3.connect("my_bd.sqlite")
        res = self.connection.cursor().execute("SELECT * FROM fractals").fetchall()
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        # Заполняем таблицу элементами
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def set_mandelbrot(self):
        self.choice_mandelbrot = QComboBox(self)
        self.choice_mandelbrot.addItem("Черно-белое множество")
        self.choice_mandelbrot.addItem("Серое множество")
        self.choice_mandelbrot.addItem("Цветное множество")
        self.choice_mandelbrot.move(20, 100)
        self.choice_mandelbrot.resize(200, 30)

        self.paint_mandelbrot = QPushButton("Рисовать", self)
        self.paint_mandelbrot.resize(100, 30)
        self.paint_mandelbrot.move(20, 150)
        self.paint_mandelbrot.clicked.connect(self.mandelbrot)
        self.window_with_mandelbrot = None

    def change_str(self):
        self.error_mess.hide()
        cur_s = self.axiom.text()
        new_s = ''
        self.recursion_depth: QComboBox
        self.theorems: QPlainTextEdit
        d = {}
        for line in self.theorems.toPlainText().split('\n'):
            s, rule = line.split()
            d[s] = d.get(s, rule)
        for _ in range(int(self.recursion_depth.currentText())):
            for el in cur_s:
                if el in d:
                    new_s += d[el]
                else:
                    new_s += el
            cur_s = new_s
            new_s = ''
        return cur_s

    def paint(self):
        try:
            if self.axiom.text() == '':
                raise Exception("Поле \"аксиома\" не заполнено!")
            elif not self.theorems.toPlainText():
                raise Exception("Поле \"теоремы\" не заполнено!")
            self.cur_string = self.change_str()
            if not self.degrees.text().isnumeric():
                raise Exception("В поле \"Угол поворота\" введено неверное значение")
            if not (1 <= int(self.degrees.text()) <= 90):
                raise Exception("В поле \"Угол поворота\" введено неверное значение")
            self.cur_angle = int(self.degrees.text())
            self.cur_rec = int(self.recursion_depth.currentText())
            self.cur_color = self.new_color_for_pen
            if self.window_with_gf is None:
                # time.sleep(0.5)
                self.window_with_gf = GeometryFractal(self)
            self.window_with_gf.my_init()
            self.window_with_gf.update()
            self.window_with_gf.show()
        except ValueError:
            self.error_mess: QLabel
            self.error_mess.setText("Поле \"теоремы\" заполнено неверно!")
            self.error_mess.show()
        except Exception as ex:
            self.error_mess: QLabel
            self.error_mess.setText(str(ex))
            self.error_mess.show()

    def choice_fractal(self):
        self.error_mess.hide()
        try:
            if not (self.index_fr.text()):
                raise Exception("Не заполнено поле \"Индекс\"")
            if not (self.rec_dep.text()):
                raise Exception("Не заполнено поле \"Глубина рекурсии\"")
            res = self.connection.cursor().execute(f"""SELECT image{self.rec_dep.text()} FROM image
             WHERE id = {self.index_fr.text()}""").fetchall()
            payload = QByteArray(res[0][0])
            pixmap = QPixmap()
            pixmap.loadFromData(payload, "PNG")
            # pixmap.scaled(pixmap.width() // 2, pixmap.height() // 2)
            if self.choice_fractal_from_bd is None:
                self.choice_fractal_from_bd = ReadyFractal()
            self.choice_fractal_from_bd.draw(pixmap)
            self.choice_fractal_from_bd.show()
        except Exception as ex:
            self.error_mess.setText(str(ex))
            self.error_mess.show()

    def new_color(self):
        color = QColorDialog()
        color = color.getColor()
        if color.isValid():
            self.new_color_for_pen = color

    def documentation(self):
        if self.w is None:
            self.w = Documentation()
        self.w.show()

    def mandelbrot(self):
        if self.window_with_mandelbrot is not None:
            self.window_with_mandelbrot.destroy()
        self.window_with_mandelbrot = Mandelbrot(self.choice_mandelbrot.currentText())
        self.window_with_mandelbrot.show()

    def type_of_fractal(self):
        if self.sender().text() == "Геометрический фрактал":
            self.show_gf()
            self.hide_ready_gf()
            self.hide_mandelbrot()
        elif self.sender().text() == "Готовый геометрический фрактал из Базы Данных":
            self.hide_gf()
            self.hide_mandelbrot()
            self.show_ready_gf()
        elif self.sender().text() == "Множество Мандельброта":
            self.hide_gf()
            self.hide_ready_gf()
            self.show_mandelbrot()
        elif self.sender().text() == "Множество Жюлиа":
            self.hide_gf()
            self.hide_ready_gf()
            self.hide_mandelbrot()

    def hide_gf(self):
        arr = [
            self.axiom,
            self.label,
            self.label_2,
            self.theorems,
            self.label_3,
            self.recursion_depth,
            self.label_4,
            self.degrees,
            self.color_btn,
            self.paint_btn
        ]
        for el in arr:
            el.hide()

    def show_gf(self):
        arr = [
            self.axiom,
            self.label,
            self.label_2,
            self.theorems,
            self.label_3,
            self.recursion_depth,
            self.label_4,
            self.degrees,
            self.color_btn,
            self.paint_btn
        ]
        for el in arr:
            el.show()

    def show_ready_gf(self):
        arr = [
            self.choice_btn,
            self.index_fr,
            self.label_5,
            self.label_6,
            self.rec_dep,
            self.tableWidget
        ]
        for el in arr:
            el.show()

    def hide_ready_gf(self):
        arr = [
            self.choice_btn,
            self.index_fr,
            self.label_5,
            self.label_6,
            self.rec_dep,
            self.tableWidget
        ]
        for el in arr:
            el.hide()

    def show_mandelbrot(self):
        arr = [
            self.choice_mandelbrot,
            self.paint_mandelbrot
        ]
        for el in arr:
            el.show()

    def hide_mandelbrot(self):
        arr = [
            self.choice_mandelbrot,
            self.paint_mandelbrot
        ]
        for el in arr:
            el.hide()


def except_hook(cls, ex, tr):
    sys.__excepthook__(cls, ex, tr)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.excepthook = except_hook
    ex.show()
    sys.exit(app.exec())
