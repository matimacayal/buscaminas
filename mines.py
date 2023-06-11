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
                    # print(f"pressing cell: {[r,c]}")
                    press_cell(r, c, player_map, mine_map)
                player_map[r, c] = str(mine_map[r, c])

def fill_neighbour_cells(cell_row, cell_col, player_map):
    for r in range(cell_row-1, cell_row+2):
        for c in range(cell_col-1, cell_col+2):
            if ([r, c] != [cell_row, cell_col]) and (0 <= r < player_map.shape[0]) and (0 <= c < player_map.shape[1]):
                # acá la lógica es que cuando una celda es 0 primero se descubre,
                # luego se revisan las vecinas, entonces para no entrar en loop para
                # presionar una celda vecina este debe estar cubierta
                player_map[r, c] = MINE_CELL_CHAR

def press_cell(cell_row, cell_col, player_map, mine_map):
    if player_map[cell_row, cell_col] == FLAG_CELL_CHAR:
        print("Can't press flagged mine")
        return
    
    cell_value = mine_map[cell_row, cell_col]
    if cell_value == -1:
        print(f"Mine. Lost game. ({cell_row}, {cell_col})")
        player_map[cell_row, cell_col] = MINE_CELL_CHAR
        # player_map[:] = MINE_CELL_CHAR
        fill_neighbour_cells(cell_row, cell_col, player_map)
        return
    elif cell_value == 0:
        # print(f"({cell_row},{cell_col}) cell empty, clearing neighbouring cells")
        player_map[cell_row, cell_col] = "0"
        clear_neighbour_cells(cell_row, cell_col, player_map, mine_map)
    else:
        # print(f"cell_value = {cell_value}")
        player_map[cell_row, cell_col] = str(cell_value)

def has_min_one_neigh_number(cell_row, cell_col, player_map):
    for r in range(cell_row-1, cell_row+2):
        for c in range(cell_col-1, cell_col+2):
            if ([r, c] != [cell_row, cell_col]) and (0 <= r < player_map.shape[0]) and (0 <= c < player_map.shape[1]):
                if player_map[r, c] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    return True
    return False

def has_min__one_none_covered_neigh(cell_row, cell_col, player_map):
    for r in range(cell_row-1, cell_row+2):
        for c in range(cell_col-1, cell_col+2):
            if ([r, c] != [cell_row, cell_col]) and (0 <= r < player_map.shape[0]) and (0 <= c < player_map.shape[1]):
                if player_map[r, c] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", FLAG_CELL_CHAR]:
                    return True
    return False

