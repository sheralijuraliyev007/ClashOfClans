class GameState:
    def __init__(self):
        self._selected = None

    def select(self, item_class):
        self._selected = item_class

    def select_unit(self, unit_class):  # <-- Add this method
        self.select(unit_class)

    def get_selected(self):
        return self._selected

    def clear_selection(self):
        self._selected = None

    def get_cost(self):
        # Example logic for cost
        if self._selected.__name__ == "Barbarian":
            return 30
        elif self._selected.__name__ == "Archer":
            return 20
        elif self._selected.__name__ in ["GoldMine", "ElixirCollector"]:
            return 50
        return 0
