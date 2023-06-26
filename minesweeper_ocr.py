import cv2
import numpy as np
from matplotlib import pyplot as plt
# from game_interface import GameInterface
import time
import pyautogui
from pathlib import Path
import re

# TODO: refactor - poner los tipos de las variables de entrada y salida de las funciones

np.set_printoptions(linewidth=200)

COVERED_CELL_CHAR = "."
FLAG_CELL_CHAR = "●"
MINE_CELL_CHAR = "*"

# color in cv2
# color     = np.array([ B , G , R ])
WHITE       = np.array([255,255,254])
DARK_GRAY   = np.array([131,131,131])
RED         = np.array([0,0,254])
BLACK       = np.array([0,0,0])
GRAY        = np.array([192,192,192])
BLUE        = np.array([254, 0, 0])
GREEN       = np.array([0, 128, 0])
PURPLE      = np.array([128, 0, 0])
LIGHT_PURPLE= np.array([147, 58, 58])
BURGUNDY    = np.array([0, 0, 128])
CYAN        = np.array([128, 128, 0])

COLORS = {
    'gray': GRAY,
    'red': RED,
    'blue': BLUE,
    'green': GREEN,
    'purple': PURPLE,
    'light_purple': LIGHT_PURPLE,
    'burgundy': BURGUNDY,
    'cyan': CYAN,
    'black': BLACK,
}
NUMBERS = {
    'gray': "0",
    'blue': "1",
    'green': "2",
    'red': "3",
    'purple': "4",
    'light_purple': "4",
    'burgundy': "5",
    'cyan': "6",
    'black': '7',
    'mine_black': MINE_CELL_CHAR # TODO: check well if doing this, or even if it needs to be done.
}

def _get_grid_corners(img_rgb):
    """
    returns the x,y pixel for the top and bottom corner of the player map

    Args:
        img_rgb (np.ndarray): imagen del screenshot en formato cv2 RGB

    Returns:
        [np.array([x1,y1]), np.array([x2,y2])]: list with top and bottom coordinates as np.ndarray
    
    Example:
        img_rgb = mcr.get_minesweeper_screenshot()
        cv2.imshow('debug_image_before',img_rgb)
        cv2.waitKey(0)
        mcr._get_grid_corners(img_rgb) 
            ->(array([ 19, 127], dtype=int64), array([619, 607], dtype=int64))
    
    """
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template_top_left_corner = cv2.imread( '.\images\minesweeper_map_top_left_corner.png',0)
    template_bottom_right_corner = cv2.imread( '.\images\minesweeper_map_bottom_right_corner.png',0)

    threshold = 0.95

    res = cv2.matchTemplate(img_gray,template_top_left_corner,cv2.TM_CCOEFF_NORMED)
    loc = np.where( res >= threshold)
    template_top_left_coord = np.concatenate(loc)[::-1]

    res = cv2.matchTemplate(img_gray,template_bottom_right_corner,cv2.TM_CCOEFF_NORMED)
    loc = np.where( res >= threshold)
    template_bottom_right_coord = np.concatenate(loc)[::-1]
    
    if template_bottom_right_coord.size == 0 or template_top_left_coord.size == 0:
        print("BREAKING: templates not found")
        return None, None

    top_left_corner = template_top_left_coord + np.array([9,17])
    bottom_right_corner = template_bottom_right_coord - np.array([1,1])
    
    return top_left_corner, bottom_right_corner

def _get_happy_face_center(img_rgb):
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template_happy_face = cv2.imread( '.\images\minesweeper_happy_face.png',0)

    threshold = 0.95

    res = cv2.matchTemplate(img_gray,template_happy_face,cv2.TM_CCOEFF_NORMED)
    loc = np.where( res >= threshold)
    happy_face_coord = np.concatenate(loc)[::-1]
    
    if happy_face_coord.size == 0:
        print("BREAKING: templates not found")
        return None

    happy_face_center = happy_face_coord + np.array([16,16]) # happy face is 34x34 pixels
    
    return happy_face_center

def get_map_metadata(img_rgb: cv2.Mat) -> dict:
    """
    From a cv2 RGB screenshot of the Minesweeper window get the position of
    the top and bottom corners, the number of rows and columns of the mine map
    and the position of the restart (happy face) button.

    Args:
        img_rgb (cv2.Mat): Minesweeper screenshot as cv2 RGB np.ndarray

    Returns:
        dict: A dictionary containing metadata about the game grid.

            The dictionary has the following structure:

            {
                "top_left_corner": np.ndarray,
                "bottom_right_corner": np.ndarray,
                "rows": int,
                "cols": int,
                "happy_face_center": np.ndarray
            }
    
    Note:
        This function assumes that the game grid and the happy face are visible and properly aligned
        in the input image. It uses image processing techniques to locate the corners and center
        of the game grid.

    Example:
        img = cv2.imread('game_image.png')
        metadata = get_map_metadata(img)
        # Access individual metadata values
        top_left_corner = metadata['top_left_corner']
        rows = metadata['rows']
        # Use the metadata for further processing
    """
    top_left_corner, bottom_right_corner = _get_grid_corners(img_rgb)
    happy_face_center = _get_happy_face_center(img_rgb)
    if not top_left_corner.any() or not bottom_right_corner.any():
        return None
    
    cols, rows = (bottom_right_corner - top_left_corner) // 20
    
    map_details = {
        "top_left_corner": top_left_corner,
        "bottom_right_corner": bottom_right_corner,
        "rows": rows,
        "cols": cols,
        "happy_face_center": happy_face_center
    }
    return map_details

