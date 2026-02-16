from core.generator.generator_logic import GeneratorLogic
from core.generator.generator_cli import GeneratorCLI
from core.utils import DataIO, Randomizer
from core.exceptions import InvalidClassNameError, InvalidMethodNameError
from pathlib import Path
from typing import Callable, Literal

valid_class_name = Literal["GeneratorCLI", "GeneratorConfigCLI"]
VALID_CLASS_NAME = {"GeneratorCLI", "GeneratorConfigCLI"}

class Container:
    def __init__(self):
        self.config_filepath = Path("data/config.yaml")
        self.dataset_filepath = Path("data/random_dataset.csv")
        self.yaml_file_handler =DataIO.create_dataio(self.config_filepath)
        self.csv_file_handler = DataIO.create_dataio(self.dataset_filepath)
        self.randomizer = Randomizer()
        self.generator_logic = GeneratorLogic(self.dataset_filepath,
                                              self.csv_file_handler,
                                              self.randomizer)
        self.generator_feature = GeneratorCLI(self.generator_logic)

class FeatureFactory(Container):
    def call_method(self, class_name: valid_class_name, method_name: str | None) -> Callable[[], None]:
        if class_name not in VALID_CLASS_NAME:
            raise InvalidClassNameError(f"Error: unknown class: {class_name}")
        if method_name is None:
            raise InvalidMethodNameError(f"Error: feature not implemented yet (method is None)")
        class_map = {
            "GeneratorCLI" : self.generator_feature
        }
        obj = class_map.get(class_name)
        try:
            return getattr(obj, method_name)
        except AttributeError:
            raise InvalidMethodNameError(f"Error: {class_name} has no method {method_name}")