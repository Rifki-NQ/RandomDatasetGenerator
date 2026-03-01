import pandas as pd
from pathlib import Path
from exceptions import MissingConfigKeyError

#warning: slower generation for dataset that generate strings

class GeneratorLogic:
    def __init__(self, generator_setting_logic, csv_file_handler, randomizer):
        self.setting = generator_setting_logic
        self.csv_file_handler = csv_file_handler
        self.rng = randomizer
    
    #register then check if the file is empty
    def check_file_destination(self) -> bool:
        dataset_filepath = self._register_dataset_destination()
        if dataset_filepath is None:
            return False
        if not dataset_filepath.exists():
            return False
        #return true if the file size is not 0 (empty)
        if dataset_filepath.stat().st_size != 0:
            return True
        return False
    
    #register file destination, raise error if something is not expected then return None
    def _register_dataset_destination(self) -> Path | None:
        dataset_filepath = self.setting.get_dataset_filepath()
        self.csv_file_handler.register_filepath(Path(dataset_filepath))
        return Path(dataset_filepath)
    
    def _get_configuration(self) -> dict[str, int | str]:
        return self.setting.read_config()
    
    def _get_config_by_key(self, *keys: str) -> list[int | str]:
        config_data = self._get_configuration()
        values = []
        for key in keys:
            if not isinstance(key, str):
                raise TypeError(f"Error: expected string argument, but got {type(key).__name__} instead")
            if key not in config_data:
                raise MissingConfigKeyError(f"Error: missing ({key}) key from the config!")
            values.append(config_data[key])
        return values
    
    def get_column_row_length(self) -> tuple[int, int]:
        return tuple(self._get_config_by_key("column_length", "row_length"))
        
    def _get_int_min_max(self) -> tuple[int, int]:
        return tuple(self._get_config_by_key("int_min", "int_max"))
    
    def _get_float_min_max(self) -> tuple[int, int]:
        return tuple(self._get_config_by_key("float_min", "float_max"))
    
    def _get_float_round(self) -> int:
        return self._get_config_by_key("float_round")[0]
    
    def _get_string_length(self) -> int:
        return self._get_config_by_key("float_round")[0]
    
    def _get_string_type(self) -> str:
        return self._get_config_by_key("string_type")[0]
        
    def generate_dataset(self, column_length: int, row_length: int) -> None:
        generated_dataset = {}
        column_name = self.rng.get_random_string(column_length, 5, "uppercase")
        for column in range(column_length):
            value = self.rng.get_random_mixed(row_length)
            generated_dataset[column_name[column]] = []
            for row in range(row_length):
                generated_dataset[column_name[column]].append(value[row])
        df_generated_dataset = pd.DataFrame(generated_dataset)
        self.csv_file_handler.save(df_generated_dataset)
        
    def generate_custom_dataset(self, column_names: list) -> None:
        #config data preparation
        column_length, row_length = self.get_column_row_length()
        int_min, int_max = self._get_int_min_max()
        float_min, float_max = self._get_float_min_max()
        float_round = self._get_float_round()
        string_length = self._get_string_length()
        string_type = self._get_string_type()
        
        generated_dataset = {}
        
        #column generation
        for column in range(column_length):
            column_name = column_names[column]
            if column_name == "skip_custom_name":
                column_name = self.rng.get_random_string(1, 5, "mixed")
            pass
            generated_dataset[column_name] = []
            #row generation per column
            for row in range(row_length):
                pass