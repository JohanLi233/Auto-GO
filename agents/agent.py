from judge import Judge
from utilities import *


class Agent:

    def __init__(self, player):
        self.step = 0
        self.player = player

    def choose_move(self, board):
        raise NotImplementedError

    def is_policy_legal(self, move, board):
        raise NotImplementedError

    def should_surrender(self, board):
        result = Judge.calculate_result(board)
        if result < -30 and self.step >= 20 and self.player == Player.black:
            return True
        elif result > 30 and self.step >= 20 and self.player == Player.white:
            return True
        else:
            return False
