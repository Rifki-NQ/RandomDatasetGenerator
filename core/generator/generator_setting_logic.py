from pathlib import Path
from dataclasses import replace, asdict, fields
from core.models.config_models import GeneratorConfig, RandomConfig
from core.exceptions import (FileNotFoundAppError, FilepathUndefinedError, MissingConfigKeyError,
                             ExtraConfigKeyError)

class GeneratorSettingLogic:
    DATASET_FILEPATH_KEY = "dataset_filepath"
    CONFIG_FILEPATH = Path("data/config.yaml")
    
    def __init__(self, yaml_file_handler):
        self.yaml_file_handler = yaml_file_handler
    
    def get_random_config(self) -> RandomConfig:
        return self._read_config().random_config()
    
    def get_dataset_filepath(self) -> str:
        config_data = self._read_config()
        dataset_filepath = config_data.dataset_filepath
        if dataset_filepath is None:
            raise FilepathUndefinedError(f"Error: {self.DATASET_FILEPATH_KEY} is undefined in the config_data!")
        return dataset_filepath
    
    def change_random_config(self, new_config: RandomConfig) -> None:
        config_data = self._read_config()
        updated_config = replace(config_data, **asdict(new_config))
        self._save_config(updated_config)
    
    def change_dataset_filepath(self, new_filepath: str) -> None:
        config_data = self._read_config()
        config_data.dataset_filepath = new_filepath
        self._save_config(config_data)
        
    def _read_config(self) -> GeneratorConfig:
        if not self.yaml_file_handler.register_filepath(self.CONFIG_FILEPATH):
            raise FileNotFoundAppError(f"Error: failed to read config data: ({self.CONFIG_FILEPATH}) because the file does not exist!")
        raw_config_data = self.yaml_file_handler.read(format_data=False)
        self._validate_config_data_keys(raw_config_data, GeneratorConfig)
        return GeneratorConfig(**raw_config_data)
    
    def _validate_config_data_keys(self, config_data: dict[str, int | str], config_model: type[GeneratorConfig]) -> None:
        expected_keys = set(f.name for f in fields(config_model))
        missing_keys = expected_keys - config_data.keys()
        extra_keys = config_data.keys() - expected_keys
        if missing_keys:
            raise MissingConfigKeyError(f"Error: {missing_keys} does not exist in the config data!")
        if extra_keys:
            raise ExtraConfigKeyError(f"Error: unexpected key {extra_keys} in config data!")
        
    def _save_config(self, config_data: GeneratorConfig) -> None:
        self.yaml_file_handler.save(asdict(config_data))