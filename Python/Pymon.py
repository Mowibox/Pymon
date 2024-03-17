import cv2
import mediapipe as mp
import time
import random as r
import serial
import serial.tools.list_ports


# Variables 
gameScene = 0
time_elapsed = None
numberOfLives = 3
level = 1
canPlay = False
listAppend = True


# Ouverture de la communication serie avec la STM32
ser = serial.Serial("COM25", baudrate=38400)

# Formation de la suite aleatoire
def memorylistMake(level):
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

# Verification de l'etat du jeu
def listCompare(playerList, memoryList):
    n = len(playerList)
    if n != 0:
        if playerList[n-1] == memoryList[n-1]:
            if n == len(memoryList):
                return 1 # Niveau réussi
            else:
                return 0 # Pas d'erreurs, le jeu continue
        else:
            return 2 #Erreur ! 
    else:
        return 0 # Rien ne se passe


# Detection des mains
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.6)

# Creation de la scene
scene = cv2.VideoCapture(0)

# Dimensionnement de la fenêtre
cv2.namedWindow('Pymon', cv2.WINDOW_NORMAL)
scene.set(3, 1280)


# Classe pour la gestion des boutons de selection
class Button:
    def __init__(self, x, y, width, height, text=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    # Dessin du rectangle dans la zone de jeu
    def draw(self, frame, color):
        cv2.rectangle(frame, (self.x, self.y), (self.x + self.width, self.y + self.height), color, 8)
        if self.text:
            text_size = cv2.getTextSize(self.text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
            text_x = self.x + (self.width - text_size[0]) // 2
            text_y = self.y - 10 + (self.height + text_size[1]) // 2
            cv2.putText(frame, self.text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 4)

    # Gestion des intersections avec la main
    def intersects(self, other_rect):
        return self.x < other_rect.x + other_rect.width and \
               self.x + self.width > other_rect.x and \
               self.y < other_rect.y + other_rect.height and \
               self.y + self.height > other_rect.y

#Texte
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
        


# Boutons & Texte
StartButton = Button(60, 50, 250, 150, 'Start')
SettingsButton = Button(950, 50, 250, 150, 'Settings')

RedButton = Button(50, 30, 250, 150, 'Red')
YellowButton = Button(960, 30, 250, 150, 'Yellow')
GreenButton = Button(50, 550, 250, 150, 'Green')
BlueButton = Button(960, 550, 250, 150, 'Blue')

gameText = Text(370, 400, "Regardez la sequence lumineuse...")
levelText = Text(540, 700, "Niveau : {}".format(level))
livesText = Text(540, 50, "Vies : {}".format(numberOfLives))


# Affichage
while scene.isOpened():
    ret, frame = scene.read()
    if not ret:
        break

    # Miroitage de la scene
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

    # Detection des mains
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(gray)

    hand_rect = None  # Initialisation du rectangle de selection

    # Dessin de rectangle de selection
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
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 6)
            hand_rect = Button(x_min, y_min, x_max - x_min, y_max - y_min) 

    # Cheevauchement
    if gameScene == 0:
        if hand_rect is not None:
            if StartButton.intersects(hand_rect):
                StartButton.draw(frame, (255, 0, 255)) 
                if time_elapsed is None:
                    time_elapsed = time.time()  
                elif time.time() - time_elapsed > 2:  
                    gameScene = 1 # Jeu
                    time_elapsed = None      
            else:
                StartButton.draw(frame, (0, 0, 0))
                time_elapsed = None
                
        if hand_rect is not None:
            if SettingsButton.intersects(hand_rect):
                SettingsButton.draw(frame, (255, 0, 255))
                if time_elapsed is None:
                    time_elapsed = time.time()  
                elif time.time() - time_elapsed > 2:  
                    gameScene = 2 # Paramètres
                    time_elapsed = None    
            else:
                SettingsButton.draw(frame, (0, 0, 0))

    if gameScene == 1 and not(canPlay):
        gameText.update_text("Regardez la sequence lumineuse...")
        levelText.update_text("Niveau : {}".format(level))
        livesText.update_text("Vies : {}".format(numberOfLives))
        livesText.draw(frame)
        levelText.draw(frame)
        gameText.draw(frame)
        if time_elapsed is None:
                time_elapsed = time.time()  
        elif time.time() - time_elapsed > 2:  
            time_elapsed = None
            memoryList = memorylistMake(level)
            for i in range(len(memoryList)):
                ser.write(memoryList[i])
                time.sleep(0.6)
                ser.write(b'n')
                time.sleep(0.6)
            playerList = []
            canPlay = True
            

    if gameScene == 1 and canPlay:
        levelText.update_text("Niveau : {}".format(level))
        livesText.update_text("Vies : {}".format(numberOfLives))
        livesText.draw(frame)
        levelText.draw(frame)
        status = listCompare(playerList, memoryList)
        if status == 1: # Niveau complété
            gameScene = 3
        elif status == 2: # Erreur !
            numberOfLives-=1
            if numberOfLives <= 0:
                gameScene = 5
            else:
                gameScene = 4
        gameText.update_text("A vous de jouer !")
        gameText.draw(frame)
        if hand_rect is not None:
            if RedButton.intersects(hand_rect):
                RedButton.draw(frame, (255, 0, 255))
                if listAppend:
                    playerList.append(b'r') 
                    listAppend = False
                ser.write(b'r')   

            elif YellowButton.intersects(hand_rect):
                YellowButton.draw(frame, (255, 0, 255)) 
                if listAppend:
                    playerList.append(b'y') 
                    listAppend = False
                ser.write(b'y')  
         
            elif GreenButton.intersects(hand_rect):
                GreenButton.draw(frame, (255, 0, 255)) 
                if listAppend:
                    playerList.append(b'g') 
                    listAppend = False
                ser.write(b'g') 
   

            elif BlueButton.intersects(hand_rect):
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

    if gameScene == 3:
        ser.write(b'n')
        gameText.update_text("Bravo ! Passons au niveau suivant !")
        livesText.update_text("Vies : {}".format(numberOfLives))
        livesText.draw(frame)
        levelText.update_text("Niveau : {}".format(level))
        levelText.draw(frame)
        gameText.draw(frame)
        if time_elapsed is None:
                time_elapsed = time.time()  
        elif time.time() - time_elapsed > 2:  
            gameScene = 1
            canPlay = False
            level += 1
            time_elapsed = None

    if gameScene == 4:
        ser.write(b'n')
        gameText.update_text("Ce n'est pas ca, Essaie encore...")
        livesText.update_text("Vies : {}".format(numberOfLives))
        livesText.draw(frame)
        levelText.update_text("Niveau : {}".format(level))
        levelText.draw(frame)
        gameText.draw(frame)
        if time_elapsed is None:
                time_elapsed = time.time()  
        elif time.time() - time_elapsed > 2:  
            gameScene = 1
            canPlay = False
            time_elapsed = None

    if gameScene == 5:
        ser.write(b'n')
        gameText.update_text("GAME OVER...")
        livesText.update_text("Vies : {}".format(numberOfLives))
        livesText.draw(frame)
        levelText.update_text("Niveau : {}".format(level))
        levelText.draw(frame)
        gameText.draw(frame)
        if time_elapsed is None:
                time_elapsed = time.time()  
        elif time.time() - time_elapsed > 2:  
            gameScene = 0
            level = 1
            numberOfLives = 3
            canPlay = False
            time_elapsed = None
        

    #Centrage du texte principal
    text_size = cv2.getTextSize(gameText.text, cv2.FONT_HERSHEY_SIMPLEX, gameText.font_scale, 2)[0]
    text_x = (frame.shape[1] - text_size[0]) // 2
    text_y = (frame.shape[0] + text_size[1]) // 2
    gameText.x = text_x
    gameText.y = text_y

       
           
    # Titre du jeu
    cv2.imshow('Pymon', frame)

    # Fin du jeu lorsque l on appuie sur q
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Fermeture de la scene
scene.release()
cv2.destroyAllWindows()
ser.close()