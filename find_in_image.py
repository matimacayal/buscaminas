import cv2
import numpy as np
from matplotlib import pyplot as plt
import time

start_time = time.time()

# img_rgb = cv2.imread('.\images\minesweeper_map.png')
# img_rgb = cv2.imread('./images/2023-06-12 (4).png')
img_rgb = cv2.imread('./images/minesweeper_24x30_soclose.png')
# img_rgb = cv2.imread('./images/2023-06-13 (14).png')
# img_rgb = cv2.imread('./images/2023-06-11 (8).png')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

search_files = [
    '.\images\minesweeper_map_top_left_corner.png',
    '.\images\minesweeper_map_bottom_right_corner.png',
    # '.\images\minesweeper_covered_cell.png',
    '.\images\minesweeper_empty_cell.png',
    # '.\images\minesweeper_happy_face.png',
    # '.\images\minesweeper_mine.png',
    # '.\images\minesweeper_flag.png',
    '.\images\minesweeper_one.png',
    '.\images\minesweeper_two.png',
    '.\images\minesweeper_three.png',
    # '.\images\minesweeper_four.png',
    # '.\images\minesweeper_five.png',
    # '.\images\minesweeper_six.png',
    # '.\images\minesweeper_seven.png',
]

prefix = '.\images\minesweeper_'
suffix = '.png'

threshold = 0.95

holder = []

for n, file_name in enumerate(search_files):
    template = cv2.imread(file_name,0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    loc = np.where( res >= threshold)
    holder.append([n, w, h, loc, file_name])

for n, w, h, loc, file_name in holder:
    for pt in zip(*loc[::-1]):
        print(f"point{n}:\t{pt}\t{file_name[len(prefix):-len(suffix)]}")
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

print(f"time: {time.time() - start_time}")

cv2.imwrite('images/_result.png',img_rgb)



# (env) PS C:\Users\mmaca\Documents\buscaminas> python .\find_cell_in_screenshot_test.py
# point: (196, 127)
# point: (216, 127)
# point: (236, 127)
# point: (316, 127)
# point: (336, 127)
# point: (356, 127)
# point: (256, 147)
# point: (276, 147)
# point: (316, 147)
# point: (176, 187)
# point: (196, 187)
# point: (216, 187)
# point: (176, 207)
# point: (276, 227)
# point: (296, 227)
# point: (256, 247)
# point: (276, 247)
# time: 0.01591944694519043