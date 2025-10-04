#!/usr/bin/env python3
"""
EcoSnake Game - Constants and Configuration
All game constants, colors, and configuration data
"""

# =============================================================================
# GAME TEXT CONFIGURATION
# =============================================================================

GAME_NAMES = {
    # Main game elements
    'game_title': 'EcoSnake Game',
    'game_subtitle': 'Environmental Protection Game',
    
    # Menu items
    'start_game': 'Start Game',
    'high_scores': 'High Scores',
    'settings': 'Settings',
    'exit': 'Exit',
    
    # Settings menu
    'select_character': 'Character',
    'select_background': 'Background',
    'select_garbage_bag': 'Garbage Bag',
    
    # UI messages
    'enter_player_name': 'ENTER PLAYER NAME',
    'type_your_name': 'Type your name here...',
    'game_over': 'GAME OVER!',
    'player': 'Player',
    'collected_trash': 'Collected Trash',
    'difficulty': 'Difficulty',
    'active': 'ACTIVE',
    'select_difficulty': 'Select Difficulty:',
    'no_scores_yet': 'No scores recorded yet!',
    'back_instruction': "Press ESC to go back",
    'confirm_button': 'ENTER - OK',
    'return_instruction': 'ESC - Go Back',
    'character_info': 'Character',
    'background_info': 'Background',
    'garbage_bag_info': 'Garbage Bag',
    'main_menu_instruction': 'ESC: Main Menu',
    'environmental_message': "Don't throw trash on the ground for a cleaner world!",
    'play_again_enter': 'Press ENTER to play again',
    'show_scores_s': 'Press S to show scores',
    'main_menu_esc': 'Press ESC for main menu',
    
    # Table headers  
    'rank': 'Rank',
    'name': 'Name',
    'score': 'Score',
    'difficulty_header': 'Difficulty',
    
    # Instructions
    'navigation_help': 'Use arrow keys to select, ENTER to confirm, ESC to exit',
    'name_length_rule': '2-12 characters',
    'exit_instruction': 'Press ESC to exit',
    'trash_collected': 'trash collected'
}

# =============================================================================
# COLOR PALETTE
# =============================================================================

BLACK = (20, 20, 30)
WHITE = (250, 250, 255)
GREEN = (46, 204, 113)
RED = (231, 76, 60)
BLUE = (52, 152, 219)
BROWN = (160, 116, 85)
YELLOW = (241, 196, 15)
GRAY = (149, 165, 166)
NEON_GREEN = (39, 174, 96)
PURPLE = (155, 89, 182)
ORANGE = (230, 126, 34)
CYAN = (26, 188, 156)
DARK_GRAY = (52, 73, 94)
LIGHT_GRAY = (200, 210, 215)
MENU_BOX_COLOR = (30, 30, 35)

# =============================================================================
# GAME ELEMENTS CONFIGURATION
# =============================================================================

# Characters
CHARACTERS_CONFIG = [
    {'name': 'Gardener', 'sprite': 'gardener.png'},
    {'name': 'Blonde Girl', 'sprite': 'blonde_girl.png'},
    {'name': 'Chubby Child', 'sprite': 'chubby_child.png'},
]

# Backgrounds
BACKGROUNDS_CONFIG = [
    {'name': 'Black', 'sprite': None},  # No sprite for black background
    {'name': 'Forest', 'sprite': 'forest.png'},
    {'name': 'Beach', 'sprite': 'beach.png'},
]

# Garbage bags
GARBAGE_BAGS_CONFIG = [
    {'name': 'Black Bag', 'sprite': 'black_bag.png'},
    {'name': 'Sweet Bag', 'sprite': 'sweet_bag.png'},
    {'name': 'Yellow Bag', 'sprite': 'yellow_bag.png'},
]

# Trash items
TRASH_ITEMS_CONFIG = [
    {'name': 'Apple', 'sprite': 'apple.png'},
    {'name': 'Banana', 'sprite': 'banana.png'},
    {'name': 'Bottle', 'sprite': 'bottle.png'},
    {'name': 'Can', 'sprite': 'can.png'},
    {'name': 'Glass Bottle', 'sprite': 'glass_bottle.png'},
    {'name': 'Plastic Pollution', 'sprite': 'plastic-pollution.png'},
]

