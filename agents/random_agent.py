from agents.agent import Agent
from judge import Judge
from settings import SURRENDER_STONE, PASS_STONE
from utilities import *
import random
import sys


class RandomAgent(Agent):
    """An agent that plays randomly"""

    def __init__(self, player):
        super().__init__(player)
        seed = random.randrange(sys.maxsize)
        self.rng = random.Random(1897694146040844402)
        # self.rng = random.Random(seed)
        print("Seed was:", seed)

    def choose_move(self, board):
        self.step += 1
        vacancy = board.find_vacancy()

        # Giving up when a lot behind
        # Would cost too long for a game if agents play towards the real end
        if self.should_surrender(board):
            return SURRENDER_STONE

        while True:
            # No space to place a stone
            if len(vacancy) == 0:
                return PASS_STONE
            move = self.rng.choice(vacancy)
            vacancy.remove(move)

            if Judge.is_legal_move(board, move, self.player):
                return move
            else:
                continue

    def is_policy_legal(self, move, board):
        return True
