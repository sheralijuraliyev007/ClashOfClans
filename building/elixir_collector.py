import pygame

from .building import Building
import time

class ElixirCollector(Building):
    def __init__(self):
        super().__init__("Elixir Collector", 100)
        self.last_produce_time = time.time()
        self.stored_elixir = 0  # ✅ Use this consistently
        self.rate = 5
        self.interval = 3
        image = pygame.image.load("./assets/photo_2025-04-30_09-46-25.jpg")
        self.image = pygame.transform.scale(image, (40, 40))

    def update(self):
        current_time = time.time()
        if current_time - self.last_produce_time >= self.interval:
            self.stored_elixir += self.rate
            self.last_produce_time = current_time

    def produce(self):
        # Optional duplicate if needed for abstract method
        self.update()

    def collect(self):
        gold = self.stored_elixir
        self.stored_elixir = 0
        return gold
