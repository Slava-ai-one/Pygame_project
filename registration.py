import sys
import pygame
import os
import sqlite3

from PyQt6.QtWidgets import QInputDialog, QPushButton, QLineEdit, QWidget, QApplication, QMessageBox, QTableWidget, \
    QTableWidgetItem, QLabel
from map import find_quick_path, start_screen, main, labyrinth, Time_or_coins, end_win, terminate, end_lose


class Registration_page(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(460, 40, 1000, 1000)
        self.setWindowTitle('Регистрация')

        self.username_line_input = QLineEdit(self)
        self.username_line_input.move(400, 300)
        self.username_line_input.resize(200, 50)

        self.ready_button = QPushButton(self)
        self.ready_button.setText('Войти')
        self.ready_button.move(450, 375)
        self.ready_button.resize(100, 25)
        self.ready_button.clicked.connect(self.check_user)

        self.con = sqlite3.connect('users_db.sqlite')


    def check_user(self):
        self.username = str(self.username_line_input.text())
        cur = self.con.cursor()
        print(cur.execute(f"""select username from users_points""").fetchall())
        try:
            print(cur.execute(f"""select points from users_points where username is '{self.username}'""").fetchone())
            if cur.execute(f"""select points from users_points where username is '{self.username}'""").fetchone() == None:
                self.mess = QMessageBox.question(self, 'A new user created!', 'New user profile has been created',
                                                 buttons=QMessageBox.StandardButton.Ok)
                if self.mess == QMessageBox.StandardButton.Ok:
                    new_user = (self.username, 0, 0)
                    cur.execute(f"""insert into users_points values(?, ?, ?)""", new_user)
                    self.con.commit()
        except Exception:
            print('Error')
            #self.mess = QMessageBox.question(self, 'A new user created!', 'New user profile has been created', buttons=QMessageBox.StandardButton.Ok)
            #if self.mess == QMessageBox.standardButton.Ok:
            #    cur.execute(f"""insert into users values (?, ?)""", new_user)
        start_screen()
        self.hide()
        self.update_user()
        ishod = main(self.username)
        if ishod == 'win':
            choise = end_win(self.username)
            if choise == ('close'):
                terminate()
            else:
                self.show_table()
        else:
            choise = end_lose(self.username)
            if choise == ('close'):
                terminate()
            else:
                self.show_table()

    def update_user(self):
        labyrinth.give_username(self.username)

    #def return_registration(self):
    #    self.restart_button.hide()
    #    self.username_line_input.show()
    #    self.ready_button.show()
    #    self.username_label.hide()
    #    self.tableWidget.hide()

    def show_table(self):
        #self.restart_button = QPushButton(self)
        #self.restart_button.move(400, 960)
        #self.restart_button.resize(200, 25)
        #self.restart_button.setText('Сыграть заново')
        #self.restart_button.clicked.connect(self.return_registration)
        self.username_line_input.hide()
        self.ready_button.hide()
        self.tableWidget = QTableWidget(self)
        self.tableWidget.resize(900, 900)
        self.tableWidget.move(50, 50)
        self.username_label = QLabel(self)
        self.username_label.setText(f'Ваше имя: {self.username}')
        self.username_label.move(250, 10)
        self.show()
        cur = self.con.cursor()
        try:
            result = cur.execute(f"""select * from users_points 
order by points DESC, time ASC""").fetchall()
            self.tableWidget.setRowCount(len(result))
            self.tableWidget.setColumnCount(len(result[0]))
            self.tableWidget.setColumnWidth(0, 295)
            self.tableWidget.setColumnWidth(1, 295)
            self.tableWidget.setColumnWidth(2, 295)
            self.tableWidget.setHorizontalHeaderLabels(['Имя пользователя', 'Собранные монеты', 'Время прохождения, в секундах'])
            for i, elem in enumerate(result):
                for j, value in enumerate(elem):
                    if j == 2 and value == 0:
                        value = 'Не смог выбраться'
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(value)))
        except Exception:
            print('Error')


    def closeEvent(self, event):
        self.con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Registration_page()
    ex.show()
    sys.exit(app.exec())