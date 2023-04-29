class AccountSignupException(Exception):
    def __init__(self, error_message: str):
        self.error_message = "Ошибка регистрации пользователя. {}".format(error_message)
