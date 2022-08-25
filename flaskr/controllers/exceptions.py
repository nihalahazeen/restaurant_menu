class ControllerException(Exception):
    """
    Controller exception class
    """

    def __init__(self, message: str = None, exception: Exception = None) -> None:
        super().__init__(message)
        self.messages = [message] if isinstance(message, (str, bytes)) else message

class UnauthorizedException(ControllerException):
    pass