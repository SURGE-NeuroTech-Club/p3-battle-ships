
# Screen and Grid Dimensions
ROWS = 6
COLS = 6
CELL_SIZE = 100  # Size of each cell in pixels
GRID_MARGIN = 50  # Space around the grid
INFO_PANEL_HEIGHT = 50  # Space at the top for info

# --- NEW: Cell ID Settings ---
ROW_LABELS = "123456"
COL_LABELS = "ABCDEF"

# --- NEW: Button Panel Settings ---
BUTTON_PANEL_TOP_MARGIN = 20
BUTTON_COLS = 9  # How many buttons per row
BUTTON_ROWS = 4  # (9 * 4 = 36)
BUTTON_WIDTH = 70
BUTTON_HEIGHT = 40
BUTTON_MARGIN = 10

# Calculate panel height based on button layout
BUTTON_PANEL_HEIGHT = (BUTTON_ROWS * (BUTTON_HEIGHT + BUTTON_MARGIN)) + BUTTON_MARGIN

# Calculate screen size
SCREEN_WIDTH = COLS * CELL_SIZE + 2 * GRID_MARGIN
# NEW: Add button panel height to total screen height
SCREEN_HEIGHT = (
    ROWS * CELL_SIZE + 2 * GRID_MARGIN + 
    INFO_PANEL_HEIGHT + BUTTON_PANEL_TOP_MARGIN + 
    BUTTON_PANEL_HEIGHT
)

# Game Settings
FPS = 60
GAME_TITLE = "SSVEP Battleship - Placement Phase"

# SSVEP Flicker Settings
BASE_FLICKER_RATE_MS = 300
FLICKER_RATE_INCREMENT = 8 
STIM_TIME_MS = 500
INTER_STIM_TIME_MS = 100  # Time between stimuli when no row/col is highlighted

# Colors (R, G, B)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GRID_BG = (20, 20, 40)  # Dark blue background
COLOR_CELL_OFF = (50, 50, 50)  # Dark gray
COLOR_CELL_ON = (100, 100, 100) # Light gray (the 'flash')
COLOR_SHIP_BG = (10, 80, 120)  # Darker blue for background of placed ship
COLOR_CURSOR = (0, 255, 0)      # Bright green for the selector
COLOR_CELL_DISABLED = (40, 0, 0) # NEW: Dark red for disabled cell

# --- NEW: Button Colors ---
COLOR_BUTTON = (50, 50, 150)
COLOR_BUTTON_DISABLED = (30, 30, 30)
COLOR_BUTTON_TEXT = (255, 255, 255)
COLOR_BUTTON_TEXT_DISABLED = (80, 80, 80)

# Image Paths
SHIP_IMAGE_PATH = 'ship.png'