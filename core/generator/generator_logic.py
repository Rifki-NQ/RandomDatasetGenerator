import pandas as pd
from pathlib import Path
from core.exceptions import FileError

class GeneratorLogic:
    def __init__(self, generator_setting_logic, csv_file_handler, randomizer):
        self.setting = generator_setting_logic
        self.csv_file_handler = csv_file_handler
        self.rng = randomizer
        
    #warning: slower generation for dataset that generate strings
    
    def register_dataset_destination(self) -> None:
        try:
            dataset_filepath = self.setting.get_dataset_filepath()
            self.csv_file_handler.register_filepath(Path(dataset_filepath))
        except FileError as e:
            print(e)
    
    def generate_dataset(self, column_length: int, row_length: int) -> None:
        self.register_dataset_destination()
        generated_dataset = {}
        column_name = self.rng.get_random_string(column_length, 5, "uppercase")
        for column in range(column_length):
            value = self.rng.get_random_mixed(row_length)
            generated_dataset[column_name[column]] = []
            for row in range(row_length):
                generated_dataset[column_name[column]].append(value[row])
        df_generated_dataset = pd.DataFrame(generated_dataset)
        self.csv_file_handler.save(df_generated_dataset)