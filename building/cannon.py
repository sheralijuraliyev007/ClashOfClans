from .building import Building


class Cannon(Building):
    def __init__(self):
        super().__init__("Cannon",120)
        self.damage = 25

    def produce(self):
        return None

    def attack(self, unit):
        print(f"{self._name} fires at {unit._name}!")
        unit.take_damage(self.damage)