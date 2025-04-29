from .unit import Unit

class Archer(Unit):
    def __init__(self):
        super().__init__("Archer", 10,30)

    def attack(self, building):
        print(f"{self._name} shoots an arrow at {building._name}!")
        building.take_damage(self._damage)