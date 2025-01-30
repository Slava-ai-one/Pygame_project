from PyQt6.QtWidgets import QInputDialog, QPushButton, QLineEdit, QWidget, QApplication, QMessageBox


class Time_or_coins(QWidget):
    global Time_left
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(500, 500, 350, 50)
        self.setWindowTitle('Кошелёк или жизнь?')

        self.time_button = QPushButton(self)
        self.time_button.setText('Отнять время жизни')
        self.time_button.move(30, 15)
        self.time_button.resize(125, 25)
        self.time_button.clicked.connect(self.answer)

        self.coins_button = QPushButton(self)
        self.coins_button.setText('Откупиться деньгами')
        self.coins_button.move(200, 15)
        self.coins_button.resize(125, 25)
        self.coins_button.clicked.connect(self.answer)

        self.current_choise = None

    def answer(self):
        if self.sender().text() == 'Отнять время жизни':
            self.current_choise = 'time'
        else:
            self.current_choise = 'coins'
        self.hide()

    def get_cur_choise(self):
        return self.current_choise

    def reset_choise(self):
        self.current_choise = None