# Difficulty levels
DIFFICULTY_CONFIG = [
    {'name': 'Easy', 'speed': 5, 'color': GREEN},
    {'name': 'Medium', 'speed': 10, 'color': ORANGE},
    {'name': 'Hard', 'speed': 18, 'color': RED},
]

# =============================================================================
# GAME SETTINGS
# =============================================================================

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
SQUARE_SIZE = 35

# =============================================================================
# GAME LOGIC CONSTANTS
# =============================================================================

TARGET_FPS = 60
# Tolerance and adjustment values
TRASH_COLLECTION_ADJUSTMENT = 8  # Subtracted from SQUARE_SIZE for generous collection
CURSOR_BLINK_FRAMES = 16  # Frames for cursor blink cycle

COLLISION_TOLERANCE = SQUARE_SIZE // 2  # For snake self-collision
TRASH_COLLECTION_TOLERANCE = SQUARE_SIZE - TRASH_COLLECTION_ADJUSTMENT  # More generous for trash collection
CURSOR_BLINK_INTERVAL = TARGET_FPS * CURSOR_BLINK_FRAMES  # Cursor blink timing

# =============================================================================
# USER INTERFACE CONSTANTS
# =============================================================================

# Base UI Layout
UI_AREA_HEIGHT = 45
UI_BORDER_HEIGHT = 2
UI_PADDING = 15
EDGE_MARGIN = 15

# Menu Positioning
MAIN_MENU_START_Y = 220
MENU_START_Y = 160
DIFFICULTY_START_Y = 220

# Menu Spacing
MENU_ITEM_SPACING = 60
MENU_ITEM_HEIGHT = 50
MENU_VERTICAL_SPACING = 140
DIFFICULTY_ITEM_SPACING = 50

# Name Input Positioning
NAME_INPUT_Y = 220
NAME_INPUT_TITLE_Y = 150
NAME_INPUT_RULE_Y = 300
NAME_INPUT_CONFIRM_Y = 380
NAME_INPUT_ESC_Y = 420

# Game Over Screen Positioning
GAME_OVER_OPTION_Y_START = 350
GAME_OVER_OPTION_Y_SPACING = 30

# Table and Line Positioning
HIGH_SCORES_TABLE_POSITIONS = [150, 200, 400, 500]
TITLE_LINE_Y = 110
TITLE_LINE_MARGIN = 100
SETTINGS_LINE_MARGIN = 100
SETTINGS_SEPARATOR_LINE_Y = 112

# Dynamic positioning
TITLE_Y_OFFSET = WINDOW_HEIGHT // 10  # 80 at default 600px height
MAIN_TITLE_Y_OFFSET = WINDOW_HEIGHT // 6  # 100 at default 600px height
SUBTITLE_Y_OFFSET = MAIN_TITLE_Y_OFFSET + 40

# Menu item positioning helpers
MENU_BOX_VERTICAL_CENTER = 120 // 2  # MENU_BOX_HEIGHT // 2
MENU_BOX_SPRITE_CENTER_Y = 40  # Vertical center for sprites in menu boxes
MENU_BOX_NAME_CENTER_Y = 30   # Vertical center for name text in menu boxes
MENU_BOX_ACTIVE_CENTER_Y = 60  # Vertical center for active indicator

# Text positioning offsets
MENU_TEXT_X_POSITION = 280  # Horizontal position for menu text from box left
CURSOR_TEXT_SPACING = 3     # Space between text and cursor
INFO_TEXT_Y_BOTTOM = WINDOW_HEIGHT - 80  # 520 at default 600px height
SETTINGS_BACK_Y = WINDOW_HEIGHT - 180    # 420 at default 600px height

# Character info positioning (top-left corner)
CHARACTER_INFO_START_X = 20
CHARACTER_INFO_START_Y = 20
CHARACTER_INFO_LINE_HEIGHT = 20

