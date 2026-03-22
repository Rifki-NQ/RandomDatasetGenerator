from dataclasses import asdict
from core.generator.base_cli import BaseCLI
from core.models.config_models import RandomConfig

class GeneratorSettingCLI(BaseCLI):
    RANDOM_CONFIG = ["column_row_length", "int_min_max", "float_min_max",
                     "float_round", "string_length", "string_type"]
    
    def __init__(self, logic):
        self.logic = logic
    
    def show_all_filepath(self) -> None:
        print("Current config filepath: data/config.yaml")
        print(f"Current dataset filepath: {self.logic.get_dataset_filepath()}")

    def update_dataset_filepath(self) -> None:
        new_filepath = self._prompt_filepath("Enter new filepath for generated dataset: ")
        self.logic.change_dataset_filepath(new_filepath)
        print("Dataset filepath updated successfully!")

    def show_random_config(self) -> None:
        print("Randomizer configuration: ")
        random_config_data = self.logic.get_random_config()
        for key, value in asdict(random_config_data).items():
            print(f"  {key.replace("_", " ")}: {value}")

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
                string_length = self._prompt_value("int", "Enter string length for random string: ")
                random_config.string_length = string_length
            case 6:
                string_type = self._prompt_string_type("Enter string type for random string: ")
                random_config.string_type = string_type
        self.logic.change_random_config(random_config)

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
        string_length = self._prompt_value("int", "Enter string length for random string: ")
        random_config["string_length"] = string_length
        #input string type
        string_type = self._prompt_string_type("Enter string type for random string: ")
        random_config["string_type"] = string_type
        
        self.logic.change_random_config(RandomConfig(**random_config))