class DAOException(Exception):
    """
    Base DAO exception class
    """

    def __init__(self, exception: Exception = None) -> None:
        super().__init__(exception)


class DAOCreateFailedError(DAOException):
    """
    DAO Create failed
    """

    message = "Create failed"


class DAOUpdateFailedError(DAOException):
    """
    DAO Update failed
    """

    message = "Updated failed"


class DAODeleteFailedError(DAOException):
    """
    DAO Delete failed
    """

    message = "Delete failed"


class DAOConfigError(DAOException):
    """
    DAO is miss configured
    """

    message = "DAO is not configured correctly missing model definition"
