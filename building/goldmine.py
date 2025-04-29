from .building import Building
import time

class GoldMine(Building):
    def __init__(self):
        super().__init__("Gold Mine", 100)
        self.last_produce_time = time.time()
        self.stored_gold = 0  # ✅ Use this consistently
        self.rate = 5
        self.interval = 3

    def update(self):
        current_time = time.time()
        if current_time - self.last_produce_time >= self.interval:
            self.stored_gold += self.rate
            self.last_produce_time = current_time

    def produce(self):
        # Optional duplicate if needed for abstract method
        self.update()

    def collect(self):
        gold = self.stored_gold
        self.stored_gold = 0
        return gold
