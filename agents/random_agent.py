from agents.agent import Agent
from judge import Judge
from settings import SURRENDER_STONE, PASS_STONE
from utilities import *
import random


class RandomAgent(Agent):
    """An agent that plays randomly"""

    def __init__(self, player):
        super().__init__(player)

    def chooseMove(self, board):
        self.step += 1
        vaccancy = board.find_vacancy()

        # Giving up when a lot behind
        # Would cost too long for a game if agents play towards the real end
        if self.should_surrender(board):
            return SURRENDER_STONE

        while True:
            # No space to place a stone
            if len(vaccancy) == 0:
                return PASS_STONE
            move = random.choice(vaccancy)
            vaccancy.remove(move)

            if Judge.is_legal_move(board, move, self.player):
                return move

    def is_policy_legal(self, move, board):
        return True
