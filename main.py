import sys
import os
import sqlite3
from PyQt5 import uic
from sys import argv, executable
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QAbstractItemView, QWidget


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        var = {k: v for k, v in cur.execute('select * from varieties').fetchall()}
        roast = {k: v for k, v in cur.execute('select * from roastings').fetchall()}
        res = list(
            map(lambda e: (e[0], var[e[1]], roast[e[2]], *e[3:]), cur.execute('select * from coffee').fetchall()))
        con.close()

        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'Название сорта', 'Cтепень обжарки', 'Тип', 'Вкус', 'Цена (руб)',
             'Упаковка (гр)'])

        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.pushButton.clicked.connect(self.run)

    def run(self):
        self.window = Window()
        self.window.show()


class Window(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.pushButton.clicked.connect(self.add)
        self.comboBox_4.currentIndexChanged.connect(self.view)
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        ids = list(map(lambda e: str(e[0]), cur.execute('select ID from coffee').fetchall()))
        self.var = {k: v for k, v in cur.execute('select * from varieties').fetchall()}
        self.roast = {k: v for k, v in cur.execute('select * from roastings').fetchall()}
        con.close()
        self.comboBox.addItems([''] + (list(self.var.values())))
        self.comboBox_2.addItems([''] + (list(self.roast.values())))
        self.comboBox_3.addItems(['', 'молотый', 'в зернах'])
        self.comboBox_4.addItems([''] + ids)

    def add(self):
        if not (self.comboBox_4.currentText()):
            con = sqlite3.connect('coffee.sqlite')
            cur = con.cursor()
            res = (list(self.var.values()).index(self.comboBox.currentText()) + 1,
                   list(self.roast.values()).index(self.comboBox_2.currentText()) + 1, self.comboBox_3.currentText(),
                   self.lineEdit.text(), self.lineEdit_2.text(), self.lineEdit_3.text())
            cur.execute(
                f"""INSERT INTO coffee (ID_variety, ID_roasting, type, description, price, size) VALUES {res}""")
            con.commit()
            con.close()
        else:
            id = int(self.comboBox_4.currentText())
            con = sqlite3.connect('coffee.sqlite')
            cur = con.cursor()
            res = (id, list(self.var.values()).index(self.comboBox.currentText()) + 1,
                   list(self.roast.values()).index(self.comboBox_2.currentText()) + 1, self.comboBox_3.currentText(),
                   self.lineEdit.text(), self.lineEdit_2.text(), self.lineEdit_3.text())
            cur.execute(f"delete from coffee where id = {id}")
            cur.execute(
                f"""INSERT INTO coffee (ID, ID_variety, ID_roasting, type, description, price, size) VALUES {res}""")
            con.commit()
            con.close()
        os.execl(executable, os.path.abspath(__file__), *argv)

    def view(self):
        if self.comboBox_4.currentText():
            id = int(self.comboBox_4.currentText())
            con = sqlite3.connect('coffee.sqlite')
            cur = con.cursor()
            res = list(map(lambda e: (str(e[0]), self.var[e[1]], self.roast[e[2]], *e[3:]),
                           cur.execute(f"select * from coffee where id = {id}").fetchall()))[0]
            self.comboBox.setCurrentText(res[1])
            self.comboBox_2.setCurrentText(res[2])
            self.comboBox_3.setCurrentText(res[3])
            self.lineEdit.setText(res[4])
            self.lineEdit_2.setText(str(res[5]))
            self.lineEdit_3.setText(str(res[6]))
            con.close()
        else:
            self.comboBox.setCurrentText('')
            self.comboBox_2.setCurrentText('')
            self.comboBox_3.setCurrentText('')
            self.lineEdit.setText('')
            self.lineEdit_2.setText('')
            self.lineEdit_3.setText('')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
