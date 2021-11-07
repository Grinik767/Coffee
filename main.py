import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QAbstractItemView


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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
