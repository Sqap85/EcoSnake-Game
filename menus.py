#!/usr/bin/env python3
"""
EcoSnake Game - Menu System
All menu-related functions and UI components
"""

import pygame
import sys
from constants import *


def safe_exit():
    """Safely exit the game"""
    pygame.quit()
    sys.exit()


def draw_menu_box(screen, box_rect, selected=False):
    """Draw a menu box with selection highlighting"""
    if selected:
        pygame.draw.rect(screen, DARK_GRAY, box_rect, 0, MENU_BOX_RADIUS)
        pygame.draw.rect(screen, CYAN, box_rect, MENU_BOX_BORDER_WIDTH_SELECTED, MENU_BOX_RADIUS)
    else:
        pygame.draw.rect(screen, MENU_BOX_COLOR, box_rect, 0, MENU_BOX_RADIUS)
        pygame.draw.rect(screen, LIGHT_GRAY, box_rect, MENU_BOX_BORDER_WIDTH, MENU_BOX_RADIUS)


def draw_selection_menu_item(screen, font, small_font, name, y, is_selected, box_x, get_sprite_func, get_active_func, preview_type, backgrounds):
    """Draw a single menu item"""
    box_rect = pygame.Rect(box_x, y-MENU_BOX_Y_OFFSET, MENU_BOX_WIDTH, MENU_BOX_HEIGHT)
    draw_menu_box(screen, box_rect, is_selected)
    
    # Show sprite/preview
    if get_sprite_func:
        sprite = get_sprite_func(name)
        if sprite:
            large_sprite = pygame.transform.scale(sprite, (LARGE_SPRITE_SIZE, LARGE_SPRITE_SIZE))
            sprite_rect = large_sprite.get_rect(center=(box_x + LARGE_SPRITE_SIZE, y + MENU_BOX_SPRITE_CENTER_Y))
            screen.blit(large_sprite, sprite_rect)
    elif preview_type == 'background':
        draw_background_preview(screen, name, box_x, y, backgrounds)
    
    # Show name
    color = CYAN if is_selected else WHITE
    name_text = font.render(name, True, color)
    name_rect = name_text.get_rect(center=(box_x + MENU_TEXT_X_POSITION, y + MENU_BOX_NAME_CENTER_Y))
    screen.blit(name_text, name_rect)
    
    # Show active indicator
    if get_active_func and get_active_func(name):
        active_text = small_font.render(GAME_NAMES['active'], True, NEON_GREEN)
        active_rect = active_text.get_rect(center=(box_x + MENU_TEXT_X_POSITION, y + MENU_BOX_ACTIVE_CENTER_Y))
        screen.blit(active_text, active_rect)


def draw_background_preview(screen, name, box_x, y, backgrounds):
    """Draw background preview for selection menu"""
    if name == 'Black':
        preview_rect = pygame.Rect(0, 0, LARGE_SPRITE_SIZE, LARGE_SPRITE_SIZE)
        preview_rect.center = (box_x + LARGE_SPRITE_SIZE, y + MENU_BOX_SPRITE_CENTER_Y)
        pygame.draw.rect(screen, BLACK, preview_rect, 0, BACKGROUND_PREVIEW_RADIUS)
    elif name in backgrounds:
        try:
            preview = pygame.transform.scale(backgrounds[name], (LARGE_SPRITE_SIZE, LARGE_SPRITE_SIZE))
            sprite_rect = preview.get_rect(center=(box_x + LARGE_SPRITE_SIZE, y + MENU_BOX_SPRITE_CENTER_Y))
            screen.blit(preview, sprite_rect)
        except (pygame.error, ValueError, TypeError):
            color = GREEN if name == 'Forest' else BLUE
            preview_rect = pygame.Rect(0, 0, LARGE_SPRITE_SIZE, LARGE_SPRITE_SIZE)
            preview_rect.center = (box_x + LARGE_SPRITE_SIZE, y + MENU_BOX_SPRITE_CENTER_Y)
            pygame.draw.rect(screen, color, preview_rect, 0, BACKGROUND_PREVIEW_RADIUS)


