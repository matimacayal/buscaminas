import pyautogui
import numpy as np
from PIL import Image


def take_screenshot(window_title):
    # Get the window's position and size
    window_info = pyautogui.getWindowsWithTitle(window_title)
    if len(window_info) == 0:
        print("Window not found.")
        return
    window = window_info[0]
    window_left = window.left
    window_top = window.top
    window_width = window.width
    window_height = window.height

    screenshot = pyautogui.screenshot(region=(window_left, window_top, window_width, window_height))

    screenshot.show()

    # Replace 'Window Title' with the actual title of the window you want to capture
    # display_window_screenshot('Minesweeper X')

    # Convert the screenshot to grayscale
    # grayscale_screenshot = screenshot.convert('L')
    
    # pil_image = Image.frombytes('RGB', screenshot.size, screenshot.tobytes())
    # grayscale_image = screenshot.convert('L')

    # # Convert the grayscale screenshot to a NumPy array
    # grayscale_array = np.array(grayscale_image)
    
    # return grayscale_array

def main():
    take_screenshot('Minesweeper X')

if __name__ == '__main__':
    main()