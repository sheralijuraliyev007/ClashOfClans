import pygame
from utils.resource_manager import ResourceManager
from building.goldmine import GoldMine
from unit.barbarian import Barbarian
from unit.archer import Archer
from ui.button import Button
from grid.grid import Grid
from utils.file_manager import FileManager
from services.sound_service import SoundService
from core.game_state import GameState

# Initialize
pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Clash UI")
font = pygame.font.SysFont(None, 32)
small_font = pygame.font.SysFont(None, 18)
clock = pygame.time.Clock()

# Services
sound_service = SoundService()
game_state = GameState()
resources = ResourceManager()
grid = Grid(rows=10, cols=10, tile_size=40, offset_x=250, offset_y=50, font=small_font)

# Load Data
def save_all():
    data = []
    for row in range(grid.rows):
        for col in range(grid.cols):
            unit = grid.grid[row][col]
            if unit:
                data.append({
                    "type": unit.__class__.__name__,
                    "row": row,
                    "col": col
                })
    FileManager.save_data(data, "grid_data.json")
    FileManager.save_data(resources.get_balance(), "resources.json")

def load_all():
    data = FileManager.load_data("grid_data.json")
    for item in data:
        unit_type = item["type"]
        row, col = item["row"], item["col"]
        if unit_type == "Barbarian":
            unit = Barbarian()
        elif unit_type == "Archer":
            unit = Archer()
        elif unit_type == "GoldMine":
            unit = GoldMine()
        else:
            continue
        grid.grid[row][col] = unit

    balance = FileManager.load_data("resources.json")
    resources._gold = balance.get("gold", 100)
    resources._elixir = balance.get("elixir", 50)

load_all()

# Callbacks
def build_goldmine():
    sound_service.play("click")
    game_state.select(GoldMine)
    print("🏗️ Gold Mine selected")

def train_barbarian():
    sound_service.play("click")
    game_state.select_unit(Barbarian)
    print("🧍‍♂️ Barbarian selected")

def train_archer():
    sound_service.play("click")
    game_state.select_unit(Archer)
    print("🏹 Archer selected")

def reset_resources():
    sound_service.play("click")
    resources._gold = 100
    resources._elixir = 50
    print("🔄 Resources reset.")

def clear_grid():
    sound_service.play("click")
    for row in range(grid.rows):
        for col in range(grid.cols):
            grid.grid[row][col] = None
    print("🧼 Grid cleared.")

def collect_gold_from_goldmine(row, col):
    sound_service.play("click")
    building = grid.grid[row][col]
    if isinstance(building, GoldMine):
        collected_gold = building.collect()
        resources.add_gold(collected_gold)
        print(f"💰 Collected {collected_gold} gold from Gold Mine at ({row}, {col}).")
    else:
        print("❌ This is not a Gold Mine.")

# UI Buttons
buttons = [
    Button(50, 50, 180, 40, "Train Barbarian (30🪙)", train_barbarian, sound=sound_service.sounds["click"]),
    Button(50, 100, 180, 40, "Train Archer (20🪙)", train_archer, sound=sound_service.sounds["click"]),
    Button(50, 200, 180, 40, "Clear Grid", clear_grid, sound=sound_service.sounds["click"]),
    Button(50, 250, 180, 40, "Reset Resources", reset_resources, sound=sound_service.sounds["click"]),
    Button(50, 350, 180, 40, "Build Gold Mine (50🪙)", build_goldmine, sound=sound_service.sounds["click"]),
]

# Main Loop
running = True
while running:
    screen.fill((245, 245, 245))
    grid.draw(screen)

    # Update all Gold Mines (produce gold)
    for row in range(grid.rows):
        for col in range(grid.cols):
            building = grid.grid[row][col]
            if isinstance(building, GoldMine):
                building.produce()

    for button in buttons:
        button.draw(screen)

    balance = resources.get_balance()
    screen.blit(font.render(f"Gold: {balance['gold']}", True, (0, 0, 0)), (400, 50))
    screen.blit(font.render(f"Elixir: {balance['elixir']}", True, (0, 0, 0)), (400, 90))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_all()
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if a GoldMine is clicked for gold collection
            mouse_x, mouse_y = event.pos
            row, col = grid.get_cell_at(mouse_x, mouse_y)

            if row is not None and col is not None:
                collect_gold_from_goldmine(row, col)

            # Handle other grid interactions (placing units, etc.)
            elif game_state.get_selected():
                selected_class = game_state.get_selected()
                cost = game_state.get_cost()

                if resources.spend_gold(cost):
                    unit_or_building = selected_class()
                    success, result = grid.place_unit(*event.pos, unit_or_building)

                    if success:
                        sound_service.play("place")
                        print(f"{unit_or_building._name} placed at {result}")
                        game_state.clear_selection()
                    else:
                        print("❌", result)
                        resources.add_gold(cost)
                else:
                    print("❌ Not enough gold.")

        for button in buttons:
            button.handle_event(event)

    # Show selected unit
    label = game_state.get_selected().__name__ if game_state.get_selected() else "None"
    screen.blit(font.render(f"Selected: {label}", True, (0, 0, 200)), (50, 160))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
