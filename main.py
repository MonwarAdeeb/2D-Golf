from tkinter import messagebox
import tkinter as tk
from time import sleep, time
import startScreen
import courses
import math
import physics
import subprocess
import sys
import get_pip
import os


def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])


try:
    print("[GAME] Trying to import pygame")
    import pygame
except:
    print("[EXCEPTION] Pygame not installed")

    try:
        print("[GAME] Trying to install pygame via pip")
        import pip
        install("pygame")
        print("[GAME] Pygame has been installed")
    except:
        print("[EXCEPTION] Pip not installed on system")
        print("[GAME] Trying to install pip")
        get_pip.main()
        print("[GAME] Pip has been installed")
        try:
            print("[GAME] Trying to install pygame")
            import pip
            install("pygame")
            print("[GAME] Pygame has been installed")
        except:
            print("[ERROR 1] Pygame could not be installed")

    import pygame


# INITIALIZATION
pygame.init()

SOUND = False

winwidth = 1080
winheight = 600
pygame.display.set_caption('Super Minigolf')

# LOAD IMAGES
icon = pygame.image.load(os.path.join('img', 'icon.ico'))
icon = pygame.transform.scale(icon, (32, 32))
background = pygame.image.load(os.path.join('img', 'back.png'))
sand = pygame.image.load(os.path.join('img', 'sand.png'))
edge = pygame.image.load(os.path.join('img', 'sandEdge.png'))
bottom = pygame.image.load(os.path.join('img', 'sandBottom.png'))
green = pygame.image.load(os.path.join('img', 'green.png'))
flag = pygame.image.load(os.path.join('img', 'flag.png'))
water = pygame.image.load(os.path.join('img', 'water.png'))
laser = pygame.image.load(os.path.join('img', 'laser.png'))
sticky = pygame.image.load(os.path.join('img', 'sticky.png'))
coinPics = [pygame.image.load(os.path.join('img', 'coin1.png')), pygame.image.load(os.path.join('img', 'coin2.png')), pygame.image.load(os.path.join('img', 'coin3.png')), pygame.image.load(os.path.join(
    'img', 'coin4.png')), pygame.image.load(os.path.join('img', 'coin5.png')), pygame.image.load(os.path.join('img', 'coin6.png')), pygame.image.load(os.path.join('img', 'coin7.png')), pygame.image.load(os.path.join('img', 'coin8.png'))]
powerMeter = pygame.image.load(os.path.join('img', 'power.png'))
powerMeter = pygame.transform.scale(powerMeter, (150, 150))

# SET ICON
pygame.display.set_icon(icon)

# GLOBAL VARIABLES
coinTime = 0
coinIndex = 0
time = 0
rollVel = 0
strokes = 0
par = 0
level = 8
flagx = 0
coins = 0
shootPos = ()
ballColor = (255, 255, 255)
ballStationary = ()
line = None
power = 0
hole = ()
objects = []
put = False
shoot = False
start = True

# LOAD MUSIC
if SOUND:
    wrong = pygame.mixer.Sound(os.path.join('sounds', 'wrong12.wav'))
    puttSound = pygame.mixer.Sound(os.path.join('sounds', 'putt.wav'))
    inHole = pygame.mixer.Sound(os.path.join('sounds', 'inHole.wav'))
    song = pygame.mixer.music.load(os.path.join('sounds', 'music.mp3'))
    splash = pygame.mixer.Sound(os.path.join('sounds', 'splash.wav'))
    pygame.mixer.music.play(-1)

# POWER UP VARS
powerUps = 7
hazard = False
stickyPower = False
mullagain = False
superPower = False
powerUpButtons = [[900, 35, 20, 'P', (255, 69, 0)], [
    1000, 35, 20, 'S', (255, 0, 255)], [950, 35, 20, 'M', (105, 105, 105)]]

# FONTS
myFont = pygame.font.SysFont('comicsansms', 50)
parFont = pygame.font.SysFont('comicsansms', 30)

win = pygame.display.set_mode((winwidth, winheight))