def press_random_cell(mine_map, player_map):
    flags_n = np.count_nonzero(player_map == FLAG_CELL_CHAR)
    mines_n = np.count_nonzero(mine_map == -1)
    cell_row, cell_col = [0,0]
    
    if flags_n < mines_n * 0.01:
        # to little flags, just random
        print("just random")
        height, width = player_map.shape
        cell_row, cell_col = random_duple(height-1, width-1)
    # elif flags_n < mines_n * 0.5:
    #     # random over covered places
    #     print("random over covers")
    #     covered_cells = np.argwhere(player_map == COVERED_CELL_CHAR)
    #     random_row = np.random.randint(len(covered_cells))
    #     cell_row, cell_col = covered_cells[random_row, :]
    # else:
    #     # random over covered cells with number neighours
    #     covered_cells = np.argwhere(player_map == COVERED_CELL_CHAR)
    #     possible_cells = np.empty((0,2), dtype=int)
    #     for r, c in covered_cells:
    #         # print(f"checking cell [{r}, {c}]")
    #         if has_min_one_neigh_number(r, c, player_map):
    #             possible_cells = np.append(possible_cells, [np.array([r,c])], axis=0)
    #             # print("added cell")
    #     # print("possible cells for random:", possible_cells)
    #     random_row = np.random.randint(len(possible_cells))
    #     cell_row, cell_col = possible_cells[random_row, :]
    else:
        print("random with probability over covers with number neighbours")
        covered_cells = np.argwhere(player_map == COVERED_CELL_CHAR)
        possible_cells = np.empty((0,2), dtype=int)
        
        flags = np.count_nonzero(player_map == FLAG_CELL_CHAR)
        remaining_mines = TOTAL_MINES - flags
        just_random_cell_probability = remaining_mines / len(covered_cells)
        print("remaining_mines", remaining_mines)
        print("len(covered_cells)", len(covered_cells))
        print("just_random_cell_probability", just_random_cell_probability)
        
        least_probable_cell = [-1,-1]
        least_probability = just_random_cell_probability
        
        for row, col in covered_cells:
            print(f"checking cell [{row}, {col}]")
            if has_min__one_none_covered_neigh(row, col, player_map):
                cell_value = -1
                neighbours_probability = 0
                # checking cell neighbours
                for r in range(row-1, row+2):
                    for c in range(col-1, col+2):
                        if ([r, c] != [row, col]) and (0 <= r < player_map.shape[0]) and (0 <= c < player_map.shape[1]):
                            cell = player_map[r, c]
                            print(f"checking [{r}, {c}] from [{row}, {col}]")
                            if cell in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                                n_neighbour_flags, n_neighbour_covered = count_neighbour_flags_and_covers(r, c, player_map)
                                cell_value = int(cell)                                
                                probability = (cell_value - n_neighbour_flags) / n_neighbour_covered
                                if probability > 1:
                                    print(f"ERROR: probability {probability} > 0")
                                    return
                                if probability > neighbours_probability:
                                    neighbours_probability = probability
                print("neighbours_probability:", neighbours_probability)
                if cell_value == -1:
                    # => neighbours_probability == 0
                    # no number neighbours
                    print("cell_value == -1")
                    if least_probability == just_random_cell_probability:
                        print("least_probability == just_random_cell_probability")
                        least_probable_cell = [row, col]
                else:
                    print("cell_value != -1")
                    if neighbours_probability <= least_probability:
                        print("neighbours_probability <= least_probability")
                        least_probability = neighbours_probability
                        least_probable_cell = [row, col]
        
        if least_probable_cell == [-1, -1]:
            # no cell is better than random over all covered cells
            print("no cell is better than random over all covered cells")
            covered_cells = np.argwhere(player_map == COVERED_CELL_CHAR)
            random_row = np.random.randint(len(covered_cells))
            least_probable_cell = covered_cells[random_row, :]
        
        cell_row, cell_col = least_probable_cell
        print(f"least probability = {least_probability} in cell [{cell_row}, {cell_col}]")
        
    print(f"random: [{cell_row}, {cell_col}]")
    press_cell(cell_row, cell_col, player_map, mine_map)
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

def press_neighbour_cells(row, col, player_map, mine_map):
    for r in range(row-1, row+2):
        for c in range(col-1, col+2):
            if ([r, c] != [row, col]) and (0 <= r < player_map.shape[0]) and (0 <= c < player_map.shape[1]):
                if player_map[r, c] == COVERED_CELL_CHAR:
                    press_cell(r, c, player_map, mine_map)

def ai_count_press_and_flag(player_map, mine_map):
    before_covers_n = np.count_nonzero(player_map == COVERED_CELL_CHAR)
    
    # non_empty_cells = np.argwhere(player_map != '.')
    non_empty_cells = np.argwhere(
        np.logical_and(
            player_map != FLAG_CELL_CHAR,
            player_map != COVERED_CELL_CHAR
            )
        )
    # print(non_empty_cells)
    for row, col in non_empty_cells:
        # print("checking ", row, col)
        flags, covers = count_neighbour_flags_and_covers(row, col, player_map)
        # Se está cayendo en esta línea porque apreta una mina,
        # los vecinos se ponen "*" y luego esto aprieta un vecino
        # y se cae al hacer int("*")
        # Entonces hay que resolver 2 cosas:
        # 1. que cuando hay bomba termine el juego
        # 2. si se apreto una bomba hay algo no funcionando bien, identificar y resolver
        cell_value = int(player_map[row, col])
        # print("cell_value", cell_value)
        if cell_value == 0 or covers == 0:
            continue
        elif flags == cell_value:
            # empty neighbouring cells
            press_neighbour_cells(row, col, player_map, mine_map)
            pass
        elif flags > cell_value:
            print(f"ERROR: sobra una bandera! ({row}, {col})")
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
    
    after_covers_n = np.count_nonzero(player_map == COVERED_CELL_CHAR)
    move_result = before_covers_n - after_covers_n
    print("move result =", move_result)
    return move_result


