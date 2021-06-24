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
