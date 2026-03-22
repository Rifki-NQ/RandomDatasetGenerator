from core.generator.base_cli import BaseCLI
from core.exceptions import (InvalidFileTypeError, FilepathNotRegisteredError, ConfigDataError,
                             FileNotEmptyError)
                
class GeneratorCLI(BaseCLI):
    def __init__(self, generator_logic, setting_cli):
        self.logic = generator_logic
        self.setting = setting_cli

    def generate_random_dataset(self, **kwargs) -> None:
        if not self._validate_file_is_empty():
            return
        
        if not kwargs:
            column_length, row_length = self._prompt_column_row_length("Enter column length: ",
                                                                       "Enter row length: ")
        else:
            column_length = kwargs.get("column_length")
            row_length = kwargs.get("row_length")
        gen = self.logic.generate_dataset(column_length, row_length)
        try:
            while True:
                progress = next(gen)
                print(f"Progress: {progress}%", flush=True, end="\r")
        except StopIteration as e:
            runtime = e.value
        print(f"Dataset generated successfully in {runtime:.2f}s!")

    def generate_custom_random_dataset(self) -> None:
        if not self._validate_file_is_empty():
            return
        
        self.setting.show_random_config()
        print("----------")
        self.setting.show_all_filepath()
        while True:
            print("----------")
            print("1. Generate random dataset\n"
                  "2. Change random configuration\n"
                  "3. Change dataset filepath\n"
                  "4. Quit")
            option = self._prompt_index("Choose an action (by index): ", 1, 4)
            print("----------")
            match option:
                case 1:
                    try:
                        column_length = self.logic.get_column_length()
                        column_names = self._prompt_column_name(column_length)
                        random_types = self._prompt_random_type(column_length)
                        
                        gen = self.logic.generate_custom_dataset(column_names, random_types)
                        print("Generating!\n",
                              "----------")
                        try:
                            while True:
                                progress = next(gen)
                                print(f"Progress: {progress}%", flush=True, end="\r")
                        except StopIteration as e:
                            runtime = e.value
                        print(f"Dataset generated sucessfully in {runtime:.2f}s!")
                        
                    except ConfigDataError as e:
                        print(e)
                        return
                case 2:
                    self.setting.change_random_config()
                case 3:
                    self.setting.update_dataset_filepath()
                case 4:
                    break
                
    def _validate_file_is_empty(self) -> bool:
        try:
            #initiate filepath registration then validate it
            self.logic.initiate_filepath_registration()
            should_run = True

        except FileNotEmptyError:
            print("File destination already has data inside it, overwrite?")
            should_run = self._prompt_option()

        except InvalidFileTypeError as e:
            print(e)
            should_run = False

        except FilepathNotRegisteredError as e:
            print(e)
            should_run = False

        return should_run