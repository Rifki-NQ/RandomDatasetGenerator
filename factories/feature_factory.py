from core.generator.base_cli import BaseCLI
from core.generator.generator_logic import GeneratorLogic
from core.generator.generator_cli import GeneratorCLI
from core.generator.generator_setting_cli import GeneratorSettingCLI
from core.generator.generator_setting_logic import GeneratorSettingLogic
from core.utils import DataIO, Randomizer
from core.exceptions import InvalidClassNameError, InvalidMethodNameError
from typing import Callable, Literal, get_args

valid_class_name = Literal["GeneratorCLI", "GeneratorSettingCLI"]
VALID_CLASS_NAME = get_args(valid_class_name)

class _Container:
    def __init__(self):
        self.yaml_file_handler =DataIO.create_dataio("yaml")
        self.csv_file_handler = DataIO.create_dataio("csv")
        self.randomizer = Randomizer()
        
        self.generator_setting_logic = GeneratorSettingLogic(self.yaml_file_handler)
        self.generator_setting_cli = GeneratorSettingCLI(self.generator_setting_logic)
        
        self.generator_logic = GeneratorLogic(self.generator_setting_logic,
                                              self.csv_file_handler,
                                              self.randomizer)
        self.generator_cli = GeneratorCLI(self.generator_logic,
                                              self.generator_setting_cli)

class FeatureFactory:
    def __init__(self):
        self.container = _Container()
    
    def call_method(self, class_name: valid_class_name, method_name: str | None) -> Callable[[], None]:
        if class_name not in VALID_CLASS_NAME:
            raise InvalidClassNameError(f"Error: unknown class: {class_name}")
        if method_name is None:
            raise InvalidMethodNameError(f"Error: feature not implemented yet (method = None)")
        
        class_map = {
            "GeneratorCLI" : self.container.generator_cli,
            "GeneratorSettingCLI": self.container.generator_setting_cli
        }
        
        obj = class_map.get(class_name)
        try:
            return BaseCLI.format(getattr(obj, method_name))
        except AttributeError:
            raise InvalidMethodNameError(f"Error: {class_name} has no method {method_name}")