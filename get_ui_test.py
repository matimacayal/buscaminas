import numpy as np
from PIL import Image
import pygetwindow as gw

# Define the program name of the Minesweeper game window
program_name = "Minesweeper X"

# Find the Minesweeper game window
game_window = gw.getWindowsWithTitle(program_name)[0]

# Get the window coordinates
window_coordinates = (game_window.left, game_window.top, game_window.right, game_window.bottom)

# Capture a screenshot of the game window
screenshot = Image.grab(window_coordinates)

# Continue with the rest of the script...
screenshot.show()