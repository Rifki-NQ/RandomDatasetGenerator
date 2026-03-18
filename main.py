import argparse
from factories.feature_factory import FeatureFactory
from core.exceptions import InputError, MenuError
from core.utils import Helper

class MenuContainer:
    @staticmethod
    def get_menu() -> list[dict]:
        return [
        {
            "label": "Generator",
            "submenu": [
                {
                    "label": "Generate random dataset",
                    "class": "GeneratorCLI",
                    "method": "generate_random_dataset"
                },
                {
                    "label": "Generate custom random dataset",
                    "class": "GeneratorCLI",
                    "method": "generate_custom_random_dataset"
                }
            ]
        },
        {
            "label": "Setting",
            "submenu": [
                {
                    "label": "Show current filepaths",
                    "class": "GeneratorSettingCLI",
                    "method": "show_all_filepath"  
                },
                {
                    "label": "Change filepath for generated dataset",
                    "class": "GeneratorSettingCLI",
                    "method": "update_dataset_filepath"
                },
                {
                    "label": "Show random value configuration",
                    "class": "GeneratorSettingCLI",
                    "method": "show_random_config"
                },
                {
                    "label": "Change random value configuration",
                    "class": "GeneratorSettingCLI",
                    "method": "change_random_config"
                },
                {
                    "label": "Update all random value configuration",
                    "class": "GeneratorSettingCLI",
                    "method": "update_random_configs"
                }
            ]
        }
    ]

class App:
    def __init__(self, menu):
        self.menu = menu
        self.feature_factory = FeatureFactory()
    
    def _prompt_index(self, min_index: int, max_index: int) -> int | None:
        while True:
            index = input("Enter by index (q to quit): ")
            if index.lower() == "q":
                return None
            try:
                if Helper.is_digit_in_range(index, min_index, max_index):
                    return int(index)
            except InputError as e:
                print(e)
    
    def menu_engine(self, menu: list[dict]) -> None:
        while True:
                menu_length = len(menu)
                for index, item in enumerate(menu, 1):
                    print(f"{index}. {item['label']}")
                index = self._prompt_index(1, menu_length)
                if index is None:
                    break
                index -= 1
                if "submenu" in menu[index]:
                    self.menu_engine(menu[index]["submenu"])
                else:
                    try:
                        self.feature_factory.call_method(class_name = menu[index]["class"],
                                                         method_name = menu[index]["method"])()
                    except MenuError as e:
                        print(f"\n{e}\n")
    
    def start_app(self) -> None:
            self.menu_engine(self.menu)
            
    def call_directly(self, class_name: str, method_name: str, **args) -> None:
        self.feature_factory.call_method(class_name, method_name)(**args)
            
if __name__ == "__main__":
    app = App(MenuContainer.get_menu())
    
    #initiate argparse for non interactive use
    parser = argparse.ArgumentParser(description="Dataset Generator")
    
    parser.add_argument("generate", nargs="?", help="Start generating dataset")
    parser.add_argument("column_length", nargs="?", type=int, default=10, help="Number of columns to generate")
    parser.add_argument("row_length", nargs="?",type=int, default=100, help="Number of rows to generate")
    
    args = parser.parse_args()
    #non interactive menu
    if args.generate == "generate":
        app.call_directly(class_name="GeneratorCLI", method_name="generate_random_dataset",
                          column_length=args.column_length, row_length=args.row_length)
    #interactive menu
    else:
        app.start_app()