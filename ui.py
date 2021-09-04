from grade import Grade


class Ui:
    def __init__(self, turn_count: int, len_of_secret_num: int) -> None:
        self.turn_count = turn_count
        self.len_of_secret_num = len_of_secret_num

    def print_game_rules(self) -> None:
        pass

    def print_secret_num_size(self, secret_num: str) -> None:
        pass

    def rate_player(self, game_result: bool, num_of_turns: int) -> None:
        pass

    def get_correct_input(self, num_of_turns: int, secret_num_len: int) -> str:
        pass

    def print_grade(self, grade: Grade) -> None:
        pass
