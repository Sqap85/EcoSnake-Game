#!/usr/bin/env python3
"""
EcoSnake Game - Game State Management
Handles settings persistence and game state
"""

import json
from constants import CHARACTERS_CONFIG, BACKGROUNDS_CONFIG, GARBAGE_BAGS_CONFIG


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