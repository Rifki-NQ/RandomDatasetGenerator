from core.exceptions import FileNotFoundAppError, FilepathNotFoundError, FilepathUndefinedError
from pathlib import Path

class GeneratorSettingLogic:
    RANDOM_CONFIG = {"column_length", "row_length", "int_min", "int_max", "float_min", 
                     "float_max", "float_round", "string_length", "string_type"}
    CONFIG_FILEPATH = Path("data/config.yaml")
    DATASET_FILEPATH_KEY = "dataset_filepath"
    
    def __init__(self, yaml_file_handler):
        self.yaml_file_handler = yaml_file_handler
        
    def read_config(self) -> dict[str, str | int]:
        if not self.yaml_file_handler.register_filepath(self.CONFIG_FILEPATH):
            raise FileNotFoundAppError(f"Error: failed to read config data: ({self.CONFIG_FILEPATH}) because the file does not exist!")
        return self.yaml_file_handler.read(format_data = False)
    
    def get_dataset_filepath(self) -> str:
        config_data = self.read_config()
        if not self.DATASET_FILEPATH_KEY in config_data:
            raise FilepathNotFoundError(f"Error: {self.DATASET_FILEPATH_KEY} does not exist in the config data!")
        dataset_filepath = config_data.get(self.DATASET_FILEPATH_KEY)
        if dataset_filepath is None:
            raise FilepathUndefinedError(f"Error: {self.DATASET_FILEPATH_KEY} is undefined in the config_data!")
        return dataset_filepath
    
    def change_dataset_filepath(self, new_filepath: str) -> None:
        config_data = self.read_config()
        config_data[self.DATASET_FILEPATH_KEY] = new_filepath
        self.yaml_file_handler.save(config_data)
        
    def get_random_config(self) -> dict[str, int | str]:
        config_data = self.read_config()
        random_config = {}
        #return only random config configurations
        for key, value in config_data.items():
            if key in self.RANDOM_CONFIG:
                random_config[key] = value
        return random_config
        
    def change_random_config(self, new_config: dict[str, int | str]) -> None:
        config_data = self.read_config()
        self.yaml_file_handler.save(config_data | new_config)