import pygame

from .unit import Unit

class Archer(Unit):
    def __init__(self):
        super().__init__("Archer", 10,30)
        image = pygame.image.load("./assets/archer.jpg")
        self.image = pygame.transform.scale(image, (40, 40))

    def attack(self, building):
        print(f"{self._name} shoots an arrow at {building._name}!")
        building.take_damage(self._damage)