import cv2
import numpy as np
from matplotlib import pyplot as plt

# img_rgb = cv2.imread('./images/2023-06-13 (14).png')
img_rgb = cv2.imread('./images/minesweeper_24x30_soclose.png')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
template_top_left_corner = cv2.imread( '.\images\minesweeper_map_top_left_corner.png',0)
template_bottom_right_corner = cv2.imread( '.\images\minesweeper_map_bottom_right_corner.png',0)

np.set_printoptions(linewidth=200)
threshold = 0.95

res = cv2.matchTemplate(img_gray,template_top_left_corner,cv2.TM_CCOEFF_NORMED)
loc = np.where( res >= threshold)
template_top_left_coord = np.concatenate(loc)[::-1]  # [value + 1 for value in list(zip(*loc[::-1]))[0]]

res = cv2.matchTemplate(img_gray,template_bottom_right_corner,cv2.TM_CCOEFF_NORMED)
loc = np.where( res >= threshold)
template_bottom_right_coord = np.concatenate(loc)[::-1] # [value + 1 for value in list(zip(*loc[::-1]))[0]]

top_left_corner = template_top_left_coord + np.array([9,17])
bottom_right_corner = template_bottom_right_coord - np.array([1,1])
cols, rows = (bottom_right_corner - top_left_corner) // 20
player_map = np.empty([rows, cols], dtype=str)

# TODO: agregar que si no encuentra alguno se detenga

print("top_left_corner", top_left_corner)
print("bottom_right_corner", bottom_right_corner)
print("grid_size", cols, rows)

# color in cv2
# color     = np.array([ B , G , R ])
white       = np.array([255,255,254])
dark_gray   = np.array([131,131,131])
red         = np.array([0,0,254])
black       = np.array([0,0,0])
gray        = np.array([192,192,192])
colors = {
    'gray': np.array([192,192,192]),
    'red': np.array([0, 0, 254]),
    'blue': np.array([254, 0, 0]),
    'green': np.array([0, 128, 0]),
    'purple': np.array([128, 0, 0]),
    'light_purple': np.array([147, 58, 58]),
    'burgundy': np.array([0, 0, 128]),
    'cyan': np.array([128, 128, 0]),
    'black': np.array([0,0,0])
    
}
numbers = {
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

white_tolerance = 10
tolerance = 3

for row in range(rows):
    for col in range(cols):
        cell_pixel = top_left_corner + np.array([col, row]) * 20
        # get image pixel
        #   pixel_b, pixel_g, pixel_r = image[row][column]
        x, y = cell_pixel + np.array([1,0])
        pixel_0_1 = img_rgb[y][x]
        # print(f"cell [{row},{col}] top left pixel ({cell_pixel}). Pixel ({x}, {y}) color  {pixel_0_1}.")
        if np.allclose(pixel_0_1, white, atol=white_tolerance):
            # covered cell: a flag or a non-pressed cell
            # print(f"cell [{row},{col}] top left pixel ({cell_pixel}). Pixel ({x}, {y}) color  {pixel_0_1}. Covered.")
            
            x9, y6 = cell_pixel + np.array([9,6])
            _, y14 = cell_pixel + np.array([9,14])
            pixel_9_6 = img_rgb[y6][x9]
            pixel_9_14 = img_rgb[y14][x9]
            if np.allclose(pixel_9_6, red, atol=3) and np.allclose(pixel_9_14, black, atol=tolerance):
                # is flag
                player_map[row, col] = FLAG_CELL_CHAR
            if np.allclose(pixel_9_6, gray, atol=3) and np.allclose(pixel_9_14, gray, atol=tolerance):
                # is covered cell
                player_map[row, col] = COVERED_CELL_CHAR
                print(f"cell [{row},{col}] Covered. Pixel colors ({x9},{y6}) {pixel_9_6} ({x9},{y14}) {pixel_9_14}.")
        #     else:
        #         print("ERROR: no cell match for colors")
        elif np.allclose(pixel_0_1, dark_gray, atol=tolerance):
            # uncovered cell: a number, a mine or an empty cell
            # print(f"cell [{row},{col}] top left pixel ({cell_pixel}). Pixel ({x}, {y}) color  {pixel_0_1}. Uncovered.")
            x, y = cell_pixel + np.array([11,14])
            pixel_11_14 = img_rgb[y][x]            
            # np.linalg.norm()
            matched_colors = []

            for color_name, color_value in colors.items():
                if np.allclose(pixel_11_14, color_value, atol=tolerance):
                    matched_colors.append(color_name)
                        
            if len(matched_colors) != 1:
                print(f"ERROR: more than one color detected. Cell [{row},{col}] Pixel ({x},{y}) colors {matched_colors}")
                break
            
            number = numbers[matched_colors[0]]
            player_map[row, col] = number
            # print(f"cell [{row},{col}] Uncovered. Pixel ({x}, {y}) #{number} color  {matched_colors} {pixel_11_14}.")

# print(player_map)
print(np.array2string(player_map, separator=' ', formatter={'str_kind': lambda x: x}))


