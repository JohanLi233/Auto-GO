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
    """An agent that plays using Monte Carlo strategy"""

    def __init__(self, player):
        super().__init__(player)
        seed = random.randrange(sys.maxsize)
        self.rng = random.Random(seed)

    def choose_move(self, board):
        mc = MonteCarlo(board, self.player, MONTE_CARLO_TIME_LIMIT)
        mc.simulate()
        mc_result = mc.get_result()

        # Check if the only move is to pass
        if len(mc_result) == 1 and PASS_STONE in mc_result:
            return PASS_STONE

        # Extract moves, win rates, and average advantages
        moves_data = []
        for move, result in mc_result.items():
            wins, games_completed, total_advantage, advantage_samples = result
            win_rate = wins / games_completed if games_completed > 0 else 0
            avg_advantage = total_advantage / advantage_samples if advantage_samples > 0 else 0
            moves_data.append((move, win_rate, avg_advantage))

        # Separate data for processing
        moves, win_rates, avg_advantages = zip(*moves_data)

        # Normalize advantages to ensure compatibility in scoring
        max_advantage = max(avg_advantages) if avg_advantages else 1
        normalized_advantages = [adv / max_advantage for adv in avg_advantages]

        # Compute scores by combining win rates and normalized advantages
        scores = [win_rate + adv for win_rate, adv in zip(win_rates, normalized_advantages)]
        idx = np.argmax(scores)
        move = moves[idx]

        # Verify if the chosen move is legal
        if Judge.is_legal_move(board, move, self.player):
            return tuple(move)
        else:
            return PASS_STONE

class MonteCarlo:

    def __init__(self, board, player, time_limit):
        self.board = board
        self.agent_player = RandomAgent(player)
        self.agent_opponent = RandomAgent(player.other())
        self.result = {}  # {move: (wins, games_completed, total_advantage, advantage_samples)}
        self.player = player
        self.time_limit = time_limit

    def simulate(self):
        start_time = time.time()
        while time.time() - start_time < self.time_limit:
            self.simulate_round()

        # If no moves were simulated, only option is to pass
        if not self.result:
            self.result[PASS_STONE] = (0, 0, 0, 0)

    def simulate_round(self):
        vacancies = self.board.find_vacancy()
        random.shuffle(vacancies)
        legal_moves_found = False

        for move in vacancies:
            new_board = copy.deepcopy(self.board)
            whos_turn = self.player

            # Check if the move is legal
            if not Judge.is_legal_move(new_board, move, self.player):
                continue

            legal_moves_found = True

            # Apply the move
            game_state, next_player = Judge.next_state(whos_turn, move, new_board)
            new_board.update_board(whos_turn, move)
            whos_turn = next_player

            # Simulate the game for a number of steps or until it ends
            for _ in range(MONTE_CARLO_STEPS):
                if whos_turn == self.player:
                    simulated_move = self.agent_player.choose_move(new_board)
                else:
                    simulated_move = self.agent_opponent.choose_move(new_board)

                game_state, next_player = Judge.next_state(whos_turn, simulated_move, new_board)
                new_board.update_board(whos_turn, simulated_move)

                if game_state in {GameState.gameover, GameState.surrender, GameState.white_win, GameState.black_win}:
                    # Determine winner and update result
                    winner, advantage = Judge.who_has_advantage(new_board)
                    win = 1 if winner == self.player else 0
                    self.update_result(move, win, 1, advantage)
                    break
                else:
                    whos_turn = next_player
            else:
                # Game did not end; estimate advantage
                _, advantage = Judge.who_has_advantage(new_board)
                self.update_result(move, 0, 0, advantage)

        # If no legal moves are found, the only option is to pass
        if not legal_moves_found:
            self.result[PASS_STONE] = (0, 0, 0, 0)

    def update_result(self, move, win, games_completed, advantage):
        record = self.result.get(move)
        if record is None:
            self.result[move] = (win, games_completed, advantage, 1)
        else:
            wins, games, total_adv, samples = record
            self.result[move] = (
                wins + win,
                games + games_completed,
                total_adv + advantage,
                samples + 1
            )

    def get_result(self):
        return self.result
