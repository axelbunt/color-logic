import sys

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QLabel, \
    QTableWidget, QHBoxLayout, QLineEdit

from grade import Grade
from ui import Ui

WIDTH, HEIGHT = 1100, 750


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
        self.state = ''
        self.init_ui()

    def init_ui(self) -> None:
        self.setGeometry(450, 200, WIDTH, HEIGHT)
        self.setFixedWidth(WIDTH)
        self.setFixedHeight(HEIGHT)
        self.setWindowTitle('Логика цвета')

        self.window = QWidget()
        self.setCentralWidget(self.window)

        # todo: поставить .svg на background
        # contents = b""
        # file = QtCore.QTemporaryFile(self.window)
        # if file.open():
        #     file.write(contents)
        #     file.flush()
        #     self.window.setStyleSheet("""background-image: url(%s);""" % file.fileName())
        # QtCore.QMetaObject.connectSlotsByName(self.window)
        # MainWindow
        # {
        #     background - image: url(bg.jpg);
        # background - repeat: no - repeat;
        # background - position: center;
        # }

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

    def set_main_window(self) -> None:
        self.btn_back = QPushButton(self)
        self.btn_back.setText('<-')
        self.btn_back.clicked.connect(self.return_to_main_window)
        self.btn_back.move(10, 10)
        self.btn_back.setVisible(False)

        self.for_text_info = QLabel(self)
        self.for_text_info.setWordWrap(True)
        self.for_text_info.setAlignment(Qt.AlignCenter)

        self.table = QTableWidget(self)
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
        if self.state == 'game finished':
            self.state = ''
        self.btn_back.setText('<-')
        self.btn_back.resize(100, 30)
        self.btn_back.setVisible(False)
        try:
            self.btn_for_console.setVisible(False)
            self.btn_for_interactive.setVisible(False)
            self.input.setVisible(False)
            self.btn_ok.setVisible(False)
            self.sub_rules.setVisible(False)
            # self.all_colors.setVisible(False)
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

        # self.all_colors = QLabel(self)
        # self.all_colors.setWordWrap(True)
        # self.all_colors.setText('Доступные цвета: "к" – красный, "з" – зеленый, "с" – синий, '
        #                         '"ж" – желтый, "б" – белый, "ч" – черный.')
        # self.all_colors.setAlignment(Qt.AlignCenter)

        self.main_layout.addWidget(self.sub_rules)
        # self.main_layout.addWidget(self.all_colors)

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
        self.state = 'game finished'

        self.input.setVisible(False)
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

        self.turn_count = self.TURN_COUNT
        self.black_tokens = 0
        self.white_tokens = 0

    def write_to_data_base(self, is_win: bool) -> None:
        # в БД: результат игры, затрачено попыток, дата/время
        pass

    def update_status(self, grade: Grade) -> None:
        self.black_tokens = grade.black
        self.white_tokens = grade.white
        self.for_text_info.setText(f'Загаданная комбинация: {"*" * len(self.secret_num)}\n\n'
                                   f'Черных фишек: {self.black_tokens}\n'
                                   f'Белых фишек: {self.white_tokens}\n'
                                   f'Попыток осталось: {self.turn_count}')

    def get_correct_input(self, num_of_turns: int, secret_num_len: int) -> str:
        guess = self.input.text().lower()
        # todo: кидать разные (собственные) виды исключений
        try:
            if num_of_turns == 0:
                raise Exception
            if len(guess) != secret_num_len:
                raise Exception

            guess_to_return = ''
            for char in guess:
                if char not in self.colors:
                    raise Exception
                guess_to_return += str(self.colors[char])
            return guess_to_return
        except Exception:
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
        self.layout_for_game.addWidget(self.for_text_info)
        self.for_text_info.setText('В разработке...')
        self.btn_for_console.setVisible(False)
        self.btn_for_interactive.setVisible(False)

        self.btn_back.setText('В главное меню')
        self.btn_back.resize(180, 30)

    def go_to_rules(self) -> None:
        self.del_main_window()
        self.btn_back.setVisible(True)
        self.for_text_info.setVisible(True)
        self.main_layout.addWidget(self.for_text_info)
        # todo: автоперенос текста - Done
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
        self.for_text_info.setText('\nВ разработке...')  # todo: убрать этот костыль

        self.table.setVisible(True)
        self.table.setColumnCount(4)
        self.table.setRowCount(0)
        self.fill_table()
        self.main_layout.addWidget(self.table)

    # todo: сделать БД, выгрузку/запись из/в БД
    def fill_table(self) -> None:
        pass

    def go_to_dev_info(self) -> None:
        self.del_main_window()
        self.btn_back.setVisible(True)
        self.for_text_info.setVisible(True)
        self.main_layout.addWidget(self.for_text_info)
        self.for_text_info.setText('Игру создал: Axelbunt54\n'
                                   'Дата начала работы: 04.09.2021\n'
                                   'Версия: v0.4')

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
