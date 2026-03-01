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

class ConfigDataError(FileError):
    """Raised when there is config related error"""
    pass

class FilepathNotFoundError(ConfigDataError):
    """Raised when a filepath is missing in the config data"""
    pass

class MissingConfigKeyError(ConfigDataError):
    """Raised when expected key in config data is missing"""
    pass

class MenuError(AppError):
    """Raised when there is menu related error"""
    pass

class InvalidClassNameError(MenuError):
    """Raised when the class name is not valid"""
    pass

class InvalidMethodNameError(MenuError):
    """Raised when the method name is not valid"""
    pass