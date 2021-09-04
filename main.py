from console import Console
from grade import Grade
from ui import Ui
from random import randint


# todo: ограничить колво возможных цифр (всего цветов 6)
def setup_new_secret_num(required_len_of_num: int) -> str:
    return str(randint(10 ** (required_len_of_num - 1), 10 ** required_len_of_num - 1))


assert len(setup_new_secret_num(4)) == 4, setup_new_secret_num(4)


def grader(guess: str, secret_num: str) -> Grade:
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


def get_guess(num_of_turns: int, secret_num: str, ui: Ui) -> Grade:
    secret_num_len = len(secret_num)

    guess = ui.get_correct_input(num_of_turns, secret_num_len)

    grade = grader(guess, secret_num)
    ui.print_grade(grade)

    return grade


def main(turn_count: int, required_len_of_secret_num: int) -> None:
    ui = Console(turn_count, required_len_of_secret_num)

    num_of_turn = 1
    secret_num = setup_new_secret_num(required_len_of_secret_num)
    game_win = False

    ui.print_game_rules()
    ui.print_secret_num_size(secret_num)

    grade = get_guess(num_of_turn, secret_num, ui)
    if grade.black == 4:
        game_win = True
    else:
        num_of_turn += 1
        while num_of_turn <= turn_count:
            grade = get_guess(num_of_turn, secret_num, ui)

            if grade.black == 4:
                game_win = True
                break

            num_of_turn += 1

    ui.rate_player(game_win, num_of_turn)


TURN_COUNT = 10
LEN_OF_SECRET_NUM = 4
if __name__ == '__main__':
    main(TURN_COUNT, LEN_OF_SECRET_NUM)
