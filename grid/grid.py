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
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hover_col = (mouse_x - self.offset_x) // self.tile_size
        hover_row = (mouse_y - self.offset_y) // self.tile_size

        for row in range(self.rows):
            for col in range(self.cols):
                rect = pygame.Rect(
                    self.offset_x + col * self.tile_size,
                    self.offset_y + row * self.tile_size,
                    self.tile_size,
                    self.tile_size
                )

                # Alternate tile color
                tile_color = (220, 220, 220) if (row + col) % 2 == 0 else (200, 200, 200)


                # Draw hover effect
                if row == hover_row and col == hover_col:
                    pygame.draw.rect(surface, (255, 255, 0), rect, 3)  # yellow border
                else:
                    pygame.draw.rect(surface, (160, 160, 160), rect, 1)  # regular border

                unit = self.grid[row][col]
                if unit:
                    if hasattr(unit, "image"):
                        surface.blit(unit.image, rect.topleft)

                    if isinstance(unit, GoldMine):
                        gold_text = self.font.render(str(unit.stored_gold), True, (255, 255, 0))
                        surface.blit(gold_text, rect.topleft)

                    # Optional: unit name in center
                    name_text = self.font.render(unit._name, True, (255, 255, 255))
                    text_rect = name_text.get_rect(center=rect.center)
                    surface.blit(name_text, text_rect)
                    grid_rect = pygame.Rect(
                        self.offset_x,
                        self.offset_y,
                        self.cols * self.tile_size,
                        self.rows * self.tile_size
                    )
                    pygame.draw.rect(surface, (100, 100, 100), grid_rect, 3)
                    pygame.draw.rect(surface, (255, 215, 0), grid_rect, 5)

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
        col = (x - self.offset_x) // self.tile_size
        row = (y - self.offset_y) // self.tile_size

        if 0 <= row < self.rows and 0 <= col < self.cols:
            return row, col
        return None



