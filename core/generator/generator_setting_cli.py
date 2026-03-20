from typing import get_args
from dataclasses import asdict
from core.utils import Helper
from core.models.config_models import GeneratorConfig, RandomConfig, STRING_TYPES
from core.exceptions import (InputError, InvalidFilepathError, RowColumnLengthError,
                             InvalidMinMaxValueError, InvalidFloatRoundError, InvalidStringTypeError,
                             InvalidConfigTypeError)

class _BaseCLI:
    @staticmethod
    def _cli_decorator(func):
        def wrapper(self):
            if self.use_decorator:
                print("----------")
            func(self)
            if self.use_decorator:
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
                
    def _prompt_filepath(self, message: str) -> str:
        while True:
            try:
                new_filepath = input(message)
                GeneratorConfig.validate_type(dataset_filepath=new_filepath)
                GeneratorConfig.validate_filepath(new_filepath)
                return new_filepath
            except (InvalidConfigTypeError, InvalidFilepathError) as e:
                print(e)
    
    def _prompt_column_row_length(self, column_message: str, row_message: str) -> tuple[int, int]:
        while True:
            try:
                column_length = input(column_message)
                row_length = input(row_message)
                GeneratorConfig.validate_type(column_length=column_length, row_length=row_length)
                GeneratorConfig.validate_row_column_length(column_length, row_length)
                return column_length, row_length
            #fix when error invalid type = row_length, printed invalid type = column_length
            except (InvalidConfigTypeError,RowColumnLengthError) as e:
                print(e)
        
    def _prompt_random_min_max(self, value_type: str, min_message: str, max_message: str) -> tuple[int, int]:
        while True:
            try:
                min_value = self._prompt_value(min_message)
                max_value = self._prompt_value(max_message)
                GeneratorConfig.validate_min_max(value_type, min_value, max_value)
                return min_value, max_value
            except InvalidMinMaxValueError as e:
                print(e)
    
    def _prompt_round_value(self, message: str) -> int:
        while True:
            try:
                round_value = self._prompt_value(message)
                GeneratorConfig.validate_float_round(round_value)
                return round_value
            except InvalidFloatRoundError as e:
                print(e)

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
            
class GeneratorSettingCLI(_BaseCLI):
    RANDOM_CONFIG = ["column_row_length", "int_min_max", "float_min_max",
                     "float_round", "string_length", "string_type"]
    
    def __init__(self, logic, use_decorator: bool = True):
        self.logic = logic
        self.use_decorator = use_decorator
    
    @_BaseCLI._cli_decorator
    def show_all_filepath(self) -> None:
        print("Current config filepath: data/config.yaml")
        print(f"Current dataset filepath: {self.logic.get_dataset_filepath()}")
    
    @_BaseCLI._cli_decorator
    def update_dataset_filepath(self) -> None:
        new_filepath = self._prompt_filepath("Enter new filepath for generated dataset: ")
        self.logic.change_dataset_filepath(new_filepath)
        print("Dataset filepath updated successfully!")
        
    @_BaseCLI._cli_decorator
    def show_random_config(self) -> None:
        print("Randomizer configuration: ")
        random_config_data = self.logic.get_random_config()
        for key, value in asdict(random_config_data).items():
            print(f"  {key.replace("_", " ")}: {value}")
        
    @_BaseCLI._cli_decorator
    def change_random_config(self) -> None:
        random_config = self.logic.get_random_config()
        counter = 1
        for key, value in asdict(random_config).items():
            if key in ("row_length", "int_max", "float_max"):
                print(f"   {key.replace("_", " ")}: {value}")
            else:
                print(f"{counter}. {key.replace("_", " ")}: {value}")
                counter+=1
        index = self._prompt_index("\nSelect which config to change: ", 1, (len(asdict(random_config)) - 3))
        match index:
            case 1:
                column_length, row_length = self._prompt_column_row_length("Enter column length: ",
                                                                           "Enter row length: ")
                random_config.column_length = column_length
                random_config.row_length = row_length
            case 2:
                int_min, int_max = self._prompt_random_min_max("int" ,"Enter min value for random int: ",
                                                                "Enter max value for random int: ")
                random_config.int_min = int_min
                random_config.int_max = int_max
            case 3:
                float_min, float_max = self._prompt_random_min_max("float", "Enter min value for random float: ",
                                                                   "Enter max value random float: ")
                random_config.float_min = float_min
                random_config.float_max = float_max
            case 4:
                float_round = self._prompt_round_value("Enter round value for random float: ")
                random_config.float_round = float_round
            case 5:
                string_length = self._prompt_value("Enter string length for random string: ")
                random_config.string_length = string_length
            case 6:
                string_type = self._prompt_string_type("Enter string type for random string: ")
                random_config.string_type = string_type
        self.logic.change_random_config(random_config)
        
    @_BaseCLI._cli_decorator
    def update_random_configs(self) -> None:
        random_config = {}
        #input column and row length
        column_length, row_length = self._prompt_column_row_length("Enter column length: ",
                                                                   "Enter row length: ")
        random_config["column_length"] = column_length
        random_config["row_length"] = row_length
        #input int min and max
        int_min, int_max = self._prompt_random_min_max("int", "Enter min value for random int: ",
                                                       "Enter max value for random int: ")
        random_config["int_min"] = int_min
        random_config["int_max"] = int_max
        #input float min and max
        float_min, float_max = self._prompt_random_min_max("float", "Enter min value for random float: ",
                                                           "Enter max value random float: ")
        random_config["float_min"] = float_min
        random_config["float_max"] = float_max
        #input float round
        float_round = self._prompt_round_value("Enter round value for random float: ")
        random_config["float_round"] = float_round
        #input string length
        string_length = self._prompt_value("Enter string length for random string: ")
        random_config["string_length"] = string_length
        #input string type
        string_type = self._prompt_string_type("Enter string type for random string: ")
        random_config["string_type"] = string_type
        
        self.logic.change_random_config(RandomConfig(**random_config))