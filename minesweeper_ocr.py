import cv2
import numpy as np
from matplotlib import pyplot as plt
import windows_ui as wui
import time

# TODO: refactor - poner los tipos de las variables de entrada y salida de las funciones

np.set_printoptions(linewidth=200)

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
    'black': '7'
}
COVERED_CELL_CHAR = "."
FLAG_CELL_CHAR = "●"
MINE_CELL_CHAR = "*"

def _get_grid_corners(img_rgb):
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
        return None, None

    top_left_corner = template_top_left_coord + np.array([9,17])
    bottom_right_corner = template_bottom_right_coord - np.array([1,1])
    
    return top_left_corner, bottom_right_corner

def minesweeper_ocr(img_rgb: cv2.Mat):
    top_left_corner, bottom_right_corner = _get_grid_corners(img_rgb)
    if not top_left_corner.any() or not bottom_right_corner.any():
        return None
    
    cols, rows = (bottom_right_corner - top_left_corner) // 20
    player_map = np.empty([rows, cols], dtype=str)

    # print("top_left_corner", top_left_corner)
    # print("bottom_right_corner", bottom_right_corner)
    # print("grid_size", cols, rows)

    white_tolerance = 10
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
                    print("ERROR: no cell match for colors")
            elif np.allclose(pixel_0_1, DARK_GRAY, atol=tolerance):
                # print(f"cell [{row},{col}] top left pixel ({cell_pixel}). Pixel ({x}, {y}) color  {pixel_0_1}. Uncovered.")
                x, y = cell_pixel + np.array([11,14])
                pixel_11_14 = img_rgb[y][x]            
                
                matched_colors = []
                for color_name, color_value in COLORS.items():
                    if np.allclose(pixel_11_14, color_value, atol=tolerance):
                        matched_colors.append(color_name)
                            
                if len(matched_colors) != 1:
                    print(f"ERROR: more than one color detected. Cell [{row},{col}] Pixel ({x},{y}) colors {matched_colors}")
                    return None
                
                number = NUMBERS[matched_colors[0]]
                player_map[row, col] = number
                # print(f"cell [{row},{col}] Uncovered. Pixel ({x}, {y}) #{number} color  {matched_colors} {pixel_11_14}.")
    
    return player_map

def get_screenshot(window_title: str = "") -> cv2.Mat:
    # TODO: avisar en caso que ventana del minesweeper no esté abierta
    img_rgb = None
    if not window_title:
        img_rgb = cv2.imread('./images/minesweeper_24x30_soclose.png')
        # img_rgb = cv2.imread('./images/2023-06-12 (4).png')
    else:
        image = wui.take_screenshot(window_title)
        img_rgb = np.array(image) 
        # Convert RGB to BGR 
        img_rgb = img_rgb[:, :, ::-1].copy()
    return img_rgb

def display_array(arr):
    print(np.array2string(arr, separator=' ', formatter={'str_kind': lambda x: x}))

def main():
    start_time = time.time()
    game_image = get_screenshot("Minesweeper X")
    if not game_image.any():
        return
    
    player_map = minesweeper_ocr(game_image)
    if player_map is None:
        return
    
    display_array(player_map)
    print(f"took {time.time() - start_time} s")
        
if __name__ == '__main__':
    main()