def get_neighbour_covers_pos(row, col, player_map, n_covers = None):
    # TODO: optimize this function, np.argwhere or other might be used to get coordinates
    #       maybe a 3x3 mask centered in row, col to make any other values false and
    #       use the np.argwhere for player_map == COVERED_CELL_CHAR
    coordinates = []
    for r in range(row-1, row+2):
        for c in range(col-1, col+2):
            if ([r, c] != [row, col]) and (0 <= r < player_map.shape[0]) and (0 <= c < player_map.shape[1]):
                cell = player_map[r, c]
                if cell == COVERED_CELL_CHAR:
                    coordinates.append([r,c])
    if n_covers and len(coordinates) != n_covers:
        print("ERROR")
    return coordinates

def count_common_items(arr1, arr2):
    set1 = set(map(tuple, arr1))
    set2 = set(map(tuple, arr2))

    common_items = set1.intersection(set2)

    count = len(common_items)
    return count

def ai2_2nd_level_counting(player_map, mine_map):
    before_covers_n = np.count_nonzero(player_map == COVERED_CELL_CHAR)
    
    # TODO: Modularize, rename variables and simplify this logic when possible
    non_empty_cells = np.argwhere(
        np.logical_and(
            player_map != FLAG_CELL_CHAR,
            player_map != COVERED_CELL_CHAR
            )
        )
    for row, col in non_empty_cells:
        # print("checking ", row, col)
        n_flags, n_covered = count_neighbour_flags_and_covers(row, col, player_map)
        cell_value = int(player_map[row, col])
        # print("cell_value", cell_value)
        if cell_value == 0  or n_covered == 0:
            continue
        
        covers_pos = get_neighbour_covers_pos(row, col, player_map, n_covered)
        missing_mines = cell_value - n_flags # n_covered - (cell_value - n_flags)
        
        # checking cell neighbours
        for r in range(row-1, row+2):
            for c in range(col-1, col+2):
                if ([r, c] != [row, col]) and (0 <= r < player_map.shape[0]) and (0 <= c < player_map.shape[1]):
                    cell = player_map[r, c]
                    if cell in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                        n_neighbour_flags, n_neighbour_covered = count_neighbour_flags_and_covers(r, c, player_map)
                        neighbour_covers_pos = get_neighbour_covers_pos(r, c, player_map, n_neighbour_covered)
                        neighbour_missing_mines = int(cell) - n_neighbour_flags # n_neighbour_covered - (int(cell) - n_neighbour_flags)
                        
                        n_common_covered = count_common_items(covers_pos, neighbour_covers_pos)
                        
                        non_common_covered = n_covered - n_common_covered
                        min_n_shared_mines = missing_mines - non_common_covered
                        if min_n_shared_mines > 0:
                            # => min_n_shared_mines number of mines in common covers
                            if  min_n_shared_mines == neighbour_missing_mines:
                                # => neighbour_non_common_covered has 0 mines
                                neigh_not_common = [item for item in neighbour_covers_pos if item not in covers_pos]
                                
                                if len(neigh_not_common) > 0:
                                    for rr, cc in neigh_not_common:
                                        if player_map[rr, cc] == COVERED_CELL_CHAR:
                                            # print(f"ai2 pressing [{rr}, {cc}] , from cell [{r}, {c}] neigh of [{row}, {col}]")
                                            press_cell(rr, cc, player_map, mine_map)
                                else: # len(neigh_not_common) == 0
                                    min_not_shared_mines = missing_mines - neighbour_missing_mines
                                    original_not_common = [item for item in covers_pos if item not in neighbour_covers_pos]
                                    if len(original_not_common) == min_not_shared_mines:
                                        for rr, cc in original_not_common:
                                            if player_map[rr, cc] == COVERED_CELL_CHAR:
                                                # print(f"ai2 flag in [{rr}, {cc}] , from cell [{r}, {c}] neigh of [{row}, {col}]")
                                                plant_flag(rr, cc, player_map)
                                        
                            elif min_n_shared_mines < neighbour_missing_mines:
                                # => nothing can be concluded, for now
                                #print(f"min_n_shared_mines < neighbour_missing_mines from cell [{r}, {c}], neigh of [{row}, {col}]")
                                pass
                            else: # min_n_shared_mines > neighbour_missing_mines:
                                # ERROR
                                print("ERROR: min_n_shared_mines > neighbour_missing_mines")
    
    after_covers_n = np.count_nonzero(player_map == COVERED_CELL_CHAR)
    move_result = before_covers_n - after_covers_n
    print("move result =", move_result)
    return move_result

