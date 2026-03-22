from typing import get_args
from typing import Literal
from core.utils import Helper
from core.models.config_models import GeneratorConfig, STRING_TYPES
from core.exceptions import (InputError, InvalidFilepathError, RowColumnLengthError,
                             InvalidMinMaxValueError, InvalidFloatRoundError, InvalidStringTypeError)

class BaseCLI:
    @staticmethod
    def format(func):
        def wrapper(**kwargs):
            print("----------")
            func(**kwargs)
            print("----------")
        return wrapper
    
    #------------------- SHARED USE -------------------
    
    def _prompt_option(self) -> bool:
        while True:
            option = input("y/n: ")
            if option.lower() == "y":
                return True
            elif option.lower() == "n":
                return False
            print("Invalid option inputted! (y = yes, n = no)")
    
    def _prompt_index(self, message: str, min_value: int, max_value: int, skip_option: bool = False) -> str | int:
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
                
    def _prompt_value(self, value_type: Literal["int", "float"], input_message: str) -> int | float:
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
    
    #------------------- SETTING CLI USE -------------------
    
    def _prompt_filepath(self, message: str) -> str:
        while True:
            try:
                new_filepath = input(message).strip().replace(" ", "_")
                GeneratorConfig.validate_filepath(new_filepath)
                return new_filepath
            except InvalidFilepathError as e:
                print(e)
    
    def _prompt_column_row_length(self, column_message: str, row_message: str) -> tuple[int, int]:
        while True:
            try:
                column_length = self._prompt_value("int", column_message)
                GeneratorConfig.validate_column_length(column_length)
                break
            except RowColumnLengthError as e:
                print(e)
        while True:
            try:
                row_length = self._prompt_value("int", row_message)
                GeneratorConfig.validate_row_length(row_length)
                break
            except RowColumnLengthError as e:
                print(e)
        return column_length, row_length
                    
    def _prompt_random_min_max(self, value_type: str, min_message: str, max_message: str) -> tuple[int, int]:
        min_value = self._prompt_value(value_type, min_message)
        while True:
            try:
                max_value = self._prompt_value(value_type, max_message)
                GeneratorConfig.validate_min_max(value_type, min_value, max_value)
                break
            except InvalidMinMaxValueError as e:
                print(e)
        return min_value, max_value
    
    def _prompt_round_value(self, message: str) -> int:
        while True:
            try:
                round_value = self._prompt_value("int", message)
                GeneratorConfig.validate_float_round(round_value)
                return round_value
            except InvalidFloatRoundError as e:
                print(e)

    #------------------- GENERATOR CLI USE -------------------

    def  _prompt_string_type(self, message: str) -> str:
        string_types = get_args(STRING_TYPES)
        for index, string_type in enumerate(string_types, 1):
            print(f"{index}. {string_type}")
        while True:
            try:
                index = self._prompt_index(message=message, min_value=1, max_value=3)
                chosen_type = string_types[index-1]
                GeneratorConfig.validate_string_type(chosen_type)
                return chosen_type
            except InvalidStringTypeError as e:
                print(e)
                
    def _prompt_random_type(self, column_length: int) -> list[int]:
        print("Choose random type (by index):\n"
              "1. int\n"
              "2. float\n"
              "3. string")
        print("or type s to use random type for the rest of the columns left\n"
              "----------")
        skip_custom_type = False
        columns_type = []
        for i in range(column_length):
            if skip_custom_type:
                type_index = None
            else:
                type_index = self._prompt_index(message=f"Enter type for column no. {i + 1} (s to skip): ",
                                                min_value=1, max_value=3, skip_option=True)
                if isinstance(type_index, str) and type_index.lower().strip() == "s":
                    type_index = None
                    skip_custom_type = True
            columns_type.append(type_index)
        return columns_type
    
    def _prompt_column_name(self, column_length: int) -> list[str | None]:
        print("Enter s to skip custom name for the rest of the columns left")
        skip_custom_name = False
        columns_name = []
        for i in range(column_length):
            if skip_custom_name:
                new_name = None
            else:
                while True:
                    new_name = input(f"Enter name for column no. {i + 1} (s to skip): ").strip()
                    if new_name.lower() == "s":
                        new_name = None
                        skip_custom_name = True
                    elif not new_name:
                        print("Column name cannot be empty")
                        continue
                    elif new_name.lower() in (col.lower() for col in columns_name):
                        print(f"Column name '{new_name}' already exists. Please choose a different name")
                        continue
                    break
            columns_name.append(new_name)
        return columns_name