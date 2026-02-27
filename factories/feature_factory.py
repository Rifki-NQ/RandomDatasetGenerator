from core.generator.generator_logic import GeneratorLogic
from core.generator.generator_cli import GeneratorCLI
from core.generator.generator_setting_cli import GeneratorSettingCLI
from core.generator.generator_setting_logic import GeneratorSettingLogic
from core.utils import DataIO, Randomizer
from core.exceptions import InvalidClassNameError, InvalidMethodNameError
from typing import Callable, Literal

valid_class_name = Literal["GeneratorCLI", "GeneratorSettingCLI"]
VALID_CLASS_NAME = {"GeneratorCLI", "GeneratorSettingCLI"}

class Container:
    def __init__(self):
        self.yaml_file_handler =DataIO.create_dataio("yaml")
        self.csv_file_handler = DataIO.create_dataio("csv")
        self.randomizer = Randomizer()
        
        #_feature is used when the object is being called as a feature
        #not when called by another feature
        
        self.generator_setting_logic = GeneratorSettingLogic(self.yaml_file_handler)
        self.generator_setting_feature = GeneratorSettingCLI(self.generator_setting_logic)
        
        self.generator_logic = GeneratorLogic(self.generator_setting_logic,
                                              self.csv_file_handler,
                                              self.randomizer)
        self.generator_setting = GeneratorSettingCLI(self.generator_setting_logic, use_decorator=False)
        self.generator_feature = GeneratorCLI(self.generator_logic,
                                              self.generator_setting)

class FeatureFactory(Container):
    def call_method(self, class_name: valid_class_name, method_name: str | None) -> Callable[[], None]:
        if class_name not in VALID_CLASS_NAME:
            raise InvalidClassNameError(f"Error: unknown class: {class_name}")
        if method_name is None:
            raise InvalidMethodNameError(f"Error: feature not implemented yet (method is None)")
        class_map = {
            "GeneratorCLI" : self.generator_feature,
            "GeneratorSettingCLI": self.generator_setting_feature
        }
        obj = class_map.get(class_name)
        try:
            return getattr(obj, method_name)
        except AttributeError:
            raise InvalidMethodNameError(f"Error: {class_name} has no method {method_name}")