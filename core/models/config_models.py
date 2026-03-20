from dataclasses import dataclass, fields
from typing import Literal, get_args
from pathlib import Path
from core.exceptions import (InvalidConfigTypeError, InvalidFilepathError, RowColumnLengthError,
                             InvalidMinMaxValueError, InvalidFloatRoundError, InvalidStringTypeError)

STRING_TYPES = Literal["uppercase", "lowercase", "mixed"]

@dataclass
class IntConfig:
    size: int
    int_min: int
    int_max: int    
    
@dataclass
class FloatConfig:
    size: int
    float_min: int
    float_max: int
    float_round: int

@dataclass
class StringConfig:
    size: int
    string_length: int
    string_type: STRING_TYPES

#note: row length = size
@dataclass
class RandomConfig:
    column_length: int
    row_length: int
    int_min: int
    int_max: int
    float_min: int
    float_max: int
    float_round: int
    string_length: int
    string_type: str
    
    def int_config(self) -> IntConfig:
        return IntConfig(
            size=self.row_length,
            int_min=self.int_min,
            int_max=self.int_max
        )
    
    def float_config(self) -> FloatConfig:
        return FloatConfig(
            size=self.row_length,
            float_min=self.float_min,
            float_max=self.float_max,
            float_round=self.float_round
        )
        
    def string_config(self) -> StringConfig:
        return StringConfig(
            size=self.row_length,
            string_length=self.string_length,
            string_type=self.string_type
        )

@dataclass
class GeneratorConfig:
    dataset_filepath: str
    column_length: int
    row_length: int
    int_min: int
    int_max: int
    float_min: int
    float_max: int
    float_round: int
    string_length: int
    string_type: str
    
    def __post_init__(self) -> None:
        GeneratorConfig.validate_type(**{f.name: getattr(self, f.name) for f in fields(self)})
        GeneratorConfig.validate_filepath(self.dataset_filepath)
        GeneratorConfig.validate_row_column_length(self.column_length, self.row_length)
        GeneratorConfig.validate_min_max("int", self.int_min, self.int_max)
        GeneratorConfig.validate_min_max("float", self.float_min, self.float_max)
        GeneratorConfig.validate_float_round(self.float_round)
        GeneratorConfig.validate_string_type(self.string_type)
    
    def random_config(self) -> RandomConfig:
        return RandomConfig(
            column_length=self.column_length,
            row_length=self.row_length,
            int_min=self.int_min,
            int_max=self.int_max,
            float_min=self.float_min,
            float_max=self.float_max,
            float_round=self.float_round,
            string_length=self.string_length,
            string_type=self.string_type
        )
    
    @staticmethod
    def validate_type(**config) -> None:
        expected = {
            "dataset_filepath": str,
            "column_length": int,
            "row_length": int,
            "int_min": int,
            "int_max": int,
            "float_min": (int, float),
            "float_max": (int, float),
            "float_round": int,
            "string_length": int,
            "string_type": str
        }
        for config_key, config_value in config.items():
            expected_type = expected[config_key]
            if not isinstance(config_value, expected_type):
                expected_type = tuple(v.__name__ for v in expected_type) if isinstance(expected_type, tuple) else f"({expected_type.__name__})"
                raise InvalidConfigTypeError(f"Error: expected {expected_type} for {config_key}, "
                                             f"got ({type(config_value).__name__}) instead")
    
    @staticmethod
    def validate_filepath(dataset_filepath: str) -> None:
        dataset_filepath = dataset_filepath.strip().replace(" ", "_")
        filepath_folder = str(Path(dataset_filepath).parent)
        if filepath_folder != "data":
            raise InvalidFilepathError("Error: dataset file must be in the designated folder (example: data/file.csv)")
        if not dataset_filepath.lower().endswith(".csv"):
            raise InvalidFilepathError("dataset file must be a csv file (example: data/file.csv)")

    @staticmethod
    def validate_row_column_length(column_length: int, row_length: int) -> None:
        if column_length < 1:
            raise RowColumnLengthError("Error: (column length) cannot be less than 1!")
        if row_length < 1:
            raise RowColumnLengthError("Error: (row length) cannot be less than 1!")
        
    @staticmethod
    def validate_min_max(value_type: str, min_value: int, max_value: int) -> None:
        if min_value >= max_value:
            raise InvalidMinMaxValueError(f"Error: {value_type} max value ({max_value}) "
                                          f"has to be higher than {value_type} max value ({min_value})!")
    
    @staticmethod
    def validate_float_round(float_round: int) -> None:
        if not 1 <= float_round <= 8:
            raise InvalidFloatRoundError(f"Error: float round ({float_round}) is out of allowed range (1 to 8)!")
    
    @staticmethod
    def validate_string_type(string_type: str) -> None:
        if string_type not in get_args(STRING_TYPES):
            raise InvalidStringTypeError(f"Error: invalid string type ({string_type}), expected {get_args(STRING_TYPES)}")