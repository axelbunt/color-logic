import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QLabel, \
    QTableWidget

from ui import Ui

WIDTH, HEIGHT = 1100, 750


def open_app(len_of_secret_num: int, turn_count: int):
    app = QApplication(sys.argv)
    ex = MyApp(len_of_secret_num, turn_count)
    ex.show()
    sys.exit(app.exec())


class MyApp(QMainWindow):
    def __init__(self, len_of_secret_num: int, turn_count: int) -> None:
        super().__init__()
        self.len_of_secret_num = len_of_secret_num
        self.turn_count = turn_count
        self.init_ui()

    def init_ui(self) -> None:
        self.setGeometry(450, 200, WIDTH, HEIGHT)
        self.setFixedWidth(WIDTH)
        self.setFixedHeight(HEIGHT)
        self.setWindowTitle('Логика цвета')

        self.window = QWidget()
        self.setCentralWidget(self.window)

        self.set_main_window()

    def set_main_window(self) -> None:
        self.btn_back = QPushButton(self)
        self.btn_back.setText('<-')
        self.btn_back.clicked.connect(self.return_to_main_window)
        self.btn_back.move(10, 10)
        self.btn_back.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_back.setVisible(False)

        self.for_text_info = QLabel(self)
        self.for_text_info.setAlignment(QtCore.Qt.AlignCenter)

        self.table = QTableWidget(self)
        self.table.setVisible(False)

        self.btn_start = QPushButton(self)
        self.btn_start.setText('Играть')
        self.btn_start.clicked.connect(self.choose_input_type)
        self.btn_start.setCursor(QtCore.Qt.PointingHandCursor)

        self.btn_rules = QPushButton(self)
        self.btn_rules.setText('Правила')
        self.btn_rules.clicked.connect(self.go_to_rules)
        self.btn_rules.setCursor(QtCore.Qt.PointingHandCursor)

        self.btn_stat = QPushButton(self)
        self.btn_stat.setText('Статистика')
        self.btn_stat.clicked.connect(self.go_to_stat)
        self.btn_stat.setCursor(QtCore.Qt.PointingHandCursor)

        self.btn_dev = QPushButton(self)
        self.btn_dev.setText('О разработчике')
        self.btn_dev.clicked.connect(self.go_to_dev_info)
        self.btn_dev.setCursor(QtCore.Qt.PointingHandCursor)

        self.btn_exit = QPushButton(self)
        self.btn_exit.setText('Выход')
        self.btn_exit.clicked.connect(self.exit)
        self.btn_exit.setCursor(QtCore.Qt.PointingHandCursor)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.btn_start)
        self.main_layout.addWidget(self.btn_rules)
        self.main_layout.addWidget(self.btn_stat)
        self.main_layout.addWidget(self.btn_dev)
        self.main_layout.addWidget(self.btn_exit)

        self.window.setLayout(self.main_layout)

    def del_main_window(self) -> None:
        self.btn_start.setVisible(False)
        self.btn_rules.setVisible(False)
        self.btn_stat.setVisible(False)
        self.btn_dev.setVisible(False)
        self.btn_exit.setVisible(False)

    def return_to_main_window(self) -> None:
        self.btn_back.setVisible(False)
        self.for_text_info.setVisible(False)
        self.table.setVisible(False)
        self.btn_start.setVisible(True)
        self.btn_rules.setVisible(True)
        self.btn_stat.setVisible(True)
        self.btn_dev.setVisible(True)
        self.btn_exit.setVisible(True)

    def choose_input_type(self) -> None:
        self.del_main_window()
        self.btn_back.setVisible(True)
        self.for_text_info.setVisible(True)
        self.main_layout.addWidget(self.for_text_info)
        self.for_text_info.setText('В разработке...')

    def go_to_rules(self) -> None:
        self.del_main_window()
        self.btn_back.setVisible(True)
        self.for_text_info.setVisible(True)
        self.main_layout.addWidget(self.for_text_info)
        # todo: автоперенос текста
        self.for_text_info.setText('Правила игры:\n\n'
                                   '"Логика цвета" – игра, похожая на игру "Быки и коровы". Ваш '
                                   'оппонент – компьютер, загадывает комбинацию, состоящую из '
                                   f'{self.len_of_secret_num} цветов (не обязательно различных).\n'
                                   'Ваша задача – отгадать загаданную комбинацию за наименьшее '
                                   f'кол-во ходов. Всего у вас будет {self.turn_count} попыток.\n'
                                   'После каждого хода компьютер выставляет черные и белые фишки '
                                   '(возможно вообще не выставляет). Черная фишка означает, что '
                                   'какой-то цвет вашей комбинации\nсовпадает с цветом в загаданной'
                                   ' комбинации по месту, белая фишка означает, что цвет в вашей '
                                   'комбинации содержится в загаднной комбинации, но находится не '
                                   'на том месте.\n')

    def go_to_stat(self) -> None:
        self.del_main_window()
        self.btn_back.setVisible(True)
        self.for_text_info.setVisible(True)
        self.main_layout.addWidget(self.for_text_info)
        self.for_text_info.setVisible(True)
        self.for_text_info.setText('\n')  # todo: убрать этот костыль

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
                                   'Версия: v0.2')

    def exit(self) -> None:
        sys.exit()


class Gui(Ui):
    def start_game(self) -> None:
        open_app(self.len_of_secret_num, self.turn_count)
