from pathlib import Path
from dataclasses import replace, asdict
from core.models.config_models import GeneratorConfig, RandomConfig
from core.exceptions import FileNotFoundAppError, FilepathUndefinedError, MissingConfigKeyError

class GeneratorSettingLogic:
    DATASET_FILEPATH_KEY = "dataset_filepath"
    RANDOM_CONFIG_KEY = {"column_length", "row_length", "int_min", "int_max", "float_min", 
                     "float_max", "float_round", "string_length", "string_type"}
    CONFIG_FILEPATH = Path("data/config.yaml")
    
    def __init__(self, yaml_file_handler):
        self.yaml_file_handler = yaml_file_handler
        
    def _read_config(self) -> GeneratorConfig:
        if not self.yaml_file_handler.register_filepath(self.CONFIG_FILEPATH):
            raise FileNotFoundAppError(f"Error: failed to read config data: ({self.CONFIG_FILEPATH}) because the file does not exist!")
        raw_config_data = self.yaml_file_handler.read(format_data=False)
        return GeneratorConfig(**raw_config_data)
    
    def _validate_config_data(self, config_data: dict[str, int | str]) -> None:
        missing_keys = self.RANDOM_CONFIG_KEY - config_data.keys()
        if self.DATASET_FILEPATH_KEY not in config_data:
            raise MissingConfigKeyError(f"Error: {self.DATASET_FILEPATH_KEY} does not exist in the config data!")
        if missing_keys:
            raise MissingConfigKeyError(f"Error: {missing_keys} does not exist in the config data!")
    
    def get_dataset_filepath(self) -> str:
        config_data = self._read_config()
        dataset_filepath = config_data.dataset_filepath
        if dataset_filepath is None:
            raise FilepathUndefinedError(f"Error: {self.DATASET_FILEPATH_KEY} is undefined in the config_data!")
        return dataset_filepath
    
    def get_random_config(self) -> RandomConfig:
        return self._read_config().random_config()
    
    def change_dataset_filepath(self, new_filepath: str) -> None:
        config_data = self.read_config()
        config_data[self.DATASET_FILEPATH_KEY] = new_filepath
        self.yaml_file_handler.save(config_data)
        
    def change_random_config(self, new_config: RandomConfig) -> None:
        config_data = self._read_config()
        updated_config = replace(config_data, **asdict(new_config))
        self.yaml_file_handler.save(asdict(updated_config))