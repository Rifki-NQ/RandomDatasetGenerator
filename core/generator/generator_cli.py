from core.generator.base_cli import BaseCLI
from core.models.enums import RandomTypes
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
            column_length, row_length = self.prompt_column_row_length("Enter column length: ",
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
            option = self.prompt_index("Choose an action (by index): ", 1, 4)
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
            should_run = self.prompt_option()

        except InvalidFileTypeError as e:
            print(e)
            should_run = False

        except FilepathNotRegisteredError as e:
            print(e)
            should_run = False

        return should_run
                
    def _prompt_random_type(self, column_length: int) -> list[RandomTypes]:
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
                type_index = self.prompt_index(message=f"Enter type for column no. {i + 1} (s to skip): ",
                                                min_value=1, max_value=3, skip_option=True)
                if isinstance(type_index, str) and type_index.lower().strip() == "s":
                    type_index = None
                    skip_custom_type = True
            columns_type.append(RandomTypes(type_index))
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