import minesweeper_ocr as mcr
from game_interface import GameInterface
from robot_player import RobotPlayer

game_interface = GameInterface("Minesweeper X")
game_interface.initialize()
robot_player = RobotPlayer()
won = False
while not won:
    img_rgb = game_interface.take_screenshot()
    player_map = mcr.image_to_arr(img_rgb)
    if game_interface.finished_game(player_map): # WIP
        won = True
        break
    next_moves = robot_player.determine_next_moves(player_map) 
    game_interface.execute(next_moves)

# TODO: WIP
# game_interface.finished_game
# get mines_left from screenshot and pass it to robot
# game_interface.execute()

# TODO: refactor name of functions between mcr and game_interface to make clearer the types of img formats
#       cv2.mat or Image (i'm almost sure cv2.mat is a np.ndarray)