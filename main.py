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
from building.elixir_collector import ElixirCollector
import os




# Initialize
pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = 1000, 700  # or any size you prefer
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)



terrain_image = pygame.image.load("assets/terrain.jpg").convert()
terrain_image = pygame.transform.scale(terrain_image, (WIDTH, HEIGHT))  # ✅ match screen





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
        elif unit_type == "ElixirCollector":
            unit = ElixirCollector("Elixir Collector")
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

def build_elixir_collector():
    sound_service.play("click")
    game_state.select(ElixirCollector)
    print("🧪 Elixir Collector selected")

def train_barbarian():
    sound_service.play("click")
    game_state.select(Barbarian)
    print("🧍‍♂️ Barbarian selected")

def train_archer():
    sound_service.play("click")
    game_state.select(Archer)
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

# UI Buttons
buttons = [
    Button(50, 50, 180, 40, "Train Barbarian (30🪙)", train_barbarian, sound=sound_service.sounds["click"]),
    Button(50, 100, 180, 40, "Train Archer (20🪙)", train_archer, sound=sound_service.sounds["click"]),
    Button(50, 150, 180, 40, "Build Elixir Collector (50🪙)", build_elixir_collector, sound=sound_service.sounds["click"]),
    Button(50, 200, 180, 40, "Clear Grid", clear_grid, sound=sound_service.sounds["click"]),
    Button(50, 250, 180, 40, "Reset Resources", reset_resources, sound=sound_service.sounds["click"]),
    Button(50, 300, 180, 40, "Build Gold Mine (50🪙)", build_goldmine, sound=sound_service.sounds["click"])
]

# Main Loop
running = True
while running:
    screen.blit(terrain_image, (0, 0)) # ✅ Now draws every frame

    grid.draw(screen)

    # Update buildings
    for row in range(grid.rows):
        for col in range(grid.cols):
            building = grid.grid[row][col]
            if isinstance(building, GoldMine) or isinstance(building, ElixirCollector):
                building.produce()

    # Draw buttons
    for button in buttons:
        button.draw(screen)

    # Display resource info
    balance = resources.get_balance()
    screen.blit(font.render(f"Gold: {balance['gold']}", True, (0, 0, 0)), (400, 50))
    screen.blit(font.render(f"Elixir: {balance['elixir']}", True, (0, 0, 0)), (400, 90))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            terrain_image = pygame.transform.scale(pygame.image.load("assets/terrain.jpg"), (WIDTH, HEIGHT))

            print(f"📐 Resized to: {event.w}x{event.h}")

        if event.type == pygame.QUIT:
            save_all()
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False



        for button in buttons:  # ✅ Moved inside event loop
            button.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            cell = grid.get_cell_at(mouse_x, mouse_y)

            if game_state.get_selected():
                selected_class = game_state.get_selected()
                cost = game_state.get_cost()

                if resources.spend_gold(cost):
                    try:
                        unit_or_building = selected_class()
                    except TypeError:
                        unit_or_building = selected_class(name=selected_class.__name__)

                    success, result = grid.place_unit(mouse_x, mouse_y, unit_or_building)

                    if success:
                        sound_service.play("place")
                        print(f"{unit_or_building._name} placed at {result}")
                        game_state.clear_selection()
                    else:
                        print("❌", result)
                        resources.add_gold(cost)
                else:
                    print("❌ Not enough gold.")

            elif cell:
                row, col = cell
                building = grid.grid[row][col]

                if isinstance(building, GoldMine):
                    collected = building.collect()
                    resources.add_gold(collected)
                    print(f"💰 Collected {collected} gold from Gold Mine.")
                elif isinstance(building, ElixirCollector):
                    collected = building.collect()
                    resources.add_elixir(collected)
                    print(f"🧪 Collected {collected} elixir from Elixir Collector.")

    # Draw selected unit/building label
    selected = game_state.get_selected()
    label = selected.__name__ if selected else "None"
    screen.blit(font.render(f"Selected: {label}", True, (0, 0, 200)), (50, 360))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
