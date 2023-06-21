import minesweeper_ocr as mcr
from game_interface import GameInterface
from robot_player import RobotPlayer

game_interface = GameInterface("Minesweeper X")
game_interface.initialize()
robot_player = RobotPlayer()
mines_total = robot_player.mines_total
won = False
while not won:
    img_rgb = game_interface.take_screenshot()
    img_arr = mcr.img_to_array(img_rgb)
    player_map, finished_game = mcr.minesweeper_ocr(img_arr, mines_total)
    if finished_game: # WIP
        won = True
        break
    next_moves = robot_player.determine_next_moves(player_map) 
    game_interface.execute(next_moves)

# TODO: WIP
# [X] game_interface.finished_game
# [X] get mines_left from screenshot and pass it to robot
# [O] game_interface.execute()

# TODO: refactor name of functions between mcr and game_interface to make clearer the types of img formats
#       cv2.mat or Image (i'm almost sure cv2.mat is a np.ndarray)