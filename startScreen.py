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

    def getSurf(self, hover=False):
        surf = pygame.Surface((160, 125), pygame.SRCALPHA, 32)
        surf = surf.convert_alpha()
        # surf.fill((255,255,255))
        pygame.draw.circle(
            surf, (0, 0, 0), (round(surf.get_width()/2), 25), 22)
        pygame.draw.circle(
            surf, self.color, (round(surf.get_width()/2), 25), 20)
        if self.locked == True:
            label = self.font.render('Price: 10', 1, (0, 0, 0))
            if hover:
                buy = self.font.render('Purchase?', 1, (64, 64, 64))
            else:
                buy = self.font.render('Purchase?', 1, (0, 0, 0))
            surf.blit(
                label, (round(surf.get_width()/2 - label.get_width()/2), 50))
            surf.blit(buy, (round(surf.get_width()/2 - label.get_width()/2), 80))
        else:
            label = self.font.render('Unlocked', 1, (0, 0, 0))
            if self.equipped == False:
                buy = self.font.render('Equip', 1, (0, 0, 0))
                surf.blit(
                    buy, (round(surf.get_width() / 2 - buy.get_width() / 2), 80))
            else:
                buy = self.font.render('Equipped', 1, (0, 0, 0))
                surf.blit(
                    buy, (round(surf.get_width() / 2 - buy.get_width() / 2), 80))
            surf.blit(
                label, (round(surf.get_width()/2 - label.get_width()/2), 50))
