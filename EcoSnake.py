#!/usr/bin/env python3
"""
EcoSnake Game - Environmental Protection Themed Snake Game
Copyright (c) 2025 Sqap85

This project is published under the MIT license.
See the LICENSE file for details.
"""

import pygame
import os
import random
import sys
import json

os.chdir(os.path.dirname(os.path.abspath(__file__)))
pygame.init()

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
COLLISION_TOLERANCE = SQUARE_SIZE // 2  # For snake self-collision
TRASH_COLLECTION_TOLERANCE = SQUARE_SIZE - 8  # More generous for trash collection
CURSOR_BLINK_INTERVAL = TARGET_FPS * 16  # 16 frames = ~267ms at 60fps

# =============================================================================
# USER INTERFACE CONSTANTS
# =============================================================================

# ┌─────────────────────────────────────────────────────────────────────────────┐
# │                            LAYOUT & POSITIONING                             │
# └─────────────────────────────────────────────────────────────────────────────┘

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

# ┌─────────────────────────────────────────────────────────────────────────────┐
# │                           DIMENSIONS & SIZING                               │
# └─────────────────────────────────────────────────────────────────────────────┘

# Menu Box Dimensions
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

# ┌─────────────────────────────────────────────────────────────────────────────┐
# │                          VISUAL STYLING                                     │
# └─────────────────────────────────────────────────────────────────────────────┘

# Border Widths
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

# =============================================================================
# PYGAME INITIALIZATION
# =============================================================================

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("EcoSnake-Game")
clock = pygame.time.Clock()

# Create fonts
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 24)

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def load_sprite(filename, size=(SQUARE_SIZE, SQUARE_SIZE)):
    """Load and scale a sprite with error handling"""
    try:
        sprite = pygame.image.load(f"assets/{filename}")
        return pygame.transform.scale(sprite, size)
    except pygame.error as e:
        print(f"Warning: Could not load sprite '{filename}': {e}")
        # Create a placeholder colored rectangle
        placeholder = pygame.Surface(size)
        placeholder.fill(GRAY)
        return placeholder
    except FileNotFoundError:
        print(f"Warning: Sprite file 'assets/{filename}' not found")
        # Create a placeholder colored rectangle
        placeholder = pygame.Surface(size)
        placeholder.fill(GRAY)
        return placeholder

def draw_menu_box(screen, box_rect, selected=False):
    """Draw a menu box with selection highlighting"""
    if selected:
        pygame.draw.rect(screen, DARK_GRAY, box_rect, 0, MENU_BOX_RADIUS)
        pygame.draw.rect(screen, CYAN, box_rect, MENU_BOX_BORDER_WIDTH_SELECTED, MENU_BOX_RADIUS)
    else:
        pygame.draw.rect(screen, MENU_BOX_COLOR, box_rect, 0, MENU_BOX_RADIUS)
        pygame.draw.rect(screen, LIGHT_GRAY, box_rect, MENU_BOX_BORDER_WIDTH, MENU_BOX_RADIUS)

def draw_score_line(screen, i, score_info, y_pos, positions):
    """Draw a single score line in the high scores table"""
    colors = [YELLOW, LIGHT_GRAY, ORANGE, CYAN, CYAN, GRAY, GRAY, GRAY, GRAY, GRAY]
    color = colors[i] if i < len(colors) else GRAY
    
    texts = [f"{i+1}.", score_info['name'][:MAX_NAME_LENGTH], str(score_info['score']), score_info['difficulty']]
    for text, x_pos in zip(texts, positions):
        text_surface = small_font.render(text, True, color)
        screen.blit(text_surface, (x_pos, y_pos))

def generic_selection_menu(title_text, options, selected_option, get_sprite_func=None, get_active_func=None, on_select_func=None, preview_type=None):
    """Generic selection menu for character/background/garbage bag selection"""
    selected = options.index(selected_option) if selected_option in options else 0
    
    while True:
        screen.fill(BLACK)
        
        # Title
        title = large_font.render(title_text.upper(), True, CYAN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 80))
        screen.blit(title, title_rect)
        
        pygame.draw.line(screen, CYAN, (TITLE_LINE_MARGIN, TITLE_LINE_Y), (WINDOW_WIDTH-TITLE_LINE_MARGIN, TITLE_LINE_Y), LINE_BORDER_WIDTH)
        
        # Show options
        for i, name in enumerate(options):
            y = MENU_START_Y + i * MENU_VERTICAL_SPACING
            is_selected = (i == selected)
            
            box_x = WINDOW_WIDTH//2 - MENU_BOX_WIDTH//2
            box_rect = pygame.Rect(box_x, y-MENU_BOX_Y_OFFSET, MENU_BOX_WIDTH, MENU_BOX_HEIGHT)
            
            draw_menu_box(screen, box_rect, is_selected)
            
            # Show sprite/preview based on type
            if get_sprite_func:
                sprite = get_sprite_func(name)
                if sprite:
                    large_sprite = pygame.transform.scale(sprite, (LARGE_SPRITE_SIZE, LARGE_SPRITE_SIZE))
                    sprite_rect = large_sprite.get_rect(center=(box_x + LARGE_SPRITE_SIZE, y + 40))
                    screen.blit(large_sprite, sprite_rect)
            elif preview_type == 'background':
                # Special handling for background preview
                if name == 'Black':
                    preview_rect = pygame.Rect(0, 0, LARGE_SPRITE_SIZE, LARGE_SPRITE_SIZE)
                    preview_rect.center = (box_x + LARGE_SPRITE_SIZE, y + 40)
                    pygame.draw.rect(screen, BLACK, preview_rect, 0, BACKGROUND_PREVIEW_RADIUS)
                elif name in BACKGROUNDS:
                    try:
                        preview = pygame.transform.scale(BACKGROUNDS[name], (LARGE_SPRITE_SIZE, LARGE_SPRITE_SIZE))
                        sprite_rect = preview.get_rect(center=(box_x + LARGE_SPRITE_SIZE, y + 40))
                        screen.blit(preview, sprite_rect)
                    except (pygame.error, ValueError, TypeError):
                        color = GREEN if name == 'Forest' else BLUE
                        preview_rect = pygame.Rect(0, 0, LARGE_SPRITE_SIZE, LARGE_SPRITE_SIZE)
                        preview_rect.center = (box_x + LARGE_SPRITE_SIZE, y + 40)
                        pygame.draw.rect(screen, color, preview_rect, 0, BACKGROUND_PREVIEW_RADIUS)
            
            # Show name
            color = CYAN if is_selected else WHITE
            name_text = font.render(name, True, color)
            name_rect = name_text.get_rect(center=(box_x + 280, y + 30))
            screen.blit(name_text, name_rect)
            
            # Show active indicator
            if get_active_func and get_active_func(name):
                active_text = small_font.render(GAME_NAMES['active'], True, NEON_GREEN)
                active_rect = active_text.get_rect(center=(box_x + 280, y + 60))
                screen.blit(active_text, active_rect)
        
        pygame.display.flip()
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                safe_exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if on_select_func:
                        on_select_func(options[selected])
                    return

