import pygame
import os
import tkinter as tk
from tkinter import messagebox
import sys

pygame.init()

win = pygame.display.set_mode((1080, 600))
title = pygame.image.load(os.path.join('img', 'title.png'))
back = pygame.image.load(os.path.join('img', 'back.png'))
course = pygame.image.load(os.path.join('img', 'course1.png'))
course1 = pygame.transform.scale(course, (200, 200))

font = pygame.font.SysFont('comicsansms', 24)

buttons = [[1080/2 - course1.get_width()/2, 260, course1.get_width(),
            course1.get_height(), 'Grassy Land']]
shopButton = []
ballObjects = []
surfaces = []


class ball():
    def __init__(self, color, locked, org):
        self.color = color
        self.locked = locked
        self.original = org
        self.price = 10
        self.equipped = False
        self.font = pygame.font.SysFont('comicsansms', 22)

    def unlock(self):
        file = open('scores.txt', 'r')
        f = file.readlines()
        file.close()

        file = open('scores.txt', 'w')
        for line in f:
            if line.find(self.original) != -1:
                file.write(self.original + '-' + 'True\n')
            else:
                file.write(line)

        self.locked = False

    def getLocked(self):
        return self.locked

    def equip(self):
        self.equipped = True

    def getEquip(self):
        return self.equipped
