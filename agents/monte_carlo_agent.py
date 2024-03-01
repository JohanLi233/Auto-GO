from agents.agent import Agent
from judge import Judge, GameState
from utilities import *
from settings import MONTE_CARLO_STEPS, PASS_STONE, MONTE_CARLO_TIME_LIMIT
from .random_agent import RandomAgent


import time
import copy
import numpy as np
import random
import sys


class MonteCarloAgent(Agent):
    """An agent that plays using monte carlo strategy"""

    def __init__(self, player):
        super().__init__(player)
        seed = random.randrange(sys.maxsize)
        self.rng = random.Random(seed)

    def choose_move(self, board):
        mc = MonteCarlo(board, self.player, MONTE_CARLO_TIME_LIMIT)
        mc_result = None

        mc.simulate()
        mc_result = mc.get_result()

        if mc_result == {-1: PASS_STONE}:
            return PASS_STONE

        moves, win_rate, advantage = zip(
            *[
                (
                    move,
                    result[0] / result[1] if result[1] != 0 else 0,
                    result[2],
                )  # o for win_rate if no games completed
                for move, result in mc_result.items()
            ]
        )

        idx = np.argmax(advantage + win_rate)

        move = moves[idx]
        if Judge.is_legal_move(board, move, self.player):
            return tuple(move)
        else:
            return PASS_STONE


class MonteCarlo:

    def __init__(self, board, player, time_limit):
        self.board = board
        self.agent_player = RandomAgent(player)
        self.agent_op = RandomAgent(player.other())
        self.result = {}  # {(0,0):(num_win, num_games_comopleted, advantage)}
        self.player = player
        self.time_limit = time_limit
        self.should_pass = False

    def simulate(self):
        self.should_pass = True
        start_time = time.time()
        num = 0
        while time.time() - start_time < self.time_limit:  # loop until time limit
            num += 1
            # print(str(num) + " simulation")

            self.simulate_round()

            if self.should_pass:
                self.result[-1] = PASS_STONE

    def simulate_round(self):
        vacancies = self.board.find_vacancy()
        random.shuffle(vacancies)

        for i in vacancies:
            new_board = copy.deepcopy(self.board)
            whos_turn = self.player
            who_win = 0

            if not Judge.is_legal_move(new_board, i, self.player):
                continue

            self.should_pass = False

            game_state, player_next = Judge.next_state(whos_turn, i, new_board)
            new_board.update_board(whos_turn, i)

            whos_turn = player_next

            vacancy = new_board.find_vacancy()
            random.shuffle(vacancy)
            vacancy_len = len(vacancy) - 1

            for _ in range(min(vacancy_len, MONTE_CARLO_STEPS)):
                if whos_turn == Player.black:
                    move = self.agent_player.choose_move(new_board)
                else:
                    move = self.agent_op.choose_move(new_board)

                game_state, player_next = Judge.next_state(whos_turn, move, new_board)
                new_board.update_board(whos_turn, move)

                if (
                    game_state != GameState.gameover
                    and game_state != GameState.surrender
                    and game_state != GameState.white_win
                    and game_state != GameState.black_win
                ):
                    whos_turn = player_next

                    _, advantages = Judge.who_has_advantage(new_board)
                    self.update_result(i, 0, 0, advantages)

                else:
                    who_win, advantages = Judge.who_has_advantage(new_board)
                    if who_win == self.player:
                        win = 1
                    else:  # 0 for oppoenent's win
                        win = 0
                    self.update_result(i, win, 1, advantages)

    def update_result(self, index, win, num_complete, advantages):
        record = self.result.get(index)
        if record == None:
            self.result[index] = (win, num_complete, advantages)
        else:
            self.result[index] = (
                record[0] + win,
                record[1] + num_complete,
                record[2] + advantages,
            )

    def get_result(self):
        return self.result
