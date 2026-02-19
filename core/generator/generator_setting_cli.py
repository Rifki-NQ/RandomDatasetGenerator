from core.utils import Helper
from core.exceptions import (InputError)

class BaseCLI:
    @staticmethod
    def cli_decorator(func):
        def wrapper(self):
            print("----------")
            func(self)
            print("----------")
        return wrapper
    
    def _prompt_index(self, message: str, min_value: int, max_value: int) -> int:
        while True:
            try:
                index = input(message)
                if Helper.is_digit_in_range(index, min_value, max_value):
                    return int(index)
            except InputError as e:
                print(e)
                
    def _prompt_value(self, input_message: str, error_message: str | None = "Value must be in digit!") -> int:
        while True:
            value = input(input_message)
            if value.isdigit():
                return int(value)
            else:
                print(error_message)
                
class GeneratorSettingCLI(BaseCLI):
    def __init__(self, logic):
        self.logic = logic
    
    @BaseCLI.cli_decorator
    def show_all_filepath(self) -> None:
        print("Current config filepath: pass")
        print("Current dataset filepath: pass")
    
    @BaseCLI.cli_decorator
    def filepath_setting(self) -> None:
        print("pass")