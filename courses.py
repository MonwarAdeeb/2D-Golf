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
        print("[GAME] Trying to install pygame via pip")
        import pip
        install("pygame")
        print("[GAME] Pygame has been installed")
    except:
        print("[EXCEPTION] Pip not installed on system")
        print("[GAME] Trying to install pip")
        get_pip.main()
        print("[GAME] Pip has been installed")