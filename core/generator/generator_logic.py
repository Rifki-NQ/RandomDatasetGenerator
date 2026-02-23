import pandas as pd
from pathlib import Path

#warning: slower generation for dataset that generate strings

class GeneratorLogic:
    def __init__(self, generator_setting_logic, csv_file_handler, randomizer):
        self.setting = generator_setting_logic
        self.csv_file_handler = csv_file_handler
        self.rng = randomizer
    
    #register then check if the file is empty
    def check_file_destination(self) -> bool:
        dataset_filepath = self._register_dataset_destination()
        if dataset_filepath is None:
            return False
        if not dataset_filepath.exists():
            return False
        #return true if the file size is not 0 (empty)
        if dataset_filepath.stat().st_size != 0:
            return True
        return False
    
    #register file destination, raise error if something is not expected then return None
    def _register_dataset_destination(self) -> Path | None:
        dataset_filepath = self.setting.get_dataset_filepath()
        self.csv_file_handler.register_filepath(Path(dataset_filepath))
        return Path(dataset_filepath)
    
    def generate_dataset(self, column_length: int, row_length: int) -> None:
        generated_dataset = {}
        column_name = self.rng.get_random_string(column_length, 5, "uppercase")
        for column in range(column_length):
            value = self.rng.get_random_mixed(row_length)
            generated_dataset[column_name[column]] = []
            for row in range(row_length):
                generated_dataset[column_name[column]].append(value[row])
        df_generated_dataset = pd.DataFrame(generated_dataset)
        self.csv_file_handler.save(df_generated_dataset)
        
    def generate_custom_dataset(self) -> None:
        pass