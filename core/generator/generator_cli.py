from core.utils import Helper
from core.exceptions import (InputError)
import time

class BaseCLI:
    @staticmethod
    def cli_decorator(func):
        def wrapper(self):
            print("----------")
            start = time.perf_counter()
            func(self)
            end = time.perf_counter()
            print(f"Dataset generated successfully in {end - start:.6f} seconds")
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
                
class GeneratorCLI(BaseCLI):
    def __init__(self, logic):
        self.logic = logic
    
    @BaseCLI.cli_decorator
    def generate_random_dataset(self):
        while True:
            column_length = self._prompt_value("Enter column length: ", "Column length must be in digit!")
            if column_length > 0:
                break
            print("Column length cannot be less than 1!")
        while True:
            row_length = self._prompt_value("Enter row length: ", "Row length must be in digit!")
            if row_length > 0:
                break
            print("Row length cannot be less than 1!")
        self.logic.generate_dataset(column_length, row_length)