import pandas as pd
import numpy as np
from pathlib import Path
from core.config_models import IntConfig, FloatConfig, StringConfig
from core.exceptions import MissingConfigKeyError

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
    
    def _get_config_by_key(self, *keys: str) -> list[int | str]:
        config_data = self.setting.read_config()
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
        return self._get_config_by_key("string_length")[0]
    
    def _get_string_type(self) -> str:
        return self._get_config_by_key("string_type")[0]
        
    def _get_random_int(self, config: IntConfig) -> int | np.ndarray:
        return self.rng.get_random_int(config)
    
    def _get_random_float(self, config: FloatConfig) -> float | np.ndarray:
        return self.rng.get_random_float(config)
    
    def _get_random_string(self, config: StringConfig) -> str | list[str]:
        return self.rng.get_random_string(config)
        
    def _get_random_by_index(self, random_index: int, **kwargs) -> int | float | str | np.ndarray | list[str]:
        #1 = int, 2 = float, 3 = string
        if random_index == 1:
            config = IntConfig(**kwargs)
            return self._get_random_int(config)
        elif random_index == 2:
            config = FloatConfig(**kwargs)
            return self._get_random_float(config)
        elif random_index == 3:
            config = StringConfig(**kwargs)
            return self._get_random_string(config)
        else:
            raise ValueError("Error: invalid random index provided!")
        
    #validate random types, return new random types index if random_type not in 1, 2, 3
    def _validate_random_type(self, random_types: list[int]) -> list[int]:
        new_random_type = []
        for random_type in random_types:
            if random_type not in (1, 2, 3):
                new_random_type.append(self.rng.get_random_int(IntConfig(size=1, int_min=1, int_max=4)))
            else:
                new_random_type.append(random_type)
        return new_random_type
    
    #validate column name, return new random column name if column name = "skip_custom_name"
    def _validate_column_name(self, column_names: list[str]) -> list[str]:
        column_name_config = StringConfig(size=1, string_length=10, string_type="uppercase")
        new_column_names = []
        for name in column_names:
            if name == "skip_custom_name":
                new_column_names.append(self.rng.get_random_string(column_name_config))
            else:
                new_column_names.append(name)
        return new_column_names
        
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
        
    def generate_custom_dataset(self, column_names: list[str], random_types: list[int]) -> None:
        #config data preparation
        column_length, row_length = self.get_column_row_length()
        int_min, int_max = self._get_int_min_max()
        float_min, float_max = self._get_float_min_max()
        float_round = self._get_float_round()
        string_length = self._get_string_length()
        string_type = self._get_string_type()
        
        #cli data validation
        random_types = self._validate_random_type(random_types=random_types)
        column_names = self._validate_column_name(column_names=column_names)
        
        #check if column names and random types length match
        if len(column_names) != len(random_types):
            raise ValueError("Error: column names and random types length mismatch!")
        
        #column generation
        generated_dataset = {}
        for column in range(column_length):
            match random_types[column]:
                case 1:
                    random_config = dict(size=row_length, int_min=int_min, int_max=int_max)
                case 2:
                    random_config = dict(size=row_length, float_min=float_min,
                                         float_max=float_max, float_round=float_round)
                case 3:
                    random_config = dict(size=row_length, string_length=string_length, string_type=string_type)
            #generate random values in bulk
            random_values = self._get_random_by_index(random_index=random_types[column], **random_config)
            generated_dataset[column_names[column]] = list(random_values)
        self.csv_file_handler.save(pd.DataFrame(generated_dataset))