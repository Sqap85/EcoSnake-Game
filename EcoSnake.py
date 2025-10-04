#!/usr/bin/env python3
"""
EcoSnake Game - Main Entry Point
"""

import pygame
import os
import sys
from constants import *
from game_state import GameState
from game_objects import TrashCollector, Trash
from menus import *


# Change to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))
pygame.init()


class Game:
    """Main game class that manages all game objects and flow"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("EcoSnake-Game")
        self.clock = pygame.time.Clock()
        
        # Create fonts
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 24)
        
        # Game state
        self.game_state = GameState()
        
        # Load sprites
        self._load_sprites()
    
    def _load_sprites(self):
        """Load and organize all game sprites"""
        self.characters = {
            char['name']: self._load_sprite(char['sprite']) 
            for char in CHARACTERS_CONFIG
        }
        
        self.trash_sprites = {
            item['name']: self._load_sprite(item['sprite'])
            for item in TRASH_ITEMS_CONFIG
        }
        
        self.garbage_bags = {
            bag['name']: self._load_sprite(bag['sprite'])
            for bag in GARBAGE_BAGS_CONFIG
        }
        
        self.backgrounds = {
            bg['name']: self._load_sprite(bg['sprite'], (WINDOW_WIDTH, WINDOW_HEIGHT))
            for bg in BACKGROUNDS_CONFIG 
            if bg['sprite'] is not None 
        }
        
        # Generate difficulty data
        self.speeds = {diff['name']: diff['speed'] for diff in DIFFICULTY_CONFIG}
        self.difficulty_colors = {diff['name']: diff['color'] for diff in DIFFICULTY_CONFIG}
    
    def _load_sprite(self, filename, size=(SQUARE_SIZE, SQUARE_SIZE)):
        """Load and scale a sprite with error handling"""
        try:
            sprite = pygame.image.load(f"assets/{filename}")
            return pygame.transform.scale(sprite, size)
        except (pygame.error, FileNotFoundError) as e:
            print(f"Warning: Could not load sprite '{filename}': {e}")
            # Create a placeholder colored rectangle
            placeholder = pygame.Surface(size)
            placeholder.fill(GRAY)
            return placeholder
    
    def main_menu(self):
        """Simplified main menu - broken into smaller functions"""
        options = [GAME_NAMES['start_game'], GAME_NAMES['high_scores'], GAME_NAMES['settings'], GAME_NAMES['exit']]
        selected = 0
        
        while True:
            self._draw_main_menu_screen(options, selected)
            action = self._handle_main_menu_input(selected, len(options))
            
            if action == 'exit':
                safe_exit()
            elif action == 'game':
                return 'game'
            elif action == 'high_scores':
                self.show_high_scores()
            elif action == 'settings':
                return 'settings'
            elif isinstance(action, int):
                selected = action
    
    def _draw_main_menu_screen(self, options, selected):
        """Draw the main menu screen"""
        self.screen.fill(BLACK)
        
        # Main title
        title = self.large_font.render(GAME_NAMES['game_title'], True, CYAN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, MAIN_TITLE_Y_OFFSET))
        self.screen.blit(title, title_rect)
        
        subtitle = self.font.render(GAME_NAMES['game_subtitle'], True, NEON_GREEN)
        subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH//2, SUBTITLE_Y_OFFSET))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Player info 
        self._draw_character_info()
        
        # Menu options
        self._draw_main_menu_options(options, selected)
        
        # Instructions
        instructions = self.small_font.render(GAME_NAMES['navigation_help'], True, GRAY)
        instructions_rect = instructions.get_rect(center=(WINDOW_WIDTH//2, INFO_TEXT_Y_BOTTOM))
        self.screen.blit(instructions, instructions_rect)
        
        pygame.display.flip()
        self.clock.tick(TARGET_FPS)
    
    def _draw_character_info(self):
        """Draw character selection info in top-left corner"""
        character_text = self.small_font.render(f'{GAME_NAMES["character_info"]}: {self.game_state.selected_character}', True, WHITE)
        self.screen.blit(character_text, (CHARACTER_INFO_START_X, CHARACTER_INFO_START_Y))
        
        background_text = self.small_font.render(f'{GAME_NAMES["background_info"]}: {self.game_state.selected_background}', True, WHITE)
        self.screen.blit(background_text, (CHARACTER_INFO_START_X, CHARACTER_INFO_START_Y + CHARACTER_INFO_LINE_HEIGHT))
        
        garbage_text = self.small_font.render(f'{GAME_NAMES["garbage_bag_info"]}: {self.game_state.selected_garbage}', True, WHITE)
        self.screen.blit(garbage_text, (CHARACTER_INFO_START_X, CHARACTER_INFO_START_Y + CHARACTER_INFO_LINE_HEIGHT * 2))
    
    def _draw_main_menu_options(self, options, selected):
        """Draw main menu option buttons"""
        for i, option in enumerate(options):
            is_selected = (i == selected)
            y = MAIN_MENU_START_Y + i * MENU_ITEM_SPACING
            
            if is_selected:
                box_x = WINDOW_WIDTH//2 - MAIN_MENU_BOX_WIDTH//2
                pygame.draw.rect(self.screen, DARK_GRAY, (box_x, y-MAIN_MENU_BOX_Y_OFFSET, MAIN_MENU_BOX_WIDTH, MAIN_MENU_BOX_HEIGHT), 0, MAIN_MENU_RADIUS)
                pygame.draw.rect(self.screen, CYAN, (box_x, y-MAIN_MENU_BOX_Y_OFFSET, MAIN_MENU_BOX_WIDTH, MAIN_MENU_BOX_HEIGHT), MAIN_MENU_BORDER_WIDTH, MAIN_MENU_RADIUS)
                pygame.draw.rect(self.screen, DARK_GRAY, (box_x+MAIN_MENU_INNER_PADDING, y-MENU_BOX_Y_OFFSET, MAIN_MENU_BOX_WIDTH-MAIN_MENU_INNER_REDUCTION, MAIN_MENU_BOX_HEIGHT-MAIN_MENU_INNER_REDUCTION), 0, SETTINGS_MENU_RADIUS)
            
            # Render menu text
            color = WHITE if is_selected else LIGHT_GRAY
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(WINDOW_WIDTH//2, y))
            self.screen.blit(text, text_rect)
    
    def _handle_main_menu_input(self, selected, options_count):
        """Handle main menu input and return action"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'exit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'exit'
                elif event.key == pygame.K_UP:
                    return (selected - 1) % options_count
                elif event.key == pygame.K_DOWN:
                    return (selected + 1) % options_count
                elif event.key == pygame.K_RETURN:
                    if selected == 0:  # Start Game
                        return 'game'
                    elif selected == 1:  # High Scores
                        return 'high_scores'
                    elif selected == 2:  # Settings
                        return 'settings'
                    elif selected == 3:  # Exit
                        return 'exit'
        return selected
    
    def settings_menu(self):
        """Simplified settings menu"""
        options = [GAME_NAMES['select_character'], GAME_NAMES['select_background'], GAME_NAMES['select_garbage_bag']]
        selected = 0
        
        while True:
            self._draw_settings_screen(options, selected)
            action = self._handle_settings_input(selected, len(options))
            
            if action == 'exit':
                return
            elif action == 'character':
                self.select_character()
            elif action == 'background':
                self.select_background()
            elif action == 'garbage':
                self.select_garbage_bag()
            elif isinstance(action, int):
                selected = action
    
    def _draw_settings_screen(self, options, selected):
        """Draw settings menu screen"""
        self.screen.fill(BLACK)
        
        title = self.large_font.render(GAME_NAMES['settings'].upper(), True, CYAN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, TITLE_Y_OFFSET))
        self.screen.blit(title, title_rect)
        
        pygame.draw.line(self.screen, CYAN, (TITLE_LINE_MARGIN, TITLE_LINE_Y), (WINDOW_WIDTH-TITLE_LINE_MARGIN, TITLE_LINE_Y), LINE_BORDER_WIDTH)
        pygame.draw.line(self.screen, DARK_GRAY, (SETTINGS_LINE_MARGIN, SETTINGS_SEPARATOR_LINE_Y), (WINDOW_WIDTH-SETTINGS_LINE_MARGIN, SETTINGS_SEPARATOR_LINE_Y), THIN_LINE_WIDTH)
        
        # Menu options
        for i, option in enumerate(options):
            is_selected = (i == selected)
            y = MENU_START_Y + i * MENU_ITEM_SPACING
            
            if is_selected:
                box_x = WINDOW_WIDTH//2 - MAIN_MENU_BOX_WIDTH//2
                pygame.draw.rect(self.screen, DARK_GRAY, (box_x, y-MAIN_MENU_BOX_Y_OFFSET, MAIN_MENU_BOX_WIDTH, MAIN_MENU_BOX_HEIGHT), 0, SETTINGS_MENU_RADIUS)
                pygame.draw.rect(self.screen, CYAN, (box_x, y-MAIN_MENU_BOX_Y_OFFSET, MAIN_MENU_BOX_WIDTH, MAIN_MENU_BOX_HEIGHT), MAIN_MENU_BORDER_WIDTH, SETTINGS_MENU_RADIUS)
            
            # Render menu text
            color = WHITE if is_selected else LIGHT_GRAY
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(WINDOW_WIDTH//2, y))
            self.screen.blit(text, text_rect)
        
        # Back info
        back_info = self.font.render(GAME_NAMES['back_instruction'], True, GRAY)
        back_rect = back_info.get_rect(center=(WINDOW_WIDTH//2, SETTINGS_BACK_Y))
        self.screen.blit(back_info, back_rect)
        
        pygame.display.flip()
        self.clock.tick(TARGET_FPS)
    
    def _handle_settings_input(self, selected, options_count):
        """Handle settings menu input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'exit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'exit'
                elif event.key == pygame.K_UP:
                    return (selected - 1) % options_count
                elif event.key == pygame.K_DOWN:
                    return (selected + 1) % options_count
                elif event.key == pygame.K_RETURN:
                    if selected == 0:  # Select Character
                        return 'character'
                    elif selected == 1:  # Select Background
                        return 'background'
                    elif selected == 2:  # Select Garbage Bag
                        return 'garbage'
        return selected
    
    def select_character(self):
        """Character selection using generic menu"""
        character_names = list(self.characters.keys())
        
        def get_sprite(name):
            return self.characters[name]
        
        def is_active(name):
            return name == self.game_state.selected_character
        
        def on_select(name):
            self.game_state.selected_character = name
            self.game_state.save_settings()
        
        generic_selection_menu(
            self.screen, self.clock, self.font, self.large_font, self.small_font,
            GAME_NAMES['select_character'],
            character_names,
            self.game_state.selected_character,
            get_sprite_func=get_sprite,
            get_active_func=is_active,
            on_select_func=on_select
        )
    
    def select_background(self):
        """Background selection using generic menu"""
        options = [bg['name'] for bg in BACKGROUNDS_CONFIG]
        
        def is_active(name):
            return name == self.game_state.selected_background
        
        def on_select(name):
            self.game_state.selected_background = name
            self.game_state.save_settings()
        
        generic_selection_menu(
            self.screen, self.clock, self.font, self.large_font, self.small_font,
            GAME_NAMES['select_background'],
            options,
            self.game_state.selected_background,
            backgrounds=self.backgrounds,
            get_active_func=is_active,
            on_select_func=on_select,
            preview_type='background'
        )
    
    def select_garbage_bag(self):
        """Garbage bag selection using generic menu"""
        options = list(self.garbage_bags.keys())
        
        def get_sprite(name):
            return self.garbage_bags[name]
        
        def is_active(name):
            return name == self.game_state.selected_garbage
        
        def on_select(name):
            self.game_state.selected_garbage = name
            self.game_state.save_settings()
        
        generic_selection_menu(
            self.screen, self.clock, self.font, self.large_font, self.small_font,
            GAME_NAMES['select_garbage_bag'],
            options,
            self.game_state.selected_garbage,
            get_sprite_func=get_sprite,
            get_active_func=is_active,
            on_select_func=on_select
        )
    
    def show_high_scores(self):
        """Display high scores with error handling"""
        import json
        try:
            with open('highscores.json', 'r') as f:
                scores = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError, IOError, OSError):
            scores = []
        
        while True:
            self.screen.fill(BLACK)
            title = self.large_font.render(GAME_NAMES['high_scores'].upper(), True, CYAN)
            title_rect = title.get_rect(center=(WINDOW_WIDTH//2, TITLE_Y_OFFSET))
            self.screen.blit(title, title_rect)
            
            if not scores:
                message = self.font.render(GAME_NAMES['no_scores_yet'], True, WHITE)
                message_rect = message.get_rect(center=(WINDOW_WIDTH//2, HIGH_SCORES_NO_SCORES_Y))
                self.screen.blit(message, message_rect)
            else:
                self._draw_high_scores_table(scores)
            
            # Back info
            back_info = self.font.render(GAME_NAMES['back_instruction'], True, GRAY)
            back_rect = back_info.get_rect(center=(WINDOW_WIDTH//2, INFO_TEXT_Y_BOTTOM))
            self.screen.blit(back_info, back_rect)
            
            pygame.display.flip()
            self.clock.tick(TARGET_FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    safe_exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        return
    
    def _draw_high_scores_table(self, scores):
        """Draw the high scores table"""
        y_pos = HIGH_SCORES_TABLE_START_Y
        positions = HIGH_SCORES_TABLE_POSITIONS
        headers = [GAME_NAMES['rank'], GAME_NAMES['name'], GAME_NAMES['score'], GAME_NAMES['difficulty_header']]
        
        for header, x_pos in zip(headers, positions):
            text = self.small_font.render(header, True, WHITE)
            self.screen.blit(text, (x_pos, y_pos))
        
        y_pos += HIGH_SCORES_HEADER_SPACING
        pygame.draw.line(self.screen, WHITE, (positions[0], y_pos), (positions[-1] + HIGH_SCORES_TABLE_EXTENSION, y_pos), THIN_LINE_WIDTH)
        y_pos += HIGH_SCORES_LINE_SPACING
        
        for i, score_info in enumerate(scores[:MAX_HIGH_SCORES]):
            self._draw_score_line(i, score_info, y_pos, positions)
            y_pos += HIGH_SCORES_ROW_SPACING
    
    def _draw_score_line(self, i, score_info, y_pos, positions):
        """Draw a single score line in the high scores table"""
        color = HIGH_SCORE_COLORS[i] if i < len(HIGH_SCORE_COLORS) else GRAY
        
        texts = [f"{i+1}.", score_info['name'][:MAX_NAME_LENGTH], str(score_info['score']), score_info['difficulty']]
        for text, x_pos in zip(texts, positions):
            text_surface = self.small_font.render(text, True, color)
            self.screen.blit(text_surface, (x_pos, y_pos))
    
    def run(self):
        """Main game loop"""
        self.game_state.load_settings()
        
        while True:
            menu_choice = self.main_menu()
            
            if menu_choice == 'settings':
                self.settings_menu()
                continue
            elif menu_choice != 'game':
                continue
            
            # Setup new game session
            if not enter_name(self.screen, self.clock, self.font, self.large_font, self.small_font, self.game_state):
                continue
            
            # Difficulty selection
            game_speed, difficulty_name = self.select_difficulty()
            if game_speed is None:
                self.game_state.player_name = ""
                continue
            
            # Run the game session
            while True:
                choice = self.run_game_session(game_speed, difficulty_name)
                if choice == 'play_again':
                    # Reset game state and play again with same settings
                    continue
                elif choice == 'main_menu':
                    # Go back to main menu
                    break
                else:
                    # ESC was pressed during game, go to main menu
                    break
    
    def select_difficulty(self):
        """Simplified difficulty selection"""
        options = list(self.speeds.keys())
        selected = 0
        
        while True:
            self.screen.fill(BLACK)
            title = self.font.render(GAME_NAMES['select_difficulty'], True, WHITE)
            title_rect = title.get_rect(center=(WINDOW_WIDTH//2, NAME_INPUT_TITLE_Y))
            self.screen.blit(title, title_rect)
            
            for i, name in enumerate(options):
                difficulty_color = self.difficulty_colors[name]
                y = DIFFICULTY_START_Y + i * DIFFICULTY_ITEM_SPACING
                
                if i == selected:
                    # Draw box for selected difficulty
                    box_x = WINDOW_WIDTH//2 - DIFFICULTY_BOX_WIDTH//2
                    pygame.draw.rect(self.screen, DARK_GRAY, (box_x, y - DIFFICULTY_BOX_Y_OFFSET, DIFFICULTY_BOX_WIDTH, DIFFICULTY_BOX_HEIGHT), 0, DIFFICULTY_MENU_RADIUS)
                    pygame.draw.rect(self.screen, difficulty_color, (box_x, y - DIFFICULTY_BOX_Y_OFFSET, DIFFICULTY_BOX_WIDTH, DIFFICULTY_BOX_HEIGHT), DIFFICULTY_MENU_BORDER_WIDTH, DIFFICULTY_MENU_RADIUS)
                    color = difficulty_color
                else:
                    color = difficulty_color
                    
                option = self.font.render(name, True, color)
                option_rect = option.get_rect(center=(WINDOW_WIDTH//2, y))
                self.screen.blit(option, option_rect)
            
            # ESC exit info
            exit_info = self.font.render(GAME_NAMES['exit_instruction'], True, GRAY)
            exit_rect = exit_info.get_rect(center=(WINDOW_WIDTH//2, GAME_OVER_EXIT_Y))
            self.screen.blit(exit_info, exit_rect)
            
            pygame.display.flip()
            self.clock.tick(TARGET_FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    safe_exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(options)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        return self.speeds[options[selected]], options[selected]
                    elif event.key == pygame.K_ESCAPE:
                        return None, None  # Return to main menu
    
    def run_game_session(self, game_speed, difficulty_name):
        """Run a complete game session"""
        collector = TrashCollector(self.characters[self.game_state.selected_character])
        trash = Trash(self.trash_sprites)
        score = 0
        last_dir = (1, 0)
        frame_counter = 0
        
        while True:
            # Handle input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    safe_exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return 'main_menu'
                    
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
            
            # Update game state
            frame_counter += 1
            
            if frame_counter >= (TARGET_FPS // game_speed):
                frame_counter = 0
                old_tail = collector.squares[-1]
                collector.move()
                
                # Check collision
                if collector.check_collision():
                    choice = self.game_over_screen(score, difficulty_name)
                    return choice
            
            # Check trash collection
            head_x, head_y = collector.squares[0]
            distance_x = abs(head_x - trash.x)
            distance_y = abs(head_y - trash.y)
            collision = (distance_x <= TRASH_COLLECTION_TOLERANCE) and (distance_y <= TRASH_COLLECTION_TOLERANCE)
            
            if collision:
                if frame_counter == 0:  # Just moved
                    collector.squares.append(old_tail)
                else:
                    collector.squares.append(collector.squares[-1])
                
                score += 1
                trash = Trash(self.trash_sprites)
            
            # Render
            self._render_game(collector, trash, score)
            self.clock.tick(TARGET_FPS)
    
    def _render_game(self, collector, trash, score):
        """Render the game screen"""
        # Draw background
        if self.game_state.selected_background in self.backgrounds:
            self.screen.blit(self.backgrounds[self.game_state.selected_background], (0, 0))
        else:
            self.screen.fill(BLACK)
            
        collector.draw(self.screen, self.garbage_bags[self.game_state.selected_garbage])
        trash.draw(self.screen)
        
        # Draw UI
        pygame.draw.rect(self.screen, DARK_GRAY, (0, 0, WINDOW_WIDTH, UI_AREA_HEIGHT))
        pygame.draw.rect(self.screen, LIGHT_GRAY, (0, UI_AREA_HEIGHT - UI_BORDER_HEIGHT, WINDOW_WIDTH, UI_BORDER_HEIGHT))
        
        # Player info
        player_text = self.small_font.render(f"{self.game_state.player_name}: {score} {GAME_NAMES['trash_collected']}", True, LIGHT_GRAY)
        self.screen.blit(player_text, (UI_PADDING, UI_PADDING))
        
        # ESC info
        esc_text = self.small_font.render(GAME_NAMES['main_menu_instruction'], True, LIGHT_GRAY)
        esc_width = esc_text.get_width()
        self.screen.blit(esc_text, (WINDOW_WIDTH - esc_width - UI_PADDING, UI_PADDING))
        
        pygame.display.flip()
    
    def game_over_screen(self, score, difficulty_name):
        """Simplified game over screen"""
        self._save_score(score, difficulty_name)
        
        while True:
            self.screen.fill(BLACK)
            
            title = self.large_font.render(GAME_NAMES['game_over'].upper(), True, RED)
            title_rect = title.get_rect(center=(WINDOW_WIDTH//2, GAME_OVER_TITLE_Y))
            self.screen.blit(title, title_rect)
            
            # Game result info
            player_text = self.font.render(f'{GAME_NAMES["player"]}: {self.game_state.player_name}', True, PURPLE)
            player_rect = player_text.get_rect(center=(WINDOW_WIDTH//2, GAME_OVER_PLAYER_Y))
            self.screen.blit(player_text, player_rect)
            
            score_text = self.font.render(f'{GAME_NAMES["collected_trash"]}: {score}', True, NEON_GREEN)
            score_rect = score_text.get_rect(center=(WINDOW_WIDTH//2, GAME_OVER_SCORE_Y))
            self.screen.blit(score_text, score_rect)
            
            # Difficulty info
            difficulty_color = self.difficulty_colors.get(difficulty_name, LIGHT_GRAY)
            difficulty_label = self.font.render(f'{GAME_NAMES["difficulty"]}: ', True, WHITE)
            difficulty_level = self.font.render(difficulty_name, True, difficulty_color)
            
            total_width = difficulty_label.get_width() + difficulty_level.get_width()
            start_x = (WINDOW_WIDTH - total_width) // 2
            
            difficulty_label_rect = difficulty_label.get_rect()
            difficulty_label_rect.x = start_x
            difficulty_label_rect.centery = GAME_OVER_DIFFICULTY_Y
            self.screen.blit(difficulty_label, difficulty_label_rect)
            
            difficulty_level_rect = difficulty_level.get_rect()
            difficulty_level_rect.x = start_x + difficulty_label_rect.width
            difficulty_level_rect.centery = GAME_OVER_DIFFICULTY_Y
            self.screen.blit(difficulty_level, difficulty_level_rect)
            
            environmental_msg = self.font.render(GAME_NAMES['environmental_message'], True, NEON_GREEN)
            environmental_rect = environmental_msg.get_rect(center=(WINDOW_WIDTH//2, GAME_OVER_MESSAGE_Y))
            self.screen.blit(environmental_msg, environmental_rect)
            
            # Draw options with highlighting
            self._draw_game_over_options()
            
            pygame.display.flip()
            self.clock.tick(TARGET_FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    safe_exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return 'play_again'  # Play again
                    elif event.key == pygame.K_s:
                        self.show_high_scores()
                    elif event.key == pygame.K_ESCAPE:
                        return 'main_menu'  # Go to main menu
    
    def _draw_game_over_options(self):
        """Draw game over screen options"""
        # ENTER option
        enter_prefix = self.font.render('Press ', True, WHITE)
        enter_key = self.font.render('ENTER', True, NEON_GREEN)
        enter_suffix = self.font.render(' to play again', True, WHITE)
        
        total_enter_width = enter_prefix.get_width() + enter_key.get_width() + enter_suffix.get_width()
        enter_start_x = (WINDOW_WIDTH - total_enter_width) // 2
        enter_y = GAME_OVER_OPTION_Y_START
        
        self.screen.blit(enter_prefix, (enter_start_x, enter_y))
        self.screen.blit(enter_key, (enter_start_x + enter_prefix.get_width(), enter_y))
        self.screen.blit(enter_suffix, (enter_start_x + enter_prefix.get_width() + enter_key.get_width(), enter_y))
        
        # S option
        s_prefix = self.font.render('Press ', True, WHITE)
        s_key = self.font.render('S', True, YELLOW)
        s_suffix = self.font.render(' to show scores', True, WHITE)
        
        total_s_width = s_prefix.get_width() + s_key.get_width() + s_suffix.get_width()
        s_start_x = (WINDOW_WIDTH - total_s_width) // 2
        s_y = GAME_OVER_OPTION_Y_START + GAME_OVER_OPTION_Y_SPACING
        
        self.screen.blit(s_prefix, (s_start_x, s_y))
        self.screen.blit(s_key, (s_start_x + s_prefix.get_width(), s_y))
        self.screen.blit(s_suffix, (s_start_x + s_prefix.get_width() + s_key.get_width(), s_y))
        
        # ESC option
        esc_prefix = self.font.render('Press ', True, WHITE)
        esc_key = self.font.render('ESC', True, RED)
        esc_suffix = self.font.render(' for main menu', True, WHITE)
        
        total_esc_width = esc_prefix.get_width() + esc_key.get_width() + esc_suffix.get_width()
        esc_start_x = (WINDOW_WIDTH - total_esc_width) // 2
        esc_y = GAME_OVER_OPTION_Y_START + (GAME_OVER_OPTION_Y_SPACING * 2)
        
        self.screen.blit(esc_prefix, (esc_start_x, esc_y))
        self.screen.blit(esc_key, (esc_start_x + esc_prefix.get_width(), esc_y))
        self.screen.blit(esc_suffix, (esc_start_x + esc_prefix.get_width() + esc_key.get_width(), esc_y))
    
    def _save_score(self, score, difficulty):
        """Save player score with comprehensive error handling"""
        import json
        try:
            with open('highscores.json', 'r') as f:
                scores = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError, IOError, OSError):
            scores = []
        
        # Check if player with same name exists
        existing_player_index = -1
        for i, player in enumerate(scores):
            if player['name'] == self.game_state.player_name:
                existing_player_index = i
                break
        
        new_score = {
            'name': self.game_state.player_name,
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
        scores = scores[:MAX_HIGH_SCORES]
        
        try:
            with open('highscores.json', 'w') as f:
                json.dump(scores, f, indent=2)
        except (IOError, OSError) as e:
            print(f"Warning: Could not save high scores: {e}")


def main():
    """Main entry point - creates and runs the game"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()