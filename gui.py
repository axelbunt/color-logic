import ctypes
import datetime
from random import randint
import sqlite3
import sys
import traceback

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QLabel, \
    QHBoxLayout, QLineEdit, QTableView, QHeaderView

from exceptions import *
from grade import Grade
from ui import Ui

WIDTH, HEIGHT = 1100, 750

my_app_id = u'color_logic'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)


def open_app(secret_num: str, turn_count: int) -> None:
    app = QApplication(sys.argv)
    ex = MyApp(turn_count, secret_num)
    ex.show()
    result = app.exec()
    sys.exit(result)


class MyApp(QMainWindow):
    def __init__(self, turn_count: int, secret_num: str) -> None:
        super().__init__()
        self.TURN_COUNT = turn_count
        self.turn_count = turn_count
        self.secret_num = secret_num
        self.black_tokens = 0
        self.white_tokens = 0
        self.colors = {'к': 1, 'з': 2, 'с': 3, 'ж': 4, 'б': 5, 'ч': 6}
        self.colors_refactor = {'#ff0000': '#008000', '#008000': '#0000ff', '#0000ff': '#ffff00',
                                '#ffff00': '#ffffff', '#ffffff': '#000000', '#000000': '#ff0000'}
        self.codes_to_colors = {'#ff0000': 'к', '#008000': 'з', '#0000ff': 'с',
                                '#ffff00': 'ж', '#ffffff': 'б', '#000000': 'ч'}
        self.input_type = ''
        self.state = ''
        self.init_ui()

        self.is_data_base_created = False
        try:
            with open('for_stat.sqlite'):
                pass
        except IOError:
            con = sqlite3.connect('for_stat.sqlite')
            cur = con.cursor()

            cur.execute("""CREATE TABLE statistic (
                                Дата TEXT PRIMARY KEY,
                                Результат TEXT,
                                "Количество ходов" INTEGER)""")
            con.close()
        finally:
            self.is_data_base_created = True

    def init_ui(self) -> None:
        self.setGeometry(450, 200, WIDTH, HEIGHT)
        self.setFixedWidth(WIDTH)
        self.setFixedHeight(HEIGHT)
        self.setWindowTitle('Логика цвета')
        self.setWindowIcon(QIcon('images/icon.png'))

        self.window = QWidget()
        self.setCentralWidget(self.window)

        self.set_main_window()
        self.setStyleSheet("""  QPushButton {
                                    font-size: 20px;
                                    border: 2px solid;
                                    border-radius: 10px;
                                    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                        stop: 0 #f6f7fa, stop: 1 #dadbde);
                                    width: 400px;
                                    height: 50px;
                                }
                                QPushButton:hover {
                                    background-color: white;
                                }
                                QLabel {
                                    font-size: 20px;
                                    width: 400px;
                                    height: 400px;
                                }""")

    def setup_new_secret_num(self, required_len_of_num: int) -> str:
        secret_num = ''
        for _ in range(required_len_of_num):
            secret_num += str(randint(1, 6))
        return secret_num

    def set_main_window(self) -> None:
        self.btn_back = QPushButton(self)
        self.btn_back.setText('<-')
        self.btn_back.clicked.connect(self.return_to_main_window)
        self.btn_back.move(10, 10)
        self.btn_back.setVisible(False)

        self.for_text_info = QLabel(self)
        self.for_text_info.setWordWrap(True)
        self.for_text_info.setAlignment(Qt.AlignCenter)

        self.table = QTableView(self)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setVisible(False)

        self.btn_start = QPushButton(self)
        self.btn_start.setText('Играть')
        self.btn_start.clicked.connect(self.choose_input_type)

        self.btn_rules = QPushButton(self)
        self.btn_rules.setText('Правила')
        self.btn_rules.clicked.connect(self.go_to_rules)

        self.btn_stat = QPushButton(self)
        self.btn_stat.setText('Статистика')
        self.btn_stat.clicked.connect(self.go_to_stat)

        self.btn_dev = QPushButton(self)
        self.btn_dev.setText('О разработчике')
        self.btn_dev.clicked.connect(self.go_to_dev_info)

        self.btn_exit = QPushButton(self)
        self.btn_exit.setText('Выход')
        self.btn_exit.clicked.connect(self.exit)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.btn_start)
        self.main_layout.addWidget(self.btn_rules)
        self.main_layout.addWidget(self.btn_stat)
        self.main_layout.addWidget(self.btn_dev)
        self.main_layout.addWidget(self.btn_exit)

        self.main_layout.setAlignment(Qt.AlignCenter)

        self.window.setLayout(self.main_layout)

    def del_main_window(self) -> None:
        self.btn_start.setVisible(False)
        self.btn_rules.setVisible(False)
        self.btn_stat.setVisible(False)
        self.btn_dev.setVisible(False)
        self.btn_exit.setVisible(False)

    def return_to_main_window(self) -> None:
        if self.state == 'waiting for input':
            self.secret_num = self.setup_new_secret_num(len(self.secret_num))
            self.turn_count = self.TURN_COUNT
            self.black_tokens = 0
            self.white_tokens = 0
        if self.state == 'game finished':
            self.state = ''
        self.btn_back.setText('<-')
        self.btn_back.resize(100, 30)
        self.btn_back.setVisible(False)
        try:
            self.btn_for_console.setVisible(False)
            self.btn_for_interactive.setVisible(False)

            for i in range(len(self.secret_num)):
                btn = self.input_layout.itemAt(i).widget()
                btn.setVisible(False)
        except AttributeError:
            pass
        try:
            self.input.setVisible(False)
        except AttributeError:
            pass
        try:
            self.btn_ok.setVisible(False)
        except AttributeError:
            pass
        try:
            self.sub_rules.setVisible(False)
        except AttributeError:
            pass
        try:
            self.all_colors.setVisible(False)
        except AttributeError:
            pass
        try:
            self.btn_for_new_game.setVisible(False)
        except AttributeError:
            pass
        self.for_text_info.setVisible(False)
        self.for_text_info.setAlignment(Qt.AlignCenter)
        self.table.setVisible(False)
        self.btn_start.setVisible(True)
        self.btn_rules.setVisible(True)
        self.btn_stat.setVisible(True)
        self.btn_dev.setVisible(True)
        self.btn_exit.setVisible(True)

    def choose_input_type(self) -> None:
        self.btn_back.setText('<-')
        self.btn_back.resize(100, 30)
        self.del_main_window()
        try:
            self.btn_for_new_game.setVisible(False)
        except AttributeError:
            pass
        self.btn_back.setVisible(True)
        self.for_text_info.setVisible(True)
        self.main_layout.addWidget(self.for_text_info)
        self.for_text_info.setText('Выберите тип ввода цветовой комбинации: \n')

        self.btn_for_console = QPushButton(self)
        self.btn_for_console.setText('Ввод с клавиатуры')
        self.btn_for_console.clicked.connect(self.setup_console_input)

        self.btn_for_interactive = QPushButton(self)
        self.btn_for_interactive.setText('Ввод мышкой')
        self.btn_for_interactive.clicked.connect(self.setup_interactive_input)

        self.layout_for_game = QHBoxLayout(self)
        self.layout_for_game.addWidget(self.btn_for_console)
        self.layout_for_game.addWidget(self.btn_for_interactive)

        self.main_layout.addLayout(self.layout_for_game)

    def setup_console_input(self) -> None:
        self.input_type = 'keyboard'
        self.state = 'waiting for input'
        self.setFocus()

        self.btn_back.setText('Прекратить игру')
        self.btn_back.resize(180, 30)
        self.btn_for_console.setVisible(False)
        self.btn_for_interactive.setVisible(False)

        self.layout_for_game.addWidget(self.for_text_info)
        self.for_text_info.setText(f'Загаданная комбинация: {"*" * len(self.secret_num)}\n\n'
                                   f'Черных фишек: {self.black_tokens}\n'
                                   f'Белых фишек: {self.white_tokens}\n'
                                   f'Попыток осталось: {self.turn_count}')
        self.for_text_info.setAlignment(Qt.AlignLeft)

        self.input = QLineEdit(self)
        self.input.setMaxLength(len(self.secret_num))
        self.input.setStyleSheet('height: 30; border-radius: 10px; border: 1px solid;'
                                 'font-size: 20px')
        self.btn_ok = QPushButton(self)
        self.btn_ok.setText('ОК')
        self.btn_ok.clicked.connect(self.call_for_correct_input)
        self.btn_ok.setStyleSheet('width: 100; height: 30')
        self.input_layout = QHBoxLayout(self)
        self.input_layout.addWidget(self.input)
        self.input_layout.addWidget(self.btn_ok)

        self.layout_for_game.addLayout(self.input_layout)

        self.sub_rules = QLabel(self)
        self.sub_rules.setWordWrap(True)
        self.sub_rules.setText(f'Вводите комбинации из {len(self.secret_num)} цветов '
                               f'в любом регистре (для подтверждения нажмите ОК или Enter).\n'
                               'Доступные цвета: "к" – красный, "з" – зеленый, "с" – синий, '
                               '"ж" – желтый, "б" – белый, "ч" – черный.')
        self.sub_rules.setAlignment(Qt.AlignCenter)

        self.main_layout.addWidget(self.sub_rules)

    def grader(self, guess: str, secret_num: str) -> Grade:
        black, white = 0, 0

        guess_for_white = []
        secret_num_for_white = []
        for i in range(len(guess)):
            if guess[i] == secret_num[i]:
                black += 1
            else:
                guess_for_white.append(guess[i])
                secret_num_for_white.append(secret_num[i])

        for char in guess_for_white:
            if char in secret_num_for_white:
                white += 1
                del secret_num_for_white[secret_num_for_white.index(char)]

        return Grade(black, white)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if self.state == 'waiting for input' and (event.key() == Qt.Key_Enter or
                                                  event.key() == Qt.Key_Return):
            self.call_for_correct_input()

    def call_for_correct_input(self) -> None:
        self.state = 'waiting for input'
        guess = self.get_correct_input(self.turn_count, len(self.secret_num))

        if guess == 'error':
            pass
        else:
            self.turn_count -= 1
            grade = self.grader(guess, self.secret_num)

            if grade.black == 4:
                self.finish_game(True)
                return
            if self.turn_count == 0:
                self.finish_game(False)
                return
            self.update_status(grade)

    def finish_game(self, is_win: bool) -> None:
        self.input_type = ''
        self.state = 'game finished'

        try:
            self.input.setVisible(False)
        except AttributeError:
            pass
        try:
            for i in range(len(self.secret_num)):
                btn = self.input_layout.itemAt(i).widget()
                btn.setVisible(False)
        except AttributeError:
            pass
        self.btn_ok.setVisible(False)

        self.sub_rules.setVisible(False)

        self.btn_back.setText('В главное меню')

        self.for_text_info.setAlignment(Qt.AlignCenter)
        if is_win:
            self.for_text_info.setText(f'Победа!\n'
                                       f'Затрачено попыток: {self.TURN_COUNT - self.turn_count}')
        else:
            color_combination = ''
            for num in self.secret_num:
                color_combination += \
                    list(self.colors.keys())[list(self.colors.values()).index(int(num))]
            self.for_text_info.setText(f'Поражение...\n'
                                       f'Затрачено попыток: {self.TURN_COUNT - self.turn_count}\n'
                                       f'Была загадана комбинация: {color_combination}')

        self.btn_for_new_game = QPushButton(self)
        self.btn_for_new_game.setText('Новая игра')
        self.btn_for_new_game.setStyleSheet('height: 30')
        self.btn_for_new_game.clicked.connect(self.choose_input_type)
        self.main_layout.addWidget(self.btn_for_new_game)

        self.write_to_data_base(is_win)

        self.secret_num = self.setup_new_secret_num(len(self.secret_num))

        self.turn_count = self.TURN_COUNT
        self.black_tokens = 0
        self.white_tokens = 0

    def write_to_data_base(self, is_win: bool) -> None:
        try:
            if not self.is_data_base_created:
                raise NoDatabase()

            con = sqlite3.connect('for_stat.sqlite')
            cur = con.cursor()

            if is_win:
                game_res = 'Победа'
            else:
                game_res = 'Поражение'

            date = datetime.datetime.today().strftime('%d %b %Y - %H:%M:%S')

            cur.execute(f"""INSERT INTO statistic
                VALUES('{date}', '{game_res}', {self.TURN_COUNT - self.turn_count})""")
            con.commit()
        except AppException:
            print(traceback.format_exc())

    def update_status(self, grade: Grade) -> None:
        self.black_tokens = grade.black
        self.white_tokens = grade.white
        self.for_text_info.setText(f'Загаданная комбинация: {"*" * len(self.secret_num)}\n\n'
                                   f'Черных фишек: {self.black_tokens}\n'
                                   f'Белых фишек: {self.white_tokens}\n'
                                   f'Попыток осталось: {self.turn_count}')

    def get_correct_input(self, num_of_turns: int, secret_num_len: int) -> str:
        guess = ''
        if self.input_type == 'keyboard':
            guess = self.input.text().lower()
        if self.input_type == 'buttons':
            for i in range(len(self.secret_num)):
                btn = self.input_layout.itemAt(i).widget()
                color = btn.palette().window().color().name()
                guess += str(self.codes_to_colors[color])

        try:
            if num_of_turns == 0:
                raise TurnsOut()
            if len(guess) != secret_num_len:
                raise WrongInputLen()

            guess_to_return = ''
            for char in guess:
                if char not in self.colors:
                    raise WrongColor()
                guess_to_return += str(self.colors[char])
            return guess_to_return
        except InputException:
            # todo: выводить уведомление о неправильном вводе
            return 'error'

    def print_grade(self, grade: Grade) -> None:
        self.black_tokens = grade.black
        self.white_tokens = grade.white
        self.for_text_info.setText(f'Загаданная комбинация: {"*" * self.len_of_secret_num}\n\n'
                                   f'Черных фишек: {self.black_tokens}\n'
                                   f'Белых фишек: {self.white_tokens}\n'
                                   f'Попыток осталось: {self.turn_count}')

    def setup_interactive_input(self) -> None:
        self.input_type = 'buttons'
        self.state = 'waiting for input'
        self.setFocus()

        self.btn_back.setText('Прекратить игру')
        self.btn_back.resize(180, 30)
        self.btn_for_console.setVisible(False)
        self.btn_for_interactive.setVisible(False)

        self.layout_for_game.addWidget(self.for_text_info)
        self.for_text_info.setText(f'Загаданная комбинация: {"*" * len(self.secret_num)}\n\n'
                                   f'Черных фишек: {self.black_tokens}\n'
                                   f'Белых фишек: {self.white_tokens}\n'
                                   f'Попыток осталось: {self.turn_count}')
        self.for_text_info.setAlignment(Qt.AlignLeft)

        self.btn_ok = QPushButton(self)
        self.btn_ok.setText('ОК')
        self.btn_ok.clicked.connect(self.call_for_correct_input)
        self.btn_ok.setStyleSheet('width: 100; height: 30')

        self.input_layout = QHBoxLayout(self)

        for _ in range(len(self.secret_num)):
            self.btn_to_choose_color = QPushButton(self)
            self.btn_to_choose_color.clicked.connect(self.change_btn_color)
            self.btn_to_choose_color.setStyleSheet('width: 160px; background-color: red')
            self.input_layout.addWidget(self.btn_to_choose_color)

        self.input_layout.addWidget(self.btn_ok)

        self.layout_for_game.addLayout(self.input_layout)

        self.sub_rules = QLabel(self)
        self.sub_rules.setWordWrap(True)
        self.sub_rules.setText('Нажимая на цветные кнопки, вы можете менять их цвет. '
                               'Последоавтельность изменения: красный - зеленый - синий - '
                               'желтый - белый - черный - ...\n'
                               'Для подтверждения нажмите OK или Enter.')
        self.sub_rules.setAlignment(Qt.AlignCenter)

        self.main_layout.addWidget(self.sub_rules)

        self.btn_back.setText('В главное меню')
        self.btn_back.resize(180, 30)

    def change_btn_color(self) -> None:
        color_to_change = self.colors_refactor[self.sender().palette().window().color().name()]
        self.sender().setStyleSheet(f'background-color: {color_to_change}; width: 160px')

    def go_to_rules(self) -> None:
        self.del_main_window()
        self.btn_back.setVisible(True)
        self.for_text_info.setVisible(True)
        self.main_layout.addWidget(self.for_text_info)
        self.for_text_info.setText('Правила игры:\n'
                                   '"Логика цвета" – игра, похожая на игру "Быки и коровы". Ваш '
                                   'оппонент – компьютер, загадывает комбинацию, состоящую из '
                                   f'{len(self.secret_num)} цветов (не обязательно различных). '
                                   'Ваша задача – отгадать загаданную комбинацию за наименьшее '
                                   f'кол-во ходов. Всего у вас будет {self.turn_count} попыток. '
                                   'После каждого хода компьютер выставляет черные и белые фишки '
                                   '(возможно вообще не выставляет). Черная фишка означает, что '
                                   'какой-то цвет вашей комбинации совпадает с цветом в загаданной '
                                   'комбинации по месту, белая фишка означает, что цвет в вашей '
                                   'комбинации содержится в загаднной комбинации, но находится не '
                                   'на том месте.')

    def go_to_stat(self) -> None:
        self.del_main_window()
        self.btn_back.setVisible(True)
        self.for_text_info.setVisible(True)
        self.main_layout.addWidget(self.for_text_info)
        self.for_text_info.setVisible(True)
        self.for_text_info.setText('\nСтатистика игр')  # todo: убрать этот костыль

        self.table.setVisible(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.fill_table()
        self.main_layout.addWidget(self.table)

    def fill_table(self) -> None:
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('for_stat.sqlite')
        db.open()

        model = QSqlTableModel(self, db)
        model.setTable('statistic')
        model.sort(0, Qt.DescendingOrder)
        model.select()

        self.table.setModel(model)

    def go_to_dev_info(self) -> None:
        self.del_main_window()
        self.btn_back.setVisible(True)
        self.for_text_info.setVisible(True)
        self.main_layout.addWidget(self.for_text_info)
        self.for_text_info.setText('Игру создал: Axelbunt54\n'
                                   'Дата начала работы: 04.09.2021\n'
                                   'Версия: v0.7')

    def exit(self) -> None:
        sys.exit()


class Gui(Ui):
    def start_game(self) -> None:
        open_app(self.secret_num, self.turn_count)

    def print_secret_num_size(self, len_of_secret_num: int) -> None:
        pass

    def rate_player(self, game_result: bool, num_of_turns: int) -> None:
        pass

    def get_correct_input(self, num_of_turns: int, secret_num_len: int) -> str:
        pass

    def print_grade(self, grade: Grade) -> None:
        pass
