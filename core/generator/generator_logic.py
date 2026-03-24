import pandas as pd
import numpy as np
from pathlib import Path
import time
from typing import Generator
from core.models.enums import RandomTypes
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
    
    def get_column_length(self) -> int:
        return self.setting.get_random_config().column_length
    
    def generate_dataset(self, column_length: int, row_length: int) -> Generator[int, None, float]:
        #initiate performance and update tracker
        generation_update = GenerationProgress(total_value=column_length)
        start = time.perf_counter()
        
        column_name = self.rng.get_random_string(StringConfig(size=column_length, string_length=5, string_type="uppercase"))
        
        #dataset generation per column
        generated_dataset = {}
        for column in range(column_length):
            value = self.rng.get_random_mixed(row_length)
            generated_dataset[column_name[column]] = self._normalize_random_value(value=value)
            yield generation_update.send_update(column + 1)
        self.csv_file_handler.save(pd.DataFrame(generated_dataset))
        
        end = time.perf_counter()
        return end - start
        
    def generate_custom_dataset(self, column_names: list[str], random_types: list[RandomTypes]) -> Generator[int, None, float]:
        column_length = self.get_column_length()
        
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
            random_values = self._get_random_by_type(random_types[column])
            generated_dataset[column_names[column]] = self._normalize_random_value(value=random_values)
            yield generation_update.send_update(column + 1)
        self.csv_file_handler.save(pd.DataFrame(generated_dataset))
        
        end = time.perf_counter()
        return end - start
    
    def _file_not_empty(self, dataset_filepath: Path) -> bool:
        if not dataset_filepath.exists():
            return False
        #return true if the file size is not 0 (empty)
        return dataset_filepath.stat().st_size != 0
    
    def _register_dataset_destination(self) -> Path:
        dataset_filepath = self.setting.get_dataset_filepath()
        self.csv_file_handler.register_filepath(Path(dataset_filepath))
        return Path(dataset_filepath)
        
    def _get_random_by_type(self, random_type: RandomTypes) -> int | float | str | np.ndarray | list[str]:
        config = self.setting.get_random_config()
        match random_type:
            case RandomTypes.INT:
                return self.rng.get_random_int(config.int_config())
            case RandomTypes.FLOAT:
                return self.rng.get_random_float(config.float_config())
            case RandomTypes.STRING:
                return self.rng.get_random_string(config.string_config())
            case _:
                raise ValueError("Error: invalid random type provided!")
        
    #convert RandomTypes.None into valid RandomTypes option (INT, FLOAT, STRING)
    def _validate_random_type(self, random_types: list[RandomTypes]) -> list[RandomTypes]:
        new_random_type = []
        for random_type in random_types:
            if random_type == RandomTypes.RANDOM:
                new_random_type.append(RandomTypes(self.rng.get_random_int(IntConfig(size=1, int_min=1, int_max=4))))
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