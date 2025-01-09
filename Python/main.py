"""
    @file        main.py
    @author      Mowibox (Ousmane THIONGANE)
    @brief       Game project developed with OpenCV and STM32 for the Image & Virtual Reality Workshop
    @version     2.0
    @date        2024-04-01
    
"""

# Imports
import time
from utils import *
from params import * 
from game_classes import *
from game_elements import *


def main():
    global max_level_easy, hard, gameState, numberOfLives, canPlay, FRAME_HEIGHT
    global max_level_hard, level, lifeColor, listAppend, time_elapsed, FRAME_WIDTH

    ser = find_box_port()
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1, 
                        min_detection_confidence=0.6, 
                        min_tracking_confidence=0.6)

    scene = cv2.VideoCapture(0)

    scene.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)  
    scene.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    while scene.isOpened():
        ret, frame = scene.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)

        width, height, _ = frame.shape
        if (int(width), int(height)) != (FRAME_WIDTH, FRAME_HEIGHT):
            frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))

        frame, hand_rect = detect_hands(frame, mp_hands, hands)

    # ========================= Menu ===========================

        if gameState == GameState.MENU:
            StartButton.draw(frame)
            SettingsButton.draw(frame)

            if hand_rect is not None:
                if StartButton.intersects(hand_rect):
                    ser.write(ColorBox.NONE.value)
                    StartButton.draw(frame, ColorBGR.PINK) 
                    if time_elapsed is None:
                        time_elapsed = time.time()  
                    elif time.time() - time_elapsed > 2:
                        time_elapsed = None  
                        gameState = GameState.PLAYING 
                else:
                    StartButton.draw(frame, ColorBGR.BLACK)  
            else:
                ser.write(ColorBox.MULTI.value)

            if hand_rect is not None:
                if SettingsButton.intersects(hand_rect):
                    ser.write(ColorBox.NONE.value)
                    SettingsButton.draw(frame, ColorBGR.PINK)
                    if time_elapsed is None:
                        time_elapsed = time.time()  
                    elif time.time() - time_elapsed > 2:
                        time_elapsed = None  
                        gameState = GameState.SETTINGS  
                else:
                    SettingsButton.draw(frame)       
            else:
                time_elapsed = None
                ser.write(ColorBox.MULTI.value)

    # ================== Observation sequence ==================

        if gameState == GameState.PLAYING and not(canPlay): 
            frame = np.zeros_like(frame)
            RedButton.draw(frame, ColorBGR.RED)
            YellowButton.draw(frame, ColorBGR.YELLOW)
            GreenButton.draw(frame, ColorBGR.GREEN)
            BlueButton.draw(frame, ColorBGR.BLUE)
            gameText.update_color(ColorBGR.WHITE)
            gameText.update_text("Watch the light sequence...")
            LevelText.update_text(f"Level: {level}")
            livesText.update_text(f"Lives: {numberOfLives}")
            livesText.update_color(lifeColor)
            livesText.draw(frame)
            LevelText.draw(frame)
            gameText.draw(frame)

            # Create the sequence to be performed
            if time_elapsed is None:
                    ser.write(ColorBox.NONE.value)
                    time_elapsed = time.time()  
            elif time.time() - time_elapsed > 3:  
                time_elapsed = None
                if hard or level == 1:
                    memoryList = generateSequence(level)
                for i in range(len(memoryList)):
                    ser.write(memoryList[i])
                    time.sleep(0.6)
                    ser.write(ColorBox.NONE.value)
                    time.sleep(0.6)
                playerList = []
                canPlay = True
                
    # ======================= Playing ==========================

        if gameState == GameState.PLAYING and canPlay: 
            RedButton.draw(frame, ColorBGR.RED)
            YellowButton.draw(frame, ColorBGR.YELLOW)
            GreenButton.draw(frame, ColorBGR.GREEN)
            BlueButton.draw(frame, ColorBGR.BLUE)
            LevelText.update_text(f"Level: {level}")
            livesText.update_text(f"Lives: {numberOfLives}")
            livesText.update_color(lifeColor)
            livesText.draw(frame)
            LevelText.draw(frame)

            status = checkGameState(playerList, memoryList) 
            if status == 1:
                if time_elapsed is None:
                    time_elapsed = time.time()  
                elif time.time() - time_elapsed > 0.3:  
                    time_elapsed = None
                    gameState = GameState.LEVEL_COMPLETE
            elif status == 2:
                numberOfLives-=1
                if numberOfLives <= 0: 
                    gameState = GameState.GAME_OVER
                else:
                    gameState = GameState.LEVEL_FAILURE

            gameText.update_color(ColorBGR.BLACK)
            gameText.update_text("Your turn!")
            gameText.draw(frame)
            if hand_rect is not None: 
                if RedButton.intersects(hand_rect):
                    RedButton.draw(frame, ColorBGR.PINK)
                    if listAppend:
                        playerList.append(ColorBox.RED.value) 
                        listAppend = False
                    ser.write(ColorBox.RED.value)   
                elif YellowButton.intersects(hand_rect): 
                    YellowButton.draw(frame, ColorBGR.PINK) 
                    if listAppend:
                        playerList.append(ColorBox.YELLOW.value) 
                        listAppend = False
                    ser.write(ColorBox.YELLOW.value)  
                elif GreenButton.intersects(hand_rect): 
                    GreenButton.draw(frame, ColorBGR.PINK) 
                    if listAppend:
                        playerList.append(ColorBox.GREEN.value) 
                        listAppend = False
                    ser.write(ColorBox.GREEN.value)
                elif BlueButton.intersects(hand_rect): 
                    BlueButton.draw(frame, ColorBGR.PINK) 
                    if listAppend:
                        playerList.append(ColorBox.BLUE.value) 
                        listAppend = False
                    ser.write(ColorBox.BLUE.value)             
                else:  
                    RedButton.draw(frame, ColorBGR.RED)
                    YellowButton.draw(frame, ColorBGR.YELLOW)
                    GreenButton.draw(frame, ColorBGR.GREEN)
                    BlueButton.draw(frame, ColorBGR.BLUE)
                    if not(listAppend):
                        listAppend = True
                    ser.write(ColorBox.NONE.value)

    # ===================== Level Complete =====================

        if gameState == GameState.LEVEL_COMPLETE:  
            ser.write(b'n')
            gameText.update_text("Congratulations! Next level!")
            gameText.update_color(ColorBGR.GREEN)
            LevelText.update_text(f"Level: {level}")
            livesText.update_text(f"Lives: {numberOfLives}")
            livesText.update_color(lifeColor)
            livesText.draw(frame)
            LevelText.draw(frame)
            gameText.draw(frame)
            if time_elapsed is None:
                    time_elapsed = time.time()  
            elif time.time() - time_elapsed > 2:  
                gameState = GameState.PLAYING
                canPlay = False

                if not(hard):
                    color = r.randint(0,3)
                    if color == 0:
                        memoryList.append(ColorBox.RED.value)
                    elif color == 1:
                        memoryList.append(ColorBox.YELLOW.value)
                    elif color == 2:
                        memoryList.append(ColorBox.GREEN.value)
                    elif color == 3:
                        memoryList.append(ColorBox.BLUE.value)
                level += 1
                time_elapsed = None

    # ====================== Level Failure =====================

        if gameState == GameState.LEVEL_FAILURE:
            ser.write(ColorBox.NONE.value)
            gameText.update_text("Try again...")
            gameText.update_color(ColorBGR.DARK_RED)
            gameText.draw(frame)
            livesText.update_text(f"Lives: {numberOfLives}")
            livesText.update_color(lifeColor)
            livesText.draw(frame)
            LevelText.update_text(f"Level: {level}")
            LevelText.draw(frame)
            if time_elapsed is None:
                    time_elapsed = time.time()  
            elif time.time() - time_elapsed > 2:  
                gameState = GameState.PLAYING
                canPlay = False
                time_elapsed = None

    # ====================== GAME OVER =========================

        if gameState == GameState.GAME_OVER:
            ser.write(ColorBox.NONE.value)
            gameText.update_text("GAME OVER...")
            gameText.update_color(ColorBGR.DARKER_RED)
            livesText.update_text(f"Lives: {numberOfLives}")
            livesText.update_color(lifeColor)
            livesText.draw(frame)
            LevelText.update_text(f"Level: {level}")
            LevelText.draw(frame)
            gameText.draw(frame)

            if not(hard):
                if level >= max_level_easy:
                    max_level_easy = level
                    newRecordText.draw(frame)
            else:
                if level >= max_level_hard:
                    max_level_hard = level
                    newRecordText.draw(frame)

            if time_elapsed is None:
                    time_elapsed = time.time()  
            elif time.time() - time_elapsed > 3:  
                gameState = GameState.MENU
                level = 1
                numberOfLives = 3
                canPlay = False
                time_elapsed = None

    # ======================= Settings ==========================
        
        if gameState == GameState.SETTINGS: 
            RankingButton.draw(frame)
            PlayerButton.draw(frame)
            BackButton.draw(frame)
            DifficultyButton.draw(frame)
        
            if hand_rect is not None:
                if BackButton.intersects(hand_rect):
                    ser.write(ColorBox.NONE.value)
                    BackButton.draw(frame, ColorBGR.PINK) 
                    if time_elapsed is None:
                        time_elapsed = time.time()  
                    elif time.time() - time_elapsed > 2:  
                        time_elapsed = None
                        gameState = GameState.MENU 
                elif DifficultyButton.intersects(hand_rect):
                    ser.write(ColorBox.NONE.value)
                    DifficultyButton.draw(frame, ColorBGR.PINK) 
                    if time_elapsed is None:
                        time_elapsed = time.time()  
                    elif time.time() - time_elapsed > 2:  
                        time_elapsed = None
                        gameState = GameState.DIFFICULTY_SETTINGS
                elif RankingButton.intersects(hand_rect):
                    ser.write(ColorBox.NONE.value)
                    RankingButton.draw(frame, ColorBGR.PINK) 
                    if time_elapsed is None:
                        time_elapsed = time.time()  
                    elif time.time() - time_elapsed > 2:  
                        time_elapsed = None
                        gameState = GameState.SCORE_SETTINGS            
                else:
                    BackButton.draw(frame)
                    DifficultyButton.draw(frame)
                    RankingButton.draw(frame)

            elif hand_rect is not None:
                if BackButton.intersects(hand_rect):
                    ser.write(ColorBox.NONE.value)
                    BackButton.draw(frame, ColorBGR.PINK) 
                    if time_elapsed is None:
                        time_elapsed = time.time()  
                    elif time.time() - time_elapsed > 2:  
                        time_elapsed = None
                        gameState = GameState.MENU   
                else:
                    BackButton.draw(frame)      
            else:
                time_elapsed = None
                ser.write(ColorBox.MULTI.value)
        
    # ================== Difficulty Settings ==================

        if gameState == GameState.DIFFICULTY_SETTINGS:
            BackButton.draw(frame)
            EasyButton.draw(frame)
            HardButton.draw(frame)
            if hand_rect is not None:
                if EasyButton.intersects(hand_rect):
                    hard = False
                elif HardButton.intersects(hand_rect):
                    hard = True

                elif BackButton.intersects(hand_rect):
                    ser.write(ColorBox.NONE.value)
                    BackButton.draw(frame, ColorBGR.PINK) 
                    if time_elapsed is None:
                        time_elapsed = time.time()  
                    elif time.time() - time_elapsed > 2:  
                        time_elapsed = None
                        gameState = GameState.SETTINGS 
                else:
                    BackButton.draw(frame)

            if hard:
                gameText.update_text("The sequence changes completely each level")
                gameText.draw(frame)
                HardButton.draw(frame, ColorBGR.ORANGE) 
                EasyButton.draw(frame)
            else:
                gameText.update_text("One color is added to the basic sequence")
                gameText.draw(frame)
                EasyButton.draw(frame, ColorBGR.GREEN) 
                HardButton.draw(frame)   

    # ===================== Score Settings =====================

        if gameState == GameState.SCORE_SETTINGS:
            scoreEasyText.update_text(f"Easy mode - Level: {max_level_easy}")
            scoreHardText.update_text(f"Hard mode - Level: {max_level_hard}")
            bestScoreText.draw(frame)
            scoreEasyText.draw(frame)
            scoreHardText.draw(frame)
            if hand_rect is not None:
                if BackButton.intersects(hand_rect):
                    ser.write(ColorBox.NONE.value)
                    BackButton.draw(frame, ColorBGR.PINK) 
                    if time_elapsed is None:
                        time_elapsed = time.time()  
                    elif time.time() - time_elapsed > 2:  
                        time_elapsed = None
                        gameState = GameState.SETTINGS 
                else:
                    BackButton.draw(frame)
            else:
                BackButton.draw(frame)
            

        text_size = cv2.getTextSize(gameText.text, 
                                    cv2.FONT_HERSHEY_SIMPLEX, 
                                    gameText.font_scale, 2)[0]
        text_x = (frame.shape[1] - text_size[0])//2
        text_y = (frame.shape[0] + text_size[1])//2
        gameText.x = text_x
        gameText.y = text_y

        if numberOfLives == 3:
            lifeColor = ColorBGR.GREEN
        elif numberOfLives == 2:
            lifeColor = ColorBGR.YELLOW
        elif numberOfLives == 1:
            lifeColor = ColorBGR.RED

        frame[int(FRAME_WIDTH*0.44):int(FRAME_WIDTH*0.44)+logo.shape[0], 
              int(FRAME_HEIGHT*0.79):int(FRAME_HEIGHT*0.79)+logo.shape[1]] = logo 
            
        cv2.imshow('Pymon', frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    scene.release()
    cv2.destroyAllWindows()
    ser.close()

if __name__ == "__main__":
    main()