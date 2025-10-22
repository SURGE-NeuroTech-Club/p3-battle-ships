

import pygame
import settings


class GridButton(pygame.sprite.Sprite):
    """
    Represents a single clickable button that corresponds to a Cell.
    """

    def __init__(self, cell_id, x, y):
        super().__init__()

        self.cell_id = cell_id
        self.state = 'enabled'  # Can be 'enabled' or 'disabled'

        self.width = settings.BUTTON_WIDTH
        self.height = settings.BUTTON_HEIGHT

        # --- Pygame Sprite setup ---
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect(topleft=(x, y))

        # --- Font and Text ---
        self.font = pygame.font.SysFont(None, 30)

        # Render the button's appearance
        self._update_image()

    def _update_image(self):
        """Internal helper to redraw the button's appearance based on state."""
        if self.state == 'enabled':
            bg_color = settings.COLOR_BUTTON
            text_color = settings.COLOR_BUTTON_TEXT
        else:  # 'disabled'
            bg_color = settings.COLOR_BUTTON_DISABLED
            text_color = settings.COLOR_BUTTON_TEXT_DISABLED

        self.image.fill(bg_color)

        # Draw text
        text_surf = self.font.render(self.cell_id, True, text_color)
        text_rect = text_surf.get_rect(center=self.image.get_rect().center)
        self.image.blit(text_surf, text_rect)

        # Draw border
        pygame.draw.rect(self.image, settings.COLOR_WHITE, self.image.get_rect(), 1)

    def handle_click(self):
        """
        Called when the button is clicked by the Game class.
        Disables the button and returns its cell_id for the game to process.
        Returns None if already disabled.
        """
        if self.state == 'enabled':
            self.state = 'disabled'
            self._update_image()  # Redraw with disabled appearance
            return self.cell_id

        return None