def increment_last_number(filename):
    regex = re.compile(r'(\d+)(?!.*\d)')  # Matches the last number in the filename
    match = regex.search(filename)
    
    if match:
        number = int(match.group(0))  # Extract the last number
        new_number = number + 1
        new_filename = regex.sub(str(new_number), filename, count=1)
        return new_filename
    
    return None

def save_image(image, filename):
    path = Path(filename)
    
    while path.exists():
        new_filename = increment_last_number(path.stem)
        
        if new_filename is not None:
            new_filename += path.suffix
            path = path.with_name(new_filename)
        else:
            path = path.with_name(path.stem + "_2" + path.suffix)
    
    path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(path), image)
    print(f"Image saved as {path}")
    

def minesweeper_ocr(img_rgb:cv2.Mat, mines_total:int = 0) -> np.ndarray:
    """
    Receives 'Minesweeper X' window screenshot as cv2 RGB and return and
    returns the player map as a rows,cols np.ndarray that the ai can use

    Args:
        img_rgb (cv2.Mat): Minesweeper screenshot as cv2 RGB np.ndarray 
        mines_total (int, optional): The total number of mines in the game.
            Used to count total flags and determine if game has enden.
            Defaults to 0.

    Returns:
        np.ndarray: if all goes well returns the player map as an np array
    
    Note:
        This function assumes that the game grid is visible and properly aligned in the input image.
        It relies on specific pixel colors to identify covered, uncovered, flagged, and mine cells.

    Performs OCR on the input image to extract information about the game grid cells.
    It analyzes the colors of pixels in specific locations to determine the state of each cell.
    The identified cells are stored in a numpy array and returned as the output.
    The function also checks for OCR errors and game completion status.
    
    Example:
        img = cv2.imread('game_image.png')
        result = minesweeper_ocr(img, mines_total=20)
        # Perform further processing on the result
    
    """
    # cv2.imshow('debug_image_before',img_rgb)
    # cv2.waitKey(0)
    
    ocr_error = False
    found_mines = False
    
    top_left_corner, bottom_right_corner = _get_grid_corners(img_rgb)
    if not top_left_corner.any() or not bottom_right_corner.any():
        return None
        
    cols, rows = (bottom_right_corner - top_left_corner) // 20
    player_map = np.empty([rows, cols], dtype=str)
    game_finished = False

    # print("top_left_corner", top_left_corner)
    # print("bottom_right_corner", bottom_right_corner)
    # print("grid_size", cols, rows)

    white_tolerance = 20
    tolerance = 3

    for row in range(rows):
        for col in range(cols):
            cell_pixel = top_left_corner + np.array([col, row]) * 20
            
            # get image pixel -> pixel_b, pixel_g, pixel_r = image[row][column]
            x, y = cell_pixel + np.array([1,0])
            pixel_0_1 = img_rgb[y][x]
            # print(f"cell [{row},{col}] top left pixel ({cell_pixel}). Pixel ({x}, {y}) color  {pixel_0_1}.")
            
            if np.allclose(pixel_0_1, WHITE, atol=white_tolerance):
                # print(f"cell [{row},{col}] top left pixel ({cell_pixel}). Pixel ({x}, {y}) color  {pixel_0_1}. Covered.")
                img_rgb[y,x] = [255,0,0]
                x9, y6 = cell_pixel + np.array([9,6])
                _, y14 = cell_pixel + np.array([9,14])
                pixel_9_6 = img_rgb[y6][x9]
                pixel_9_14 = img_rgb[y14][x9]
                if np.allclose(pixel_9_6, RED, atol=3) and np.allclose(pixel_9_14, BLACK, atol=tolerance):
                    player_map[row, col] = FLAG_CELL_CHAR
                elif np.allclose(pixel_9_6, GRAY, atol=3) and np.allclose(pixel_9_14, GRAY, atol=tolerance):
                    player_map[row, col] = COVERED_CELL_CHAR
                    # print(f"cell [{row},{col}] Covered. Pixel colors ({x9},{y6}) {pixel_9_6} ({x9},{y14}) {pixel_9_14}.")
                else:
                    print(f'OCR failed [{row},{col}]. No color match for pixels 9,6({x9},{y6}){pixel_9_6} 9,14({x9},{y14}){pixel_9_14}')
            elif np.allclose(pixel_0_1, DARK_GRAY, atol=tolerance):
                # print(f"cell [{row},{col}] top left pixel ({cell_pixel}). Pixel ({x}, {y}) color  {pixel_0_1}. Uncovered.")
                img_rgb[y,x] = [0,0,255]
                x, y = cell_pixel + np.array([11,14])
                pixel_11_14 = img_rgb[y][x]
                
                matched_colors = []
                for color_name, color_value in COLORS.items():
                    if np.allclose(pixel_11_14, color_value, atol=tolerance):
                        if color_name == "black":
                            # cell could be 7 or MINE
                            x, y = cell_pixel + np.array([8,8])
                            pixel_8_8 = img_rgb[y][x]
                            if np.allclose(pixel_8_8, WHITE, atol=tolerance):
                                found_mines = True
                                matched_colors.append("mine_black")
                                continue
                            else:
                                print(f'OCR failed [{row},{col}]. No color match for pixels 8,8({x},{y}){pixel_8_8}')
                        matched_colors.append(color_name)
                if matched_colors == []:
                    print(f'OCR failed [{row},{col}]. No color match for pixels 11,14({x},{y}){pixel_11_14}')
                    
                if len(matched_colors) != 1:
                    print(f"ERROR: more than one color detected. Cell [{row},{col}] Pixel ({x},{y}) colors {matched_colors}")
                    return None
                
                number = NUMBERS[matched_colors[0]]
                player_map[row, col] = number
                # print(f"cell [{row},{col}] Uncovered. Pixel ({x}, {y}) #{number} color  {matched_colors} {pixel_11_14}.")
            else:
                print(f'OCR failed [{row},{col}]. No color match in pixel 0,1({x},{y}){pixel_0_1}')
                        
            if player_map[row, col] == '':
                ocr_error = True
                print(f'OCR failed. Empty cell [{row},{col}]')
    
    print(f"player_map:\n", player_map)
    
    if mines_total <= 0:
        print(f"WARNING: mines_total = {mines_total}")
    print(f'top corner {top_left_corner}, bottom corner{bottom_right_corner}')
    print(f'player_map.shape = {rows, cols}')
    
    # cv2.imshow('debug_image_after',img_rgb)
    # cv2.waitKey(0)
    
    if ocr_error:
        print("OCR ERROR -> TRUE")
        save_image(img_rgb, 'images/ocr_tests/ocr_error_image.png')
        # cv2.imwrite('images/debug_image_after.png',img_rgb)
    else:
        print("OCR witho No Errors")
        save_image(img_rgb, 'images/ocr_tests/ocr_success_image.png')
    
    if (mines_total != 0
        and np.count_nonzero(player_map == COVERED_CELL_CHAR) == 0
        and MINE_CELL_CHAR not in player_map
        and np.count_nonzero(player_map == FLAG_CELL_CHAR) == mines_total):
        print("game_finished = True")
        game_finished = True
        
    return player_map, found_mines, game_finished  # TODO: move game_finished variable to other part to have clean function

