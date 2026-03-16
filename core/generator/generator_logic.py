import pandas as pd
import numpy as np
from pathlib import Path
import time
from typing import Generator
from core.models.progress_models import GenerationProgress
from core.models.config_models import IntConfig, FloatConfig, StringConfig
from core.exceptions import FileNotEmptyError

#warning: slower generation for dataset that generate strings

class GeneratorLogic:
    def __init__(self, generator_setting_logic, csv_file_handler, randomizer):
        self.setting = generator_setting_logic
        self.csv_file_handler = csv_file_handler
        self.rng = randomizer
    
    def initiate_filepath_registration(self) -> None:
        dataset_filepath = self._register_dataset_destination()
        if self._file_not_empty(dataset_filepath=dataset_filepath):
            raise FileNotEmptyError()
    
    def _file_not_empty(self, dataset_filepath: Path) -> bool:
        if not dataset_filepath.exists():
            return False
        #return true if the file size is not 0 (empty)
        return dataset_filepath.stat().st_size != 0
    
    def _register_dataset_destination(self) -> Path:
        dataset_filepath = self.setting.get_dataset_filepath()
        self.csv_file_handler.register_filepath(Path(dataset_filepath))
        return Path(dataset_filepath)
        
    def get_column_length(self) -> int:
        return self.setting.get_random_config()["column_length"]
        
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
        
    #validate random types, fill random type with number 1 to 3 if random type is None
    def _validate_random_type(self, random_types: list[int | None]) -> list[int]:
        new_random_type = []
        for random_type in random_types:
            if random_type is None:
                new_random_type.append(self.rng.get_random_int(IntConfig(size=1, int_min=1, int_max=4)))
            else:
                new_random_type.append(random_type)
        return new_random_type
    
    #validate column name, return new random column name if column name is None
    def _validate_column_name(self, column_names: list[str | None]) -> list[str]:
        column_name_config = StringConfig(size=1, string_length=10, string_type="uppercase")
        new_column_names = []
        for name in column_names:
            if name is None:
                new_column_names.append(self.rng.get_random_string(column_name_config))
            else:
                new_column_names.append(name)
        return new_column_names
        
    #convert any scalar value into list, return original if not scalar
    def _normalize_random_value(self, value: np.ndarray | list | int | float | str) -> np.ndarray | list:
        if isinstance(value, (int, float, str)):
            return [value]
        return value
        
    def generate_dataset(self, column_length: int, row_length: int) -> Generator[int, None, float]:
        #initiate performance and update tracker
        generation_update = GenerationProgress(total_value=column_length)
        start = time.perf_counter()
        
        generated_dataset = {}
        column_name = self.rng.get_random_string(StringConfig(size=column_length,
                                                              string_length=5,
                                                              string_type="uppercase"))
        #dataset generation per column
        for column in range(column_length):
            value = self.rng.get_random_mixed(row_length)
            generated_dataset[column_name[column]] = self._normalize_random_value(value=value)
            yield generation_update.send_update(column + 1)
        self.csv_file_handler.save(pd.DataFrame(generated_dataset))
        
        end = time.perf_counter()
        return end - start
        
    def generate_custom_dataset(self, column_names: list[str], random_types: list[int]) -> Generator[int, None, float]:
        #random config data preparation
        random_config = self.setting.get_random_config()
        
        column_length, row_length = random_config["column_length"], random_config["row_length"]
        int_min, int_max = random_config["int_min"], random_config["int_max"]
        float_min, float_max = random_config["float_min"], random_config["float_max"]
        float_round = random_config["float_round"]
        string_length = random_config["string_length"]
        string_type = random_config["string_type"]
        
        #cli data validation
        random_types = self._validate_random_type(random_types=random_types)
        column_names = self._validate_column_name(column_names=column_names)
        
        #check if column names and random types length match
        if len(column_names) != len(random_types):
            raise ValueError("Error: column names and random types length mismatch!")
        
        #initiate performance and update tracker
        generation_update = GenerationProgress(total_value=column_length)
        start = time.perf_counter()
        
        #dataset generation per column
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
            generated_dataset[column_names[column]] = self._normalize_random_value(value=random_values)
            yield generation_update.send_update(column + 1)
        self.csv_file_handler.save(pd.DataFrame(generated_dataset))
        
        end = time.perf_counter()
        return end - start