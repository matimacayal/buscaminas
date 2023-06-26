import pyautogui
import numpy as np
from PIL import Image
import minesweeper_ocr as mcr
import time

class GameInterface():
    
    def __init__(self, window_title: str):
        self.top_left_map_corner = None
        self.bottom_right_map_corner = None
        self.rows = None
        self.cols = None
        self.window_title = window_title
        self.happy_face_center = None
    
    def initialize(self):
        print("Initialize GameInterface for", self.window_title)
        # get map info
        img_array = mcr.img_to_array(image=self.take_screenshot(display=False))
        game_info = mcr.get_map_metadata(img_array)
        self.top_left_map_corner = game_info["top_left_corner"]
        self.bottom_right_map_corner = game_info["bottom_right_corner"]
        self.rows = game_info["rows"]
        self.cols = game_info["cols"]
        self.happy_face_center = game_info["happy_face_center"]
        print(f"top_left: {self.top_left_map_corner}\n"
              f"bottom_right: {self.bottom_right_map_corner}\n"
              f"rows: {self.rows}\n"
              f"cols: {self.cols}\n"
              f"happy_face: {self.happy_face_center}")
    
    def take_screenshot(self, display:bool = False, as_rgb_array:bool = False):
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
        
        if as_rgb_array:
            screenshot = mcr.img_to_array(screenshot)
        
        return screenshot
    
    def image_to_nparray(self, image: Image):
        img_rgb = np.array(image) 
        # Convert RGB to BGR 
        img_rgb = img_rgb[:, :, ::-1].copy()
        return img_rgb

    def _click_window(self, window_title:str, x:int, y:int, button:str = 'left'):
        window_info = pyautogui.getWindowsWithTitle(window_title)
        if len(window_info) == 0:
            print("Window not found.")
            return
        window = window_info[0]
        window_left = window.left
        window_top = window.top

        absolute_x = window_left + x
        absolute_y = window_top + y

        pyautogui.click(absolute_x, absolute_y, button=button)

    def click_cell(self, row:int, col:int, button:str = 'left'):
        # grid_top = 127
        # grid_left = 16
        grid_left, grid_top = self.top_left_map_corner
        x = col * 20 + 10 + grid_left
        y = row * 20 + 10 + grid_top
        self._click_window('Minesweeper X', x, y, button)
    
    def righ_click_cell(self, row: int, col: int):
        self.click_cell(row, col, button='right')

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
    
    def execute(self, movements: list):
        print("movements:", movements)
        for movement in movements:
            row, col = movement["row_col"]
            action = movement["movement"]
            if action == "PRESS":
                # print(f"PRESS: {action} in {row},{col}")
                self.click_cell(row, col)
            elif action == "PLANT_FLAG":
                # print(f"PLANT_FLAG: {action} in {row},{col}")
                self.righ_click_cell(row, col)
            else:
                print("ERROR: invalid movement ->", action)
    
    def restart_game(self):
        x, y = self.happy_face_center
        self._click_window('Minesweeper X', x, y)
        time.sleep(0.1)
        self._click_window('Minesweeper X', x, y)

# if __name__ == '__main__':
#     main()