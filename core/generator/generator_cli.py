from core.utils import Helper
from core.exceptions import (InputError, InvalidFileTypeError, FilepathUndefinedError)
import time

class BaseCLI:
    @staticmethod
    def cli_decorator(func):
        def wrapper(self):
            print("----------")
            try:
                #validate file destination
                if self.logic.check_file_destination():
                    print("File destination already has data inside it, overwrite?")
                    if not self._prompt_option():
                        #cancel operation if user input no overwrite
                        print("Operation cancelled!")
                        print("----------")
                        return
                start = time.perf_counter()
                func(self)
                end = time.perf_counter()
                print(f"Dataset generated successfully in {end - start:.6f} seconds")
            except InvalidFileTypeError as e:
                print(e)
            except FilepathUndefinedError as e:
                print(e, "please check if the file type provided is valid (csv or yaml)")
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
                
    def _prompt_option(self) -> bool:
        while True:
            option = input("y/n: ")
            if option.lower() == "y":
                return True
            elif option.lower() == "n":
                return False
            print("Invalid option inputted! (y = yes, n = no)")
                
class GeneratorCLI(BaseCLI):
    def __init__(self, logic):
        self.logic = logic
    
    @BaseCLI.cli_decorator
    def generate_random_dataset(self) -> None:
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