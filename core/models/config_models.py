from dataclasses import dataclass
from typing import Literal
from core.exceptions import InvalidConfigTypeError

strformats = Literal["uppercase", "lowercase", "mixed"]

@dataclass
class ConfigValidator:
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
        self._validate_type()
    
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

@dataclass
class IntConfig:
    size: int = 1
    int_min: int = 1
    int_max: int = 2

@dataclass
class FloatConfig:
    size: int = 1
    float_min: int = 1
    float_max: int = 2
    float_round: int | None = None

@dataclass
class StringConfig:
    size: int = 1
    string_length: int = 1
    string_type: strformats | None = None
    