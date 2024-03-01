from os import error
import time
from gui import *
from board import Board
import sys


def replay():
    if len(sys.argv) < 2:
        raise error("Game id required")

    gui = Gui()
    board = Board()

    move_records = board.load_game(sys.argv[1])

    gui.draw_board()
    gui.update(board)

    for move in move_records:
        time.sleep(0.1)
        board.update_environment(move[0], move[1])
        gui.draw_board()
        gui.update(board)

    time.sleep(1)

    gui.quit()


if __name__ == "__main__":
    replay()