# Game over screen positioning
GAME_OVER_TITLE_Y = MAIN_TITLE_Y_OFFSET  # 100 at default 600px height
GAME_OVER_PLAYER_Y = WINDOW_HEIGHT * 170 // 600  # 170 at default, scales with window
GAME_OVER_SCORE_Y = WINDOW_HEIGHT * 200 // 600   # 200 at default, scales with window  
GAME_OVER_DIFFICULTY_Y = WINDOW_HEIGHT * 230 // 600  # 230 at default, scales with window
GAME_OVER_MESSAGE_Y = WINDOW_HEIGHT * 290 // 600  # 290 at default, scales with window
GAME_OVER_EXIT_Y = WINDOW_HEIGHT * 450 // 600     # 450 at default, scales with window

# High scores "no scores" message position
HIGH_SCORES_NO_SCORES_Y = WINDOW_HEIGHT * 200 // 600  # 200 at default, scales with window

# High scores table positioning
HIGH_SCORES_TABLE_START_Y = WINDOW_HEIGHT * 130 // 600  # 130 at default, scales with window
HIGH_SCORES_HEADER_SPACING = 25  # Space after headers
HIGH_SCORES_LINE_SPACING = 15    # Space after header line
HIGH_SCORES_ROW_SPACING = 25     # Space between score rows

# Trash spawn boundaries (in grid units, not pixels)
TRASH_SPAWN_MARGIN_X = 1  # Minimum distance from left/right edges  
TRASH_SPAWN_MARGIN_Y = 3  # Minimum distance from top (accounts for UI area)
TRASH_SPAWN_EDGE_BUFFER = 2  # Buffer from right/bottom edges

# High scores configuration
MAX_HIGH_SCORES = 10  # Maximum number of high scores to keep and display

# High score ranking colors (in order from 1st place to last)
HIGH_SCORE_COLORS = [YELLOW, LIGHT_GRAY, ORANGE] + [CYAN] * 2 + [GRAY] * (MAX_HIGH_SCORES - 5)

# Dimensions & Sizing
MENU_BOX_WIDTH = 500
MENU_BOX_HEIGHT = 120
MAIN_MENU_BOX_WIDTH = 250
MAIN_MENU_BOX_HEIGHT = 50
DIFFICULTY_BOX_WIDTH = 200
DIFFICULTY_BOX_HEIGHT = 40

# Input Field Dimensions
NAME_INPUT_WIDTH = 400
NAME_INPUT_HEIGHT = 60

# Sprite Dimensions
LARGE_SPRITE_SIZE = 80

# Text Constraints
MAX_NAME_LENGTH = 12
MIN_NAME_LENGTH = 2

# Visual Styling
MENU_BOX_BORDER_WIDTH = 2
MENU_BOX_BORDER_WIDTH_SELECTED = 4
NAME_INPUT_BORDER_WIDTH = 3
LINE_BORDER_WIDTH = 3
THIN_LINE_WIDTH = 1
CURSOR_LINE_WIDTH = 2
MAIN_MENU_BORDER_WIDTH = 3
SETTINGS_MENU_BORDER_WIDTH = 3
DIFFICULTY_MENU_BORDER_WIDTH = 3

# Border Radius
MENU_BOX_RADIUS = 15
NAME_INPUT_RADIUS = 10
BACKGROUND_PREVIEW_RADIUS = 5
MAIN_MENU_RADIUS = 12
SETTINGS_MENU_RADIUS = 10
DIFFICULTY_MENU_RADIUS = 10

# Box Offsets and Padding
MENU_BOX_Y_OFFSET = 20
MAIN_MENU_BOX_Y_OFFSET = 25
DIFFICULTY_BOX_Y_OFFSET = 20
MAIN_MENU_INNER_PADDING = 5
MAIN_MENU_INNER_REDUCTION = 10

# Spacing and Margins
CURSOR_MARGIN = 15
HIGH_SCORES_TABLE_EXTENSION = 80