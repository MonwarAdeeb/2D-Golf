import subprocess
import sys
import get_pip
import os


def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])
