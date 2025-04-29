from abc import ABC, abstractmethod

class Building(ABC):

    def __init__(self, name, hp):
        self._name = name
        self._hp = hp

    @abstractmethod
    def produce(self):
        pass

    def take_damage(self, amount):
        self._hp -= amount
        print(f"{self._name} took {amount} damage. Remaining HP: {self._hp}")

    def is_destroyed(self):
        return self._hp <= 0

    
