import pygame
import random
import cv2
import mediapipe as mp
from pygame import mixer, time
import pyautogui
import numpy as np
import time
import threading

# Initialize the pygame
pygame.init()

a_x, a_y = pyautogui.size()
print(a_x, a_y)
# create the screen
screen = pygame.display.set_mode((a_x, a_y), pygame.RESIZABLE)
full_screen_image = pygame.image.load('bubblesort_game_screen_final.jpg')

# GameOver
bg = pygame.image.load('End Screen.jpg')
game_over_text = pygame.font.Font('freesansbold.ttf', 45)
game_over_text_fs = pygame.font.Font('freesansbold.ttf', 72)

# Title and Icon for game window.
pygame.display.set_caption("Bubble Sort")
icon = pygame.image.load('Diamond_Block-MC-Square.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('DOT-16.png')
scaling_factor = 2
playerImg = pygame.transform.scale(playerImg,
                                   (playerImg.get_width() * scaling_factor, playerImg.get_height() * scaling_factor))
playerX = 1
playerY = 37
playerY_change = 0
playerX_change = 0
tmpX = 0
tmpY = 0
playerScore = 0
player_rect = playerImg.get_rect()

# To hide the windows mouse cursor
pygame.mouse.set_visible(True)
idle_time_to_hide_cursor = 3
last_mouse_movement_time = time.time()


def show_game_over():
    scaled_background = pygame.transform.scale(bg, (a_x, a_y))
    screen.blit(scaled_background, (0, 0))

    # game_over = game_over_text_fs.render("GAME OVER ", True, (255, 255, 223))
    # game_over_rect = game_over.get_rect(center=((2.9 * a_x // 5) - 73, a_y - 490))

    game_over = game_over_text.render("GAME OVER", True, (255, 255, 223))
    text_width, text_height = game_over.get_size()
    # Calculate the x and y coordinates for the text
    p = ((a_x // 2) - (text_width / 2.3))
    q = (a_y // 2) + (a_y // 10)
    game_over_rect = game_over.get_rect(topleft=(p, q))

    r = ((a_x // 2) - (text_width / 4))
    s = (a_y // 2) + (a_y / 4.5)
    show_score(r, s, 40, (255, 255, 255))



    screen.blit(game_over, game_over_rect)
    # mouse_pos = pygame.mouse.get_pos()
    # if game_over_rect.collidepoint(mouse_pos):
    #     game_over = game_over_text.render("GAME OVER ", True, (0, 0, 0))
    #     screen.blit(game_over, game_over_rect)


# Showing Player on the game window
def show_player(x, y):
    screen.blit(playerImg, (x, y))


# Converting string to img for rendering text on window. There is no direct support for printing text on the window in 'pygame'
text_font = pygame.font.SysFont(None, 40)
text_font1 = pygame.font.SysFont(None, 60)


# Showing score on the game window
def show_score(x,y,size, text_col):
    score = pygame.font.Font('freesansbold.ttf', size)
    final_score = score.render("Score : " + str(playerScore), True, text_col)
    screen.blit(final_score, (x, y))



# Timer to stop the game
clock = pygame.time.Clock()
start = 200


# Showing timer on the game window
def show_timer(text, font, text_col, size):
    time_font = pygame.font.Font('freesansbold.ttf', size)
    timerImg = time_font.render(text, True, text_col)
    screen.blit(timerImg, ((screen.get_width() - 180), 10))


# Showing random integer on the game window for telling user that which balloon should be popped
def show_randInt(text, font, text_col):
    randIntImg = font.render(text, True, text_col)
    screen.blit(randIntImg, (int(screen.get_width() / 2), 10))


# Assigning balloon images to a variable for further use in creating objects of that particular balloons
b_img_1 = 'red_1 1 (Custom).png'
b_img_2 = 'red_2 1 (Custom).png'
b_img_3 = 'red_3 1 (Custom).png'
b_img_4 = 'red_4 1 (Custom).png'
b_img_5 = 'red_5 1 (Custom).png'


# Main balloon class
class Balloon:

    def __init__(self, x, y, img_name):
        self.balloonX = x
        self.balloonY = y
        self.balloonImg = pygame.image.load(img_name)

    def show_balloon(self):
        screen.blit(self.balloonImg, (self.balloonX, self.balloonY))


# Choosing which balloon should be popped.
I = 1


def b_choose():
    global I

    I = random.randint(1, 5)
    if I == 1:
        return b_img_1
    if I == 2:
        return b_img_2
    if I == 3:
        return b_img_3
    if I == 4:
        return b_img_4
    if I == 5:
        return b_img_5


# Getting random coordinates with use of random function and will be used in "get_cord_list()" function.
def get_cord():
    x = random.randint(0, (screen.get_width() - 64))
    y = random.randint(53, (screen.get_height() - 150))
    return x, y


# Initial list for the coordinates of the balloon.
res = [(604, 114), (17, 170), (269, 285), (51, 146), (328, 424)]


# This function will give the coordinate list for 5 balloon and which has low possibility of getting overlapped.
def get_cord_list():
    for j in range(5):
        res.append(get_cord())


def create_obj():
    global b1
    global b2
    global b3
    global b4
    global b5
    b1 = Balloon(res[0][0], res[0][1], b_img_1)
    b2 = Balloon(res[1][0], res[1][1], b_img_2)
    b3 = Balloon(res[2][0], res[2][1], b_img_3)
    b4 = Balloon(res[3][0], res[3][1], b_img_4)
    b5 = Balloon(res[4][0], res[4][1], b_img_5)


def show_balloons():
    b1.show_balloon()
    b2.show_balloon()
    b3.show_balloon()
    b4.show_balloon()
    b5.show_balloon()


def show_screen():
    scaled_game_background = pygame.transform.scale(full_screen_image, (screen.get_width(), screen.get_height()))
    # screen.fill((255, 255, 255))
    screen.blit(scaled_game_background, (0, 0))


# Game loop
cnt = 0
count = 0
flg1 = 0
flg2 = 0
flag = 0
p_ratio_x = 0
p_ratio_y = 0
fullscreen = False
running = True

##################################
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
# wScr, hScr = autopy.screen.size()
frameR = 100  # Frame Reduction
smoothening = 5
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
tempX, tempY = 0, 0
###################################


class handDetector():
    def __init__(self, mode=False, maxHands=1, complexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.complexity = complexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.complexity,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(self.results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0, draw=True):
        xList = []
        yList = []
        bbox = []
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                # print(id, cx, cy)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax

            if draw:
                cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20),
                              (0, 255, 0), 2)

        return self.lmList, bbox


detector = handDetector(maxHands=1)


# tempX = 0
# tempY = 0

# def game_function():
#     global screen
#     global full_screen_image
#     global b1
#     global b2
#     global b3
#     global b4
#     global b5
#     global start
#     global running
#     global fullscreen
#     global cnt
#     global count
#     global flg1
#     global flg2
#     global flag
#     global p_ratio_x
#     global p_ratio_y
#     global bg
#     global game_over_text
#     global game_over_text_fs
#     global playerX
#     global playerY
#     global playerY_change
#     global playerX_change
#     global tmpX
#     global tmpY
#     global playerScore
#     global player_rect
#     global idle_time_to_hide_cursor
#     global last_mouse_movement_time
#     global text_font
#     global text_font1
#     global b_img_1
#     global b_img_2
#     global b_img_3
#     global b_img_4
#     global b_img_5
#     global I
#     global tempX
#     global tempY
#     global plocX
#     global plocY
#     global clocX
#     global clocY


def timer_count():
    global start

    while start > 0:
        start -= 1
        clock.tick(2500)


timer_thread = threading.Thread(target=timer_count)

timer_thread.start()
# timer_thread.join()

while running:
    # screen.fill((0, 180, 180))

    # t = threading.Thread(target=show_screen())
    # t.start()
    # Stopping game loop when timer over

    print(start)
    show_screen()

    # Windows mouse cursor
    if pygame.mouse.get_rel() != (0, 0):
        # Mouse has moved, reset the timer
        last_mouse_movement_time = time.time()
    # Check if it's time to hide the cursor
    if time.time() - last_mouse_movement_time > idle_time_to_hide_cursor:
        pygame.mouse.set_visible(False)
    else:
        pygame.mouse.set_visible(True)

    # print(clock.tick() - start_time)

    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = cv2.flip(img, 1)

    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]  # Tip of the index finger (x1,y1)
        # print(x1, y1)
    else:
        x1, y1 = 0, 0
    cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                  (255, 0, 255), 2)

    header_line = pygame.draw.line(screen, (0, 0, 0), (0, 50), (screen.get_width(), 50), 4)

    show_randInt(str(I), text_font1, (0, 0, 0))

    # For input from keyboard.
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # Play with help of keyboard keys.
            # if event.key == pygame.K_UP or event.key == pygame.K_w:
            #     playerY_change = -5
            # if event.key == pygame.K_DOWN or event.key == pygame.K_s:
            #     playerY_change = 5
            # if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            #     playerX_change = -5
            # if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            #     playerX_change = 5
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_f:
                # Getting the relative position of player to the size of fullscreen.
                p_ratio_x = playerX / screen.get_width()
                p_ratio_y = playerY / screen.get_height()
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    playerX = screen.get_width() * p_ratio_x
                    playerY = screen.get_height() * p_ratio_y
                else:
                    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
                    # Reassigning the position of player according to the previous relative position in fullscreen mode.
                    playerX = screen.get_width() * p_ratio_x
                    playerY = screen.get_height() * p_ratio_y
                    flg1 = 1
        # Play with help of keyboard keys.
        # if event.type == pygame.KEYUP:
        #     if event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_DOWN or event.key == pygame.K_s:
        #         playerY_change = 0
        #     if event.key == pygame.K_LEFT or event.key == pygame.K_a or event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        #         playerX_change = 0
    # Play with help of keyboard keys.
    # # Player clamping in window
    # tmpY = playerY + playerY_change
    # if (screen.get_height() - 16) >= tmpY >= 36:
    #     playerY += playerY_change
    # tmpX = playerX + playerX_change
    # if (screen.get_width() - 16) >= tmpX >= 0:
    #     playerX += playerX_change

    if start <= 0:
        show_game_over()

        # Display replay and exit options
        replay_text = text_font1.render("Replay", True, (255, 255, 255))
        exit_text = text_font1.render("Exit", True, (255, 255, 255))
        replay_rect = replay_text.get_rect(center=(a_x / 2.95, a_y - 200))
        exit_rect = exit_text.get_rect(center=(2 * a_x / 2.95, a_y - 200))
        screen.blit(replay_text, replay_rect)
        screen.blit(exit_text, exit_rect)

        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()

        # Check if the mouse is over the replay button
        if replay_rect.collidepoint(mouse_pos):
            replay_text = text_font1.render("Replay", True, (0, 0, 0))
            screen.blit(replay_text, replay_rect)

            if mouse_clicked[0]:  # Left mouse button clicked
                start = 2599  # Reset the timer
                playerScore = 0  # Reset the score
                res.clear()
                get_cord_list()  # Generate new balloon positions
                I = random.randint(1, 5)  # Choose a new balloon type

        # Check if the mouse is over the exit button
        if exit_rect.collidepoint(mouse_pos):
            exit_text = text_font1.render("Exit", True, (0, 0, 0))
            screen.blit(exit_text, exit_rect)

            if mouse_clicked[0]:  # Left mouse button clicked
                running = False  # Exit the game

    else:

        # 5. Convert Coordinates
        if x1 == 0 and y1 == 0:
            x1, y1 = tempX, tempY

        x3 = np.interp(x1, (frameR, wCam - frameR), (0, a_x))
        y3 = np.interp(y1, (frameR, hCam - frameR), (0, a_y))
        tempX, tempY = x1, y1

        # 6. Smoothen Values
        clocX = plocX + (x3 - plocX) / smoothening
        clocY = plocY + (y3 - plocY) / smoothening

        plocX, plocY = clocX, clocY

        show_player(a_x - clocX, clocY)
        # cv2.imshow("Image", img)
        # cv2.waitKey(1)

        player_rect = pygame.Rect(a_x - clocX, clocY, 10, 10)

        if flg1 == 1:
            res.clear()
            get_cord_list()

        create_obj()

        b1_rect = pygame.Rect(b1.balloonX, b1.balloonY, 110, 110)
        b2_rect = pygame.Rect(b2.balloonX, b2.balloonY, 110, 110)
        b3_rect = pygame.Rect(b3.balloonX, b3.balloonY, 110, 110)
        b4_rect = pygame.Rect(b4.balloonX, b4.balloonY, 110, 110)
        b5_rect = pygame.Rect(b5.balloonX, b5.balloonY, 110, 110)

        # for checking the collision between balloons.
        while cnt < 1:
            if b1_rect.colliderect(b2_rect):
                cnt += 1
                flg2 = 1
            elif b1_rect.colliderect(b3_rect):
                cnt += 1
                flg2 = 1
            elif b1_rect.colliderect(b4_rect):
                cnt += 1
                flg2 = 1
            elif b1_rect.colliderect(b5_rect):
                cnt += 1
                flg2 = 1
            elif b2_rect.colliderect(b3_rect):
                cnt += 1
                flg2 = 1
            elif b2_rect.colliderect(b4_rect):
                cnt += 1
                flg2 = 1
            elif b2_rect.colliderect(b5_rect):
                cnt += 1
                flg2 = 1
            elif b3_rect.colliderect(b4_rect):
                cnt += 1
                flg2 = 1
            elif b3_rect.colliderect(b5_rect):
                cnt += 1
                flg2 = 1
            elif b4_rect.colliderect(b5_rect):
                cnt += 1
                flg2 = 1

            if flg2 == 1:
                res.clear()
                get_cord_list()
                create_obj()
                b1_rect = pygame.Rect(b1.balloonX, b1.balloonY, 70, 70)
                b2_rect = pygame.Rect(b2.balloonX, b2.balloonY, 70, 70)
                b3_rect = pygame.Rect(b3.balloonX, b3.balloonY, 70, 70)
                b4_rect = pygame.Rect(b4.balloonX, b4.balloonY, 70, 70)
                b5_rect = pygame.Rect(b5.balloonX, b5.balloonY, 70, 70)
            if flg2 == 0:
                break
            flg2 = 0
            cnt = 0

        show_balloons()

        if I == 1:
            tmp1 = b1_rect
        if I == 2:
            tmp1 = b2_rect
        if I == 3:
            tmp1 = b3_rect
        if I == 4:
            tmp1 = b4_rect
        if I == 5:
            tmp1 = b5_rect

        if player_rect.colliderect(tmp1):
            pop_sound = mixer.Sound('balloon_pop.wav')
            pop_sound.play()
            res.clear()
            get_cord_list()
            playerScore += 1
            flag = 1

        if flag == 1:
            choosenImg = b_choose()
            flag = 0

        show_score(10,10,40, (0, 0, 0))
        show_timer("Time : " + str(int(start / 100)), text_font, (0, 0, 0), 40)

        flg1 = 0

        if start <= 0:
            running = False

    pygame.display.update()

    # clock.stop()
# timer_thread.join()


# clock.tick(100)
#
# p1 = multiprocessing.Process(target = game_function)
# p2 = multiprocessing.Process(target = timer_count)


# if __name__ == '__main__':
#     p1.start()
#     p2.start()
#     p1.join()
#     p2.join()
