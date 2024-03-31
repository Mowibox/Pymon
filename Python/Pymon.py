import cv2
import mediapipe as mp
import time
import random as r
import serial
import serial.tools.list_ports

# Variables
gameScene = 0               # Game state management
time_elapsed = None         # Time variable
numberOfLives = 3           # Number of lives
level = 1                   # Level
canPlay = False             # Ability to play or not
listAppend = True           # Add elements to the user sequence
lifeColor = (0, 255, 0)     # Color of life points
hard = False                # Difficulty management
max_level_easy = 1          # Best score easy mode management  
max_level_hard = 1          # Best score hard mode management  


# Open serial communication with STM32
ports = serial.tools.list_ports.comports()
stm32_port = None
for port, desc, hwid in sorted(ports):
    if "STMicroelectronics STLink Virtual COM Port" in desc:  # Check description to find STM32 port
        stm32_port = port
        break

ser = serial.Serial(stm32_port, baudrate=38400)

# Generate the random sequence to guess
def memorylistMake(level):
    if hard or level == 1:
        memoryList = []
        for i in range(level+2):
            color = r.randint(0,3)
            if color == 0:
                memoryList.append(b'r')
            elif color == 1:
                memoryList.append(b'y')
            elif color == 2:
                memoryList.append(b'g')
            elif color == 3:
                memoryList.append(b'b')
    return memoryList

# Check the game state
def listCompare(playerList, memoryList):
    n = len(playerList)
    if n != 0:
        if playerList[n-1] == memoryList[n-1]:
            if n == len(memoryList):
                return 1 # Level passed
            else:
                return 0 # No errors, game continues
        else:
            return 2 # Error!
    else:
        return 0 # Nothing happens

# Hands detection
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.6)

# Scene creation
scene = cv2.VideoCapture(0)

# Window sizing
cv2.namedWindow('Pymon', cv2.WINDOW_NORMAL)
scene.set(3, 1280)

