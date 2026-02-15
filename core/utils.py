import pandas as pd
import yaml
from typing import Any
from core.exceptions import (ValueNotDigitError, OutOfBoundValueError)

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