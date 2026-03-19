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

class FileError(AppError):
    """Raised when there is file related error"""
    pass

class InvalidFileTypeError(FileError):
    """Raisen when the file type is not a valid type"""
    pass

class FileNotFoundAppError(FileError):
    """Raised when the file is not found"""
    pass

class FilepathUndefinedError(FileError):
    """Raised when the file path has not defined"""
    pass

class EmptyDataError(FileError):
    """Raised when the file is empty"""
    pass

class FileNotEmptyError(FileError):
    """Raised when a file is expected to be empty but contains data"""
    pass

class ConfigDataError(FileError):
    """Raised when there is config related error"""
    pass

class MissingConfigKeyError(ConfigDataError):
    """Raised when expected key in config data is missing"""
    pass

class ExtraConfigKeyError(ConfigDataError):
    """Raised when config data contains key that is not excpected"""
    pass

class InvalidConfigTypeError(ConfigDataError):
    """Raised when config data contains value type that is not expected"""
    pass

class RowColumnLengthError(ConfigDataError):
    """Raised when config data contains invalid value for column or row length"""
    pass

class InvalidMinMaxValueError(ConfigDataError):
    """Raised when config data contains max_value that is not greater than min_value"""
    pass

class InvalidFloatRoundError(ConfigDataError):
    """Raised when config data float_round value is not in the allowed range"""
    pass

class InvalidStringTypeError(ConfigDataError):
    """Raised when config data string_type value is invalid"""

class MenuError(AppError):
    """Raised when there is menu related error"""
    pass

class InvalidClassNameError(MenuError):
    """Raised when the class name is not valid"""
    pass

class InvalidMethodNameError(MenuError):
    """Raised when the method name is not valid"""
    pass