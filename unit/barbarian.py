from .unit import Unit

class Barbarian(Unit):
    def __init__(self):
        super().__init__("Barbarian", 20,60)

    def attack(self, building):
        print(f"{self._name} attacks {building._name}!")
        building.take_damage(self._damage)