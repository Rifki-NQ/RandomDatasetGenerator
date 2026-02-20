from pathlib import Path
from core.utils import Helper
from core.exceptions import InputError

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
            
class GeneratorSettingCLI(BaseCLI):
    def __init__(self, logic):
        self.logic = logic
    
    @BaseCLI.cli_decorator
    def show_all_filepath(self) -> None:
        print("Current config filepath: data/config.yaml")
        print(f"Current dataset filepath: {self.logic.get_dataset_filepath()}")
    
    @BaseCLI.cli_decorator
    def update_dataset_filepath(self) -> None:
        new_filepath = self._prompt_filepath("Enter new filepath for generated dataset: ")
        self.logic.change_dataset_filepath(new_filepath)
        print("Dataset filepath updated successfully!")