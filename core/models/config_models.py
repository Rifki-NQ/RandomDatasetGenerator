from dataclasses import dataclass
from typing import Literal

strformats = Literal["uppercase", "lowercase", "mixed"]

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
    