def get_next_move(last_move, last_move_result, player_map):
    next_move = ""
    if np.count_nonzero(player_map == "0") == 0:
        next_move = "r"
        print(f"next move: {next_move}")
        return next_move
    
    if last_move_result > 0:
        next_move = AI1_KEY
    elif last_move_result == 0:
        if last_move == AI1_KEY:
            next_move = AI2_KEY
        elif last_move == AI2_KEY:
            next_move = "r"
        else:
            next_move = "r"
    else: # last_move_result < 0
        print("ERROR: last_move_result < 0")
        
    print(f"next move: {next_move}")
    return next_move
        

COVERED_CELL_CHAR = "." # "▫" # "▪" # "■" # "☐"
FLAG_CELL_CHAR = "●" #"⬤" # "¤" # "◘" #"█" # "•" # "¤"
MINE_CELL_CHAR = "*" # "*"

AI1_KEY = "a1"
AI2_KEY = "a2"
RANDOM_KEY = "r"
EXIT_KEY = "exit"
FLAG_KEY = "f"

MAP_WIDTH = 30
MAP_HEIGHT = 24
TOTAL_MINES = 150

if __name__ == '__main__':
    width = MAP_WIDTH
    height = MAP_HEIGHT
    mines = TOTAL_MINES
    # width = 78
    # height = 49
    # mines = 800
    
    # total_covers = width * height
    total_flags = 0
    next_move = ""
    move_result = 0
    # TODO: implement a better way of calcuating each move_result
    
    np.set_printoptions(linewidth=150)
    while 1:
        mine_map = build_minesweeper_map(height, width, mines)
        player_map = np.full((height, width), COVERED_CELL_CHAR, dtype=str)
        
        print_map(player_map)
            
        while np.count_nonzero(player_map == COVERED_CELL_CHAR) != 0:
            txt = input("input:")
            if not txt:
                previous_move = next_move
                next_move = get_next_move(previous_move, move_result, player_map)
            else:
                next_move = txt
            
            if EXIT_KEY in next_move.lower():
                break
            elif RANDOM_KEY in next_move.lower():
                r, c = press_random_cell(mine_map, player_map)
                move_result += 1
            elif FLAG_KEY in next_move.lower():
                _, next_move = next_move.split(" ")
                r, c = next_move.split(",")
                r, c = [int(r), int(c)]
                plant_flag(r, c, player_map)
            elif AI1_KEY in next_move.lower():
                move_result = ai_count_press_and_flag(player_map, mine_map)
            elif AI2_KEY in next_move.lower():
                move_result = ai2_2nd_level_counting(player_map, mine_map)
            else:
                try:
                    r, c = next_move.split(",")
                    r, c = [int(r), int(c)]
                    press_cell(r, c, player_map, mine_map)
                except ValueError as err:
                    print("Error:", err)
                except:
                    print("Input error, try again:")
                                
            print_map(player_map)
            
            if player_map[r,c] == MINE_CELL_CHAR:
                print("💣You hit a mine! Try again 😁")
                break
    
        if np.count_nonzero(player_map == COVERED_CELL_CHAR) == 0:
            print("Congratulations! You won 🎉")
            break
    
    
    
    
    
    
    
    




