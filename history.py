import sqlite3
from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QTableWidget


class History(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(500, 500)
        self.tableWidget = QTableWidget(self)
        self.tableWidget.resize(500, 500)
        self.tableWidget.move(0, 0)

    def print_history(self):
        connection = sqlite3.connect("my_bd.sqlite")
        res = connection.cursor().execute("SELECT axiom, theorems, degrees, recursion FROM history").fetchall()
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        # Заполняем таблицу элементами
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        connection.close()

    def paintEvent(self, event):
        self.print_history()
