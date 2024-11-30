from PyQt6.QtWidgets import QWidget, QPlainTextEdit


class Documentation(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(600, 600)
        self.doc = QPlainTextEdit(self)
        self.doc.resize(600, 600)
        with open("documentation.txt", 'r', encoding="utf8") as fin:
            text = fin.read()
        self.doc.setPlainText(text)
        self.doc.setDisabled(True)