def debug_mcr():
    minesweeper_ocr(debug=True)

# def image_to_arr(self, image) -> np.ndarray:
def img_to_array(image) -> np.ndarray:
        img_rgb = np.array(image) 
        # Convert RGB to BGR 
        img_rgb = img_rgb[:, :, ::-1].copy()
        return img_rgb

def display_array(arr):
    # TODO: implementar que avise si hay celdas no validas o vacías
    print(np.array2string(arr, separator=' ', formatter={'str_kind': lambda x: x}))

def save_minesweeper_screenshot():
    window = pyautogui.getWindowsWithTitle("Minesweeper X")[0]
    screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
    screenshot.save('images/screenshot.png')

def get_minesweeper_screenshot():
    """
    returns a screenshot of the 'Minesweeper X' window

    Returns:
        np.ndarray: imagen en formato cv2 RGB
    """
    window = pyautogui.getWindowsWithTitle("Minesweeper X")[0]
    screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
    img_rgb = np.array(screenshot) 
    img_rgb = img_rgb[:, :, ::-1].copy()
    return img_rgb

def find_image_in_image(
    # img_url_1:str = 'images/minesweeper_map_top_left_corner.png',
    img_url_1:str = 'images/minesweeper_map_bottom_right_corner.png',
    img_url_2 = 'images/screenshot.png'  # 'images/minesweeper_24x30_soclose.png'
    ):
    if type(img_url_2) is str:
        img_url_2 = cv2.imread(img_url_2)
    img_rgb = img_url_2.copy()
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(img_url_1,0)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.95
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]):
        print(f"image found in pixel: {pt}")
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

    # cv2.imwrite('res.png',img_rgb)
    cv2.imshow('result', img_rgb)
    cv2.waitKey(0)

    
# def main():
#     start_time = time.time()
#     # game_interface = GameInterface(window_title="Minesweeper X")
#     screenshot = game_interface.take_screenshot(display=True)
#     game_image = img_to_array(screenshot)
#     player_map = minesweeper_ocr(game_image)[0]
#     if player_map is None:
#         print("couldn't get ocr")
#         return
    
#     display_array(player_map)
#     print(f"took {time.time() - start_time} s")
    
        
# if __name__ == '__main__':
#     main()