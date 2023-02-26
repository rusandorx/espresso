import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget


class FormWidget(QWidget):
    def __init__(self, on_confirm):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.on_confirm = on_confirm
        self.pushButton.clicked.connect(self.on_click)

    def set_fields(self, data):
        self.NameEdit.setText(str(data[0]))
        self.RoastBox.setValue(int(data[1]))
        self.GroundButton.setChecked(False if data[2] == 'False' else True)
        self.DescriptionEdit.setText(str(data[3]))
        self.PriceBox.setValue(int(data[4]))
        self.AmountBox.setValue(int(data[5]))

    def on_click(self):
        data = (self.NameEdit.text(), self.RoastBox.value(), 1 if self.GroundButton.isChecked() else 0,
                self.DescriptionEdit.text(), self.PriceBox.value(), self.AmountBox.value())
        self.on_confirm(data)


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.addForm = FormWidget(self.add_data)
        self.changeForm = FormWidget(self.change_data)
        self.connection = sqlite3.connect('coffee.sqlite')
        self.init_table()

        self.pushButton.clicked.connect(lambda state: self.addForm.show())
        self.pushButton_2.clicked.connect(self.show_change_form)
        self.current_row = None

    def add_data(self, data):
        try:
            cur = self.connection.cursor()
            data = tuple(map(lambda x: f'"{x}"', data))
            data = ('Null', *data)
            cur.execute(f'''
                insert into coffee values ({','.join(data)})
            ''').fetchall()
            self.init_table()
            self.addForm.hide()
        except Exception as e:
            print('Нельзя добавить кофе с именем которое уже существует')

    def show_change_form(self):
        self.current_row = self.tableWidget.currentRow()
        if self.current_row == -1:
            return print('Не выбрана строчка для редактирования')
        data = [self.tableWidget.item(self.current_row, i).text() for i in range(1, self.tableWidget.columnCount())]
        self.changeForm.set_fields(data)
        self.changeForm.show()

    def change_data(self, data):
        id = self.tableWidget.item(self.current_row, 0).text()

        cur = self.connection.cursor()
        data = tuple(map(lambda x: f'"{x}"', data))
        data = {f'"{key}" = {value}' for key, value in
                zip(('name', 'roast', 'ground', 'description', 'cost (rubles)', 'amount'), data)}
        cur.execute(f'''
            update coffee set {','.join(data)} where id = {id}
        ''').fetchall()
        self.init_table()
        self.changeForm.hide()

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
                if j == 3:
                    elem = True if elem else False
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
