from gui import *
from agents.player_agent import PlayerAgent
from agents.sequential_agent import SequentialAgent
from agents.random_agent import RandomAgent

from board import Board
from judge import *

import time


def main():
    black_win_count = 0
    for i in range(STIMULATE_STPES):
        board = Board()
        gui = Gui()

        if GUI_ON:
            gui.draw_board()
            gui.update(board)

        # agent_b = PlayerAgent(Player.black)
        agent_b = SequentialAgent(Player.black)
        # agent_b = RandomAgent(Player.black)
        agent_w = RandomAgent(Player.white)
        if PRINT_BOARD:
            board.print_board()
        whosTurn = Player.black
        player_next = whosTurn
        game_state = GameState.game_continue
        while game_state == GameState.game_continue:
            print(Judge.calculate_result(board))
            # time.sleep(0.1)
            if whosTurn == Player.black:
                move = agent_b.choose_move(board)
            else:
                move = agent_w.choose_move(board)

            # insure that the move is legal
            if not Judge.is_legal_move(board, move, whosTurn):
                continue

            game_state, player_next = Judge.next_state(whosTurn, move, board)
            board.update_environment(whosTurn, move)
            if (
                game_state != GameState.game_over
                and game_state != GameState.surrender
                and GameState != GameState.white_win
                and GameState != GameState.black_win
            ):
                if PRINT_BOARD:
                    board.print_board()
                whosTurn = player_next
                print(whosTurn)

            if GUI_ON:
                gui.update(board)

        if game_state == GameState.surrender:
            print(player_next, "wins")
            if player_next == Player.black:
                black_win_count += 1
        if game_state == GameState.game_over:
            result = Judge.calculate_result(board)
            if result > 0:
                black_win_count += 1
                print("black wins")
            elif result < 0:
                print("white wins")
            # not possible for ties
        if game_state == GameState.black_win:
            black_win_count += 1
            print("black wins")

        if game_state == GameState.white_win:
            print("white wins")

        if GUI_ON:
            time.sleep(1)
            gui.quit()

        print("black win rate: " + str((black_win_count / (i + 1))))


if __name__ == "__main__":
    main()
