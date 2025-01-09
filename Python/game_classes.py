"""
    @file        utils.py
    @author      Mowibox (Ousmane THIONGANE)
    @brief       Classes for the Pymon game project
    @version     1.0
    @date        2025-01-08
    
"""

# Imports 
import cv2
import numpy as np
from enum import Enum, IntEnum

class GameState(IntEnum):
    MENU = 0
    PLAYING = 1
    SETTINGS = 2
    LEVEL_COMPLETE = 3
    LEVEL_FAILURE = 4
    GAME_OVER = 5
    DIFFICULTY_SETTINGS = 6
    SCORE_SETTINGS = 7


class ColorBox(Enum):
    RED = bytearray(b'r')
    YELLOW = bytearray(b'y')
    GREEN = bytearray(b'g')
    BLUE = bytearray(b'b')
    MULTI = bytearray(b'm')
    NONE = bytearray(b'n')


class ColorBGR(tuple):
    RED = (0, 0, 255)
    DARK_RED = (0, 0, 220)
    DARKER_RED = (0, 0, 180)
    ORANGE = (0, 80, 255)
    YELLOW = (0, 255, 255)
    GOLD = (0, 230, 245)
    GREEN = (0, 255, 0)
    DARK_GREEN = (0, 220, 0)
    CYAN = (255, 255, 0)
    BLUE = (255, 0, 0)
    PINK = (255, 0, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)


class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: str=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, frame: np.ndarray, color: tuple=ColorBGR.BLACK):
        """
        Draws the rectangle button in the provided frame

        @param frame: The actual frame
        @param color: The button color 
        """
        cv2.rectangle(frame, (self.x, self.y), (self.x + self.width, self.y + self.height), color, 8)
        if self.text:
            text_size = cv2.getTextSize(self.text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
            text_x = self.x + (self.width - text_size[0])//2
            text_y = self.y - 10 + (self.height + text_size[1])//2
            cv2.putText(frame, self.text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 4)

    def intersects(self, hand_rect) -> bool:
        """
        Checks if the button object intersects with the hand

        @param other_rect: The hand rectangle detection
        """
        return self.x < hand_rect.x + hand_rect.width and \
               self.x + self.width > hand_rect.x and \
               self.y < hand_rect.y + hand_rect.height and \
               self.y + self.height > hand_rect.y
    

class Text:
    def __init__(self, x, y, text, font_scale=1, color=ColorBGR.BLACK, thickness=3, font=cv2.FONT_HERSHEY_SIMPLEX):
        self.x = x
        self.y = y
        self.text = text
        self.font_scale = font_scale
        self.color = color
        self.thickness = thickness
        self.font = font

    def draw(self, frame: np.ndarray):
        """
        Draw the text on the provided frame

        @param frame: The actual frame
        """
        cv2.putText(frame, self.text, (self.x, self.y), self.font, self.font_scale, self.color, self.thickness)

    def update_text(self, text: str):
        """
        Changes the displayed text

        @param text: The new text
        """
        self.text = text

    def update_color(self, color: tuple) -> tuple:
        """
        Changes the color of the text

        @param color: The new text color
        """
        self.color = color