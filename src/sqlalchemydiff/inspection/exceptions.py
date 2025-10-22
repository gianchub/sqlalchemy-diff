class SqlalchemydiffException(Exception):
    """Base exception for all sqlalchemydiff exceptions."""


class InspectorNotSupported(SqlalchemydiffException):
    """Exception raised when an inspector is not supported by the version of sqlalchemy."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class UnknownInspector(SqlalchemydiffException, ValueError):
    """Exception raised when an unknown inspector is provided."""
