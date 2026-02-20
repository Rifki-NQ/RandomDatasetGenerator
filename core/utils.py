import pandas as pd
import numpy as np
import yaml
import string
from typing import Any, Literal
from pathlib import Path
from abc import ABC, abstractmethod
from core.exceptions import (ValueNotDigitError, OutOfBoundValueError, FilepathUndefinedError,
                             FileNotFoundAppError, InvalidFileTypeError, EmptyDataError)
strformats = Literal["uppercase", "lowercase", "mixed"]

class Helper:
    @staticmethod
    def is_digit_in_range(value: str, min_value: int, max_value: int) -> bool:
        if value.isdigit():
            value = int(value)
            if min_value <= value <= max_value:
                return True
            raise OutOfBoundValueError("Error: Inputted value is out of range!")
        raise ValueNotDigitError("Error: Inputted value must be in digit!")
    
    @staticmethod
    def get_dict_depth(dict_data: dict[Any, Any]) -> int:
        depth = 1
        max_child_depth = 0
        for value in dict_data.values():
            if isinstance(value, dict):
                child_depth = Helper.get_dict_depth(value)
                max_child_depth = max(max_child_depth, child_depth)
        return depth + max_child_depth
    
class DataIO(ABC):
    def __init__(self):
        self.file_path: Path | None = None
    
    @abstractmethod
    def read(self, **kwargs):
        pass
    
    @abstractmethod
    def save(self, data):
        pass
    
    @abstractmethod
    def register_filepath(self, file_path: Path):
        pass
    
    @staticmethod
    def create_dataio(file_type: Literal["csv", "yaml"]) -> DataIO:
        valid_file_types = {"csv", "yaml"}
        if not file_type in valid_file_types:
            raise InvalidFileTypeError("Error: invalid file type provided!")
        if file_type == "csv":
            return CSVFileHandler()
        elif file_type == "yaml":
            return YAMLFileHandler()
        
    def _check_file_path(self) -> None:
        if self.file_path is None:
            raise FilepathUndefinedError("Error: filepath has not registered yet!")
    
class CSVFileHandler(DataIO):
    def __init__(self):
        super().__init__()
    
    #return true if the file exist
    def register_filepath(self, file_path: Path) -> bool:
        if file_path.suffix.lstrip(".") != "csv":
            raise InvalidFileTypeError("Error: invalid file type provided!")
        self.file_path = file_path
        return file_path.exists()
    
    def read(self, **kwargs) -> pd.DataFrame:
        self._check_file_path()
        display_all = kwargs.get("display_all", False)
        try:
            if display_all:
                pd.set_option("display.max_rows", None)
            df = pd.read_csv(self.file_path)
            return df
        except pd.errors.EmptyDataError:
            raise EmptyDataError(f"Error: failed to read ({self.file_path}) because the file is empty!")
        except FileNotFoundError:
            raise FileNotFoundAppError(f"Error: failed to read ({self.file_path}) because the file does not exist!")
         
    def save(self, data):
        self._check_file_path()
        data.to_csv(self.file_path, index=False)
         
class YAMLFileHandler(DataIO):
    def __init__(self):
        super().__init__()
    
    #return true if the file exist
    def register_filepath(self, file_path: Path) -> bool:
        if file_path.suffix.lstrip(".") != "yaml":
            raise InvalidFileTypeError("Error: invalid file type provided!")
        self.file_path = file_path
        return file_path.exists()

    def _format_yaml(self, data) -> str:
        formatted_yaml = yaml.dump(
            data,
            sort_keys=False,
            default_flow_style=False
        )
        return formatted_yaml
    
    def read(self, **kwargs) -> dict[str, Any]:
        self._check_file_path()
        format_data = kwargs.get("format_data", False)
        try:
            with open(self.file_path, "r") as file:
                data = yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundAppError(f"Error: failed to read ({self.file_path}) because the file does not exist!")
        #return error if any data is empty
        if data is None:
            raise EmptyDataError(f"Error: failed to read ({self.file_path}) because the file is empty!")
        if format_data:
            data = self._format_yaml(data)
        return data
        
    def save(self, data):
        self._check_file_path()
        with open(self.file_path, "w+") as file:
            yaml.safe_dump(data, file, sort_keys=False)
            
class Randomizer:
    def __init__(self):
        self.SEED = 42
        self.rng = np.random.default_rng()
        
    def get_random_int(self,
                       size: int = 1,
                       min_value: int = 1,
                       max_value: int = 2
                       ) -> np.ndarray | int:
        value = self.rng.integers(min_value, max_value, size)
        if size == 1:
            value = value[0]
        return value
    
    def get_random_float(self,
                         size: int = 1,
                         min_value: int = 1,
                         max_value: int = 2,
                         round_size: int | None = None
                         ) -> np.ndarray | float:
        value = self.rng.uniform(min_value, max_value, size)
        if round_size is not None:
            value = np.round(value, round_size)
        if size == 1:
            value = value[0]
        return value
    
    def _get_random_letters(self, strformat: strformats | None) -> str:
        if strformat is None:
            strformat = "mixed"
        if strformat == "lowercase":
            return string.ascii_lowercase
        elif strformat == "uppercase":
            return string.ascii_uppercase
        elif strformat == "mixed":
            return string.ascii_letters
    
    def get_random_string(self,
                          size: int = 1,
                          str_length: int = 1,
                          strformat: strformats | None = None
                          ) -> list[str] | str:
        letters = np.array(list(self._get_random_letters(strformat)))
        random_str = self.rng.choice(letters, size=(size, str_length))
        value = ["".join(row) for row in random_str]
        if size == 1:
            value = value[0]
        return value
    
    #generation is theoretically slower since it has to produce many random values
    def get_random_mixed(self, size: int = 1) -> list[Any] | Any:
        value = []
        rng_choice_range = self.rng.choice([2, 3, 4, 5, 6, 7, 8, 9, 10])
        rng_choice_round_range = self.rng.choice([2, 3, 4, 5])
        random_choices = [lambda: self.get_random_int(1, 1, rng_choice_range).item(),
                         lambda: self.get_random_float(1, 1, rng_choice_range, rng_choice_round_range).item(),
                         lambda: self.get_random_string(1, rng_choice_range, "mixed")]
        for i in range(size):
            choosen_type = self.rng.choice(random_choices)
            value.append(choosen_type())
        if size == 1:
            value = value[0]
        return value
            