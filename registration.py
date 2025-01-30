import sys
import pygame
import os
import sqlite3

from PyQt6.QtWidgets import QInputDialog, QPushButton, QLineEdit, QWidget, QApplication, QMessageBox
from map import find_quick_path, start_screen, main, labyrinth, Time_or_coins


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
        print(cur.execute(f"""select username from users""").fetchall())
        try:
            print(cur.execute(f"""select points from users where username is '{self.username}'""").fetchone())
            if cur.execute(f"""select points from users where username is '{self.username}'""").fetchone() == None:
                self.mess = QMessageBox.question(self, 'A new user created!', 'New user profile has been created',
                                                 buttons=QMessageBox.StandardButton.Ok)
                if self.mess == QMessageBox.StandardButton.Ok:
                    new_user = (self.username, '0')
                    cur.execute(f"""insert into users values(?, ?)""", new_user)
                    self.con.commit()
        except Exception:
            print('Error')
            #self.mess = QMessageBox.question(self, 'A new user created!', 'New user profile has been created', buttons=QMessageBox.StandardButton.Ok)
            #if self.mess == QMessageBox.standardButton.Ok:
            #    cur.execute(f"""insert into users values (?, ?)""", new_user)
        start_screen()
        self.update_user()
        main(self.username)
        self.hide()

    def update_user(self):
        labyrinth.give_username(self.username)

    def closeEvent(self, event):
        self.con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Registration_page()
    ex.show()
    sys.exit(app.exec())