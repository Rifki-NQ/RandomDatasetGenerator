import pandas as pd

class GeneratorLogic:
    def __init__(self, yaml_file_handler, csv_file_handler, randomizer):
        self.yaml_file_handler = yaml_file_handler
        self.csv_file_handler = csv_file_handler
        self.rng = randomizer
        
    #warning: slower generation for dataset that generate strings
    
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