# Class for button management
class Button:
    def __init__(self, x, y, width, height, text=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    # Draw the rectangle in the game area
    def draw(self, frame, color):
        cv2.rectangle(frame, (self.x, self.y), (self.x + self.width, self.y + self.height), color, 8)
        if self.text:
            text_size = cv2.getTextSize(self.text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
            text_x = self.x + (self.width - text_size[0]) // 2
            text_y = self.y - 10 + (self.height + text_size[1]) // 2
            cv2.putText(frame, self.text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 4)

    # Handle intersections with the hand
    def intersects(self, other_rect):
        return self.x < other_rect.x + other_rect.width and \
               self.x + self.width > other_rect.x and \
               self.y < other_rect.y + other_rect.height and \
               self.y + self.height > other_rect.y

# Text
class Text:
    def __init__(self, x, y, text, font_scale=1, color=(255, 255, 255), thickness=2, font=cv2.FONT_HERSHEY_SIMPLEX):
        self.x = x
        self.y = y
        self.text = text
        self.font_scale = font_scale
        self.color = color
        self.thickness = thickness
        self.font = font

    def draw(self, frame):
        cv2.putText(frame, self.text, (self.x, self.y), self.font, self.font_scale, self.color, self.thickness)

    def update_text(self, text):
        self.text = text

    def update_color(self, color):
        self.color = color

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
LevelText = Text(580, 560, "Level: {}".format(level), color=(0, 0, 0))
livesText = Text(560, 50, "Lives: {}".format(numberOfLives))
newRecordText = Text(550, 520, "New record!", color=(0, 230, 245))

EasyButton = Button(950, 50, 250, 150, 'Easy')
HardButton = Button(60, 50, 250, 150, 'Hard')

bestScoreText = Text(560, 50, "Best score", color=(0, 230, 245))
scoreEasyText = Text(470, 490, "Easy mode - Level: {}".format(max_level_easy), color=(0, 0, 0))
scoreHardText = Text(470, 540, "Hard mode - Level: {}".format(max_level_hard), color=(0, 0, 0))

# Logo
logo = cv2.imread('Python\img\Pymonlogo.png')
logo = cv2.resize(logo, (150,150))

# Display the scene
while scene.isOpened():
    ret, frame = scene.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    # Menu
    if gameScene == 0 :
        StartButton.draw(frame, (0, 0, 0))
        SettingsButton.draw(frame, (0, 0, 0))
    
    if gameScene == 1:
        RedButton.draw(frame, (0, 0, 255))
        YellowButton.draw(frame, (0, 255, 255))
        GreenButton.draw(frame, (0, 255, 0))
        BlueButton.draw(frame, (255, 0, 0))
    
    if gameScene == 2:
        RankingButton.draw(frame, (0, 0, 0))
        PlayerButton.draw(frame, (0, 0, 0))
        BackButton.draw(frame, (0, 0, 0))
        DifficultyButton.draw(frame, (0, 0, 0))

    if gameScene == 6:
        BackButton.draw(frame, (0, 0, 0))
        EasyButton.draw(frame, (0, 0, 0))
        HardButton.draw(frame, (0, 0, 0))

    # Hand detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(gray)

    hand_rect = None  # Initialize selection rectangle
    # Draw selection rectangle
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
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (255, 0, 200), 6)
            hand_rect = Button(x_min, y_min, x_max - x_min, y_max - y_min) 

    # Overlap
    if gameScene == 0: # Menu
        if hand_rect is not None:
            if StartButton.intersects(hand_rect):
                ser.write(b'n')
                StartButton.draw(frame, (255, 0, 255)) 
                if time_elapsed is None:
                    time_elapsed = time.time()  
                elif time.time() - time_elapsed > 2:
                    time_elapsed = None  
                    gameScene = 1 # Game   
            else:
                StartButton.draw(frame, (0, 0, 0))
                
        else:
            ser.write(b'm')
                
        if hand_rect is not None:
            if SettingsButton.intersects(hand_rect):
                ser.write(b'n')
                SettingsButton.draw(frame, (255, 0, 255))
                if time_elapsed is None:
                    time_elapsed = time.time()  
                elif time.time() - time_elapsed > 2:
                    time_elapsed = None  
                    gameScene = 2 # Settings
                    
            else:
                SettingsButton.draw(frame, (0, 0, 0))
                
        else:
            time_elapsed = None
            ser.write(b'm')

    if gameScene == 1 and not(canPlay): # Observation of sequence
        gameText.update_color((0, 0, 0))
        gameText.update_text("Watch the light sequence...")
        LevelText.update_text("Level: {}".format(level))
        livesText.update_text("Lives: {}".format(numberOfLives))
        livesText.update_color(lifeColor)
        livesText.draw(frame)
        LevelText.draw(frame)
        gameText.draw(frame)

        # Create the sequence to be performed
        if time_elapsed is None:
                ser.write(b'n')
                time_elapsed = time.time()  
        elif time.time() - time_elapsed > 3:  
            time_elapsed = None
            if hard or level == 1:
                memoryList = memorylistMake(level)
            for i in range(len(memoryList)):
                ser.write(memoryList[i])
                time.sleep(0.6)
                ser.write(b'n')
                time.sleep(0.6)
            playerList = []
            canPlay = True
            

    if gameScene == 1 and canPlay: # Game space
        LevelText.update_text("Level: {}".format(level))
        livesText.update_text("Lives: {}".format(numberOfLives))
        livesText.update_color(lifeColor)
        livesText.draw(frame)
        LevelText.draw(frame)

        status = listCompare(playerList, memoryList) # Check the level state
        if status == 1: # Level passed
            gameScene = 3
        elif status == 2: # Error!
            numberOfLives-=1
            if numberOfLives <= 0: # GAME OVER
                gameScene = 5
            else:
                gameScene = 4
        gameText.update_color((0, 0, 0))
        gameText.update_text("Your turn!")
        gameText.draw(frame)
        if hand_rect is not None: # Red contact
            if RedButton.intersects(hand_rect):
                RedButton.draw(frame, (255, 0, 255))
                if listAppend:
                    playerList.append(b'r') 
                    listAppend = False
                ser.write(b'r')   

            elif YellowButton.intersects(hand_rect): # Yellow contact
                YellowButton.draw(frame, (255, 0, 255)) 
                if listAppend:
                    playerList.append(b'y') 
                    listAppend = False
                ser.write(b'y')  
         
            elif GreenButton.intersects(hand_rect): # Green contact
                GreenButton.draw(frame, (255, 0, 255)) 
                if listAppend:
                    playerList.append(b'g') 
                    listAppend = False
                ser.write(b'g') 
   

            elif BlueButton.intersects(hand_rect): # Blue contact
                BlueButton.draw(frame, (255, 0, 255)) 
                if listAppend:
                    playerList.append(b'b') 
                    listAppend = False
                ser.write(b'b')             
  
            else:  
                RedButton.draw(frame, (0, 0, 255))
                YellowButton.draw(frame, (0, 255, 255))
                GreenButton.draw(frame, (0, 255, 0))
                BlueButton.draw(frame, (255, 0, 0))
                if not(listAppend):
                    listAppend = True
                ser.write(b'n')
    
    if gameScene == 2:  # Settings
        if hand_rect is not None:
            if BackButton.intersects(hand_rect):
                ser.write(b'n')
                BackButton.draw(frame, (255, 0, 255)) 
                if time_elapsed is None:
                    time_elapsed = time.time()  
                elif time.time() - time_elapsed > 2:  
                    time_elapsed = None
                    gameScene = 0 # Back to menu 

            elif DifficultyButton.intersects(hand_rect):
                ser.write(b'n')
                DifficultyButton.draw(frame, (255, 0, 255)) 
                if time_elapsed is None:
                    time_elapsed = time.time()  
                elif time.time() - time_elapsed > 2:  
                    time_elapsed = None
                    gameScene = 6 # Difficulty
            
            elif RankingButton.intersects(hand_rect):
                ser.write(b'n')
                RankingButton.draw(frame, (255, 0, 255)) 
                if time_elapsed is None:
                    time_elapsed = time.time()  
                elif time.time() - time_elapsed > 2:  
                    time_elapsed = None
                    gameScene = 7 # Max Score            

            else:
                BackButton.draw(frame, (0, 0, 0))
                DifficultyButton.draw(frame, (0, 0, 0))
                RankingButton.draw(frame, (0, 0, 0))

        elif hand_rect is not None:
            if BackButton.intersects(hand_rect):
                ser.write(b'n')
                BackButton.draw(frame, (255, 0, 255)) 
                if time_elapsed is None:
                    time_elapsed = time.time()  
                elif time.time() - time_elapsed > 2:  
                    time_elapsed = None
                    gameScene = 0 # Game  
            else:
                BackButton.draw(frame, (0, 0, 0))
                
        else:
            time_elapsed = None
            ser.write(b'm')

    if gameScene == 3:  # Level complete
        ser.write(b'n')
        gameText.update_text("Congratulations! Next level!")
        gameText.update_color((0, 220, 0))
        livesText.update_text("Lives: {}".format(numberOfLives))
        livesText.update_color(lifeColor)
        livesText.draw(frame)
        LevelText.update_text("Level: {}".format(level))
        LevelText.draw(frame)
        gameText.draw(frame)
        if time_elapsed is None:
                time_elapsed = time.time()  
        elif time.time() - time_elapsed > 2:  
            gameScene = 1
            canPlay = False
            if not(hard):
                color = r.randint(0,3)
                if color == 0:
                    memoryList.append(b'r')
                elif color == 1:
                    memoryList.append(b'y')
                elif color == 2:
                    memoryList.append(b'g')
                elif color == 3:
                    memoryList.append(b'b')
            level += 1
            time_elapsed = None

    if gameScene == 4: # Level failure
        ser.write(b'n')
        gameText.update_text("Try again...")
        gameText.update_color((0, 0, 220))
        gameText.draw(frame)
        livesText.update_text("Lives: {}".format(numberOfLives))
        livesText.update_color(lifeColor)
        livesText.draw(frame)
        LevelText.update_text("Level: {}".format(level))
        LevelText.draw(frame)
        if time_elapsed is None:
                time_elapsed = time.time()  
        elif time.time() - time_elapsed > 2:  
            gameScene = 1
            canPlay = False
            time_elapsed = None

    if gameScene == 5: # GAME OVER 
        ser.write(b'n')
        gameText.update_text("GAME OVER...")
        gameText.update_color((0, 0, 180))
        livesText.update_text("Lives: {}".format(numberOfLives))
        livesText.update_color(lifeColor)
        livesText.draw(frame)
        LevelText.update_text("Level: {}".format(level))
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
            gameScene = 0
            level = 1
            numberOfLives = 3
            canPlay = False
            time_elapsed = None
    

    if gameScene == 6: # Difficulty selection
        if hand_rect is not None:
            if EasyButton.intersects(hand_rect):
                hard = False

            elif HardButton.intersects(hand_rect):
                hard = True

            elif BackButton.intersects(hand_rect):
                ser.write(b'n')
                BackButton.draw(frame, (255, 0, 255)) 
                if time_elapsed is None:
                    time_elapsed = time.time()  
                elif time.time() - time_elapsed > 2:  
                    time_elapsed = None
                    gameScene = 2 # Back to settings 
            else:
                BackButton.draw(frame, (0, 0, 0))

        if hard:
            gameText.update_text("The sequence changes completely each level")
            gameText.update_color((0, 0, 0))
            gameText.draw(frame)
            HardButton.draw(frame, (0, 80, 255)) 
            EasyButton.draw(frame, (0, 0, 0))
        else:
            gameText.update_text("One color is added to the basic sequence")
            gameText.update_color((0, 0, 0))
            gameText.draw(frame)
            EasyButton.draw(frame, (80, 255, 0)) 
            HardButton.draw(frame, (0, 0, 0))   

    if gameScene == 7: # Score display
        scoreEasyText.update_text("Easy mode - Level: {}".format(max_level_easy))
        scoreHardText.update_text("Hard mode - Level: {}".format(max_level_hard))
        bestScoreText.draw(frame)
        scoreEasyText.draw(frame)
        scoreHardText.draw(frame)
        if hand_rect is not None:
            if BackButton.intersects(hand_rect):
                ser.write(b'n')
                BackButton.draw(frame, (255, 0, 255)) 
                if time_elapsed is None:
                    time_elapsed = time.time()  
                elif time.time() - time_elapsed > 2:  
                    time_elapsed = None
                    gameScene = 2 # Back to settings 
            else:
                BackButton.draw(frame, (0, 0, 0))
        else:
            BackButton.draw(frame, (0, 0, 0))
        
        
    # Text coloration of lives
    if numberOfLives == 3:
        lifeColor = (0, 255, 0)
    elif numberOfLives == 2:
        lifeColor = (0, 255, 255)
    elif numberOfLives == 1:
        lifeColor = (0, 0, 255)

    # Centering the main text
    text_size = cv2.getTextSize(gameText.text, cv2.FONT_HERSHEY_SIMPLEX, gameText.font_scale, 2)[0]
    text_x = (frame.shape[1] - text_size[0]) // 2
    text_y = (frame.shape[0] + text_size[1]) // 2
    gameText.x = text_x
    gameText.y = text_y

    # Display logo
    frame[570:570+logo.shape[0], 565:565+logo.shape[1]] = logo 
           
    # Game title
    cv2.imshow('Pymon', frame)

    # End game on pressing q
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Close scene
scene.release()
cv2.destroyAllWindows()
ser.close()
