from core.utils import Helper
from core.exceptions import (InputError, InvalidFileTypeError, FilepathUndefinedError,
                             ConfigDataError)
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
            
    def _prompt_row_column_length(self) -> tuple[int, int]:
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
        return column_length, row_length
    
    def _prompt_column_name(self, column_length: int) -> list[str]:
        print("Enter s to skip custom name for the rest of columns left")
        skip_custom_name = False
        columns_name = []
        for i in range(column_length):
            if not skip_custom_name:
                new_name = input(f"Enter name for column no. {i} (s to skip): ")
            if new_name.strip().lower() == "s":
                new_name = "skip_custom_name"
                skip_custom_name = True
            columns_name.append(new_name)
        return columns_name
                
class GeneratorCLI(BaseCLI):
    def __init__(self, generator_logic, setting_cli):
        self.logic = generator_logic
        self.setting = setting_cli
    
    @BaseCLI.cli_decorator
    def generate_random_dataset(self) -> None:
        column_length, row_length = self._prompt_row_column_length()
        self.logic.generate_dataset(column_length, row_length)
        
    @BaseCLI.cli_decorator
    def generate_custom_random_dataset(self) -> None:
        self.setting.show_random_config()
        print("")
        self.setting.show_all_filepath()
        print("----------")
        print("1. Generate random dataset with current configuration\n"
              "2. Change configuration")
        option = self._prompt_index("Choose an action (by index): ", 1, 2)
        if option == 1:
            try:
                column_length = self.logic.get_column_row_length()[0]
                column_names = self._prompt_column_name(column_length)
                self.logic.generate_custom_dataset(column_names)
            except ConfigDataError as e:
                print(e)
                return
        elif option == 2:
            pass