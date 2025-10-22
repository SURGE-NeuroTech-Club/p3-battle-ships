
import pygame
import settings


class Cell(pygame.sprite.Sprite):
    """
    Represents a single cell on the game grid.
    Each cell manages its own state (empty, ship, disabled) and
    its own SSVEP visual flicker.
    """

    def __init__(self, row, col, cell_id):
        super().__init__()

        self.row = row
        self.col = col
        self.cell_id = cell_id  # NEW: Store the cell's ID (e.g., "A1")
        self.state = 'empty'  # Can be 'empty', 'ship', or 'disabled'

        # --- Positioning ---
        self.size = settings.CELL_SIZE
        self.x_pos = settings.GRID_MARGIN + self.col * self.size
        self.y_pos = settings.GRID_MARGIN + settings.INFO_PANEL_HEIGHT + self.row * self.size

        # --- Pygame Sprite setup ---
        self.image = pygame.Surface((self.size, self.size))
        self.rect = self.image.get_rect(topleft=(self.x_pos, self.y_pos))

        # --- SSVEP Flicker Logic ---
        self.is_lit = False
        cell_index = (self.row * settings.COLS) + self.col
        self.flicker_rate = settings.BASE_FLICKER_RATE_MS + (cell_index * settings.FLICKER_RATE_INCREMENT)
        self.last_flicker_time = pygame.time.get_ticks()

        # --- Ship Image ---
        self.ship_image = None
        try:
            original_ship_image = pygame.image.load(settings.SHIP_IMAGE_PATH).convert_alpha()
            self.ship_image = pygame.transform.scale(original_ship_image, (self.size, self.size))
        except pygame.error as e:
            print(f"Warning: Could not load ship image '{settings.SHIP_IMAGE_PATH}': {e}")

    def update(self):
        """
        Update is called once per frame.
        This handles the cell's flicker logic and visual state.
        """
        # Only flicker if the cell is 'empty'
        if self.state == 'empty':
            self._handle_flicker()
        else:
            self.is_lit = False  # Stop flashing if 'ship' or 'disabled'

        self._draw_cell()

    def _handle_flicker(self):
        """Toggles the 'is_lit' state based on its unique flicker_rate."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_flicker_time > self.flicker_rate:
            self.is_lit = not self.is_lit
            self.last_flicker_time = current_time

    def _draw_cell(self):
        """Updates the cell's self.image Surface with the correct color/image."""

        if self.state == 'empty':
            # Apply flicker if empty
            final_color = settings.COLOR_CELL_ON if self.is_lit else settings.COLOR_CELL_OFF
            self.image.fill(final_color)

        elif self.state == 'ship':
            # Cell with a ship doesn't flicker and displays the ship image
            self.image.fill(settings.COLOR_SHIP_BG)
            if self.ship_image:
                self.image.blit(self.ship_image, (0, 0))

        elif self.state == 'disabled':
            # NEW: Draw the disabled state (dark red)
            self.image.fill(settings.COLOR_CELL_DISABLED)

        # Draw a border around the cell (always)
        pygame.draw.rect(self.image, settings.COLOR_WHITE, self.image.get_rect(), 1)

    def place_ship(self):
        """
        Sets the cell's state to 'ship'.
        Returns False if already occupied or disabled.
        """
        if self.state == 'empty':
            self.state = 'ship'
            self.is_lit = False  # Stop flashing
            return True
        return False

    def disable(self):
        """
        NEW: Sets the cell's state to 'disabled'.
        This is called when the corresponding button is clicked.
        """
        if self.state == 'empty':  # Can only disable empty cells
            self.state = 'disabled'
            self.is_lit = False  # Stop flashing
            return True
        return False