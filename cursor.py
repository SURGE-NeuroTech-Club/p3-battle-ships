
import pygame
import settings


class Cursor(pygame.sprite.Sprite):
    """
    A visual indicator for the currently selected cell.
    This is what the user controls (with keys now, with SSVEP later).
    """

    def __init__(self):
        super().__init__()
        self.size = settings.CELL_SIZE

        # Create a transparent surface for the cursor
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        # Draw a thick, bright border
        pygame.draw.rect(
            self.image,
            settings.COLOR_CURSOR,
            self.image.get_rect(),
            4  # Border thickness
        )

        self.rect = self.image.get_rect(topleft=(0, 0))
        self.row = 0
        self.col = 0
        self._update_position()

    def _update_position(self):
        """Internal helper to move the cursor rect to the correct screen coords."""
        self.rect.topleft = (
            settings.GRID_MARGIN + self.col * self.size,
            settings.GRID_MARGIN + settings.INFO_PANEL_HEIGHT + self.row * self.size
        )

    def move(self, dr, dc):
        """
        Moves the cursor by a given delta in rows (dr) and columns (dc).
        Wraps around the grid.
        """
        self.row = (self.row + dr) % settings.ROWS
        self.col = (self.col + dc) % settings.COLS
        self._update_position()

    def get_selected_pos(self):
        """Returns the (row, col) of the currently selected cell."""
        return (self.row, self.col)