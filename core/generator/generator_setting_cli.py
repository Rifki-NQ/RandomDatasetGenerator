from pathlib import Path
from core.utils import Helper
from core.exceptions import InputError

class BaseCLI:
    @staticmethod
    def cli_decorator(func):
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
            new_filepath = input(message)
            new_filepath_folder = str(Path(new_filepath).parent)
            new_filepath_file = Path(new_filepath).suffix
            if new_filepath_folder != "data":
                print("dataset file must be in designated folder (example: data/file.csv)")
                continue
            if new_filepath_file != ".csv":
                print("dataset file must be a csv file (example: data/file.csv)")
                continue
            return new_filepath
        
    def _prompt_column_row_length(self, column_message: str, row_message: str) -> tuple[int, int]:
        while True:
            column_length = self._prompt_value(column_message)
            if column_length > 0:
                break
            print("Column length cannot be less than 1!")
        while True:
            row_length = self._prompt_value(row_message)
            if row_length > 0:
                break
            print("Row length cannot be less than 1!")
        return column_length, row_length
        
    def _prompt_random_min_max(self, min_message: str, max_message: str) -> tuple[int, int]:
        while True:
            min_value = input(min_message)
            if min_value.isdigit():
                min_value = int(min_value)
            else:
                print("Value must be in digit!")
                continue
            if min_value < 0:
                print("Min value cannot be less than zero!")
                continue
            break
        while True:
            max_value = input(max_message)
            if max_value.isdigit():
                max_value = int(max_value)
            else:
                print("Value must be in digit!")
                continue
            if max_value <= min_value:
                print("Max value must be greater than min value!")
                continue
            break
        return min_value, max_value
    
    def _prompt_round_value(self, message: str) -> int:
        while True:
            round_value = input(message)
            if round_value.isdigit():
                round_value = int(round_value)
            else:
                print("Value must be in digit!")
                continue
            if not 1 <= round_value <= 8:
                print("Allowed round value range is 1 to 8!")
                continue
            return round_value

    def  _prompt_string_type(self, message: str) -> str:
        string_type = ["uppercase", "lowercase", "mixed"]
        for i, s_type in enumerate(string_type, 1):
            print(f"{i}. {s_type}")
        while True:
            choosen_type = input(message)
            if choosen_type.isdigit():
                choosen_type = int(choosen_type)
            else:
                print("Value must be in digit!")
                continue
            if not 1 <= choosen_type <= 3:
                print("Invalid index choice! (1 to 3)")
                continue
            return string_type[choosen_type - 1]
            
class GeneratorSettingCLI(BaseCLI):
    def __init__(self, logic, use_decorator: bool = True):
        self.logic = logic
        self.use_decorator = use_decorator
        self.random_config = ["column_row_length", "int_min_max", "float_min_max",
                              "float_round", "string_length", "string_type"]
    
    @BaseCLI.cli_decorator
    def show_all_filepath(self) -> None:
        print("Current config filepath: data/config.yaml")
        print(f"Current dataset filepath: {self.logic.get_dataset_filepath()}")
    
    @BaseCLI.cli_decorator
    def update_dataset_filepath(self) -> None:
        new_filepath = self._prompt_filepath("Enter new filepath for generated dataset: ")
        self.logic.change_dataset_filepath(new_filepath)
        print("Dataset filepath updated successfully!")
        
    @BaseCLI.cli_decorator
    def show_random_config(self) -> None:
        print("Randomizer configuration: ")
        random_config_data = self.logic.get_random_config()
        for key, value in random_config_data.items():
            print(f"  {key.replace("_", " ")}: {value}")
        
    @BaseCLI.cli_decorator
    def update_random_config(self) -> None:
        random_configs = []
        for config in self.random_config:
            if config == "column_row_length":
                random_configs.extend(self._prompt_column_row_length("Enter column length: ",
                                                                         "Enter row length: "))
            elif config == "int_min_max":
                random_configs.extend(self._prompt_random_min_max("Enter min value for random int: ",
                                                                  "Enter max value for random int: "))
            elif config == "float_min_max":
                random_configs.extend(self._prompt_random_min_max("Enter min value for random float: ",
                                                                  "Enter max value random float: "))
            elif config == "float_round":
                random_configs.append(self._prompt_round_value("Enter round value for random float: "))
            elif config == "string_length":
                random_configs.append(self._prompt_value("Enter string length for random string: "))
            elif config == "string_type":
                random_configs.append(self._prompt_string_type("Enter string type for random string: "))
        self.logic.change_random_config(random_configs)