def handle_selection_menu_input(selected, options_count, on_select_func, options):
    """Handle input for selection menu"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            safe_exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return selected, True  # Exit
            elif event.key == pygame.K_UP:
                selected = (selected - 1) % options_count
            elif event.key == pygame.K_DOWN:
                selected = (selected + 1) % options_count
            elif event.key == pygame.K_RETURN:
                if on_select_func:
                    on_select_func(options[selected])
                return selected, True  # Exit
    return selected, False


def generic_selection_menu(screen, clock, font, large_font, small_font, title_text, options, selected_option, backgrounds=None, get_sprite_func=None, get_active_func=None, on_select_func=None, preview_type=None):
    """Simplified selection menu"""
    selected = options.index(selected_option) if selected_option in options else 0
    
    while True:
        screen.fill(BLACK)
        
        # Title
        title = large_font.render(title_text.upper(), True, CYAN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, TITLE_Y_OFFSET))
        screen.blit(title, title_rect)
        
        pygame.draw.line(screen, CYAN, (TITLE_LINE_MARGIN, TITLE_LINE_Y), (WINDOW_WIDTH-TITLE_LINE_MARGIN, TITLE_LINE_Y), LINE_BORDER_WIDTH)
        
        # Show options
        box_x = WINDOW_WIDTH//2 - MENU_BOX_WIDTH//2
        for i, name in enumerate(options):
            y = MENU_START_Y + i * MENU_VERTICAL_SPACING
            is_selected = (i == selected)
            draw_selection_menu_item(screen, font, small_font, name, y, is_selected, box_x, get_sprite_func, get_active_func, preview_type, backgrounds)
        
        pygame.display.flip()
        clock.tick(TARGET_FPS)
        
        # Handle input
        selected, should_exit = handle_selection_menu_input(selected, len(options), on_select_func, options)
        if should_exit:
            return


def draw_name_input_box(screen, font, input_text, box_rect):
    """Draw the name input box with text and cursor"""
    pygame.draw.rect(screen, MENU_BOX_COLOR, box_rect, 0, NAME_INPUT_RADIUS)
    pygame.draw.rect(screen, YELLOW if input_text else GRAY, box_rect, NAME_INPUT_BORDER_WIDTH, NAME_INPUT_RADIUS)
    
    # Show text
    if input_text:
        text = font.render(input_text, True, WHITE)
    else:
        text = font.render(GAME_NAMES['type_your_name'], True, GRAY)
    text_rect = text.get_rect(center=box_rect.center)
    screen.blit(text, text_rect)
    
    # Draw blinking cursor
    if pygame.time.get_ticks() % CURSOR_BLINK_INTERVAL < (CURSOR_BLINK_INTERVAL // 2):
        if input_text:
            cursor_x = text_rect.right + CURSOR_TEXT_SPACING
        else:
            cursor_x = box_rect.left + UI_PADDING
        pygame.draw.line(screen, YELLOW, (cursor_x, box_rect.top + CURSOR_MARGIN), (cursor_x, box_rect.bottom - CURSOR_MARGIN), CURSOR_LINE_WIDTH)


def draw_name_input_instructions(screen, font, small_font, input_text):
    """Draw instructions for name input"""
    # Rules
    rule = small_font.render(GAME_NAMES['name_length_rule'], True, GRAY)
    rule_rect = rule.get_rect(center=(WINDOW_WIDTH//2, NAME_INPUT_RULE_Y))
    screen.blit(rule, rule_rect)
    
    # Enter button
    enter_active = len(input_text.strip()) >= MIN_NAME_LENGTH
    enter_color = GREEN if enter_active else GRAY
    enter_text = font.render(GAME_NAMES['confirm_button'], True, enter_color)
    enter_rect = enter_text.get_rect(center=(WINDOW_WIDTH//2, NAME_INPUT_CONFIRM_Y))
    screen.blit(enter_text, enter_rect)
    
    # ESC instruction
    esc_text = small_font.render(GAME_NAMES['return_instruction'], True, GRAY)
    esc_rect = esc_text.get_rect(center=(WINDOW_WIDTH//2, NAME_INPUT_ESC_Y))
    screen.blit(esc_text, esc_rect)


def handle_name_input_event(event, input_text):
    """Handle a single input event for name entry"""
    if event.type == pygame.QUIT:
        safe_exit()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            return input_text, 'exit'
        elif event.key == pygame.K_RETURN:
            if len(input_text.strip()) >= MIN_NAME_LENGTH:
                return input_text.strip(), 'confirm'
        elif event.key == pygame.K_BACKSPACE:
            return input_text[:-1], 'continue'
        else:
            if event.unicode.isprintable() and len(input_text) < MAX_NAME_LENGTH:
                return input_text + event.unicode, 'continue'
    return input_text, 'continue'


def enter_name(screen, clock, font, large_font, small_font, game_state):
    """Get player name input"""
    input_text = ""
    
    while True:
        screen.fill(BLACK)
        
        # Title
        title = large_font.render(GAME_NAMES['enter_player_name'], True, YELLOW)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, NAME_INPUT_TITLE_Y))
        screen.blit(title, title_rect)
        
        # Input box
        box_rect = pygame.Rect(WINDOW_WIDTH//2 - NAME_INPUT_WIDTH//2, NAME_INPUT_Y, NAME_INPUT_WIDTH, NAME_INPUT_HEIGHT)
        draw_name_input_box(screen, font, input_text, box_rect)
        
        # Instructions
        draw_name_input_instructions(screen, font, small_font, input_text)
        
        pygame.display.flip()
        clock.tick(TARGET_FPS)
        
        # Handle events
        for event in pygame.event.get():
            input_text, action = handle_name_input_event(event, input_text)
            if action == 'exit':
                return False
            elif action == 'confirm':
                game_state.player_name = input_text
                return True