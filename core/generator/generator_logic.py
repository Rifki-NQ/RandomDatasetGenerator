import numpy as np
import string
from typing import Literal

strformats = Literal["uppercase", "lowercase", "mixed"]

class Randomizer:
    def __init__(self):
        self.SEED = 42
        self.rng = np.random.default_rng(self.SEED)
        
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
        