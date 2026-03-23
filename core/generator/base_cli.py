from typing import Literal
from core.utils import Helper
from core.models.config_models import GeneratorConfig
from core.exceptions import (InputError, RowColumnLengthError)

class BaseCLI:
    @staticmethod
    def format(func):
        def wrapper(**kwargs):
            print("----------")
            func(**kwargs)
            print("----------")
        return wrapper
    
    def prompt_option(self) -> bool:
        while True:
            option = input("y/n: ")
            if option.lower() == "y":
                return True
            elif option.lower() == "n":
                return False
            print("Invalid option inputted! (y = yes, n = no)")
    
    def prompt_index(self, message: str, min_value: int, max_value: int, skip_option: bool = False) -> str | int:
        while True:
            try:
                raw = input(message)
                if raw.strip().lower() == "s" and skip_option:
                    return raw
                if Helper.is_digit_in_range(raw, min_value, max_value):
                    index = int(raw)
                    return index
            except InputError as e:
                print(e)
                
    def prompt_value(self, value_type: Literal["int", "float"], input_message: str) -> int | float:
        converters = {"int": (int,), "float": (int, float)}
        expected_type = " or ".join(v.__name__  for v in converters[value_type])
        while True:
            value = input(input_message)
            for convert in converters[value_type]:
                try:
                    return convert(value)
                except ValueError:
                    pass
            print(f"Invalid value type!, expected value type: {expected_type}")
            
    def prompt_column_row_length(self, column_message: str, row_message: str) -> tuple[int, int]:
        while True:
            try:
                column_length = self.prompt_value("int", column_message)
                GeneratorConfig.validate_column_length(column_length)
                break
            except RowColumnLengthError as e:
                print(e)
        while True:
            try:
                row_length = self.prompt_value("int", row_message)
                GeneratorConfig.validate_row_length(row_length)
                break
            except RowColumnLengthError as e:
                print(e)
        return column_length, row_length