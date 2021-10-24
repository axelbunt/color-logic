from ui import Ui
from grade import Grade


def _is_input_right(input_info: str, required_len_of_secret_num: int) -> bool:
    if len(input_info) != required_len_of_secret_num:
        return False
    return True


class Console(Ui):
    def start_game(self) -> None:
        print('"Логика цвета" – игра, похожая на игру "Быки и коровы". Ваш оппонент – компьютер, '
              f"загадывает комбинацию, состоящую из {self.len_of_secret_num} цифр (не обязательно "
              f"различных). В данной интерпретации для удобства цвета заменены цифрами (различные "
              "цифры обозначают различные цвета). Ваша задача – отгадать загаданное число за "
              f"наименьшее кол-во ходов. Всего у вас будет {self.turn_count} попыток.\n"
              "После каждого хода компьютер выставляет черные и белые фишки (возможно вообще не "
              "выставляет). Черная фишка означает, что какая-то цифра вашего числа совпадает с "
              "цифрой в загаданном числе по месту, белая фишка означает, что цифра вашего числа "
              "содержится в загаднном числе, но находится не на том месте.\n")
        self.print_secret_num_size(self.len_of_secret_num)

    def print_secret_num_size(self, len_of_secret_num: int) -> None:
        print(f'Загадана комбинация: {"*" * len_of_secret_num}.\n')

    def get_correct_input(self, num_of_turns: int, secret_num_len: int) -> str:
        guess = input(f'Ход {num_of_turns}. Ответ: ')
        if not _is_input_right(guess, secret_num_len):
            while not _is_input_right(guess, secret_num_len):
                guess = input(f'Ход {num_of_turns}. Ответ: ')

        return guess

    def print_grade(self, grade: Grade) -> None:
        print(f'Результат: {grade.black} черных, {grade.white} белых.\n')
        # todo: измениение слов "черных", "белых" взависимости от значений grade.black и grade.white
        #       (make_pretty_grade_output)

    def rate_player(self, game_result: bool, num_of_turns: int) -> None:
        if game_result:
            print(f'Победа!\nПотрачено попыток: {num_of_turns}')
        else:
            print('Поражение...')
