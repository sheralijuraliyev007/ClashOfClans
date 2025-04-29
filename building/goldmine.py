from .building import Building
import time


class GoldMine(Building):
    def __init__(self):
        super().__init__("Gold Mine", 100)
        self.last_produce_time = time.time()
        self.gold_stored = 0
        self.rate = 5
        self.interval = 3


    def update(self):
        current_time = time.time()
        if current_time - self.last_produce_time >= self.interval:
            self.gold_stored += self.rate
            self.last_produce_time = current_time


    def collect(self):
        gold = self.gold_stored
        self.gold_stored = 0
        return gold

