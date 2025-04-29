from .building import Building


class TownHall(Building):
    def __init__(self):
        super().__init__("Town Hall",200)
        self.gold_stored = 100
        self.elixir_stored = 50

    def produce(self):
        return None


    def is_game_over(self):
        return self.is_destroyed()