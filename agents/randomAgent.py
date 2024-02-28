from agents.agent import Agent
from judge import Judge
from utilities import *
from settings import PASS_STONE, SURRENDER_STONE
import random


class RandomAgent(Agent):
    """An agent that plays randomly"""

    def __init__(self, player):
        super().__init__(player)
        self.step = 0

    def chooseMove(self, board):
        self.step += 1
        legal_moves = board.find_vacancy()

        # Giving up when a lot behind
        # Would cost too long for a game if agents play towards the real end
        result = Judge.calculate_result(board)
        if result < -30 and self.step >= 20 and self.player == Player.black:
            return SURRENDER_STONE
        elif result > 30 and self.step >= 20 and self.player == Player.white:
            return SURRENDER_STONE

        while True:
            if len(legal_moves) == 0:
                # No space to place a stone
                return PASS_STONE
            move = random.choice(legal_moves)
            legal_moves.remove(move)

            if Judge.is_legal_move(board, move, self.player):
                return move

    def isPolicyLegal(self, move, board):
        return True
