from dataclasses import dataclass
from typing import Literal
from core.exceptions import InvalidConfigTypeError

strformats = Literal["uppercase", "lowercase", "mixed"]

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
    