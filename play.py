from gui import *
from agents.player_agent import PlayerAgent
from agents.sequential_agent import SequentialAgent
from board import Board
from judge import *

from agents.random_agent import RandomAgent

import time


def main():
    board = Board()

    gui = Gui()

    if GUI_ON:
        gui.draw_board()
        gui.update(board)

    # agent_b = PlayerAgent(Player.black)
    agent_b = SequentialAgent(Player.black)
    agent_w = RandomAgent(Player.white)
    board.print_board()
    whosTurn = Player.black
    player_next = whosTurn
    game_state = GameState.game_continue
    count = 0
    while game_state == GameState.game_continue:
        print(Judge.calculate_result(board))
        count += 1
        # time.sleep(0.1)
        if whosTurn == Player.black:
            move = agent_b.choose_move(board)
        else:
            move = agent_w.chooseMove(board)
        # Double insurance that the move is legal
        if not Judge.is_legal_move(board, move, whosTurn):
            continue
        [game_state, player_next] = Judge.next_state(whosTurn, move, board)
        board.update_environment(whosTurn, move)
        if game_state != GameState.game_over and game_state != GameState.surrender:
            board.print_board()
            whosTurn = player_next
            print(whosTurn)
        if GUI_ON:
            gui.update(board)

    if game_state == GameState.surrender:
        print(player_next, "wins!")
    if game_state == GameState.game_over:
        result = Judge.calculate_result(board)
        if result > 0:
            print("black wins")
        elif result < 0:
            print("white wins")
        # not possible for ties

    if GUI_ON:
        time.sleep(1)


if __name__ == "__main__":
    main()
