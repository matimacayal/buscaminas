import pyautogui
import numpy as np
from PIL import Image

# def display_window_screenshot(window_title):

def get_np_array_screenshot():
    window_title = 'Minesweeper X'
    # Get the window's position and size
    window_info = pyautogui.getWindowsWithTitle(window_title)
    window = window_info[0]
    window_left = window.left
    window_top = window.top
    window_width = window.width
    window_height = window.height

    # Capture the screenshot
    screenshot = pyautogui.screenshot(region=(window_left, window_top, window_width, window_height))

    # Display the screenshot
    screenshot.show()

    # Replace 'Window Title' with the actual title of the window you want to capture
    # display_window_screenshot('Minesweeper X')

    # Convert the screenshot to grayscale
    # grayscale_screenshot = screenshot.convert('L')
    
    pil_image = Image.frombytes('RGB', screenshot.size, screenshot.tobytes())
    grayscale_image = screenshot.convert('L')

    # Convert the grayscale screenshot to a NumPy array
    grayscale_array = np.array(grayscale_image)
    
    return grayscale_array


# Define the region of the game window to capture
# You may need to adjust these coordinates based on your screen resolution
# window_coordinates = (x1, y1, x2, y2)  # (top-left x, top-left y, bottom-right x, bottom-right y)

# Capture a screenshot of the game window
# screenshot = Image.grab(window_coordinates)

# Convert the screenshot image to grayscale
# grayscale_image = screenshot.convert('L')

# Define the colors of the numbers in the Minesweeper game
number_colors = {
    (192, 192, 192): 0,  # Gray color for empty cells
    (0, 0, 255): 1,      # Blue color for the number 1
    (0, 128, 0): 2,      # Green color for the number 2
    # Define the rest of the number colors (3, 4, 5, 6, 7, 8) here
}

# Define the color of the mines in the Minesweeper game
mine_color = (255, 0, 0)  # Red color for mines

# Convert the grayscale image to a numpy array
game_grid = get_np_array_screenshot()

# Translate the colors in the numpy array to their corresponding values
for color, value in number_colors.items():
    mask = np.all(game_grid == color, axis=2)
    game_grid[mask] = value

mask = np.all(game_grid == mine_color, axis=2)
game_grid[mask] = -1  # Use -1 to represent mines in the game grid

# Now you have the game grid as a numpy array with values representing the cells
print(game_grid)









# import numpy as np
# from PIL import Image
# from PIL import ImageGrab
# import pygetwindow as gw

# # Define the program name of the Minesweeper game window
# program_name = "Minesweeper X"
# # program_name = "Reloj"
# # program_name = "Picture-in-Picture"

# # Find the Minesweeper game window
# game_window = gw.getWindowsWithTitle(program_name)
# print(game_window)
# game_window = game_window[0]
# print(game_window)

# # Get the window coordinates
# window_left = game_window.left + 258 # Adjust left coordinate to exclude window border
# window_top = game_window.top + 42  # Adjust top coordinate to exclude window title bar
# window_right = game_window.right + 380  # Adjust right coordinate to exclude window border
# window_bottom = game_window.bottom + 165  # Adjust bottom coordinate to exclude window border

# # Get the window coordinates
# # window_coordinates = (game_window.left, game_window.top, game_window.right, game_window.bottom)
# window_coordinates = (window_left, window_top, window_right, window_bottom)

# # Capture a screenshot of the game window
# screenshot = ImageGrab.grab(window_coordinates)

# # Continue with the rest of the script...
# screenshot.show()
