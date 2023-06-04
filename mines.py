import numpy as np
import random
import itertools

# function that given a coordinate can iterate over theit's neighbours and count mines
def count_bombs(row, col, mines_map):
    sum = 0
    for r in range(row-1, row+2):
        for c in range(col-1, col+2):
            if ([r, c] != [row, col]) and (0 <= r < mines_map.shape[0]) and (0 <= c < mines_map.shape[1]):
                if mines_map[r, c] == -1:
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
                # acá la lógica es que cuando una celda es 0 primero se descubre,
                # luego se revisan las vecinas, entonces para no entrar en loop para
                # presionar una celda vecina este debe estar cubierta
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
        
def add_coordinates(array):
    num_rows, num_cols = array.shape

    # Create index arrays for the first row and column
    row_indexes = (np.arange(num_rows) % 10).reshape(-1, 1)
    col_indexes = (np.arange(num_cols) % 10).reshape(1, -1)

    # Create an empty array with the desired shape
    new_array = np.full((num_rows + 1, num_cols + 1), "0", dtype=str)

    # Assign the index values to the first row and column
    new_array[0, 1:] = col_indexes[0, :]
    new_array[1:, 0] = row_indexes[:, 0]

    # Assign the original array values to the remaining cells
    new_array[1:, 1:] = array
    
    return new_array

def print_map(player_map):
    print_map = add_coordinates(player_map)
    
    for row in print_map:
            print(' '.join(row))

# ai player
def count_neighbour_flags_and_covers(row, col, player_map):
    flags = 0
    covers = 0
    for r in range(row-1, row+2):
        for c in range(col-1, col+2):
            if ([r, c] != [row, col]) and (0 <= r < player_map.shape[0]) and (0 <= c < player_map.shape[1]):
                cell = player_map[r, c]
                if cell == FLAG_CELL_CHAR:
                    flags += 1
                elif cell == COVERED_CELL_CHAR:
                    covers += 1
    return flags, covers

def fill_neighbours_with_flags(row, col, player_map):
    # TODO: check if 
    for r in range(row-1, row+2):
        for c in range(col-1, col+2):
            if ([r, c] != [row, col]) and (0 <= r < player_map.shape[0]) and (0 <= c < player_map.shape[1]):
                if player_map[r, c] == COVERED_CELL_CHAR:
                    player_map[r, c] = FLAG_CELL_CHAR

def ai_mark_flags(player_map):
    # non_empty_cells = np.argwhere(player_map != '.')
    non_empty_cells = np.argwhere(np.logical_and(player_map != FLAG_CELL_CHAR, player_map != COVERED_CELL_CHAR))
    print(non_empty_cells)
    for row, col in non_empty_cells:
        print("checking ", row, col)
        flags, covers = count_neighbour_flags_and_covers(row, col, player_map)
        cell_value = int(player_map[row, col])
        print("cell_value", cell_value)
        if cell_value == 0:
            continue
        elif flags == cell_value:
            # empty neighbouring cells
            pass
        elif flags > cell_value:
            print("ERROR: sobra una bandera!")
        elif flags < cell_value:
            if covers == cell_value - flags:
                # put flag in neighbour covers
                fill_neighbours_with_flags(row, col, player_map)
                pass
            elif covers < cell_value - flags:
                print("ERROR: number bigger than neighbouring cells, this should not happen")
                pass
            elif covers > cell_value - flags:
                # nada, falta info todavía
                pass
    

COVERED_CELL_CHAR = "."
FLAG_CELL_CHAR = "■" # "◘" #"█" # "•" # "¤"
MINE_CELL_CHAR = "X" # "*"

if __name__ == '__main__':
    width = 30
    height = 24
    mines = 100
    
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
            # 1ro: contar los 88 y 99 alrededor
            # 2do marcar las banderas
            # 3ro presionar celdas
            
            # valor - flags
            #     > 0 => si valor - 88's misma lógica
            #     = 0 => si es que hay 88's, borrarlos,
            #            si no, nada
            #     < 0 => 
            ai_mark_flags(player_map)
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
    
    
    
    
    
    
    
    




