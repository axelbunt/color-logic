from grade import Grade


class Ui:
    def __init__(self, turn_count: int, secret_num: str) -> None:
        self.turn_count = turn_count
        self.secret_num = secret_num

    def start_game(self) -> None:
        pass

    def print_secret_num_size(self, len_of_secret_num: int) -> None:
        pass

    def rate_player(self, game_result: bool, num_of_turns: int) -> None:
        pass

    def get_correct_input(self, num_of_turns: int, secret_num_len: int) -> str:
        pass

    def print_grade(self, grade: Grade) -> None:
        pass
