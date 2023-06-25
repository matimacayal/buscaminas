import minesweeper_ocr as mcr
from game_interface import GameInterface
from robot_player import RobotPlayer
import time

def main():
    game_interface = GameInterface(window_title="Minesweeper X")
    game_interface.initialize()
    robot_player = RobotPlayer(mines_total=200)
    mines_total = robot_player.mines_total
    won = False
    while not won:
        input("enter to continue:")
        img_rgb = game_interface.take_screenshot(display=True, as_rgb_array=True)
        player_map, finished_game = mcr.minesweeper_ocr(img_rgb, mines_total)
        if finished_game: # WIP
            won = True
            print("Won 😁")
            break
        next_moves = robot_player.determine_next_moves(player_map) 
        game_interface.execute(next_moves)

    print("EOS")

def test_ocr():
    start_time = time.time()
    game_interface = GameInterface(window_title="Minesweeper X")
    screenshot = game_interface.take_screenshot(display=False)
    screenshot.save('images/screenshot.png')
    game_image = mcr.img_to_array(screenshot)
    player_map = mcr.minesweeper_ocr(game_image)[0]
    if player_map is None:
        print("couldn't get ocr")
        return
    # print(player_map)
    # mcr.display_array(player_map)
    print(f"took {time.time() - start_time} s")

if __name__ == '__main__':
    # main()
    test_ocr()