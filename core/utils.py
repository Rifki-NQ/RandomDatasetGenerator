import pandas as pd
import yaml
from typing import Any
from pathlib import Path
from abc import ABC, abstractmethod
from core.exceptions import (ValueNotDigitError, OutOfBoundValueError, InvalidFileTypeError,
                             FileNotFoundAppError, EmptyDataError)

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
    @abstractmethod
    def read(self, **kwargs):
        pass
    
    @abstractmethod
    def save(self, data):
        pass
    
    @staticmethod
    def create_dataio(file_path: Path) -> DataIO:
        valid_file_types = {"csv", "yaml"}
        file_type = file_path.suffix.lstrip(".")
        if not file_type in valid_file_types:
            raise InvalidFileTypeError("Error: invalid file type provided!")
        if not file_path.exists() and file_type == "csv":
            raise FileNotFoundAppError(f"Error: failed to read/write ({file_path}) because the file does not exist!")
        elif not file_path.exists() and file_type == "yaml":
            raise FileNotFoundAppError(f"Error: failed to read/write ({file_path}) because the file does not exist!")
        if file_type == "csv":
            return CSVFileHandler(file_path)
        elif file_type == "yaml":
            return YAMLFileHandler(file_path)
    
class CSVFileHandler(DataIO):
    def __init__(self, file_path: Path):
        self.file_path = file_path
    
    def read(self, **kwargs) -> pd.DataFrame:
        display_all = kwargs.get("display_all", False)
        try:
            if display_all:
                pd.set_option("display.max_rows", None)
            df = pd.read_csv(self.file_path)
            return df
        except pd.errors.EmptyDataError:
            raise EmptyDataError(f"Error: failed to read ({self.file_path}) because the file is empty!")
        except FileNotFoundError:
            raise FileNotFoundAppError(f"Error: failed to read/write ({self.file_path}) because the file does not exist!")
         
    def save(self, df):
        df.to_csv(self.file_path, index=False)
         
class YAMLFileHandler(DataIO):
    def __init__(self, file_path: Path):
        self.file_path = file_path
    
    def _format_yaml(self, data) -> str:
        formatted_yaml = yaml.dump(
            data,
            sort_keys=False,
            default_flow_style=False
        )
        return formatted_yaml
    
    def read(self, **kwargs) -> dict[str, Any]:
        format_data = kwargs.get("format_data", False)
        try:
            with open(self.file_path, "r") as file:
                data = yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundAppError(f"Error: failed to read/write ({self.file_path}) because the file does not exist!")
        #return error if any data is empty
        if data is None:
            raise EmptyDataError(f"Error: failed to read ({self.file_path}) because the file is empty!")
        if format_data:
            data = self._format_yaml(data)
        return data
        
    def save(self, data):
        with open(self.file_path, "w+") as file:
            yaml.safe_dump(data, file, sort_keys=False)