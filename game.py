import sys
import random

import pygame

import settings
from cell import Cell
from cursor import Cursor
from grid_button import GridButton
from ship import Ship


class Game:
    """
    The main game class.
    Manages the game loop, event handling, updating, and drawing.
    """

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.is_running = True

        # --- Game Objects ---
        self.all_sprites = pygame.sprite.Group()
        self.cursor_group = pygame.sprite.Group()
        self.button_group = pygame.sprite.Group()

        # Dictionaries for quick object access
        self.cells_by_pos = {}
        self.cells_by_id = {}
        self.buttons = {}

        self.placed_ships = []

        # --- Row/Column Highlighting with Random Selection ---
        self.available_rows = list(range(settings.ROWS))  # [0, 1, 2, 3, 4, 5]
        self.available_cols = list(range(settings.COLS))  # [0, 1, 2, 3, 4, 5]
        self.highlight_type = None  # 'row' or 'col'
        self.highlighted_index = None  # Which row or column is currently highlighted
        self.last_highlight_time = pygame.time.get_ticks()
        self.is_inter_stim_period = False  # Track if we're in the gap between stimuli
        
        # Initialize first stimulus
        self._select_next_highlight()

        self._create_grid()
        self._create_cursor()
        self._create_buttons()

        # --- UI ---
        self.font = pygame.font.SysFont(None, 36)

    def _create_grid(self):
        """Populates the grid with Cell objects."""
        print("Creating 6x6 grid...")
        for r in range(settings.ROWS):
            for c in range(settings.COLS):
                col_label = settings.COL_LABELS[c]
                row_label = settings.ROW_LABELS[r]
                cell_id = f"{col_label}{row_label}"

                cell = Cell(row=r, col=c, cell_id=cell_id)

                self.all_sprites.add(cell)
                self.cells_by_pos[(r, c)] = cell
                self.cells_by_id[cell_id] = cell

        print(f"Created {len(self.cells_by_pos)} cells.")

    def _create_cursor(self):
        """Creates the player's cursor."""
        self.cursor = Cursor()
        self.cursor_group.add(self.cursor)

    def _create_buttons(self):
        """Populates the button panel."""
        print("Creating 36 buttons...")
        panel_start_x = (settings.SCREEN_WIDTH - (settings.BUTTON_COLS * (
                    settings.BUTTON_WIDTH + settings.BUTTON_MARGIN)) + settings.BUTTON_MARGIN) / 2

        panel_start_y = (settings.GRID_MARGIN + settings.INFO_PANEL_HEIGHT + (
                    settings.ROWS * settings.CELL_SIZE) + settings.BUTTON_PANEL_TOP_MARGIN)

        cell_ids = sorted(self.cells_by_id.keys())

        for i, cell_id in enumerate(cell_ids):
            btn_row = i // settings.BUTTON_COLS
            btn_col = i % settings.BUTTON_COLS

            btn_x = panel_start_x + btn_col * (settings.BUTTON_WIDTH + settings.BUTTON_MARGIN)
            btn_y = panel_start_y + btn_row * (settings.BUTTON_HEIGHT + settings.BUTTON_MARGIN)

            button = GridButton(cell_id, btn_x, btn_y)
            self.button_group.add(button)
            self.buttons[cell_id] = button

    def run(self):
        """Starts the main game loop."""
        while self.is_running:
            self.clock.tick(settings.FPS)
            self._handle_events()
            self._update()
            self._draw()

        pygame.quit()
        sys.exit()

    def _handle_events(self):
        """Processes all user input and events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self._handle_button_click(event.pos)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_running = False

                if event.key == pygame.K_UP:
                    self.cursor.move(dr=-1, dc=0)
                elif event.key == pygame.K_DOWN:
                    self.cursor.move(dr=1, dc=0)
                elif event.key == pygame.K_LEFT:
                    self.cursor.move(dr=0, dc=-1)
                elif event.key == pygame.K_RIGHT:
                    self.cursor.move(dr=0, dc=1)

                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    self._place_ship()

    def _handle_button_click(self, mouse_pos):
        """Check if a button was clicked and disable the corresponding cell."""
        for button in self.button_group:
            if button.rect.collidepoint(mouse_pos):
                cell_id_to_disable = button.handle_click()
                # Handle Cell Callback

                # if cell_id_to_disable:
                #     cell = self.cells_by_id.get(cell_id_to_disable)
                #     if cell:
                #         cell.disable()
                #         print(f"Button {cell_id_to_disable} clicked. Cell disabled.")
                #     break

    # --- MODIFIED METHOD ---
    def _place_ship(self):
        """Attempts to place a ship at the cursor's current position."""
        selected_pos = self.cursor.get_selected_pos()
        target_cell = self.cells_by_pos[selected_pos]

        if target_cell.state == 'disabled':
            print(f"Cannot place ship: Cell {target_cell.cell_id} is disabled.")
        elif target_cell.place_ship():
            # Ship was placed successfully
            new_ship = Ship(row=selected_pos[0], col=selected_pos[1])
            self.placed_ships.append(new_ship)
            print(f"Placed ship at {target_cell.cell_id}. Total ships: {len(self.placed_ships)}")

            # --- REMOVED ---  # The following 3 lines were removed to stop  # ship placement from disabling the button.  #  # button = self.buttons.get(target_cell.cell_id)  # if button:  #     button.handle_click()

        else:
            # Cell was already occupied
            print(f"Cannot place ship: Cell {target_cell.cell_id} is already occupied.")

    def _update(self):
        """Updates all game objects in the all_sprites group."""
        self._update_row_col_highlighting()
        self.all_sprites.update()
        self.cursor_group.update()
        self.button_group.update()
    
    def _update_row_col_highlighting(self):
        """
        Cycles through rows and columns with random selection and no replacement.
        - Randomly chooses row or column (50/50)
        - Selects without replacement from available pool
        - Refreshes pool when empty
        - Includes inter-stimulus interval where nothing is highlighted
        """
        current_time = pygame.time.get_ticks()
        
        if self.is_inter_stim_period:
            # We're in the gap between stimuli - check if it's time to show next stimulus
            if current_time - self.last_highlight_time >= settings.INTER_STIM_TIME_MS:
                self.last_highlight_time = current_time
                self.is_inter_stim_period = False
                self._select_next_highlight()
            
            # Turn off all highlights during inter-stimulus period
            for cell in self.cells_by_pos.values():
                cell.set_highlighted(False)
        else:
            # We're showing a stimulus - check if it's time to go to inter-stimulus period
            if current_time - self.last_highlight_time >= settings.STIM_TIME_MS:
                self.last_highlight_time = current_time
                self.is_inter_stim_period = True
            
            # Update all cells to reflect the current highlighting
            for (r, c), cell in self.cells_by_pos.items():
                if self.highlight_type == 'row' and r == self.highlighted_index:
                    cell.set_highlighted(True)
                elif self.highlight_type == 'col' and c == self.highlighted_index:
                    cell.set_highlighted(True)
                else:
                    cell.set_highlighted(False)
    
    def _select_next_highlight(self):
        """
        Randomly selects the next row or column to highlight.
        Uses random selection without replacement.
        """
        # Randomly choose between row and column (50/50 probability)
        self.highlight_type = random.choice(['row', 'col'])
        
        # Select from the appropriate pool
        if self.highlight_type == 'row':
            # If no rows available, refresh the pool
            if not self.available_rows:
                self.available_rows = list(range(settings.ROWS))
                print("Row pool refreshed")
            
            # Randomly select and remove a row from available pool
            self.highlighted_index = random.choice(self.available_rows)
            self.available_rows.remove(self.highlighted_index)
            print(f"Selected ROW {self.highlighted_index + 1} (remaining rows: {len(self.available_rows)})")
            
        else:  # 'col'
            # If no columns available, refresh the pool
            if not self.available_cols:
                self.available_cols = list(range(settings.COLS))
                print("Column pool refreshed")
            
            # Randomly select and remove a column from available pool
            self.highlighted_index = random.choice(self.available_cols)
            self.available_cols.remove(self.highlighted_index)
            col_label = settings.COL_LABELS[self.highlighted_index]
            print(f"Selected COLUMN {col_label} (remaining cols: {len(self.available_cols)})")

    def _draw_info_panel(self):
        """Draws the top info panel."""
        panel_rect = pygame.Rect(0, 0, settings.SCREEN_WIDTH, settings.INFO_PANEL_HEIGHT)
        pygame.draw.rect(self.screen, settings.COLOR_GRID_BG, panel_rect)

        ship_count = len(self.placed_ships)
        text = f"Ships Placed: {ship_count} | Use Arrows/Space or Click Buttons"
        text_surface = self.font.render(text, True, settings.COLOR_WHITE)

        text_rect = text_surface.get_rect(center=(settings.SCREEN_WIDTH / 2, settings.INFO_PANEL_HEIGHT / 2))
        self.screen.blit(text_surface, text_rect)

    def _draw_grid_labels(self):
        """Draws the A-F and 1-6 labels on the grid margins."""

        # 1. Draw Column Labels (A-F)
        for i, label in enumerate(settings.COL_LABELS):
            text_surf = self.font.render(label, True, settings.COLOR_WHITE)
            x_pos = settings.GRID_MARGIN + (i * settings.CELL_SIZE) + (settings.CELL_SIZE / 2)
            y_pos = settings.INFO_PANEL_HEIGHT + (settings.GRID_MARGIN / 2)
            text_rect = text_surf.get_rect(center=(x_pos, y_pos))
            self.screen.blit(text_surf, text_rect)

        # 2. Draw Row Labels (1-6)
        for i, label in enumerate(settings.ROW_LABELS):
            text_surf = self.font.render(label, True, settings.COLOR_WHITE)
            x_pos = settings.GRID_MARGIN / 2
            y_pos = (settings.INFO_PANEL_HEIGHT + settings.GRID_MARGIN + (i * settings.CELL_SIZE) + (
                        settings.CELL_SIZE / 2))
            text_rect = text_surf.get_rect(center=(x_pos, y_pos))
            self.screen.blit(text_surf, text_rect)

    def _draw(self):
        """Draws everything to the screen."""
        self.screen.fill(settings.COLOR_BLACK)

        self._draw_grid_labels()

        # Draw all cells (flashing, ships, disabled)
        self.all_sprites.draw(self.screen)

        # Draw the cursor on top
        self.cursor_group.draw(self.screen)

        # Draw all the buttons
        self.button_group.draw(self.screen)

        # Draw the UI
        self._draw_info_panel()

        pygame.display.flip()
