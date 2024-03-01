from agents.agent import Agent
from judge import Judge
from settings import SURRENDER_STONE, PASS_STONE
from utilities import *
import random
import sys


class RandomAgent(Agent):
    """An agent that plays at random"""

    def __init__(self, player):
        super().__init__(player)
        seed = random.randrange(sys.maxsize)
        self.rng = random.Random(seed)
        # print("Seed was:", seed)

    def choose_move(self, board):
        vacancy = board.find_vacancy()
        self.rng.shuffle(vacancy)
        for i in vacancy:
            if Judge.is_legal_move(board, i, self.player):
                return i
        return PASS_STONE
