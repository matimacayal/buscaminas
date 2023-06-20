import numpy as np
import random
import itertools
import time

class MinesweeperEngine:
    COVERED_CELL_CHAR = "." # "▫" # "▪" # "■" # "☐"
    FLAG_CELL_CHAR = "●" #"⬤" # "¤" # "◘" #"█" # "•" # "¤"
    MINE_CELL_CHAR = "*" # "*"
    
    level = {
        1: "easy",
        2: "medium",
        3: "hard",
        4: "challenge",
        5: "impossible",
    }
    
    map_config = {
        "easy": [8, 8, 10],         # 15.625% of cells are a mine
        "medium": [16, 16, 40],     # 15.625%
        "hard": [16, 30, 99],       # 20.625%
        "challenge": [24, 30, 200], # 27.78%
        "impossible": [48, 60, 800] # 27.78%
    }
    
    def __init__(self, map_height: int, map_width: int, mines: int):
        # TODO: check if we want to automatically create the map here or in another function by the user.
        self.width = map_width
        self.height = map_height
        self.mines_total = mines
        self.map_array = self.build_minesweeper_map(self.height, self.width, self.mines_total)
    
    @classmethod
    def create_by_difficulty(cls, difficulty):
        # TODO: add a default configuration for minesweeper
        if type(difficulty) is int:
            if difficulty not in cls.level.keys():
                print("Please enter a level between 1 to 5 or the difficulty")
            difficulty = cls.level[difficulty]
        elif type(difficulty) is not str:
            print("Please enter a valid argument type (int or str)")
        
        if difficulty not in cls.map_config.keys():
            print("Please enter a valid difficulty (easy, medium, hard, challenge, impossible)")
        
        h, w, mines = cls.map_config[difficulty]
        
        return cls(map_height=h, map_width=w, mines=mines)
    
    def __repr__(self):
        return (f"MinesweeperGame("
                "height: {self.height}, "
                "width: {self.height}, "
                "mines_total: {self.mines_total})")
    
    # function that given a coordinate can iterate over theit's neighbours and count mines
    def _count_bombs(self, row: int, col: int, mines_map: np.ndarray) -> int:
        sum = 0
        for r in range(row-1, row+2):
            for c in range(col-1, col+2):
                if ([r, c] != [row, col]) and (0 <= r < mines_map.shape[0]) and (0 <= c < mines_map.shape[1]):
                    if mines_map[r, c] == -1:
                        sum += 1
        return sum

    def _random_duple(self, R1: int, R2: int, N: int = 1) -> list:
        duple = random.sample(list(itertools.product(range(R1), range(R2))), N)
        if N == 1:
            return duple[0]
        
        return duple

    def build_minesweeper_map(self, map_height: int, map_width: int, total_mines: int) -> np.ndarray:
        arr = np.zeros((map_height, map_width))
        
        # randomly distribute 10 mines in the 64 blocks array
        mine_coordinates = self._random_duple(map_height, map_width, N = total_mines)
        for mine in mine_coordinates:
            arr[mine] = -1
            
        for row, _ in enumerate(arr):
            for col, value in enumerate(_):
                if value != -1:
                    sum = self._count_bombs(row, col, arr)
                    arr[row,col] = sum
        return arr

    def _press_neighbours(self, cell_row: int, cell_col: int, player_map: np.ndarray, mine_map: np.ndarray) -> None:
        for r in range(cell_row-1, cell_row+2):
            for c in range(cell_col-1, cell_col+2):
                if ([r, c] != [cell_row, cell_col]) and (0 <= r < player_map.shape[0]) and (0 <= c < player_map.shape[1]):
                    # acá la lógica es que cuando una celda es 0 primero se descubre,
                    # luego se revisan las vecinas, entonces para no entrar en loop para
                    # presionar una celda vecina este debe estar cubierta
                    if mine_map[r, c] == 0 and player_map[r, c] == self.COVERED_CELL_CHAR:
                        # print(f"pressing cell: {[r,c]}")
                        self.press_cell_action(r, c, player_map, mine_map)
                    player_map[r, c] = str(mine_map[r, c])
    
    def _fill_neighbour_with(self, cell_row: int, cell_col: int, player_map: np.ndarray, character: str) -> None:
        for r in range(cell_row-1, cell_row+2):
            for c in range(cell_col-1, cell_col+2):
                if ([r, c] != [cell_row, cell_col]) and (0 <= r < player_map.shape[0]) and (0 <= c < player_map.shape[1]):
                    # acá la lógica es que cuando una celda es 0 primero se descubre,
                    # luego se revisan las vecinas, entonces para no entrar en loop para
                    # presionar una celda vecina este debe estar cubierta
                    player_map[r, c] = character
    
    def _add_coordinates(self, array: np.ndarray) -> np.ndarray:
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
    
    def press_cell_action(self, cell_row: int, cell_col: int, player_map: np.ndarray, mine_map: np.ndarray) -> None:
        assert 0 <= cell_row < self.height, "Row value out of minesweeper map bounds"
        assert 0 <= cell_col < self.width, "Column value out of minesweeper map bounds"
        
        if player_map[cell_row, cell_col] == self.FLAG_CELL_CHAR:
            print("Can't press flagged mine")
            return
        
        cell_value = mine_map[cell_row, cell_col]
        if cell_value == -1:
            print(f"Mine. Lost game. ({cell_row}, {cell_col})")
            player_map[cell_row, cell_col] = self.MINE_CELL_CHAR
            # player_map[:] = MINE_CELL_CHAR
            self._fill_neighbour_with(cell_row, cell_col, player_map, self.MINE_CELL_CHAR)
            return
        elif cell_value == 0:
            # print(f"({cell_row},{cell_col}) cell empty, clearing neighbouring cells")
            player_map[cell_row, cell_col] = "0"
            self._press_neighbours(cell_row, cell_col, player_map, mine_map)
        else:
            # print(f"cell_value = {cell_value}")
            player_map[cell_row, cell_col] = str(cell_value)
    
    def plant_flag_action(self, cell_row: int, cell_col: int, player_map: np.ndarray) -> None:
        # TODO: Implement total flags planted
        assert 0 <= cell_row < self.height, "Row value out of minesweeper map bounds"
        assert 0 <= cell_col < self.width, "Column value out of minesweeper map bounds"
        
        current_value = player_map[cell_row, cell_col]
        if current_value == self.COVERED_CELL_CHAR:
            player_map[cell_row, cell_col] = self.FLAG_CELL_CHAR
        elif current_value == self.FLAG_CELL_CHAR:
            player_map[cell_row, cell_col] = self.COVERED_CELL_CHAR
        else:
            print("Can't flag pressed mine")

    def print_map(self, player_map: np.ndarray) -> None:
        map_cli = self._add_coordinates(player_map)
        
        for row in map_cli:
            print(' '.join(row))
            










