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

# Buttons & Texts
StartButton = Button(60, 50, 250, 150, 'Start')
SettingsButton = Button(950, 50, 250, 150, 'Settings')

PlayerButton = Button(60, 50, 250, 150, 'Player')
DifficultyButton = Button(950, 50, 250, 150, 'Difficulty')
BackButton = Button(60, 550, 250, 150, 'Back')
RankingButton = Button(950, 550, 250, 150, 'Score')

RedButton = Button(50, 30, 250, 150, 'Red')
YellowButton = Button(960, 30, 250, 150, 'Yellow')
GreenButton = Button(50, 550, 250, 150, 'Green')
BlueButton = Button(960, 550, 250, 150, 'Blue')

gameText = Text(370, 400, "Watch the light sequence...")
LevelText = Text(580, 560, f"Level: {level}")
livesText = Text(560, 50, f"Lives: {numberOfLives}")
newRecordText = Text(550, 520, "New record!", color=ColorBGR.GOLD)

EasyButton = Button(950, 50, 250, 150, 'Easy')
HardButton = Button(60, 50, 250, 150, 'Hard')

bestScoreText = Text(560, 50, "Best score", color=ColorBGR.GOLD)
scoreEasyText = Text(470, 490, f"Easy mode - Level: {max_level_easy}")
scoreHardText = Text(470, 540, f"Hard mode - Level: {max_level_hard}")

logo_path = os.path.join(os.getcwd(), 'Python', 'img', 'Pymonlogo.png')
logo = cv2.imread(logo_path)
logo = cv2.resize(logo, (150,150))
