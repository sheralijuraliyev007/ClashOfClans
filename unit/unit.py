from abc import ABC, abstractmethod

class Unit(ABC):
    def __init__(self, name, damage, hp):
        self._name = name
        self._damage = damage
        self._hp = hp #Default

    @abstractmethod
    def attack(self, building):
        pass

    def take_damage(self, amount):
        self._hp -= amount
        print(f"{self._name} took {amount} damage. HP left: {self._hp}")

    def is_dead(self):
        return self._hp <= 0
