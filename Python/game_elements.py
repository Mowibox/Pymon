"""
    @file        game_elements.py
    @author      Mowibox (Ousmane THIONGANE)
    @brief       Game elements for the Pymon game project
    @version     1.0
    @date        2025-01-09
    
"""

# Imports 
import os
from params import *
from utils import Button
from game_classes import *


def scale_width(factor: float) -> int:
    """
    Adjusts the width of an element based on the frame size

    @param factor: The scaling factor
    """
    return int(FRAME_WIDTH * factor)

def scale_height(factor: float) -> int:
    """
    Adjusts the height of an element based on the frame size

    @param factor: The scaling factor
    """
    return int(FRAME_HEIGHT * factor)

# Buttons & Texts
StartButton = Button(scale_width(0.05), scale_height(0.07), scale_width(0.2), scale_height(0.2), 'Start')
SettingsButton = Button(scale_width(0.75), scale_height(0.07), scale_width(0.2), scale_height(0.2), 'Settings')

PlayerButton = Button(scale_width(0.05), scale_height(0.07), scale_width(0.2), scale_height(0.2), 'Player')
DifficultyButton = Button(scale_width(0.75), scale_height(0.07), scale_width(0.2), scale_height(0.2), 'Difficulty')
BackButton = Button(scale_width(0.05), scale_height(0.75), scale_width(0.2), scale_height(0.2), 'Back')
RankingButton = Button(scale_width(0.75), scale_height(0.75), scale_width(0.2), scale_height(0.2), 'Score')

RedButton = Button(scale_width(0.04), scale_height(0.05), scale_width(0.2), scale_height(0.2), 'Red')
YellowButton = Button(scale_width(0.75), scale_height(0.05), scale_width(0.2), scale_height(0.2), 'Yellow')
GreenButton = Button(scale_width(0.04), scale_height(0.75), scale_width(0.2), scale_height(0.2), 'Green')
BlueButton = Button(scale_width(0.75), scale_height(0.75), scale_width(0.2), scale_height(0.2), 'Blue')

gameText = Text(scale_width(0.29), scale_height(0.55), "Watch the light sequence...")
LevelText = Text(scale_width(0.45), scale_height(0.78), f"Level: {level}")
livesText = Text(scale_width(0.44), scale_height(0.07), f"Lives: {numberOfLives}")
newRecordText = Text(scale_width(0.43), scale_height(0.72), "New record!", color=ColorBGR.GOLD)

EasyButton = Button(scale_width(0.75), scale_height(0.07), scale_width(0.2), scale_height(0.2), 'Easy')
HardButton = Button(scale_width(0.05), scale_height(0.07), scale_width(0.2), scale_height(0.2), 'Hard')

bestScoreText = Text(scale_width(0.44), scale_height(0.07), "Best score", color=ColorBGR.GOLD)
scoreEasyText = Text(scale_width(0.37), scale_height(0.68), f"Easy mode - Level: {max_level_easy}")
scoreHardText = Text(scale_width(0.37), scale_height(0.75), f"Hard mode - Level: {max_level_hard}")

# Logo
logo_path = os.path.join(os.getcwd(), 'Python', 'img', 'Pymonlogo.png')
logo = cv2.imread(logo_path)
logo = cv2.resize(logo, (scale_width(0.12), scale_height(0.2)))
