"""
    @file        utils.py
    @author      Mowibox (Ousmane THIONGANE)
    @brief       Utilitary functions for the Pymon project
    @version     1.0
    @date        2025-01-08
    
"""

# Imports 
import serial
import random as r
import numpy as np
from params import *
import mediapipe as mp
from game_classes import *
import serial.tools.list_ports


def find_box_port(baudrate: int=38400) -> serial.Serial:
    """
    Finds and open the serial communication with the game box

    @param: baudrate: The serial communication baudrate. Default is 38400
    """
    ports = serial.tools.list_ports.comports()
    stm32_port = None
    for port, desc, _ in sorted(ports):
        if "STM32" in desc:  # Check port description to find STM32 port
            stm32_port = port
            break

    return serial.Serial(stm32_port, baudrate=baudrate)


def detect_hands(frame: np.ndarray, 
                 mp_hands: mp.solutions.hands, 
                 hands: mp.solutions.hands.Hands) -> tuple:
    """
    Detects and displays the player's hand

    @param frame: The actual frame 
    @param mp_hands: The Mediapipe hands solution
    @param hands: The Mediapipe hands object
    """

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(gray)

    hand_rect = None  
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            x_min, y_min, x_max, y_max = float('inf'), float('inf'), 0, 0
            for landmark in hand_landmarks.landmark:
                x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
                if x < x_min:
                    x_min = x
                if x > x_max:
                    x_max = x
                if y < y_min:
                    y_min = y
                if y > y_max:
                    y_max = y

            landmark_drawing_spec = mp.solutions.drawing_utils.DrawingSpec(color=ColorBGR.CYAN)
            mp.solutions.drawing_utils.draw_landmarks(frame, 
                                                      hand_landmarks, 
                                                      mp_hands.HAND_CONNECTIONS, 
                                                      landmark_drawing_spec)

            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (255, 0, 255), 6)
            hand_rect = Button(x_min, y_min, x_max - x_min, y_max - y_min) 
            return frame, hand_rect
    else:
        return frame, hand_rect
    

def generateSequence(level: int) -> list:
    """
    Creates the random sequence to guess

    @param level: The game level
    """
    if hard or level == 1:
        memoryList = []
        for _ in range(level+2):
            color = r.choice(list(ColorBox)[:-2]).value
            memoryList.append(color)
    return memoryList


def checkGameState(playerList: list, memoryList: list) -> int:
    """
    Checks the game state by comparing the player list
    and the sequence to perform

    @param playerList: The player sequence
    @param memoryList: The sequence to perform

    [Status values]
    - 0: No errors made by the player choice, game continues
    - 1: The level is completed successfully
    - 2: An error is made by the player, 1 life is lost
    - 3: No event is triggered
    """
    n = len(playerList)
    if n != 0:
        if playerList[n-1] == memoryList[n-1]:
            if n == len(memoryList):
                return 1 
            else:
                return 0 
        else:
            return 2 
    else:
        return 0 