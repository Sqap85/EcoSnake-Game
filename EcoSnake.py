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
# NAMING CONFIGURATION
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
    
    # Characters
    'character1': 'Gardener',
    'character2': 'Blonde Girl', 
    'character3': 'Chubby Child',
    
    # Backgrounds
    'background1': 'Black',
    'background2': 'Forest',
    'background3': 'Beach',
    
    # Garbage bags
    'garbage_bag1': 'Sweet Bag',
    'garbage_bag2': 'Yellow Bag',
    'garbage_bag3': 'Black Bag',
    
    # Difficulty levels
    'difficulty1': 'Easy',
    'difficulty2': 'Medium',
    'difficulty3': 'Hard',
    
    # Settings menu
    'select_character': 'Select Character',
    'select_background': 'Select Background',
    'select_garbage_bag': 'Select Garbage Bag',
    
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
    'press_esc_back': "Press ESC to go back",
    'press_enter_ok': 'ENTER - OK',
    'press_esc_return': 'ESC - Go Back',
    'character_info': 'Character',
    'background_info': 'Background',
    'garbage_bag_info': 'Garbage Bag',
    'press_esc_main_menu': 'ESC: Main Menu',
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
    'arrow_keys_select': 'Use arrow keys to select, ENTER to confirm, ESC to exit',
    '2_12_characters': '2-12 characters',
    'press_esc_exit': 'Press ESC to exit',
    'trash_collected': 'trash collected'
}

# Color Palette
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

# Game settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
SQUARE_SIZE = 30

# UI Constants
UI_AREA_HEIGHT = 45
UI_BORDER_HEIGHT = 2
MENU_BOX_WIDTH = 500
MENU_BOX_HEIGHT = 120
MENU_ITEM_SPACING = 60
MENU_ITEM_HEIGHT = 50
EDGE_MARGIN = 15
LARGE_SPRITE_SIZE = 80
NAME_INPUT_WIDTH = 400
NAME_INPUT_HEIGHT = 60
MAX_NAME_LENGTH = 12
MIN_NAME_LENGTH = 2

SPEEDS = {
    GAME_NAMES['difficulty1']: 5,
    GAME_NAMES['difficulty2']: 10,
    GAME_NAMES['difficulty3']: 18
}

# Difficulty colors
DIFFICULTY_COLORS = {
    GAME_NAMES['difficulty1']: GREEN,
    GAME_NAMES['difficulty2']: ORANGE, 
    GAME_NAMES['difficulty3']: RED
}
FPS = 60

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("EcoSnake-Game")
clock = pygame.time.Clock()


# Sprite loading function
def load_sprite(filename, size=(SQUARE_SIZE, SQUARE_SIZE)):
    sprite = pygame.image.load(f"assets/{filename}")
    return pygame.transform.scale(sprite, size)

# Characters
CHARACTERS = {
    GAME_NAMES['character1']: load_sprite("gardener.png"),
    GAME_NAMES['character2']: load_sprite("blonde_girl.png"),
    GAME_NAMES['character3']: load_sprite("chubby_child.png")
}

# Trash types
TRASH_SPRITES = {
    'apple': load_sprite("apple.png"),
    'banana': load_sprite("banana.png"),
    'bottle': load_sprite("bottle.png"),
    'landfill': load_sprite("landfill.png")
}

# Garbage bags
GARBAGE_BAGS = {
    GAME_NAMES['garbage_bag1']: load_sprite("sweet_bag.png"),
    GAME_NAMES['garbage_bag2']: load_sprite("yellow_bag.png"),
    GAME_NAMES['garbage_bag3']: load_sprite("black_bag.png")
}

# Backgrounds
BACKGROUNDS = {
    GAME_NAMES['background2']: load_sprite("forest.png", (WINDOW_WIDTH, WINDOW_HEIGHT)),
    GAME_NAMES['background3']: load_sprite("beach.png", (WINDOW_WIDTH, WINDOW_HEIGHT))
}

# Create fonts
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 24)

# Menu helper functions
def draw_menu_box(screen, box_rect, selected=False):
    if selected:
        pygame.draw.rect(screen, DARK_GRAY, box_rect, 0, 15)
        pygame.draw.rect(screen, CYAN, box_rect, 4, 15)
    else:
        pygame.draw.rect(screen, (30, 30, 35), box_rect, 0, 15)
        pygame.draw.rect(screen, LIGHT_GRAY, box_rect, 2, 15)

