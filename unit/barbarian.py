import pygame

from .unit import Unit

class Barbarian(Unit):
    def __init__(self):
        super().__init__("Barbarian", 20, 60)
        TILE_SIZE = 40

        image = pygame.image.load("assets/barbarian.jpg")
        self.image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))

    def attack(self, building):
        print(f"{self._name} attacks {building._name}!")
        building.take_damage(self._damage)