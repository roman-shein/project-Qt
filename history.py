import sqlite3
from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QTableWidget, QLabel, QPushButton, QLineEdit


class History(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(500, 500)
        self.tableWidget = QTableWidget(self)
        self.tableWidget.resize(500, 350)
        self.tableWidget.move(0, 0)

        self.clear_all = QPushButton("Отчистить историю запросов", self)
        self.clear_all.resize(200, 30)
        self.clear_all.move(10, 360)
        self.clear_all.clicked.connect(self.delete_all)

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

    def delete_all(self):
        connection = sqlite3.connect("my_bd.sqlite")
        connection.cursor().execute("""delete from history""")
        connection.commit()
        connection.close()
        self.update()