class MinesweeperCliGame:
        
    def main():
        width = MAP_WIDTH
        height = MAP_HEIGHT
        mines = TOTAL_MINES
        # width = 78
        # height = 49
        # mines = 800
        
        # total_covers = width * height
        total_flags = 0
        next_move = ""
        move_result = 0 # TODO: implement a better way of calcuating each move_result
        
        tries = 0
        start_time = time.time()
        
        np.set_printoptions(linewidth=150)
        while 1:
            mine_map = build_minesweeper_map(height, width, mines)
            player_map = np.full((height, width), COVERED_CELL_CHAR, dtype=str)
            tries += 1
            
            print_map(player_map)
            
            # Conditions to win
            # - all flags planted
            # - no mines pressed/displayed
            # - all covers presses (zero displayed)
            # while np.count_nonzero(player_map == COVERED_CELL_CHAR) != 0 or MINE_CELL_CHAR in player_map or np.count_nonzero(player_map == FLAG_CELL_CHAR) != TOTAL_MINES:
            while (
                np.count_nonzero(player_map == COVERED_CELL_CHAR) != 0
                or MINE_CELL_CHAR in player_map
                or np.count_nonzero(player_map == FLAG_CELL_CHAR) != TOTAL_MINES
            ):
                txt = "" # input("input:")
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
        
            if (
                np.count_nonzero(player_map == COVERED_CELL_CHAR) == 0
                and MINE_CELL_CHAR not in player_map
                and np.count_nonzero(player_map == FLAG_CELL_CHAR) == TOTAL_MINES
            ):
                total_time = time.time() - start_time
                print("Congratulations! You won 🎉")
                print(f"Grid size [{MAP_WIDTH}, {MAP_HEIGHT}] with {TOTAL_MINES} mines")
                print(f"It took {tries} tries")
                print(f"and {total_time // 60} minutes and {total_time % 60} seconds")
                break
        
        
        
        
        
        
        
        




