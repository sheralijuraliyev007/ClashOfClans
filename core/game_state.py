class GameState:
    def __init__(self):
        self.selected_class = None  # Could be a unit or building

    def select(self, cls):  # Accepts any class like Barbarian or GoldMine
        self.selected_class = cls

    def clear_selection(self):
        self.selected_class = None

    def get_selected(self):
        return self.selected_class

    def get_cost(self):
        if self.selected_class.__name__ == "Barbarian":
            return 30
        elif self.selected_class.__name__ == "Archer":
            return 20
        elif self.selected_class.__name__ == "GoldMine":
            return 50
        return 0
