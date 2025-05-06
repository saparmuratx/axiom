class UserNotActiveException(Exception):
    def __init__(self, message="User is not active"):
        super().__init__(message)
        self.message = message


class InvalidPasswordException(Exception):
    def __init__(self, message="Invalid password"):
        super().__init__(message)
        self.message = message


class UserNotUniqueException(Exception):
    def __init__(self, message="User email already in use"):
        super().__init__(message)
        self.message = message
