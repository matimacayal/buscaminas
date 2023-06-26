import numpy as np
import random
import itertools
import time
from minesweeper_ocr import COVERED_CELL_CHAR, FLAG_CELL_CHAR, MINE_CELL_CHAR

class RobotPlayer:
    AI1_KEY = "a1"
    AI2_KEY = "a2"
    RANDOM_KEY = "r"
    EXIT_KEY = "exit"
    FLAG_KEY = "f"
    
    PRESS = "PRESS"
    PLANT_FLAG = "PLANT_FLAG"
        
    def __init__(self, mines_total: int):
        self.game = None
        self.last_move_result = 1 # initial state
        self.last_move = ""
        self.next_moves = []
        self.mines_total = mines_total
    
    def __repr__(self):
        return f"Item()"
    
    def set_mines_total(self, total_mines):
        self.mines_total = total_mines
    
    def remove_duplicate_moves(self):
        movements = self.next_moves
        unique_movements = []
        seen_movements = set()
        
        for movement in movements:
            movement_tuple = (
                movement['movement'],
                tuple(movement['row_col'])
            )
            
            if movement_tuple not in seen_movements:
                seen_movements.add(movement_tuple)
                unique_movements.append(movement)
        return unique_movements
    
    def determine_next_moves(self, player_map: np.ndarray) -> list:
        """
        Determines the next moves to be taken by the robot player based on the current game state.

        Args:
            player_map (np.ndarray): The grid of cells representing the current state of the game.
            mines_to_find (int): The number of mines yet to be found.

        Returns:
            list: A list of next moves to be taken.

        Raises:
            None

        This function analyzes the player_map and mines_to_find to decide the next moves for the robot player.
        It considers the current game state, previous moves, and certain conditions to determine the appropriate move
        algorithm to use. The result of the chosen move algorithm is stored in the last_move_result attribute,
        and the list of next moves is stored in the next_moves attribute.

        Note:
            This function assumes that the robot player runs the entire game continuously, without any human player
            input or interruptions between moves.

        """
        self.next_moves = []
        
        move_algorithm = self._decide_next_logic(player_map)
        if move_algorithm == self.AI1_KEY:
            self.last_move_result = self.ai1_count_press_and_flag(player_map)
        elif move_algorithm == self.AI2_KEY:
            self.last_move_result = self.ai2_2nd_level_counting(player_map)
        elif move_algorithm == self.RANDOM_KEY:
            self.last_move_result = self.press_random_cell(player_map)
        else:
            print("INVALID move_algorithm KEY")
        
        self.next_moves = self.remove_duplicate_moves()
        
        return self.next_moves

    def _decide_next_logic(self, player_map):
        # TODO: vamos a asumir por ahora que el robot corre todo el juego de corrido,
        #       el jugador no hace jugadas entremedio y el robot otras, no es un asistente
        #       por ahora. Ojo que si puede partir desde la mitad de un juego.
        next_move = ""
        if np.count_nonzero(player_map == "0") == 0:
            next_move = "r"
            print(f"next move: {next_move}")
            return next_move
        
        if self.last_move_result > 0:
            next_move = self.AI1_KEY
        elif self.last_move_result == 0:
            if self.last_move == self.AI1_KEY:
                next_move = self.AI2_KEY
            elif self.last_move == self.AI2_KEY:
                next_move = "r"
            else:
                next_move = "r"
        else: # last_move_result < 0
            print("ERROR: last_move_result < 0")
            
        print(f"next move: {next_move}")
        self.last_move = next_move
        return next_move
    
    def ai1_count_press_and_flag(self, player_map):
        # before_covers_n = np.count_nonzero(player_map == COVERED_CELL_CHAR)
        
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
            flags, covers = self._count_neighbour_flags_and_covers(row, col, player_map)
            cell_value = int(player_map[row, col])
            # print("cell_value", cell_value)
            if cell_value == 0 or covers == 0:
                continue
            elif flags == cell_value:
                # empty neighbouring cells
                self._press_neighbour_cells(row, col, player_map)
            elif flags > cell_value:
                print(f"ERROR: sobra una bandera! ({row}, {col})")
            elif flags < cell_value:
                if covers == cell_value - flags:
                    # put flag in neighbour covers
                    self._fill_neighbours_with_flags(row, col, player_map)
                elif covers < cell_value - flags:
                    print("ERROR: number bigger than neighbouring cells, this should not happen")
                elif covers > cell_value - flags:
                    # nada, falta info todavía
                    pass
        
        move_result = len(self.next_moves)
        print("move result =", move_result)
        return move_result
    
    def press_random_cell(self, player_map):
        flags_count = np.count_nonzero(player_map == FLAG_CELL_CHAR)
        # TODO: esto asume que todas las banderas están bien puestas
        # TODO: el núm. total de minas está hardcodeado por ahora
        mines_to_find = self.mines_total - flags_count
        # mines_total = flags_count + mines_to_find
        cell_row, cell_col = [0,0]
        
        if flags_count < self.mines_total * 0.01:
            # to little flags, just random
            print("just random")
            height, width = player_map.shape
            cell_row, cell_col = self._random_duple(height-1, width-1)
            
            # print(f"random: [{cell_row}, {cell_col}]")
            self.next_moves.append({"movement":self.PRESS, "row_col": [cell_row, cell_col]})
            return 1
        
        print("random with probability over covers with number neighbours")
        covered_cells = np.argwhere(player_map == COVERED_CELL_CHAR)
        possible_cells = np.empty((0,2), dtype=int)
        
        flags = np.count_nonzero(player_map == FLAG_CELL_CHAR)
        just_random_cell_probability = mines_to_find / len(covered_cells)
        # print("remaining_mines", remaining_mines)
        # print("len(covered_cells)", len(covered_cells))
        # print("just_random_cell_probability", just_random_cell_probability)
        
        least_probable_cell = [-1,-1]
        least_probability = just_random_cell_probability
        
        for row, col in covered_cells:
            # print(f"checking cell [{row}, {col}]")
            if self._has_min_one_none_covered_neigh(row, col, player_map):
                cell_value = -1
                neighbours_probability = 0
                # checking cell neighbours
                for r in range(row-1, row+2):
                    for c in range(col-1, col+2):
                        if ([r, c] != [row, col]) and (0 <= r < player_map.shape[0]) and (0 <= c < player_map.shape[1]):
                            cell = player_map[r, c]
                            # print(f"checking [{r}, {c}] from [{row}, {col}]")
                            if cell in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                                n_neighbour_flags, n_neighbour_covered = self._count_neighbour_flags_and_covers(r, c, player_map)
                                cell_value = int(cell)                                
                                probability = (cell_value - n_neighbour_flags) / n_neighbour_covered
                                if probability > 1:
                                    print(f"ERROR: probability {probability} > 0")
                                    return
                                if probability > neighbours_probability:
                                    neighbours_probability = probability
                # print("neighbours_probability:", neighbours_probability)
                if cell_value == -1:
                    # => neighbours_probability == 0
                    # no number neighbours
                    # print("cell_value == -1")
                    if least_probability == just_random_cell_probability:
                        # print("least_probability == just_random_cell_probability")
                        least_probable_cell = [row, col]
                else:
                    # print("cell_value != -1")
                    if neighbours_probability <= least_probability:
                        # print("neighbours_probability <= least_probability")
                        least_probability = neighbours_probability
                        least_probable_cell = [row, col]
        
        if least_probable_cell == [-1, -1]:
            # no cell is better than random over all covered cells
            print("no particular cell is better than any random covered cells")
            covered_cells = np.argwhere(player_map == COVERED_CELL_CHAR)
            random_row = np.random.randint(len(covered_cells))
            least_probable_cell = covered_cells[random_row, :]
        
        cell_row, cell_col = least_probable_cell
        print(f"least probability = {least_probability} in cell [{cell_row}, {cell_col}]")
            
        print(f"random: [{cell_row}, {cell_col}]")
        # press_cell(cell_row, cell_col, player_map, mine_map)
        self.next_moves.append({"movement":self.PRESS, "row_col": [cell_row, cell_col]})
        return 1
    
    def ai2_2nd_level_counting(self, player_map):
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
            n_flags, n_covered = self._count_neighbour_flags_and_covers(row, col, player_map)
            cell_value = int(player_map[row, col])
            # print("cell_value", cell_value)
            if cell_value == 0  or n_covered == 0:
                continue
            
            covers_pos = self._get_neighbour_covers_pos(row, col, player_map, n_covered)
            missing_mines = cell_value - n_flags
            
            # checking cell neighbours
            for r in range(row-1, row+2):
                for c in range(col-1, col+2):
                    if ([r, c] != [row, col]) and (0 <= r < player_map.shape[0]) and (0 <= c < player_map.shape[1]):
                        cell = player_map[r, c]
                        if cell in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                            n_neighbour_flags, n_neighbour_covered = self._count_neighbour_flags_and_covers(r, c, player_map)
                            neighbour_covers_pos = self._get_neighbour_covers_pos(r, c, player_map, n_neighbour_covered)
                            neighbour_missing_mines = int(cell) - n_neighbour_flags
                            
                            n_common_covered = self._count_common_items(covers_pos, neighbour_covers_pos)
                            
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

                                                self.next_moves.append({"movement":self.PRESS, "row_col": [rr, cc]})
                                    else: # len(neigh_not_common) == 0
                                        min_not_shared_mines = missing_mines - neighbour_missing_mines
                                        original_not_common = [item for item in covers_pos if item not in neighbour_covers_pos]
                                        if len(original_not_common) == min_not_shared_mines:
                                            for rr, cc in original_not_common:
                                                if player_map[rr, cc] == COVERED_CELL_CHAR:
                                                    # print(f"ai2 flag in [{rr}, {cc}] , from cell [{r}, {c}] neigh of [{row}, {col}]")
                                                    self.next_moves.append({"movement":self.PLANT_FLAG, "row_col": [rr, cc]})
                                            
                                elif min_n_shared_mines < neighbour_missing_mines:
                                    # => nothing can be concluded, for now
                                    #print(f"min_n_shared_mines < neighbour_missing_mines from cell [{r}, {c}], neigh of [{row}, {col}]")
                                    pass
                                else: # min_n_shared_mines > neighbour_missing_mines:
                                    # ERROR
                                    print("ERROR: min_n_shared_mines > neighbour_missing_mines")
        
        # after_covers_n = np.count_nonzero(player_map == COVERED_CELL_CHAR)
        # move_result = before_covers_n - after_covers_n
        
        move_result = len(self.next_moves)
        print("move result =", move_result)
        return move_result 
    
    def _random_duple(self, R1: int, R2: int, N: int = 1):
        duple = random.sample(list(itertools.product(range(R1), range(R2))), N)
        if N == 1:
            return duple[0]
        
        return duple
    
    def _has_min_one_neigh_number(self, cell_row, cell_col, player_map):
        for r in range(cell_row-1, cell_row+2):
            for c in range(cell_col-1, cell_col+2):
                if ([r, c] != [cell_row, cell_col]) and (0 <= r < player_map.shape[0]) and (0 <= c < player_map.shape[1]):
                    if player_map[r, c] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                        return True
        return False

    def _has_min_one_none_covered_neigh(self, cell_row, cell_col, player_map):
        for r in range(cell_row-1, cell_row+2):
            for c in range(cell_col-1, cell_col+2):
                if ([r, c] != [cell_row, cell_col]) and (0 <= r < player_map.shape[0]) and (0 <= c < player_map.shape[1]):
                    if player_map[r, c] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", FLAG_CELL_CHAR]:
                        return True
        return False
    
    def _random_over_covered_cells(self, player_map):
        # random over covered places
        print("random over covers")
        covered_cells = np.argwhere(player_map == COVERED_CELL_CHAR)
        random_row = np.random.randint(len(covered_cells))
        cell_row, cell_col = covered_cells[random_row, :]
    
    def _random_over_covered_with_number_neighs(self, player_map):
        # random over covered cells with number neighours
            covered_cells = np.argwhere(player_map == COVERED_CELL_CHAR)
            possible_cells = np.empty((0,2), dtype=int)
            for r, c in covered_cells:
                # print(f"checking cell [{r}, {c}]")
                if self._has_min_one_neigh_number(r, c, player_map):
                    possible_cells = np.append(possible_cells, [np.array([r,c])], axis=0)
                    # print("added cell")
            # print("possible cells for random:", possible_cells)
            random_row = np.random.randint(len(possible_cells))
            cell_row, cell_col = possible_cells[random_row, :]

    def _count_neighbour_flags_and_covers(self, row, col, player_map):
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
    
    def _count_common_items(self, arr1, arr2):
        set1 = set(map(tuple, arr1))
        set2 = set(map(tuple, arr2))

        common_items = set1.intersection(set2)

        count = len(common_items)
        return count
    
    def _get_neighbour_covers_pos(self, row, col, player_map, n_covers = None):
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

    def _fill_neighbours_with_flags(self, row, col, player_map):
        for r in range(row-1, row+2):
            for c in range(col-1, col+2):
                if ([r, c] != [row, col]) and (0 <= r < player_map.shape[0]) and (0 <= c < player_map.shape[1]):
                    if player_map[r, c] == COVERED_CELL_CHAR:
                        # player_map[r, c] = FLAG_CELL_CHAR
                        self.next_moves.append({"movement":self.PLANT_FLAG, "row_col": [r, c]})

    def _press_neighbour_cells(self, row, col, player_map):
        for r in range(row-1, row+2):
            for c in range(col-1, col+2):
                if ([r, c] != [row, col]) and (0 <= r < player_map.shape[0]) and (0 <= c < player_map.shape[1]):
                    if player_map[r, c] == COVERED_CELL_CHAR:
                        # press_cell(r, c, player_map, mine_map)
                        self.next_moves.append({"movement":self.PRESS, "row_col": [r, c]})
                        



