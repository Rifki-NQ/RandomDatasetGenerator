class AppError(Exception):
    """Raised when there is app related error"""
    pass

class InputError(AppError):
    """Raised when there is input related error"""
    pass

class ValueNotDigitError(InputError):
    """Raised when the value is not a digit"""
    pass

class OutOfBoundValueError(InputError):
    """Raised when the value is out of the allowed range"""
    pass