def draw_score_line(screen, i, score_info, y_pos, positions):
    colors = [YELLOW, LIGHT_GRAY, ORANGE, CYAN, CYAN, GRAY, GRAY, GRAY, GRAY, GRAY]
    color = colors[i] if i < len(colors) else GRAY
    
    texts = [f"{i+1}.", score_info['name'][:12], str(score_info['score']), score_info['difficulty']]
    for text, x_pos in zip(texts, positions):
        text_surface = small_font.render(text, True, color)
        screen.blit(text_surface, (x_pos, y_pos))


# Game State Management
class GameState:
    def __init__(self):
        self.player_name = ""
        self.selected_character = GAME_NAMES['character1']
        self.selected_background = GAME_NAMES['background1']
        self.selected_garbage = GAME_NAMES['garbage_bag1']
    
    def save_settings(self):
        settings = {
            'selected_character': self.selected_character,
            'selected_background': self.selected_background,
            'selected_garbage': self.selected_garbage
        }
        try:
            with open('settings.json', 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Settings could not be saved: {e}")
    
    def load_settings(self):
        try:
            with open('settings.json', 'r', encoding='utf-8') as f:
                settings = json.load(f)
                self.selected_character = settings.get('selected_character', GAME_NAMES['character1'])
                self.selected_background = settings.get('selected_background', GAME_NAMES['background1'])
                self.selected_garbage = settings.get('selected_garbage', GAME_NAMES['garbage_bag1'])
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            # Use default values if file doesn't exist or is corrupted
            self.selected_character = GAME_NAMES['character1']
            self.selected_background = GAME_NAMES['background1']
            self.selected_garbage = GAME_NAMES['garbage_bag1']

# Global game state instance
game_state = GameState()

# Utility Functions
def safe_exit():
    """Safely exit the game"""
    pygame.quit()
    sys.exit()

def handle_quit_event():
    """Handle pygame QUIT event"""
    safe_exit()

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
        
        UI_AREA_HEIGHT = 45
        
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

    def collect_trash(self):
        self.squares.append(self.squares[-1])

    def draw(self, screen):
        head_x, head_y = self.squares[0]
        screen.blit(self.character_sprite, (head_x, head_y))
        selected_garbage_sprite = GARBAGE_BAGS[game_state.selected_garbage]
        for (x, y) in self.squares[1:]:
            screen.blit(selected_garbage_sprite, (x, y))

    def check_collision(self):
        head = self.squares[0]
        return head in self.squares[1:]

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

# Score table functions
def save_score(name, score, difficulty):
    try:
        with open('highscores.json', 'r') as f:
            scores = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
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
    
    with open('highscores.json', 'w') as f:
        json.dump(scores, f, indent=2)

def show_high_scores():
    try:
        with open('highscores.json', 'r') as f:
            scores = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
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
            positions = [150, 200, 400, 500]
            headers = [GAME_NAMES['rank'], GAME_NAMES['name'], GAME_NAMES['score'], GAME_NAMES['difficulty_header']]
            
            for header, x_pos in zip(headers, positions):
                text = small_font.render(header, True, WHITE)
                screen.blit(text, (x_pos, y_pos))
            
            y_pos += 25
            pygame.draw.line(screen, WHITE, (positions[0], y_pos), (positions[-1] + 80, y_pos), 1)
            y_pos += 15
            
            for i, score_info in enumerate(scores[:10]):
                draw_score_line(screen, i, score_info, y_pos, positions)
                y_pos += 25
        
        # Back info
        back_info = font.render(GAME_NAMES['press_esc_back'], True, GRAY)
        back_rect = back_info.get_rect(center=(WINDOW_WIDTH//2, 520))
        screen.blit(back_info, back_rect)
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    return

def enter_name():
    input_text = ""
    while True:
        screen.fill(BLACK)
        
        # Title
        title = large_font.render(GAME_NAMES['enter_player_name'], True, YELLOW)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 150))
        screen.blit(title, title_rect)
        
        # Input box 
        box_rect = pygame.Rect(WINDOW_WIDTH//2 - 200, 220, 400, 60)
        pygame.draw.rect(screen, (30, 30, 30), box_rect, 0, 10)
        pygame.draw.rect(screen, YELLOW if input_text else GRAY, box_rect, 3, 10)
        
        # Show written text
        if input_text:
            text = font.render(input_text, True, WHITE)
        else:
            text = font.render(GAME_NAMES['type_your_name'], True, GRAY)
        text_rect = text.get_rect(center=box_rect.center)
        screen.blit(text, text_rect)
        
        # Cursor
        if pygame.time.get_ticks() % 1000 < 500:
            if input_text:
                cursor_x = text_rect.right + 3
            else:
                cursor_x = box_rect.left + 15
            pygame.draw.line(screen, YELLOW, (cursor_x, box_rect.top + 15), (cursor_x, box_rect.bottom - 15), 2)
        
        # Rules
        rule = small_font.render(GAME_NAMES['2_12_characters'], True, GRAY)
        rule_rect = rule.get_rect(center=(WINDOW_WIDTH//2, 300))
        screen.blit(rule, rule_rect)
        
        # Instructions
        enter_active = len(input_text.strip()) >= 2
        enter_color = GREEN if enter_active else GRAY
        enter_text = font.render(GAME_NAMES['press_enter_ok'], True, enter_color)
        enter_rect = enter_text.get_rect(center=(WINDOW_WIDTH//2, 380))
        screen.blit(enter_text, enter_rect)
        
        esc_text = small_font.render(GAME_NAMES['press_esc_return'], True, GRAY)
        esc_rect = esc_text.get_rect(center=(WINDOW_WIDTH//2, 420))
        screen.blit(esc_text, esc_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
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
                    if event.unicode.isprintable() and len(input_text) < 12:
                        input_text += event.unicode

def select_character():
    character_names = list(CHARACTERS.keys())
    selected = character_names.index(game_state.selected_character) if game_state.selected_character in character_names else 0
    
    while True:
        screen.fill(BLACK)
        
        title = large_font.render(GAME_NAMES['select_character'].upper(), True, CYAN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 80))
        screen.blit(title, title_rect)
        
        pygame.draw.line(screen, CYAN, (100, 110), (WINDOW_WIDTH-100, 110), 3)
        
        # Show characters
        start_y = 160
        for i, name in enumerate(character_names):
            y = start_y + i * 140
            is_selected = (i == selected)
            
            box_width = 500
            box_height = 120
            box_x = WINDOW_WIDTH//2 - box_width//2
            box_rect = pygame.Rect(box_x, y-20, box_width, box_height)
            
            draw_menu_box(screen, box_rect, is_selected)
            
            # Show character sprite
            character_sprite = CHARACTERS[name]
            large_sprite = pygame.transform.scale(character_sprite, (80, 80))
            sprite_rect = large_sprite.get_rect(center=(box_x + 80, y + 40))
            screen.blit(large_sprite, sprite_rect)
            
            color = CYAN if is_selected else WHITE
            name_text = font.render(name, True, color)
            name_rect = name_text.get_rect(center=(box_x + 280, y + 30))
            screen.blit(name_text, name_rect)
            
            if name == game_state.selected_character:
                active_text = small_font.render(GAME_NAMES['active'], True, NEON_GREEN)
                active_rect = active_text.get_rect(center=(box_x + 280, y + 60))
                screen.blit(active_text, active_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Return to settings menu
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(character_names)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(character_names)
                elif event.key == pygame.K_RETURN:
                    game_state.selected_character = character_names[selected]
                    game_state.save_settings()
                    return

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
        menu_start_y = 220
        for i, option in enumerate(options):
            color = WHITE if i == selected else LIGHT_GRAY
            y = menu_start_y + i * 60
            
            if i == selected:
                pygame.draw.rect(screen, DARK_GRAY, (250, y-25, 300, 50), 0, 12)
                pygame.draw.rect(screen, CYAN, (250, y-25, 300, 50), 3, 12)
                pygame.draw.rect(screen, (52, 73, 94), (255, y-20, 290, 40), 0, 10)
            
            text = font.render(option, True, color)
            text_rect = text.get_rect(center=(WINDOW_WIDTH//2, y))
            screen.blit(text, text_rect)
        
        # Instructions
        instructions = small_font.render(GAME_NAMES['arrow_keys_select'], True, GRAY)
        instructions_rect = instructions.get_rect(center=(WINDOW_WIDTH//2, 520))
        screen.blit(instructions, instructions_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
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
                        pygame.quit()
                        sys.exit()

def settings_menu():
    options = [GAME_NAMES['select_character'], GAME_NAMES['select_background'], GAME_NAMES['select_garbage_bag']]
    selected = 0
    
    while True:
        screen.fill(BLACK)
        
        title = large_font.render(GAME_NAMES['settings'].upper(), True, CYAN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 80))
        screen.blit(title, title_rect)
        
        pygame.draw.line(screen, CYAN, (100, 110), (WINDOW_WIDTH-100, 110), 3)
        pygame.draw.line(screen, DARK_GRAY, (100, 112), (WINDOW_WIDTH-100, 112), 1)
        
        # Menu options
        menu_start_y = 160
        for i, option in enumerate(options):
            color = WHITE if i == selected else LIGHT_GRAY
            y = menu_start_y + i * 60
            
            if i == selected:
                pygame.draw.rect(screen, DARK_GRAY, (250, y-25, 300, 50), 0, 10)
                pygame.draw.rect(screen, CYAN, (250, y-25, 300, 50), 3, 10)
            
            text = font.render(option, True, color)
            text_rect = text.get_rect(center=(WINDOW_WIDTH//2, y))
            screen.blit(text, text_rect)
        
        # Back info
        back_info = font.render(GAME_NAMES['press_esc_back'], True, GRAY)
        back_rect = back_info.get_rect(center=(WINDOW_WIDTH//2, 420))
        screen.blit(back_info, back_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
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
    options = [GAME_NAMES['background1'], GAME_NAMES['background2'], GAME_NAMES['background3']]
    selected = options.index(game_state.selected_background) if game_state.selected_background in options else 0
    
    while True:
        screen.fill(BLACK)
        
        title = large_font.render(GAME_NAMES['select_background'].upper(), True, CYAN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 80))
        screen.blit(title, title_rect)
        
        pygame.draw.line(screen, CYAN, (100, 110), (WINDOW_WIDTH-100, 110), 3)
        
        # Show backgrounds
        start_y = 160
        for i, name in enumerate(options):
            y = start_y + i * 140
            is_selected = (i == selected)
            
            box_width = 500
            box_height = 120
            box_x = WINDOW_WIDTH//2 - box_width//2
            box_rect = pygame.Rect(box_x, y-20, box_width, box_height)
            
            draw_menu_box(screen, box_rect, is_selected)
            
            # Background preview
            if name == GAME_NAMES['background1']:
                preview_rect = pygame.Rect(0, 0, 80, 80)
                preview_rect.center = (box_x + 80, y + 40)
                pygame.draw.rect(screen, BLACK, preview_rect, 0, 5)
            elif name in BACKGROUNDS:
                try:
                    preview = pygame.transform.scale(BACKGROUNDS[name], (80, 80))
                    sprite_rect = preview.get_rect(center=(box_x + 80, y + 40))
                    screen.blit(preview, sprite_rect)
                except (pygame.error, ValueError, TypeError):
                    color = (0, 100, 0) if name == GAME_NAMES['background2'] else (30, 144, 255)
                    preview_rect = pygame.Rect(0, 0, 80, 80)
                    preview_rect.center = (box_x + 80, y + 40)
                    pygame.draw.rect(screen, color, preview_rect, 0, 5)
            
            color = CYAN if is_selected else WHITE
            name_text = font.render(name, True, color)
            name_rect = name_text.get_rect(center=(box_x + 280, y + 30))
            screen.blit(name_text, name_rect)
            
            if name == game_state.selected_background:
                active_text = small_font.render(GAME_NAMES['active'], True, NEON_GREEN)
                active_rect = active_text.get_rect(center=(box_x + 280, y + 60))
                screen.blit(active_text, active_rect)
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    game_state.selected_background = options[selected]
                    game_state.save_settings()
                    return
                elif event.key == pygame.K_ESCAPE:
                    return

def select_garbage_bag():
    options = list(GARBAGE_BAGS.keys())
    selected = options.index(game_state.selected_garbage) if game_state.selected_garbage in options else 0
    
    while True:
        screen.fill(BLACK)
        
        title = large_font.render(GAME_NAMES['select_garbage_bag'].upper(), True, CYAN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 80))
        screen.blit(title, title_rect)
        
        pygame.draw.line(screen, CYAN, (100, 110), (WINDOW_WIDTH-100, 110), 3)
        
        # Show garbage bags
        start_y = 160
        for i, name in enumerate(options):
            y = start_y + i * 140
            is_selected = (i == selected)
            
            box_width = 500
            box_height = 120
            box_x = WINDOW_WIDTH//2 - box_width//2
            box_rect = pygame.Rect(box_x, y-20, box_width, box_height)
            
            draw_menu_box(screen, box_rect, is_selected)
            
            # Show garbage bag sprite
            garbage_sprite = GARBAGE_BAGS[name]
            large_sprite = pygame.transform.scale(garbage_sprite, (80, 80))
            sprite_rect = large_sprite.get_rect(center=(box_x + 80, y + 40))
            screen.blit(large_sprite, sprite_rect)
            
            color = CYAN if is_selected else WHITE
            name_text = font.render(name, True, color)
            name_rect = name_text.get_rect(center=(box_x + 280, y + 30))
            screen.blit(name_text, name_rect)
            
            if name == game_state.selected_garbage:
                active_text = small_font.render(GAME_NAMES['active'], True, NEON_GREEN)
                active_rect = active_text.get_rect(center=(box_x + 280, y + 60))
                screen.blit(active_text, active_rect)
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    game_state.selected_garbage = options[selected]
                    game_state.save_settings()
                    return
                elif event.key == pygame.K_ESCAPE:
                    return

def select_difficulty():
    options = list(SPEEDS.keys())
    selected = 0
    while True:
        screen.fill(BLACK)
        title = font.render(GAME_NAMES['select_difficulty'], True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 150))
        screen.blit(title, title_rect)
        
        for i, name in enumerate(options):
            difficulty_color = DIFFICULTY_COLORS[name]
            if i == selected:
                # Draw box for selected difficulty
                pygame.draw.rect(screen, DARK_GRAY, (WINDOW_WIDTH//2 - 130, 220 + i*50 - 20, 260, 40), 0, 10)
                pygame.draw.rect(screen, difficulty_color, (WINDOW_WIDTH//2 - 130, 220 + i*50 - 20, 260, 40), 3, 10)
                color = difficulty_color
            else:
                color = difficulty_color
                
            y = 220 + i*50
            option = font.render(name, True, color)
            option_rect = option.get_rect(center=(WINDOW_WIDTH//2, y))
            screen.blit(option, option_rect)
        
        # ESC exit info
        exit_info = font.render(GAME_NAMES['press_esc_exit'], True, GRAY)
        exit_rect = exit_info.get_rect(center=(WINDOW_WIDTH//2, 450))
        screen.blit(exit_info, exit_rect)
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
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
        enter_y = 350
        
        screen.blit(enter_prefix, (enter_start_x, enter_y))
        screen.blit(enter_key, (enter_start_x + enter_prefix.get_width(), enter_y))
        screen.blit(enter_suffix, (enter_start_x + enter_prefix.get_width() + enter_key.get_width(), enter_y))
        
        # S option
        s_prefix = font.render('Press ', True, WHITE)
        s_key = font.render('S', True, YELLOW)
        s_suffix = font.render(' to show scores', True, WHITE)
        
        total_s_width = s_prefix.get_width() + s_key.get_width() + s_suffix.get_width()
        s_start_x = (WINDOW_WIDTH - total_s_width) // 2
        s_y = 380
        
        screen.blit(s_prefix, (s_start_x, s_y))
        screen.blit(s_key, (s_start_x + s_prefix.get_width(), s_y))
        screen.blit(s_suffix, (s_start_x + s_prefix.get_width() + s_key.get_width(), s_y))
        
        # ESC option
        esc_prefix = font.render('Press ', True, WHITE)
        esc_key = font.render('ESC', True, RED)
        esc_suffix = font.render(' for main menu', True, WHITE)
        
        total_esc_width = esc_prefix.get_width() + esc_key.get_width() + esc_suffix.get_width()
        esc_start_x = (WINDOW_WIDTH - total_esc_width) // 2
        esc_y = 410
        
        screen.blit(esc_prefix, (esc_start_x, esc_y))
        screen.blit(esc_key, (esc_start_x + esc_prefix.get_width(), esc_y))
        screen.blit(esc_suffix, (esc_start_x + esc_prefix.get_width() + esc_key.get_width(), esc_y))
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return 'replay'
                elif event.key == pygame.K_s:
                    show_high_scores()
                elif event.key == pygame.K_ESCAPE:
                    return 'menu'

def main():
    global FPS
    
    # Load settings at game start
    game_state.load_settings()
    
    while True:
        menu_choice = main_menu()
        
        if menu_choice == 'settings':
            settings_menu()
            continue
        elif menu_choice != 'game':
            continue
        
        # Player name and difficulty selection
        game_speed = None
        difficulty_name = None
        
        while True:
            if not enter_name():
                break
            
            game_speed, difficulty_name = select_difficulty()
            
            if game_speed is None or difficulty_name is None:
                game_state.player_name = ""
                continue
            else:
                break
        
        if game_speed is None or difficulty_name is None:
            continue
        
        # Game loop
        while True:
            collector = TrashCollector(CHARACTERS[game_state.selected_character])
            trash = Trash()
            score = 0
            last_dir = (1, 0)
            grow = False
            game_over = False
            return_to_main = False
            frame_counter = 0
            
            while not game_over and not return_to_main:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            return_to_main = True
                            break
                        
                        new_dir = None
                        if event.key == pygame.K_UP and last_dir != (0, 1):
                            new_dir = (0, -1)
                        elif event.key == pygame.K_DOWN and last_dir != (0, -1):
                            new_dir = (0, 1)
                        elif event.key == pygame.K_LEFT and last_dir != (1, 0):
                            new_dir = (-1, 0)
                        elif event.key == pygame.K_RIGHT and last_dir != (-1, 0):
                            new_dir = (1, 0)
                        if new_dir:
                            collector.dir_x, collector.dir_y = new_dir
                            last_dir = new_dir

                frame_counter += 1
                
                move_time = False
                if frame_counter >= (60 // game_speed):
                    frame_counter = 0
                    move_time = True
                    old_tail = collector.squares[-1]
                    collector.move()
                    
                    # Check collision right after movement
                    if collector.check_collision():
                        game_over = True
                        break
                
                head_x, head_y = collector.squares[0]
                
                collision = (abs(head_x - trash.x) <= SQUARE_SIZE//2) and (abs(head_y - trash.y) <= SQUARE_SIZE//2)
                
                if collision:
                    if move_time:
                        collector.squares.append(old_tail)
                    else:
                        collector.squares.append(collector.squares[-1])
                    
                    score += 1
                    trash = Trash()

                # Draw background
                if game_state.selected_background in BACKGROUNDS:
                    screen.blit(BACKGROUNDS[game_state.selected_background], (0, 0))
                else:
                    screen.fill(BLACK)
                    
                collector.draw(screen)
                trash.draw(screen)
                
                pygame.draw.rect(screen, DARK_GRAY, (0, 0, WINDOW_WIDTH, 45))
                pygame.draw.rect(screen, LIGHT_GRAY, (0, 43, WINDOW_WIDTH, 2))
                
                # Left side - Player info
                player_text = small_font.render(f"{game_state.player_name}: {score} {GAME_NAMES['trash_collected']}", True, LIGHT_GRAY)
                screen.blit(player_text, (15, 15))
                
                # Right side - ESC info
                esc_info = small_font.render(GAME_NAMES['press_esc_main_menu'], True, LIGHT_GRAY)
                esc_width = esc_info.get_width()
                screen.blit(esc_info, (WINDOW_WIDTH - esc_width - 15, 15))
                
                pygame.display.flip()
                clock.tick(60)
        
            if return_to_main:
                break
                
            if game_over:
                result = game_over_screen(score, difficulty_name)
                if result == 'replay':
                    continue
                elif result == 'menu':
                    break
            
            break

if __name__ == "__main__":
    main()