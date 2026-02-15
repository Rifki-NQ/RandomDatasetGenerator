from core.exceptions import InputError
from core.utils import Helper
from typing import Any

class MenuContainer:
    @staticmethod
    def get_menu() -> dict[str, Any]:
        return {"Generator": {
                    1: "Generate random dataset"
                }}

class App:
    def __init__(self):
        self.menu = MenuContainer.get_menu()
        self.menu_max_depth = Helper.get_dict_depth(self.menu)
        self.choosen_menu = []
        self.is_running = True
    
    def prompt_index(self, min_index, max_index) -> int:
        while True:
            index = input("Enter by index: ")
            try:
                if Helper.is_digit_in_range(index, min_index, max_index):
                    return int(index)
            except InputError as e:
                print(e)
    
    def show_menu(self, data: dict[str, Any], show_index: int) -> None:
        for menu, submenu in data.items():
            if show_index == 1:
                print(menu)
            else:
                self.show_menu(submenu, show_index)
                
    def process_input(self, index: int) -> None:
        pass
    
    def start_app(self) -> None:
        show_index = 1
        while self.is_running:
            self.show_menu(self.menu, show_index)
            index = self.prompt_index()
            
    
if __name__ == "__main__":
    app = App()
    app.start_app()