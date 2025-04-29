
class ResourceManager:
    def __init__(self, gold=100,elixir=50):
        self._gold = gold
        self._elixir = elixir

    def add_gold(self, amount):
        self._gold += amount
        print(f"🪙 Gold increased by {amount}. Total: {self._gold}")

    def spend_gold(self, amount):
        if self._gold >= amount:
            self._gold -= amount
            print(f"🪙 Spent {amount} gold. Remaining: {self._gold}")
            return True
        else:
            print("❌ Not enough gold.")
            return False
    def add_elixir(self,amount):
        self._elixir +=amount
        print(f"🔮 Elixir increased by {amount}. Total: {self._elixir}")

    def spend_elixir(self,amount):
        if self._elixir>=amount:
            self._elixir-=amount
            print(f"🔮 Spent {amount} elixir. Remaining: {self._elixir}")
            return True
        else:
            print("❌ Not enough elixir.")
            return False

    def get_balance(self):
        return {"gold": self._gold, "elixir": self._elixir}

