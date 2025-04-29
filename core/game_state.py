from unit.barbarian import Barbarian
from unit.archer import Archer

class GameState:
    def __init__(self):
        self.selected_unit = None

    def select_unit(self, unit_class):
        self.selected_unit = unit_class

    def get_selected_unit(self):
        return self.selected_unit

    def get_cost(self):
        if self.selected_unit == Barbarian:
            return 30
        elif self.selected_unit == Archer:
            return 20
        return 0

    def clear_selection(self):
        self.selected_unit = None
