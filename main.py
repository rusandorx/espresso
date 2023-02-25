import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.connection = sqlite3.connect('coffee.sqlite')
        self.init_table()

    def init_table(self):
        cur = self.connection.cursor()
        res = cur.execute('''
            select * from coffee
        ''').fetchall()
        header = tuple(zip(*cur.description))[0]
        self.tableWidget.setColumnCount(len(header))
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(header)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
