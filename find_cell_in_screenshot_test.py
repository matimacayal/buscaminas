import cv2
import numpy as np
from matplotlib import pyplot as plt
import time

start_time = time.time()

img_rgb = cv2.imread('.\images\minesweeper_map.png')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
template = cv2.imread('.\images\minesweeper_covered_cell.png',0)
# template = cv2.imread('.\images\minesweeper_mine.png',0)
# template = cv2.imread('.\images\minesweeper_flag.png',0)
# template = cv2.imread('.\images\minesweeper_one.png',0)
# template = cv2.imread('.\images\minesweeper_three.png',0)
# template = cv2.imread('.\images\minesweeper_happy_face.png',0)
w, h = template.shape[::-1]

res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
threshold = 0.95
loc = np.where( res >= threshold)
# for pt in zip(*loc[::-1]):
#     print(f"point: {pt}")
#     cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

# print()
print(f"time: {time.time() - start_time}")

cv2.imwrite('images/result.png',img_rgb)



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