from core.exceptions import InputError
from core.utils import Helper

class MenuContainer:
    @staticmethod
    def get_menu() -> dict[str, dict[int, str]]:
        return {"Generator": {
                    1: "Generate random dataset"
                },
                "Setting": {
                    1: "Set custom generator config"
                }}

class App:
    def __init__(self):
        self.menu = MenuContainer.get_menu()
        self.menu_depth = None
    
    def start_app(self):
        pass
    
if __name__ == "__main__":
    app = App()
    app.start_app()