def safe_exit():
    """Safely exit the game"""
    pygame.quit()
    sys.exit()

# =============================================================================
# AUTO-GENERATED GAME DATA
# =============================================================================

# Auto-generated difficulty settings
SPEEDS = {
    diff['name']: diff['speed']
    for diff in DIFFICULTY_CONFIG
}

DIFFICULTY_COLORS = {
    diff['name']: diff['color']
    for diff in DIFFICULTY_CONFIG
}

# Auto-generated sprites
CHARACTERS = {
    char['name']: load_sprite(char['sprite']) 
    for char in CHARACTERS_CONFIG
}

TRASH_SPRITES = {
    item['name']: load_sprite(item['sprite'])
    for item in TRASH_ITEMS_CONFIG
}

GARBAGE_BAGS = {
    bag['name']: load_sprite(bag['sprite'])
    for bag in GARBAGE_BAGS_CONFIG
}

BACKGROUNDS = {
    bg['name']: load_sprite(bg['sprite'], (WINDOW_WIDTH, WINDOW_HEIGHT))
    for bg in BACKGROUNDS_CONFIG 
    if bg['sprite'] is not None 
}

# =============================================================================
# GAME STATE MANAGEMENT
# =============================================================================

class GameState:
    def __init__(self):
        self.player_name = ""
        # Default selections from configuration
        self.selected_character = CHARACTERS_CONFIG[0]['name']
        self.selected_background = BACKGROUNDS_CONFIG[0]['name']
        self.selected_garbage = GARBAGE_BAGS_CONFIG[0]['name']
    
    def save_settings(self):
        """Save current settings to JSON file with error handling"""
        settings = {
            'selected_character': self.selected_character,
            'selected_background': self.selected_background,
            'selected_garbage': self.selected_garbage
        }
        try:
            with open('settings.json', 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
        except (IOError, OSError) as e:
            print(f"Warning: Settings could not be saved: {e}")
        except Exception as e:
            print(f"Unexpected error saving settings: {e}")
    
    def load_settings(self):
        """Load settings from JSON file with comprehensive error handling"""
        try:
            with open('settings.json', 'r', encoding='utf-8') as f:
                settings = json.load(f)
                self.selected_character = settings.get('selected_character', CHARACTERS_CONFIG[0]['name'])
                self.selected_background = settings.get('selected_background', BACKGROUNDS_CONFIG[0]['name'])
                self.selected_garbage = settings.get('selected_garbage', GARBAGE_BAGS_CONFIG[0]['name'])
        except FileNotFoundError:
            print("Info: Settings file not found, using defaults")
            self._set_default_settings()
        except json.JSONDecodeError as e:
            print(f"Warning: Settings file corrupted ({e}), using defaults")
            self._set_default_settings()
        except (IOError, OSError) as e:
            print(f"Warning: Could not read settings file ({e}), using defaults")
            self._set_default_settings()
        except Exception as e:
            print(f"Unexpected error loading settings ({e}), using defaults")
            self._set_default_settings()
    
    def _set_default_settings(self):
        """Set default settings values"""
        # Default selections from configuration
        self.selected_character = CHARACTERS_CONFIG[0]['name']
        self.selected_background = BACKGROUNDS_CONFIG[0]['name']
        self.selected_garbage = GARBAGE_BAGS_CONFIG[0]['name']

# Global game state instance
game_state = GameState()

# =============================================================================
# PERFORMANCE OPTIMIZATION - TEXT CACHING
# =============================================================================

class TextCache:
    """Cache frequently used rendered text surfaces for better performance"""
    
    def __init__(self):
        self.cache = {}
        self.menu_texts = {}
        self.static_texts = {}
    
    def get_text(self, text, font, color, cache_key=None):
        """Get cached text surface or render and cache if not exists"""
        key = cache_key or f"{text}_{font}_{color}"
        
        if key not in self.cache:
            self.cache[key] = font.render(text, True, color)
        
        return self.cache[key]
    
    def preload_menu_texts(self):
        """Preload commonly used menu texts for better performance"""
        # Main menu texts
        for text in [GAME_NAMES['start_game'], GAME_NAMES['high_scores'], 
                    GAME_NAMES['settings'], GAME_NAMES['exit']]:
            self.menu_texts[f"main_{text}_white"] = font.render(text, True, WHITE)
            self.menu_texts[f"main_{text}_gray"] = font.render(text, True, LIGHT_GRAY)
        
        # Settings menu texts
        for text in [GAME_NAMES['select_character'], GAME_NAMES['select_background'], 
                    GAME_NAMES['select_garbage_bag']]:
            self.menu_texts[f"settings_{text}_white"] = font.render(text, True, WHITE)
            self.menu_texts[f"settings_{text}_gray"] = font.render(text, True, LIGHT_GRAY)
        
        # Static texts
        self.static_texts['navigation_help'] = small_font.render(GAME_NAMES['navigation_help'], True, GRAY)
        self.static_texts['back_instruction'] = font.render(GAME_NAMES['back_instruction'], True, GRAY)
        self.static_texts['name_length_rule'] = small_font.render(GAME_NAMES['name_length_rule'], True, GRAY)
        self.static_texts['return_instruction'] = small_font.render(GAME_NAMES['return_instruction'], True, GRAY)
    
    def get_menu_text(self, menu_type, text, selected=False):
        """Get cached menu text with selection state"""
        color_suffix = "white" if selected else "gray"
        key = f"{menu_type}_{text}_{color_suffix}"
        return self.menu_texts.get(key)
    
    def clear_cache(self):
        """Clear all cached texts"""
        self.cache.clear()
        self.menu_texts.clear()
        self.static_texts.clear()

# Global text cache instance
text_cache = TextCache()

# =============================================================================
# GAME MANAGEMENT CLASSES
# =============================================================================

class GameSession:
    """Manages a single game session from start to finish"""
    
    def __init__(self, player_name, difficulty_name, game_speed):
        self.player_name = player_name
        self.difficulty_name = difficulty_name
        self.game_speed = game_speed
        self.score = 0
        self.collector = None
        self.trash = None
        self.last_dir = (1, 0)
        self.frame_counter = 0
        
        # Performance optimizations
        self.cached_background = None
        self.cached_ui_background = None
        self.cached_esc_text = None
        self.cached_player_text = None
        self.last_score = -1  # Track score changes for text re-rendering
        
    def initialize_game_objects(self):
        """Initialize game objects for a new session"""
        self.collector = TrashCollector(CHARACTERS[game_state.selected_character])
        self.trash = Trash()
        self.score = 0
        self.last_dir = (1, 0)
        self.frame_counter = 0
        
        # Initialize performance caches
        self._cache_background()
        self._cache_ui_elements()
    
    def _cache_background(self):
        """Cache the background surface to avoid repeated blitting"""
        self.cached_background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        
        if game_state.selected_background in BACKGROUNDS:
            self.cached_background.blit(BACKGROUNDS[game_state.selected_background], (0, 0))
        else:
            self.cached_background.fill(BLACK)
    
    def _cache_ui_elements(self):
        """Cache static UI elements that don't change frequently"""
        # Cache UI background (top bar)
        self.cached_ui_background = pygame.Surface((WINDOW_WIDTH, UI_AREA_HEIGHT))
        self.cached_ui_background.fill(DARK_GRAY)
        
        # Draw the bottom border on cached surface
        pygame.draw.rect(self.cached_ui_background, LIGHT_GRAY, 
                        (0, UI_AREA_HEIGHT - UI_BORDER_HEIGHT, WINDOW_WIDTH, UI_BORDER_HEIGHT))
        
        # Cache ESC instruction text (never changes during gameplay)
        self.cached_esc_text = small_font.render(GAME_NAMES['main_menu_instruction'], True, LIGHT_GRAY)
    
    def handle_input(self, events):
        """Handle player input during gameplay"""
        for event in events:
            if event.type == pygame.QUIT:
                safe_exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'escape'
                
                new_dir = None
                if event.key == pygame.K_UP and self.last_dir != (0, 1):
                    new_dir = (0, -1)
                elif event.key == pygame.K_DOWN and self.last_dir != (0, -1):
                    new_dir = (0, 1)
                elif event.key == pygame.K_LEFT and self.last_dir != (1, 0):
                    new_dir = (-1, 0)
                elif event.key == pygame.K_RIGHT and self.last_dir != (-1, 0):
                    new_dir = (1, 0)
                
                if new_dir:
                    self.collector.dir_x, self.collector.dir_y = new_dir
                    self.last_dir = new_dir
        return None
    
    def update_game_state(self):
        """Update game state and check for collisions"""
        self.frame_counter += 1
        
        move_time = False
        if self.frame_counter >= (TARGET_FPS // self.game_speed):
            self.frame_counter = 0
            move_time = True
            old_tail = self.collector.squares[-1]
            self.collector.move()
            
            # Check collision right after movement
            if self.collector.check_collision():
                return 'collision'
        
        # Check trash collection
        head_x, head_y = self.collector.squares[0]
        distance_x = abs(head_x - self.trash.x)
        distance_y = abs(head_y - self.trash.y)
        collision = (distance_x <= TRASH_COLLECTION_TOLERANCE) and (distance_y <= TRASH_COLLECTION_TOLERANCE)
        
        if collision:
            if move_time:
                self.collector.squares.append(old_tail)
            else:
                self.collector.squares.append(self.collector.squares[-1])
            
            self.score += 1
            self.trash = Trash()
        
        return None
    
    def render(self):
        """Render the game screen with performance optimizations"""
        # Use cached background instead of repeated blitting/filling
        screen.blit(self.cached_background, (0, 0))
            
        self.collector.draw(screen)
        self.trash.draw(screen)
        
        # Use cached UI background
        screen.blit(self.cached_ui_background, (0, 0))
        
        # Left side - Player info (only re-render when score changes)
        if self.score != self.last_score:
            self.cached_player_text = small_font.render(
                f"{self.player_name}: {self.score} {GAME_NAMES['trash_collected']}", 
                True, LIGHT_GRAY
            )
            self.last_score = self.score
        
        screen.blit(self.cached_player_text, (UI_PADDING, UI_PADDING))
        
        # Right side - ESC info (use cached text)
        esc_width = self.cached_esc_text.get_width()
        screen.blit(self.cached_esc_text, (WINDOW_WIDTH - esc_width - UI_PADDING, UI_PADDING))
        
        pygame.display.flip()
    
    def play(self):
        """Main game loop for this session"""
        self.initialize_game_objects()
        game_over = False
        return_to_main = False
        
        while not game_over and not return_to_main:
            events = pygame.event.get()
            
            input_result = self.handle_input(events)
            if input_result == 'escape':
                return_to_main = True
                break
            
            update_result = self.update_game_state()
            if update_result == 'collision':
                game_over = True
                break
            
            self.render()
            clock.tick(TARGET_FPS)
        
        if return_to_main:
            return 'menu'
        elif game_over:
            return game_over_screen(self.score, self.difficulty_name)


class GameManager:
    """Manages the overall game flow and state"""
    
    def __init__(self):
        self.running = True
    
    def setup_new_session(self):
        """Setup a new game session with player name and difficulty"""
        # Player name input
        if not enter_name():
            return None, None, None
        
        # Difficulty selection
        game_speed, difficulty_name = select_difficulty()
        
        if game_speed is None or difficulty_name is None:
            game_state.player_name = ""
            return None, None, None
        
        return game_state.player_name, difficulty_name, game_speed
    
    def run_game_session(self, player_name, difficulty_name, game_speed):
        """Run a complete game session"""
        while True:
            session = GameSession(player_name, difficulty_name, game_speed)
            result = session.play()
            
            if result == 'menu':
                break
            elif result == 'replay':
                continue
            else:
                break
    
    def run(self):
        """Main application loop"""
        game_state.load_settings()
        
        while self.running:
            menu_choice = main_menu()
            
            if menu_choice == 'settings':
                settings_menu()
                continue
            elif menu_choice != 'game':
                continue
            
            # Setup new game session
            player_name, difficulty_name, game_speed = self.setup_new_session()
            
            if player_name is None:
                continue
            
            # Run the game session
            self.run_game_session(player_name, difficulty_name, game_speed)

# =============================================================================
# GAME OBJECTS
# =============================================================================

class TrashCollector:
    def __init__(self, character_sprite):
        self.dir_x = 1
        self.dir_y = 0
        self.squares = []
        self.character_sprite = character_sprite
        start_x = (WINDOW_WIDTH // 2 // SQUARE_SIZE) * SQUARE_SIZE
        start_y = (WINDOW_HEIGHT // 2 // SQUARE_SIZE) * SQUARE_SIZE
        self.squares.append((start_x, start_y))

    def move(self):
        head_x, head_y = self.squares[0]
        new_x = head_x + self.dir_x * SQUARE_SIZE
        new_y = head_y + self.dir_y * SQUARE_SIZE
        
        if new_x < 0:
            new_x = WINDOW_WIDTH - SQUARE_SIZE
        elif new_x >= WINDOW_WIDTH:
            new_x = 0
            
        if new_y < UI_AREA_HEIGHT:
            new_y = WINDOW_HEIGHT - SQUARE_SIZE
        elif new_y >= WINDOW_HEIGHT:
            new_y = UI_AREA_HEIGHT
            
        new_head = (new_x, new_y)
        self.squares = [new_head] + self.squares[:-1]

    def draw(self, screen):
        head_x, head_y = self.squares[0]
        screen.blit(self.character_sprite, (head_x, head_y))
        selected_garbage_sprite = GARBAGE_BAGS[game_state.selected_garbage]
        for (x, y) in self.squares[1:]:
            screen.blit(selected_garbage_sprite, (x, y))

    def check_collision(self):
        head_x, head_y = self.squares[0]
        # Check if head collides with any body segment with tolerance
        for segment_x, segment_y in self.squares[1:]:
            if (abs(head_x - segment_x) <= COLLISION_TOLERANCE and 
                abs(head_y - segment_y) <= COLLISION_TOLERANCE):
                return True
        return False

class Trash:
    def __init__(self):
        min_x = 1
        max_x = (WINDOW_WIDTH // SQUARE_SIZE) - 2
        min_y = 3
        max_y = (WINDOW_HEIGHT // SQUARE_SIZE) - 2
        
        self.x = random.randint(min_x, max_x) * SQUARE_SIZE
        self.y = random.randint(min_y, max_y) * SQUARE_SIZE
        
        self.type = random.choice(list(TRASH_SPRITES.keys()))
        self.sprite = TRASH_SPRITES[self.type]
    
    def draw(self, screen):
        screen.blit(self.sprite, (self.x, self.y))

# =============================================================================
# FILE MANAGEMENT FUNCTIONS
# =============================================================================
def save_score(name, score, difficulty):
    """Save player score with comprehensive error handling"""
    try:
        with open('highscores.json', 'r') as f:
            scores = json.load(f)
    except FileNotFoundError:
        print("Info: High scores file not found, creating new one")
        scores = []
    except json.JSONDecodeError as e:
        print(f"Warning: High scores file corrupted ({e}), starting fresh")
        scores = []
    except (IOError, OSError) as e:
        print(f"Warning: Could not read high scores ({e}), starting fresh")
        scores = []
    
    # Check if player with same name exists
    existing_player_index = -1
    for i, player in enumerate(scores):
        if player['name'] == name:
            existing_player_index = i
            break
    
    new_score = {
        'name': name,
        'score': score,
        'difficulty': difficulty
    }
    
    if existing_player_index != -1:
        # If player exists, only update if score is better
        if score > scores[existing_player_index]['score']:
            scores[existing_player_index] = new_score
    else:
        # Add new player
        scores.append(new_score)
    
    scores.sort(key=lambda x: x['score'], reverse=True)
    scores = scores[:10]
    
    try:
        with open('highscores.json', 'w') as f:
            json.dump(scores, f, indent=2)
    except (IOError, OSError) as e:
        print(f"Warning: Could not save high scores: {e}")
    except Exception as e:
        print(f"Unexpected error saving high scores: {e}")

def show_high_scores():
    """Display high scores with error handling"""
    try:
        with open('highscores.json', 'r') as f:
            scores = json.load(f)
    except FileNotFoundError:
        scores = []
    except json.JSONDecodeError as e:
        print(f"Warning: High scores file corrupted ({e})")
        scores = []
    except (IOError, OSError) as e:
        print(f"Warning: Could not read high scores ({e})")
        scores = []
    
    while True:
        screen.fill(BLACK)
        title = large_font.render(GAME_NAMES['high_scores'].upper(), True, CYAN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 80))
        screen.blit(title, title_rect)
        
        
        if not scores:
            message = font.render(GAME_NAMES['no_scores_yet'], True, WHITE)
            message_rect = message.get_rect(center=(WINDOW_WIDTH//2, 200))
            screen.blit(message, message_rect)
        else:
            y_pos = 130
            positions = HIGH_SCORES_TABLE_POSITIONS
            headers = [GAME_NAMES['rank'], GAME_NAMES['name'], GAME_NAMES['score'], GAME_NAMES['difficulty_header']]
            
            for header, x_pos in zip(headers, positions):
                text = small_font.render(header, True, WHITE)
                screen.blit(text, (x_pos, y_pos))
            
            y_pos += 25
            pygame.draw.line(screen, WHITE, (positions[0], y_pos), (positions[-1] + HIGH_SCORES_TABLE_EXTENSION, y_pos), THIN_LINE_WIDTH)
            y_pos += 15
            
            for i, score_info in enumerate(scores[:10]):
                draw_score_line(screen, i, score_info, y_pos, positions)
                y_pos += 25
        
        # Back info - use cached text
        back_info = text_cache.static_texts.get('back_instruction') or font.render(GAME_NAMES['back_instruction'], True, GRAY)
        back_rect = back_info.get_rect(center=(WINDOW_WIDTH//2, 520))
        screen.blit(back_info, back_rect)
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                safe_exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    return

# =============================================================================
# MENU & UI FUNCTIONS
# =============================================================================

def enter_name():
    input_text = ""
    while True:
        screen.fill(BLACK)
        
        # Title
        title = large_font.render(GAME_NAMES['enter_player_name'], True, YELLOW)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, NAME_INPUT_TITLE_Y))
        screen.blit(title, title_rect)
        
        # Input box 
        box_rect = pygame.Rect(WINDOW_WIDTH//2 - NAME_INPUT_WIDTH//2, NAME_INPUT_Y, NAME_INPUT_WIDTH, NAME_INPUT_HEIGHT)
        pygame.draw.rect(screen, MENU_BOX_COLOR, box_rect, 0, NAME_INPUT_RADIUS)
        pygame.draw.rect(screen, YELLOW if input_text else GRAY, box_rect, NAME_INPUT_BORDER_WIDTH, NAME_INPUT_RADIUS)
        
        # Show written text
        if input_text:
            text = font.render(input_text, True, WHITE)
        else:
            text = font.render(GAME_NAMES['type_your_name'], True, GRAY)
        text_rect = text.get_rect(center=box_rect.center)
        screen.blit(text, text_rect)
        
        # Cursor
        if pygame.time.get_ticks() % CURSOR_BLINK_INTERVAL < (CURSOR_BLINK_INTERVAL // 2):
            if input_text:
                cursor_x = text_rect.right + 3
            else:
                cursor_x = box_rect.left + UI_PADDING
            pygame.draw.line(screen, YELLOW, (cursor_x, box_rect.top + CURSOR_MARGIN), (cursor_x, box_rect.bottom - CURSOR_MARGIN), CURSOR_LINE_WIDTH)
        
        # Rules - use cached text
        rule = text_cache.static_texts.get('name_length_rule') or small_font.render(GAME_NAMES['name_length_rule'], True, GRAY)
        rule_rect = rule.get_rect(center=(WINDOW_WIDTH//2, NAME_INPUT_RULE_Y))
        screen.blit(rule, rule_rect)
        
        # Instructions
        enter_active = len(input_text.strip()) >= 2
        enter_color = GREEN if enter_active else GRAY
        enter_text = text_cache.get_text(GAME_NAMES['confirm_button'], font, enter_color, f"confirm_button_{enter_color}")
        enter_rect = enter_text.get_rect(center=(WINDOW_WIDTH//2, NAME_INPUT_CONFIRM_Y))
        screen.blit(enter_text, enter_rect)
        
        # Use cached return instruction text
        esc_text = text_cache.static_texts.get('return_instruction') or small_font.render(GAME_NAMES['return_instruction'], True, GRAY)
        esc_rect = esc_text.get_rect(center=(WINDOW_WIDTH//2, NAME_INPUT_ESC_Y))
        screen.blit(esc_text, esc_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                safe_exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_RETURN:
                    if len(input_text.strip()) >= 2:
                        game_state.player_name = input_text.strip()
                        return True
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if event.unicode.isprintable() and len(input_text) < MAX_NAME_LENGTH:
                        input_text += event.unicode

def select_character():
    character_names = list(CHARACTERS.keys())
    
    def get_sprite(name):
        return CHARACTERS[name]
    
    def is_active(name):
        return name == game_state.selected_character
    
    def on_select(name):
        game_state.selected_character = name
        game_state.save_settings()
    
    generic_selection_menu(
        GAME_NAMES['select_character'],
        character_names,
        game_state.selected_character,
        get_sprite_func=get_sprite,
        get_active_func=is_active,
        on_select_func=on_select
    )

def main_menu():
    options = [GAME_NAMES['start_game'], GAME_NAMES['high_scores'], GAME_NAMES['settings'], GAME_NAMES['exit']]
    selected = 0
    
    while True:
        screen.fill(BLACK)
        
        # Main title
        title = large_font.render(GAME_NAMES['game_title'], True, CYAN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 100))
        screen.blit(title, title_rect)
        
        subtitle = font.render(GAME_NAMES['game_subtitle'], True, NEON_GREEN)
        subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH//2, 140))
        screen.blit(subtitle, subtitle_rect)
        
        # Player info 
        character_text = small_font.render(f'{GAME_NAMES["character_info"]}: {game_state.selected_character}', True, WHITE)
        screen.blit(character_text, (20, 20))
        background_text = small_font.render(f'{GAME_NAMES["background_info"]}: {game_state.selected_background}', True, WHITE)
        screen.blit(background_text, (20, 40))
        garbage_text = small_font.render(f'{GAME_NAMES["garbage_bag_info"]}: {game_state.selected_garbage}', True, WHITE)
        screen.blit(garbage_text, (20, 60))
        
        # Menu options
        for i, option in enumerate(options):
            is_selected = (i == selected)
            y = MAIN_MENU_START_Y + i * MENU_ITEM_SPACING
            
            if is_selected:
                box_x = WINDOW_WIDTH//2 - MAIN_MENU_BOX_WIDTH//2
                pygame.draw.rect(screen, DARK_GRAY, (box_x, y-MAIN_MENU_BOX_Y_OFFSET, MAIN_MENU_BOX_WIDTH, MAIN_MENU_BOX_HEIGHT), 0, MAIN_MENU_RADIUS)
                pygame.draw.rect(screen, CYAN, (box_x, y-MAIN_MENU_BOX_Y_OFFSET, MAIN_MENU_BOX_WIDTH, MAIN_MENU_BOX_HEIGHT), MAIN_MENU_BORDER_WIDTH, MAIN_MENU_RADIUS)
                pygame.draw.rect(screen, DARK_GRAY, (box_x+MAIN_MENU_INNER_PADDING, y-MENU_BOX_Y_OFFSET, MAIN_MENU_BOX_WIDTH-MAIN_MENU_INNER_REDUCTION, MAIN_MENU_BOX_HEIGHT-MAIN_MENU_INNER_REDUCTION), 0, SETTINGS_MENU_RADIUS)
            
            # Use cached text instead of rendering every frame
            cached_text = text_cache.get_menu_text("main", option, is_selected)
            if cached_text:
                text_rect = cached_text.get_rect(center=(WINDOW_WIDTH//2, y))
                screen.blit(cached_text, text_rect)
            else:
                # Fallback to dynamic rendering if cache miss
                color = WHITE if is_selected else LIGHT_GRAY
                text = font.render(option, True, color)
                text_rect = text.get_rect(center=(WINDOW_WIDTH//2, y))
                screen.blit(text, text_rect)
        
        # Instructions - use cached text
        instructions = text_cache.static_texts.get('navigation_help') or small_font.render(GAME_NAMES['navigation_help'], True, GRAY)
        instructions_rect = instructions.get_rect(center=(WINDOW_WIDTH//2, 520))
        screen.blit(instructions, instructions_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                safe_exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    safe_exit()
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:  # Start Game
                        return 'game'
                    elif selected == 1:  # High Scores
                        show_high_scores()
                    elif selected == 2:  # Settings
                        return 'settings'
                    elif selected == 3:  # Exit
                        safe_exit()

def settings_menu():
    options = [GAME_NAMES['select_character'], GAME_NAMES['select_background'], GAME_NAMES['select_garbage_bag']]
    selected = 0
    
    while True:
        screen.fill(BLACK)
        
        title = large_font.render(GAME_NAMES['settings'].upper(), True, CYAN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 80))
        screen.blit(title, title_rect)
        
        pygame.draw.line(screen, CYAN, (TITLE_LINE_MARGIN, TITLE_LINE_Y), (WINDOW_WIDTH-TITLE_LINE_MARGIN, TITLE_LINE_Y), LINE_BORDER_WIDTH)
        pygame.draw.line(screen, DARK_GRAY, (SETTINGS_LINE_MARGIN, SETTINGS_SEPARATOR_LINE_Y), (WINDOW_WIDTH-SETTINGS_LINE_MARGIN, SETTINGS_SEPARATOR_LINE_Y), THIN_LINE_WIDTH)
        
        # Menu options
        for i, option in enumerate(options):
            is_selected = (i == selected)
            y = MENU_START_Y + i * MENU_ITEM_SPACING
            
            if is_selected:
                box_x = WINDOW_WIDTH//2 - MAIN_MENU_BOX_WIDTH//2
                pygame.draw.rect(screen, DARK_GRAY, (box_x, y-MAIN_MENU_BOX_Y_OFFSET, MAIN_MENU_BOX_WIDTH, MAIN_MENU_BOX_HEIGHT), 0, SETTINGS_MENU_RADIUS)
                pygame.draw.rect(screen, CYAN, (box_x, y-MAIN_MENU_BOX_Y_OFFSET, MAIN_MENU_BOX_WIDTH, MAIN_MENU_BOX_HEIGHT), MAIN_MENU_BORDER_WIDTH, SETTINGS_MENU_RADIUS)
            
            # Use cached text instead of rendering every frame
            cached_text = text_cache.get_menu_text("settings", option, is_selected)
            if cached_text:
                text_rect = cached_text.get_rect(center=(WINDOW_WIDTH//2, y))
                screen.blit(cached_text, text_rect)
            else:
                # Fallback to dynamic rendering if cache miss
                color = WHITE if is_selected else LIGHT_GRAY
                text = font.render(option, True, color)
                text_rect = text.get_rect(center=(WINDOW_WIDTH//2, y))
                screen.blit(text, text_rect)
        
        # Back info - use cached text
        back_info = text_cache.static_texts.get('back_instruction') or font.render(GAME_NAMES['back_instruction'], True, GRAY)
        back_rect = back_info.get_rect(center=(WINDOW_WIDTH//2, 420))
        screen.blit(back_info, back_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                safe_exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:  # Select Character
                        select_character()
                    elif selected == 1:  # Select Background
                        select_background()
                    elif selected == 2:  # Select Garbage Bag
                        select_garbage_bag()

def select_background():
    options = [bg['name'] for bg in BACKGROUNDS_CONFIG]
    
    def is_active(name):
        return name == game_state.selected_background
    
    def on_select(name):
        game_state.selected_background = name
        game_state.save_settings()
    
    generic_selection_menu(
        GAME_NAMES['select_background'],
        options,
        game_state.selected_background,
        get_sprite_func=None,  # No sprite function for backgrounds
        get_active_func=is_active,
        on_select_func=on_select,
        preview_type='background'  # Special preview type for backgrounds
    )

def select_garbage_bag():
    options = list(GARBAGE_BAGS.keys())
    
    def get_sprite(name):
        return GARBAGE_BAGS[name]
    
    def is_active(name):
        return name == game_state.selected_garbage
    
    def on_select(name):
        game_state.selected_garbage = name
        game_state.save_settings()
    
    generic_selection_menu(
        GAME_NAMES['select_garbage_bag'],
        options,
        game_state.selected_garbage,
        get_sprite_func=get_sprite,
        get_active_func=is_active,
        on_select_func=on_select
    )

def select_difficulty():
    options = list(SPEEDS.keys())
    selected = 0
    while True:
        screen.fill(BLACK)
        title = font.render(GAME_NAMES['select_difficulty'], True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, NAME_INPUT_TITLE_Y))
        screen.blit(title, title_rect)
        
        for i, name in enumerate(options):
            difficulty_color = DIFFICULTY_COLORS[name]
            y = DIFFICULTY_START_Y + i * DIFFICULTY_ITEM_SPACING
            
            if i == selected:
                # Draw box for selected difficulty
                box_x = WINDOW_WIDTH//2 - DIFFICULTY_BOX_WIDTH//2
                pygame.draw.rect(screen, DARK_GRAY, (box_x, y - DIFFICULTY_BOX_Y_OFFSET, DIFFICULTY_BOX_WIDTH, DIFFICULTY_BOX_HEIGHT), 0, DIFFICULTY_MENU_RADIUS)
                pygame.draw.rect(screen, difficulty_color, (box_x, y - DIFFICULTY_BOX_Y_OFFSET, DIFFICULTY_BOX_WIDTH, DIFFICULTY_BOX_HEIGHT), DIFFICULTY_MENU_BORDER_WIDTH, DIFFICULTY_MENU_RADIUS)
                color = difficulty_color
            else:
                color = difficulty_color
            option = font.render(name, True, color)
            option_rect = option.get_rect(center=(WINDOW_WIDTH//2, y))
            screen.blit(option, option_rect)
        
        # ESC exit info
        exit_info = font.render(GAME_NAMES['exit_instruction'], True, GRAY)
        exit_rect = exit_info.get_rect(center=(WINDOW_WIDTH//2, 450))
        screen.blit(exit_info, exit_rect)
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                safe_exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    return SPEEDS[options[selected]], options[selected]
                elif event.key == pygame.K_ESCAPE:
                    return None, None  # Return to main menu

def game_over_screen(score, difficulty_name):
    save_score(game_state.player_name, score, difficulty_name)
    
    while True:
        screen.fill(BLACK)

        title = large_font.render(GAME_NAMES['game_over'].upper(), True, RED)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 100))
        screen.blit(title, title_rect)
        
        # Game result info
        player_text = font.render(f'{GAME_NAMES["player"]}: {game_state.player_name}', True, PURPLE)
        player_rect = player_text.get_rect(center=(WINDOW_WIDTH//2, 170))
        screen.blit(player_text, player_rect)
        
        score_text = font.render(f'{GAME_NAMES["collected_trash"]}: {score}', True, NEON_GREEN)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH//2, 200))
        screen.blit(score_text, score_rect)
        
        difficulty_color = DIFFICULTY_COLORS.get(difficulty_name, LIGHT_GRAY)
        
        # Write "Difficulty:" label in white
        difficulty_label = font.render(f'{GAME_NAMES["difficulty"]}: ', True, WHITE)
        difficulty_label_rect = difficulty_label.get_rect()
        
        # Write difficulty level in color
        difficulty_level = font.render(difficulty_name, True, difficulty_color)
        difficulty_level_rect = difficulty_level.get_rect()
        
        # Align two texts side by side
        total_width = difficulty_label_rect.width + difficulty_level_rect.width
        start_x = (WINDOW_WIDTH - total_width) // 2
        
        difficulty_label_rect.x = start_x
        difficulty_label_rect.centery = 230
        screen.blit(difficulty_label, difficulty_label_rect)
        
        difficulty_level_rect.x = start_x + difficulty_label_rect.width
        difficulty_level_rect.centery = 230
        screen.blit(difficulty_level, difficulty_level_rect)
        
        environmental_msg = font.render(GAME_NAMES['environmental_message'], True, NEON_GREEN)
        environmental_rect = environmental_msg.get_rect(center=(WINDOW_WIDTH//2, 290))
        screen.blit(environmental_msg, environmental_rect)
        
        # Draw options with highlighting
        
        # ENTER option
        enter_prefix = font.render('Press ', True, WHITE)
        enter_key = font.render('ENTER', True, NEON_GREEN)
        enter_suffix = font.render(' to play again', True, WHITE)
        
        total_enter_width = enter_prefix.get_width() + enter_key.get_width() + enter_suffix.get_width()
        enter_start_x = (WINDOW_WIDTH - total_enter_width) // 2
        enter_y = GAME_OVER_OPTION_Y_START
        
        screen.blit(enter_prefix, (enter_start_x, enter_y))
        screen.blit(enter_key, (enter_start_x + enter_prefix.get_width(), enter_y))
        screen.blit(enter_suffix, (enter_start_x + enter_prefix.get_width() + enter_key.get_width(), enter_y))
        
        # S option
        s_prefix = font.render('Press ', True, WHITE)
        s_key = font.render('S', True, YELLOW)
        s_suffix = font.render(' to show scores', True, WHITE)
        
        total_s_width = s_prefix.get_width() + s_key.get_width() + s_suffix.get_width()
        s_start_x = (WINDOW_WIDTH - total_s_width) // 2
        s_y = GAME_OVER_OPTION_Y_START + GAME_OVER_OPTION_Y_SPACING
        
        screen.blit(s_prefix, (s_start_x, s_y))
        screen.blit(s_key, (s_start_x + s_prefix.get_width(), s_y))
        screen.blit(s_suffix, (s_start_x + s_prefix.get_width() + s_key.get_width(), s_y))
        
        # ESC option
        esc_prefix = font.render('Press ', True, WHITE)
        esc_key = font.render('ESC', True, RED)
        esc_suffix = font.render(' for main menu', True, WHITE)
        
        total_esc_width = esc_prefix.get_width() + esc_key.get_width() + esc_suffix.get_width()
        esc_start_x = (WINDOW_WIDTH - total_esc_width) // 2
        esc_y = GAME_OVER_OPTION_Y_START + (GAME_OVER_OPTION_Y_SPACING * 2)
        
        screen.blit(esc_prefix, (esc_start_x, esc_y))
        screen.blit(esc_key, (esc_start_x + esc_prefix.get_width(), esc_y))
        screen.blit(esc_suffix, (esc_start_x + esc_prefix.get_width() + esc_key.get_width(), esc_y))
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                safe_exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return 'replay'
                elif event.key == pygame.K_s:
                    show_high_scores()
                elif event.key == pygame.K_ESCAPE:
                    return 'menu'

def main():
    """Main entry point - creates and runs the game manager"""
    # Initialize text cache for better performance
    text_cache.preload_menu_texts()
    
    game_manager = GameManager()
    game_manager.run()

if __name__ == "__main__":
    main()