#!/usr/bin/env python3
"""
EcoSnake Game - Core Game Objects
TrashCollector, Trash, and related game logic
"""

import pygame
import random
from constants import *


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

    def draw(self, screen, selected_garbage_sprite):
        head_x, head_y = self.squares[0]
        screen.blit(self.character_sprite, (head_x, head_y))
        for (x, y) in self.squares[1:]:
            screen.blit(selected_garbage_sprite, (x, y))

    def check_collision(self):
        """Optimized collision detection - skip first few segments (can't collide immediately)"""
        if len(self.squares) < 4:  # Can't collide with itself if too short
            return False
            
        head_x, head_y = self.squares[0]
        # Skip first 3 segments (head can't immediately collide with neck/shoulder)
        for segment_x, segment_y in self.squares[3:]:
            if (abs(head_x - segment_x) <= COLLISION_TOLERANCE and 
                abs(head_y - segment_y) <= COLLISION_TOLERANCE):
                return True
        return False


class Trash:
    def __init__(self, trash_sprites):
        min_x = TRASH_SPAWN_MARGIN_X
        max_x = (WINDOW_WIDTH // SQUARE_SIZE) - TRASH_SPAWN_EDGE_BUFFER
        min_y = TRASH_SPAWN_MARGIN_Y
        max_y = (WINDOW_HEIGHT // SQUARE_SIZE) - TRASH_SPAWN_EDGE_BUFFER
        
        self.x = random.randint(min_x, max_x) * SQUARE_SIZE
        self.y = random.randint(min_y, max_y) * SQUARE_SIZE
        
        self.type = random.choice(list(trash_sprites.keys()))
        self.sprite = trash_sprites[self.type]
    
    def draw(self, screen):
        screen.blit(self.sprite, (self.x, self.y))