class scoreSheet():
    def __init__(self, parr):
        self.parList = parr
        self.par = sum(self.parList)
        self.holes = 9
        self.finalScore = None
        self.parScore = 0
        self.strokes = []
        self.win = win
        self.winwidth = winwidth
        self.winheight = winheight
        self.width = 400
        self.height = 510
        self.font = pygame.font.SysFont('comicsansms', 22)
        self.bigFont = pygame.font.SysFont('comicsansms', 30)

    def getScore(self):
        return sum(self.strokes) - sum(self.parList[:len(self.strokes)])

    def getPar(self):
        return self.par

    def getStrokes(self):
        return sum(self.strokes)

    def drawSheet(self, score=0):
        self.strokes.append(score)
        grey = (220, 220, 220)

        text = self.bigFont.render(
            'Strokes: ' + str(sum(self.strokes)), 1, grey)
        self.win.blit(text, (800, 330))
        text = self.bigFont.render('Par: ' + str(self.par), 1, grey)
        self.win.blit(text, (240 - (text.get_width()/2),
                             300 - (text.get_height()/2)))
        text = self.bigFont.render('Score: ', 1, grey)
        self.win.blit(text, (800, 275))

        scorePar = sum(self.strokes) - sum(self.parList[:len(self.strokes)])
        if scorePar < 0:
            color = (0, 166, 0)
        elif scorePar > 0:
            color = (255, 0, 0)
        else:
            color = grey

        textt = self.bigFont.render(str(scorePar), 1, color)
        win.blit(textt, (805 + text.get_width(), 275))

        startx = self.winwidth/2 - self.width / 2
        starty = self.winheight/2 - self.height/2
        pygame.draw.rect(
            self.win, grey, (startx, starty, self.width, self.height))

        # Set up grid
        for i in range(1, 4):
            # Column Lines
            pygame.draw.line(self.win, (0, 0, 0), (startx + (i * (self.width/3)),
                                                   starty), (startx + (i * (self.width/3)), starty + self.height), 2)
        for i in range(1, 11):
            # Rows
            if i == 1:  # Display all headers for rows
                blit = self.font.render('Hole', 2, (0, 0, 0))
                self.win.blit(blit, (startx + 40, starty + 10))
                blit = self.font.render('Par', 2, (0, 0, 0))
                self.win.blit(blit, (startx + 184, starty + 10))
                blit = self.font.render('Stroke', 2, (0, 0, 0))
                self.win.blit(blit, (startx + 295, starty + 10))
                blit = self.font.render(
                    'Press the mouse to continue...', 1, (128, 128, 128))
                self.win.blit(blit, (384, 565))
            else:  # Populate rows accordingly
                blit = self.font.render(str(i - 1), 1, (128, 128, 128))
                self.win.blit(blit, (startx + 56, starty + 10 +
                                     ((i - 1) * (self.height/10))))

                blit = self.font.render(
                    str(self.parList[i - 2]), 1, (128, 128, 128))
                self.win.blit(blit, (startx + 60 + 133, starty +
                                     10 + ((i - 1) * (self.height/10))))
                try:  # Catch the index out of range error, display the stokes each level
                    if self.strokes[i - 2] < self.parList[i - 2]:
                        color = (0, 166, 0)
                    elif self.strokes[i - 2] > self.parList[i - 2]:
                        color = (255, 0, 0)
                    else:
                        color = (0, 0, 0)

                    blit = self.font.render(str(self.strokes[i - 2]), 1, color)
                    self.win.blit(
                        blit, ((startx + 60 + 266, starty + 10 + ((i - 1) * (self.height/10)))))
                except:
                    blit = self.font.render('-', 1, (128, 128, 128))
                    self.win.blit(blit, (startx + 62 + 266,
                                         starty + 10 + ((i - 1) * (self.height/10))))

            # Draw row lines
            pygame.draw.line(self.win, (0, 0, 0), (startx, starty + (i * (self.height/10))),
                             (startx + self.width, starty + (i * (self.height / 10))), 2)


def error():
    if SOUND:
        wrong.play()
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showerror(
        'Out of Powerups!', 'You have no more powerups remaining for this course, press ok to continue...')
    try:
        root.destroy()
    except:
        pass


