class GeneratorSettingLogic:
    def __init__(self, yaml_file_handler):
        self.yaml_file_handler = yaml_file_handler
        
    def get_current_filepath(self) -> str:
        if self.yaml_file_handler.read("data/config.yaml"):
            pass