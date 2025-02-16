import sys
import pygame
import os
import sqlite3

from PyQt6.QtWidgets import QInputDialog, QPushButton, QLineEdit, QWidget, QApplication, QMessageBox, QTableWidget, \
    QTableWidgetItem, QLabel
from map import find_quick_path, start_screen, main, labyrinth, Time_or_coins, end_win, terminate, end_lose
from bowling import bowling


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

        self.ready_button_dungeon = QPushButton(self)
        self.ready_button_dungeon.setText('Сыграть в игру "Dungeon"')
        self.ready_button_dungeon.move(325, 375)
        self.ready_button_dungeon.resize(175, 25)
        self.ready_button_dungeon.clicked.connect(self.check_user_dungeon)

        self.ready_button_bowling = QPushButton(self)
        self.ready_button_bowling.setText('Сыграть в игру "Bowling"')
        self.ready_button_bowling.move(525, 375)
        self.ready_button_bowling.resize(175, 25)
        self.ready_button_bowling.clicked.connect(self.check_user_bowling)

        self.con = sqlite3.connect('users_db.sqlite')


    def check_user_dungeon(self):
        self.username = str(self.username_line_input.text())
        cur = self.con.cursor()
        try:
            if cur.execute(f"""select points from users_points where username is '{self.username}'""").fetchone() == None:
                self.mess = QMessageBox.question(self, 'A new user created!', 'New user profile has been created',
                                                 buttons=QMessageBox.StandardButton.Ok)
                if self.mess == QMessageBox.StandardButton.Ok:
                    new_user = (self.username, 0, 0, 0)
                    cur.execute(f"""insert into users_points values(?, ?, ?, ?)""", new_user)
                    self.con.commit()
        except Exception:
            print('Error')
            #self.mess = QMessageBox.question(self, 'A new user created!', 'New user profile has been created', buttons=QMessageBox.StandardButton.Ok)
            #if self.mess == QMessageBox.standardButton.Ok:
            #    cur.execute(f"""insert into users values (?, ?)""", new_user)
        self.hide()
        start_screen()
        self.update_user()
        ishod = main(self.username)
        if ishod == 'win':
            choise = end_win(self.username)
            if choise == ('close'):
                terminate()
            else:
                self.show_table('dungeon')
        else:
            choise = end_lose(self.username)
            if choise == ('close'):
                terminate()
            else:
                self.show_table('dungeon')

    def check_user_bowling(self):
        self.username = str(self.username_line_input.text())
        cur = self.con.cursor()
        try:
            if cur.execute(f"""select points_of_bowling from users_points where username is '{self.username}'""").fetchone() == None:
                self.mess = QMessageBox.question(self, 'A new user created!', 'New user profile has been created',
                                                 buttons=QMessageBox.StandardButton.Ok)
                if self.mess == QMessageBox.StandardButton.Ok:
                    new_user = (self.username, 0, 0, 0)
                    cur.execute(f"""insert into users_points values(?, ?, ?, ?)""", new_user)
                    self.con.commit()
        except Exception:
            print('Error')
            #self.mess = QMessageBox.question(self, 'A new user created!', 'New user profile has been created', buttons=QMessageBox.StandardButton.Ok)
            #if self.mess == QMessageBox.standardButton.Ok:
            #    cur.execute(f"""insert into users values (?, ?)""", new_user)
        self.hide()
        ishod = bowling(self.username)
        if ishod == 'win':
            self.show_table('bowling')
        else:
            self.show_table('bowling')

    def update_user(self):
        labyrinth.give_username(self.username)

    #def return_registration(self):
    #    self.restart_button.hide()
    #    self.username_line_input.show()
    #    self.ready_button.show()
    #    self.username_label.hide()
    #    self.tableWidget.hide()

    def show_table(self, game):
        #self.restart_button = QPushButton(self)
        #self.restart_button.move(400, 960)
        #self.restart_button.resize(200, 25)
        #self.restart_button.setText('Сыграть заново')
        #self.restart_button.clicked.connect(self.return_registration)
        if game == 'dungeon':
            self.username_line_input.hide()
            self.ready_button_dungeon.hide()
            self.ready_button_bowling.hide()
            self.tableWidget = QTableWidget(self)
            self.tableWidget.resize(900, 900)
            self.tableWidget.move(50, 50)
            self.username_label = QLabel(self)
            self.username_label.setText(f'Ваше имя: {self.username}')
            self.username_label.move(250, 10)
            self.show()
            cur = self.con.cursor()
            try:
                result = cur.execute(f"""select username, points, time from users_points 
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
        else:
            self.username_line_input.hide()
            self.ready_button_dungeon.hide()
            self.ready_button_bowling.hide()
            self.tableWidget = QTableWidget(self)
            self.tableWidget.resize(900, 900)
            self.tableWidget.move(50, 50)
            self.username_label = QLabel(self)
            self.username_label.setText(f'Ваше имя: {self.username}')
            self.username_label.move(250, 10)
            self.show()
            cur = self.con.cursor()
            try:
                result = cur.execute(f"""select username, points_of_bowling from users_points 
                                            order by points_of_bowling DESC""").fetchall()
                self.tableWidget.setRowCount(len(result))
                self.tableWidget.setColumnCount(len(result[0]))
                self.tableWidget.setColumnWidth(0, 445)
                self.tableWidget.setColumnWidth(1, 445)
                self.tableWidget.setHorizontalHeaderLabels(
                    ['Имя пользователя', 'Сбитые кегли'])
                for i, elem in enumerate(result):
                    for j, value in enumerate(elem):
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