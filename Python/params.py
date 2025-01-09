"""
    @file        params.py
    @author      Mowibox (Ousmane THIONGANE)
    @brief       Parameters for the Pymon game project
    @version     1.0
    @date        2025-01-08
    
"""
# Imports
from game_classes import GameState, ColorBGR 

# Variables
level = 1                       # Game level
hard = False                    # Difficulty management
canPlay = False                 # Ability to play or not
numberOfLives = 3               # Number of lives
listAppend = True               # Add elements to the user sequence, prevents switch bouncing
max_level_easy = 1              # Best score easy mode management  
max_level_hard = 1              # Best score hard mode management  
FRAME_WIDTH = 1280              # Frame Width
FRAME_HEIGHT = 720              # Frame Height
time_elapsed = None             # Time management variable
lifeColor = ColorBGR.GREEN      # Color of life points
gameState = GameState.MENU      # Game state management

