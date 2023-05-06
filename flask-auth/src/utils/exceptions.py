class AccountSignupException(Exception):
    def __init__(self, error_message: str):
        self.error_message = f"Ошибка регистрации пользователя. {error_message}"


class AccountSigninException(Exception):
    def __init__(self, error_message: str):
        self.error_message = f"Ошибка аутентификации пользователя. {error_message}"
