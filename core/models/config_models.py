from dataclasses import dataclass
from typing import Literal, get_args
from core.exceptions import (InvalidConfigTypeError, RowColumnLengthError,
                             InvalidMinMaxValueError, InvalidFloatRoundError,
                             InvalidStringTypeError)

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
    
    def __post_init__(self) -> None:
        self._validate_type()
        self._validate_row_column_length()
        self._validate_min_max()
        self._validate_float_round()
        self._validate_string_type()
    
    def _validate_type(self) -> None:
        expected = {
            "dataset_filepath": str,
            "column_length": int,
            "row_length": int,
            "int_min": int,
            "int_max": int,
            "float_min": int,
            "float_max": int,
            "float_round": int,
            "string_length": int,
            "string_type": str
        }
        for key, expected_type in expected.items():
            value = getattr(self, key)
            if not isinstance(value, expected_type):
                raise InvalidConfigTypeError(f"Error: expected ({expected_type.__name__}) for {key}, "
                                             f"got ({type(value).__name__}) instead")

    def _validate_row_column_length(self) -> None:
        if self.column_length < 1:
            raise RowColumnLengthError("Error: column_length cannot be less than 1!")
        if self.row_length < 1:
            raise RowColumnLengthError("Error: row_length cannot be less than 1!")
        
    def _validate_min_max(self) -> None:
        if self.int_min >= self.int_max:
            raise InvalidMinMaxValueError(f"Error: int_max value ({self.int_max}) "
                                          f"has to be higher than int_min value ({self.int_min})!")
        if self.float_min >= self.float_max:
            raise InvalidMinMaxValueError(f"Error: float_max value ({self.float_max}) "
                                          f"has to be higher than float_min value ({self.float_min})!")
    
    def _validate_float_round(self) -> None:
        if not 1 <= self.float_round <= 8:
            raise InvalidFloatRoundError(f"Error: float_round ({self.float_round}) is out of allowed range (1 to 8)!")
    
    def _validate_string_type(self) -> None:
        if self.string_type not in get_args(STRING_TYPES):
            raise InvalidStringTypeError(f"Error: invalid string_type ({self.string_type}), expected {get_args(STRING_TYPES)}")