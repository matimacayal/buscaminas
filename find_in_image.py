import cv2
import numpy as np
from matplotlib import pyplot as plt
import time

# TODO: refactor - poner los tipos de las variables de entrada y salida de las funciones
# TODO: se podría crear una clase y se carga la imagen y luego se usa la misma imagen en la clase con distintos templates


def get_loc(img_rgb, template):
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    threshold = 0.95

    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    loc = np.where( res >= threshold)
    template_loc = np.concatenate(loc)[::-1]
    
    return template_loc

def main():
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


if __name__ == '__main__':
    main()