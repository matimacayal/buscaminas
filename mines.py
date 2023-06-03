import numpy as np
import random
import itertools

# function that given a coordinate can iterate over theit's neighbours and count mines
def count_bombs(row, col, array):
    sum = 0
    for r in range(row-1, row+2):
        for c in range(col-1, col+2):
            if ([r, c] != [row, col]) and (0 <= r < array.shape[0]) and (0 <= c < array.shape[1]):
                if array[r, c] == -1:
                    sum += 1
    return sum

def random_duple(R1, R2, N=1):
    duple = random.sample(list(itertools.product(range(R1), range(R2))), N)
    if N == 1:
        return duple[0]
    
    return duple

def build_minesweeper_map(map_height, map_width, total_mines):
    arr = np.zeros((map_height, map_width))
    
    # randomly distribute 10 mines in the 64 blocks array
    mine_coordinates = random_duple(map_height, map_width, N = total_mines)
    for mine in mine_coordinates:
        arr[mine] = -1
        
    for row, _ in enumerate(arr):
        for col, value in enumerate(_):
            if value != -1:
                sum = count_bombs(row, col, arr)
                arr[row,col] = sum
                    
    return arr

def clear_neighbour_cells(cell_row, cell_col, player_map, mine_map):
    for r in range(cell_row-1, cell_row+2):
        for c in range(cell_col-1, cell_col+2):
            if ([r, c] != [cell_row, cell_col]) and (0 <= r < player_map.shape[0]) and (0 <= c < player_map.shape[1]):
                # print(f"checking cell: {[r,c]}")
                if mine_map[r, c] == 0 and player_map[r, c] == COVERED_CELL_CHAR:
                    print(f"pressing cell: {[r,c]}")
                    press_cell(r, c, player_map, mine_map)
                player_map[r, c] = str(mine_map[r, c])

def press_cell(cell_row, cell_col, player_map, mine_map):
    if player_map[cell_row, cell_col] == FLAG_CELL_CHAR:
        print("Can't press flagged mine")
        return
    
    cell_value = mine_map[cell_row, cell_col]
    if cell_value == -1:
        print("Mine. Lost game.")
        player_map[cell_row, cell_col] = MINE_CELL_CHAR
        return
    elif cell_value == 0:
        print(f"({cell_row},{cell_col}) cell empty, clearing neighbouring cells")
        player_map[cell_row, cell_col] = "0"
        clear_neighbour_cells(cell_row, cell_col, player_map, mine_map)
    else:
        print(f"cell_value = {cell_value}")
        player_map[cell_row, cell_col] = str(cell_value)

def press_random_cell(mine_map, grid):
    height, width = grid.shape
    cell_row, cell_col = random_duple(height-1, width-1)
    press_cell(cell_row, cell_col, grid, mine_map)
    return cell_row, cell_col
    
def plant_flag(cell_row, cell_col, player_map):
    # TODO: Implement total flags planted
    current_value = player_map[cell_row, cell_col]
    if current_value == COVERED_CELL_CHAR:
        player_map[cell_row, cell_col] = FLAG_CELL_CHAR
    elif current_value == FLAG_CELL_CHAR:
        player_map[cell_row, cell_col] = COVERED_CELL_CHAR
    else:
        print("Can't flag pressed mine")

def print_map(player_map):
    for row in player_map:
            print(' '.join(row))


COVERED_CELL_CHAR = "."
FLAG_CELL_CHAR = "^"
MINE_CELL_CHAR = "*"

if __name__ == '__main__':
    width = 8
    height = 8
    mines = 2
    
    np.set_printoptions(linewidth=150)
    mine_map = build_minesweeper_map(height, width, mines)
    player_map = np.full((height, width), COVERED_CELL_CHAR, dtype=str)
    
    print_map(player_map)
        
    while np.count_nonzero(player_map == COVERED_CELL_CHAR) != 0:
        txt = input("input:")
        if "exit" in txt.lower():
            break
        elif "r" in txt.lower():
            r, c = press_random_cell(mine_map, player_map)
        elif "f" in txt.lower():
            _, txt = txt.split(" ")
            r, c = txt.split(",")
            r, c = [int(r), int(c)]
            plant_flag(r, c, player_map)
        elif "ai" in txt.lower():
            pass
            # 1ro: contar los 88 y 99 alrededor
            # 2do marcar las banderas
            # 3ro presionar celdas
            
            # valor - flags
            #     > 0 => si valor - 88's misma lógica
            #     = 0 => si es que hay 88's, borrarlos,
            #            si no, nada
            #     < 0 => 
        else:
            r, c = txt.split(",")
            r, c = [int(r), int(c)]
            press_cell(r, c, player_map, mine_map)
        
        print_map(player_map)
        
        if player_map[r,c] == MINE_CELL_CHAR:
            print("💣You hit a mine! Try again 😁")
            break
    
    if np.count_nonzero(player_map == COVERED_CELL_CHAR) == 0:
        print("Congratulations! You won 🎉")
    
    
    
    
    
    
    
    




