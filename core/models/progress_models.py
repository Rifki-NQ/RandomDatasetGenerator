from dataclasses import dataclass

@dataclass
class GenerationProgress:
    total_value: int = 1
    
    def send_update(self, current_value: int) -> int:
        return round(current_value / self.total_value * 100)