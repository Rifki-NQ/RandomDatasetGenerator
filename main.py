from core.exceptions import InputError
from core.utils import Helper
from typing import Any

class MenuContainer:
    @staticmethod
    def get_menu() -> dict[str, Any]:
        return [
        {
            "label": "Generator",
            "submenu": [
                {
                    "label": "Generate random dataset",
                    "action": None
                },
                {
                    "label": "Generate random custom dataset",
                    "action": None
                }
            ]
        },
        {
            "label": "Setting",
            "submenu": [
                {
                    "label": "Set random config",
                    "action": None
                }
            ]
        }
    ]

class App:
    def __init__(self, menu):
        self.menu = menu
    
    def _prompt_index(self, min_index, max_index) -> int:
        while True:
            index = input("Enter by index: ")
            try:
                if Helper.is_digit_in_range(index, min_index, max_index):
                    return int(index)
            except InputError as e:
                print(e)
    
    def menu_engine(self, menu: list[dict]) -> None:
        while True:
                menu_length = len(menu)
                for index, item in enumerate(menu, 1):
                    print(f"{index}. {item["label"]}")
                index = self._prompt_index(1, menu_length)
                index -= 1
                if "submenu" in menu[index]:
                    self.menu_engine(menu[index]["submenu"])
                else:
                    print("A method is being run!")
    
    def start_app(self) -> None:
            self.menu_engine(self.menu)
            
if __name__ == "__main__":
    app = App(MenuContainer.get_menu())
    app.start_app()