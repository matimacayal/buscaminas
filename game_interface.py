import pyautogui
import numpy as np
from PIL import Image
import minesweeper_ocr as mcr

class GameInterface():
    
    def __init__(self, window_title: str):
        self.top_left_map_corner = None
        self.bottom_right_map_corner = None
        self.rows = None
        self.cols = None
        self.window_title = window_title
    
    def initialize(self):
        # get map info
        img_array = mcr.image_to_nparray(self.take_screenshot())
        game_info = mcr.get_map_details(img_array)
        self.top_left_map_corner = game_info["top_left_corner"]
        self.bottom_right_map_corner = game_info["bottom_right_corner"]
        self.rows = game_info["rows"]
        self.cols = game_info["cols"]
        print(f"top_left: {self.top_left_map_corner}"
              f"bottom_right: {self.bottom_right_map_corner}"
              f"rows: {self.rows}"
              f"cols: {self.cols}")
    
    def take_screenshot(self, display:bool = False) -> Image:
        # Get the window's position and size
        window_info = pyautogui.getWindowsWithTitle(self.window_title)
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
    
    def image_to_nparray(self, image: Image):
        img_rgb = np.array(image) 
        # Convert RGB to BGR 
        img_rgb = img_rgb[:, :, ::-1].copy()
        return img_rgb

    def _click_window(self, window_title, x, y):
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

    def click_cell(self, row, col):
        # grid_top = 127
        # grid_left = 16
        grid_left, grid_top = self.top_left_map_corner
        x = col * 20 + 10 + grid_left
        y = row * 20 + 10 + grid_top
        self._click_window('Minesweeper X', x, y)

    def play_minesweeper(self):
        while 1:
            txt = input("input:")
            if "e" in txt.lower():
                break
            elif "r" in txt.lower():
                self._click_window('Minesweeper X', 315, 91)
                self._click_window('Minesweeper X', 315, 91)
                continue
            r, c = txt.split(",")
            r, c = [int(r), int(c)]
            self.click_cell(r,c)

    def main(self):
        # click_window('Minesweeper X', 226, 175)
        # take_screenshot('Minesweeper X')
        self.play_minesweeper()

# if __name__ == '__main__':
#     main()