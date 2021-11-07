class AppException(Exception):
    pass


class NoDatabase(AppException):
    pass


class InputException(AppException):
    pass


class TurnsOut(InputException):
    pass


class WrongInputLen(InputException):
    pass


class WrongColor(InputException):
    pass
