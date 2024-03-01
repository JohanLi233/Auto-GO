from gui import *
from agents.player_agent import PlayerAgent
from agents.sequential_agent import SequentialAgent
from agents.random_agent import RandomAgent
from agents.random_policy_agent import RandomPolicyAgent
from agents.monte_carlo_agent import MonteCarloAgent

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
        # agent_b = SequentialAgent(Player.black)
        # agent_b = RandomPolicyAgent(Player.black)
        agent_b = MonteCarloAgent(Player.black)
        # agent_b = RandomAgent(Player.black)

        # agent_w = PlayerAgent(Player.white)
        # agent_w = SequentialAgent(Player.white)
        agent_w = RandomPolicyAgent(Player.white)
        # agent_w = RandomAgent(Player.white)

        if PRINT_BOARD:
            board.print_board()
        whosTurn = Player.black
        player_next = whosTurn
        game_state = GameState.game_continue
        while game_state == GameState.game_continue:
            # print(Judge.calculate_result(board))
            if whosTurn == Player.black:
                move = agent_b.choose_move(board)
            else:
                move = agent_w.choose_move(board)

            # insure that the move is legal
            if not Judge.is_legal_move(board, move, whosTurn):
                continue

            game_state, player_next = Judge.next_state(whosTurn, move, board)
            board.update_board(whosTurn, move)
            if (
                game_state != GameState.gameover
                and game_state != GameState.surrender
                and game_state != GameState.white_win
                and game_state != GameState.black_win
            ):
                whosTurn = player_next
                if PRINT_BOARD:
                    board.print_board()
                    print(whosTurn)

            if GUI_ON:
                gui.update(board)

        who_wins = Judge.get_result(board, player_next, game_state)
        if who_wins == Player.black:
            black_win_count += 1
            board.move_records.append(Player.black)
            print("Black wins")
        else:
            board.move_records.append(Player.white)
            print("White wins")

        if GUI_ON:
            time.sleep(1)
            gui.quit()

        if STORE_GAME:
            board.store_game()

        print("black win rate: " + str((black_win_count / (i + 1))))


if __name__ == "__main__":
    main()
