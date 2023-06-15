import pyautogui
import numpy as np
from PIL import Image


def take_screenshot(window_title: str, display:bool = False) -> Image:
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

    if display:
        screenshot.show()
    
    return screenshot

    # Replace 'Window Title' with the actual title of the window you want to capture
    # display_window_screenshot('Minesweeper X')

    # Convert the screenshot to grayscale
    # grayscale_screenshot = screenshot.convert('L')
    
    # pil_image = Image.frombytes('RGB', screenshot.size, screenshot.tobytes())
    # grayscale_image = screenshot.convert('L')

    # # Convert the grayscale screenshot to a NumPy array
    # grayscale_array = np.array(grayscale_image)
    
    # return grayscale_array

def click_window(window_title, x, y):
    window_info = pyautogui.getWindowsWithTitle(window_title)
    if len(window_info) == 0:
        print("Window not found.")
        return
    window = window_info[0]
    window_left = window.left
    window_top = window.top

    absolute_x = window_left + x
    absolute_y = window_top + y

    pyautogui.click(absolute_x, absolute_y)

def click_cell(row, col):
    grid_top = 127
    grid_left = 16
    x = col * 20 + 10 + grid_left
    y = row * 20 + 10 + grid_top
    click_window('Minesweeper X', x, y)

def play_minesweeper():
    while 1:
        txt = input("input:")
        if "e" in txt.lower():
            break
        elif "r" in txt.lower():
            click_window('Minesweeper X', 315, 91)
            click_window('Minesweeper X', 315, 91)
            continue
        r, c = txt.split(",")
        r, c = [int(r), int(c)]
        click_cell(r,c)

def main():
    # click_window('Minesweeper X', 226, 175)
    # take_screenshot('Minesweeper X')
    play_minesweeper()

if __name__ == '__main__':
    main()