from core.exceptions import FileNotFoundAppError, FilepathNotFoundError, FilepathUndefinedError
from pathlib import Path

class GeneratorSettingLogic:
    def __init__(self, yaml_file_handler):
        self.yaml_file_handler = yaml_file_handler
        self.CONFIG_FILEPATH = Path("data/config.yaml")
        self.dataset_filepath_key = "dataset_filepath"
        
    def _read_config(self) -> dict[str, str]:
        if not self.yaml_file_handler.register_filepath(self.CONFIG_FILEPATH):
            raise FileNotFoundAppError("Error: failed to read config data: (data/config.yaml) because the file does not exist!")
        return self.yaml_file_handler.read(format_data = False)
    
    def get_dataset_filepath(self) -> str:
        filepath_data = self._read_config()
        if not self.dataset_filepath_key in filepath_data:
            raise FilepathNotFoundError(f"Error: {self.dataset_filepath_key} does not exist in the config data!")
        dataset_filepath = filepath_data.get(self.dataset_filepath_key)
        if dataset_filepath is None:
            raise FilepathUndefinedError(f"Error: {self.dataset_filepath_key} is undefined in the config_data!")
        return dataset_filepath
    
    def change_dataset_filepath(self, new_filepath: str) -> None:
        filepath_data = self._read_config() 
        filepath_data[self.dataset_filepath_key] = new_filepath
        self.yaml_file_handler.save(filepath_data)