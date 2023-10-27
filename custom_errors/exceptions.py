class OnbordingDataError(Exception):
    """Error Handler Class for Landvoice Data Exception Handling."""


class UserNotFound(OnbordingDataError):
    """User record not found."""

class PasswordMismatch(OnbordingDataError):
    """Password does not match."""

class EmailExist(OnbordingDataError):
    """existing email."""

class UsernameExist(OnbordingDataError):
    """existing username."""

class StudentNotAdded(OnbordingDataError):
    """This student was not added."""
