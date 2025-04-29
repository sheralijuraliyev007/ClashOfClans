import pygame
from building.goldmine import GoldMine

class Grid:
    def __init__(self, rows, cols, tile_size, offset_x=0, offset_y=0, font=None):
        self.rows = rows
        self.cols = cols
        self.tile_size = tile_size
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        self.font = font  # This will now be passed in

    def draw(self, surface):
        for row in range(self.rows):
            for col in range(self.cols):
                rect = pygame.Rect(
                    self.offset_x + col * self.tile_size,
                    self.offset_y + row * self.tile_size,
                    self.tile_size,
                    self.tile_size
                )
                pygame.draw.rect(surface, (200, 200, 200), rect, 1)

                unit = self.grid[row][col]
                if unit:
                    if isinstance(unit, GoldMine):
                        gold_text = self.font.render(str(unit.stored_gold), True, (255, 255, 0))
                        surface.blit(gold_text, rect.topleft)

                    # Draw a filled tile for now (optional)
                    pygame.draw.rect(surface, (0, 128, 255), rect)

                    # Draw unit name centered
                    name_text = self.font.render(unit._name, True, (255, 255, 255))
                    text_rect = name_text.get_rect(center=rect.center)
                    surface.blit(name_text, text_rect)

    def place_unit(self, x, y, unit):
        col = (x - self.offset_x) // self.tile_size
        row = (y - self.offset_y) // self.tile_size

        if 0 <= row < self.rows and 0 <= col < self.cols:
            if self.grid[row][col] is None:
                self.grid[row][col] = unit
                return True, (row, col)
            else:
                return False, "Tile already occupied."
        return False, "Clicked outside the grid."

    def get_cell_at(self, x, y):
        """Returns the (row, col) of the cell that was clicked, or None if out of bounds."""
        col = (x - self.offset_x) // self.tile_size
        row = (y - self.offset_y) // self.tile_size

        if 0 <= row < self.rows and 0 <= col < self.cols:
            return row, col
        return None
