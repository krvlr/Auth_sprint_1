class AccountSignupException(Exception):
    def __init__(self, error_message: str):
        self.error_message = f"Ошибка регистрации пользователя. {error_message}"


class AccountSigninException(Exception):
    def __init__(self, error_message: str):
        self.error_message = f"Ошибка аутентификации пользователя. {error_message}"


class AccountRefreshException(Exception):
    def __init__(self, error_message: str):
        self.error_message = f"Ошибка при попытке воспользоваться refresh токеном. {error_message}"


class AccountPasswordChangeException(Exception):
    def __init__(self, error_message: str):
        self.error_message = f"Ошибка изменения пароля пользователя. {error_message}"


class AccountSignoutException(Exception):
    def __init__(self, error_message: str):
        self.error_message = f"Ошибка при попытке выйти из аккаунта. {error_message}"


class AccountSignoutAllException(Exception):
    def __init__(self, error_message: str):
        self.error_message = f"Ошибка при попытке выйти со всех устройств аккаунта. {error_message}"


class AccountHistoryException(Exception):
    def __init__(self, error_message: str):
        self.error_message = (
            f"Ошибка при попытке получения истории действий пользователя. {error_message}"
        )
