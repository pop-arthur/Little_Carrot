import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget
import sys
from game_process import init_game


# функция проверяет есть ли данное имя в бд и возвращает True или False
def player_exists(player_name):
    con = sqlite3.connect('little_carrot.db')
    cur = con.cursor()

    try:
        cur.execute(f"SELECT count(*) FROM users WHERE player_name = '{player_name}'")
        value = cur.fetchone()
        if value[0] == 0:
            return False
        else:
            return True
    finally:
        cur.close()
        con.close()


# добавляет игрока в db
def add_player(player_name):
    con = sqlite3.connect('little_carrot.db')
    cur = con.cursor()
    level, map, health = 1, 1, 0

    try:
        cur.execute(f"INSERT OR IGNORE INTO users(player_name, level, map, health) "
                    f"VALUES('{player_name}',{level} , {map}, {health});")
    finally:
        con.commit()
        cur.close()
        con.close()


class HelloScreen(QWidget):
    def __init__(self):
        super(HelloScreen, self).__init__()
        uic.loadUi('data/qt/hello_widget.ui', self)
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setFixedSize(1000, 800)
        self.setWindowTitle("Little Carrot")

        self.account_settings_widget = None

        self.continue_game_button.clicked.connect(self.continue_game)
        self.new_game_button.clicked.connect(self.new_game)
        self.account_button.clicked.connect(self.account_settings)
        self.exit_button.clicked.connect(self.exit_clicked)
        self.update_current_player()

    def continue_game(self):
        # запустить игру, подгрузив текущий прогресс игрока
        self.close()
        init_game()


    def new_game(self):
        # запусить для игрока игру с начала
        pass

    def account_settings(self):
        # смена аккаунта
        self.account_settings_widget = SignInSignUp(self)

    def exit_clicked(self):
        # выход
        self.close()

    def update_current_player(self):
        with open("data/qt/current_player.txt", "r", encoding="utf-8") as file:
            data = file.readlines()
            if data:
                self.account_status_label.setText(f"Выполнен вход: {data[0]}")
            else:
                self.account_status_label.setText("Вход не выполнен")


class SignInSignUp(QWidget):
    def __init__(self, hello_screen):
        self.hello_screen = hello_screen
        super(SignInSignUp, self).__init__()
        uic.loadUi("data/qt/sign_in_sign_up.ui", self)
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setFixedSize(469, 112)
        self.setWindowTitle("Смена аккаунта")

        self.sign_in_widget = None
        self.sign_up_widget = None

        self.sign_in_button.clicked.connect(self.sign_in)
        self.sign_up_button.clicked.connect(self.sign_up)

    def sign_in(self):
        self.close()
        self.sign_in_widget = InputPlayerName("sign in", self.hello_screen)

    def sign_up(self):
        self.close()
        self.sign_up_widget = InputPlayerName("sign up", self.hello_screen)


class InputPlayerName(QWidget):
    def __init__(self, type_of_call, hello_screen):
        self.type_of_call = type_of_call
        self.hello_screen = hello_screen
        super(InputPlayerName, self).__init__()
        uic.loadUi("data/qt/input_player_name.ui", self)
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setWindowTitle("Смена аккаунта")

        self.ok_button.clicked.connect(self.ok_pressed)

    def ok_pressed(self):
        player_name = self.player_name_lineedit.text()

        # проверка что пользователь ввёл что-либо
        if not player_name:
            self.status_label.setText("Введите имя игрока")

        # вход
        elif self.type_of_call == "sign in":
            if player_exists(player_name):
                with open("data/qt/current_player.txt", "w", encoding="utf-8") as file:
                    file.write(player_name)
                self.hello_screen.update_current_player()
                self.close()
            else:
                self.status_label.setText("Игрок не найден")

        # регистрация
        elif self.type_of_call == "sign up":
            if not player_exists(player_name):
                add_player(player_name)
                with open("data/qt/current_player.txt", "w", encoding="utf-8") as file:
                    file.write(player_name)
                self.hello_screen.update_current_player()
                self.close()
            else:
                self.status_label.setText("Данное имя уже используется")


def init_hello_screen():
    sys._excepthook = sys.excepthook

    def exception_hook(exctype, value, traceback):
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)

    sys.excepthook = exception_hook

    app = QApplication(sys.argv)
    ex = HelloScreen()
    sys.exit(app.exec())


if __name__ == '__main__':
    init_hello_screen()