def endScreen():  # Display this screen when the user completes trhe course
    global start, starting, level, sheet, coins
    starting = True
    start = True

    # Draw all text to display on screen
    win.blit(background, (0, 0))
    text = myFont.render('Course Completed!', 1, (64, 64, 64))
    win.blit(text, (winwidth/2 - text.get_width()/2, 210))
    text = parFont.render('Par: ' + str(sheet.getPar()), 1, (64, 64, 64))
    win.blit(text, ((winwidth/2 - text.get_width()/2, 320)))
    text = parFont.render(
        'Strokes: ' + str(sheet.getStrokes()), 1, (64, 64, 64))
    win.blit(text, ((winwidth/2 - text.get_width()/2, 280)))
    blit = parFont.render('Press the mouse to continue...', 1, (64, 64, 64))
    win.blit(blit, (winwidth/2 - blit.get_width()/2, 510))
    text = parFont.render('Score: ' + str(sheet.getScore()), 1, (64, 64, 64))
    win.blit(text, ((winwidth/2 - text.get_width()/2, 360)))
    text = parFont.render('Coins Collected: ' + str(coins), 1, (64, 64, 64))
    win.blit(text, ((winwidth/2 - text.get_width()/2, 470)))
    pygame.display.update()

    # RE-WRITE TEXT FILE Contaning Scores
    oldscore = 0
    oldcoins = 0
    file = open('scores.txt', 'r')
    f = file.readlines()
    for line in file:
        l = line.split()
        if l[0] == 'score':
            oldscore = str(l[1]).strip()
        if l[0] == 'coins':
            oldcoins = str(l[1]).strip()

    file = open('scores.txt', 'w')
    if str(oldscore).lower() != 'none':
        if sheet.getScore() < int(oldscore):
            text = myFont.render('New Best!', 1, (64, 64, 64))
            win.blit(text, (winwidth/2 - text.get_width()/2, 130))
            pygame.display.update()
            file.write('score ' + str(sheet.getScore()) + '\n')
            file.write('coins ' + str(int(oldcoins) + coins) + '\n')
        else:
            file.write('score ' + str(oldscore) + '\n')
            file.write('coins ' + str(int(oldcoins) + coins) + '\n')
    else:
        file.write('score ' + str(sheet.getScore()) + '\n')
        file.write('coins ' + str(int(oldcoins) + coins) + '\n')

    co = 0
    for line in f:
        if co > 2:
            file.write(line)
        co += 1

    file.close()

    # Wait
    loop = True
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                loop = False
                break
    level = 1
    setup(level)
    list = courses.getPar(1)
    par = list[level - 1]
    sheet = scoreSheet(list)
    starting = True
    hover = False
    while starting:
        pygame.time.delay(10)
        startScreen.mainScreen(hover)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                hover = startScreen.shopClick(pos)
                course = startScreen.click(pos)
                startScreen.mouseOver(course != None)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if startScreen.click(pos) != None:
                    starting = False
                    break
                if startScreen.shopClick(pos) == True:
                    surface = startScreen.drawShop()
                    win.blit(surface, (0, 0))
                    pygame.display.update()
                    shop = True
                    while shop:
                        for event in pygame.event.get():
                            pygame.time.delay(10)
                            if event.type == pygame.QUIT:
                                pygame.quit()
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                pos = pygame.mouse.get_pos()
                                if pos[0] > 10 and pos[0] < 100 and pos[1] > 560:
                                    shop = False
                                    break
                                surface = startScreen.drawShop(pos, True)
                                win.blit(surface, (0, 0))
                                pygame.display.update()

            if event.type == pygame.QUIT:
                pygame.quit()
                break


def setup(level):  # Setup objects for the level from module courses
    global line, par, hole, power, ballStationary, objects, ballColor, stickyPower, superPower, mullagain
    ballColor = (255, 255, 255)
    stickyPower = False
    superPower = False
    mullagain = False
    if level >= 10:
        endScreen()  # Completed the course
    else:
        list = courses.getPar(1)
        par = list[level - 1]
        pos = courses.getStart(level, 1)
        ballStationary = pos

        objects = courses.getLvl(level)

        # Create the borders if sand is one of the objects
        for i in objects:
            if i[4] == 'sand':
                objects.append([i[0] - 16, i[1], 16, 64, 'edge'])
                objects.append(
                    [i[0] + ((i[2] // 64) * 64), i[1], 16, 64, 'edge'])
                objects.append([i[0], i[1] + 64, i[2], 16, 'bottom'])
            elif i[4] == 'flag':
                # Define the position of the hole
                hole = (i[0] + 2, i[1] + i[3])

        line = None
        power = 1


def fade():  # Fade out screen when player gets ball in hole
    fade = pygame.Surface((winwidth, winheight))
    fade.fill((0, 0, 0))
    for alpha in range(0, 300):
        fade.set_alpha(alpha)
        redrawWindow(ballStationary, None, False, False)
        win.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(1)


def showScore():  # Display the score from class scoreSheet
    global level
    sleep(2)
    level += 1
    sheet.drawSheet(strokes)
    pygame.display.update()
    go = True
    while go:  # Wait until user clicks until we move to next level
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
