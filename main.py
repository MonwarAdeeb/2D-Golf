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
