from agents.agent import Agent
from judge import Judge
from utilities import *
from settings import PASS_STONE


class SequentialAgent(Agent):
    """An agent that plays left down corner all the way to up right corner sequentially"""

    def __init__(self, player):
        super().__init__(player)
        self.step = 0

    def choose_move(self, board):
        self.step += 1
        vacancy = board.find_vacancy()

        while True:
            if len(vacancy) == 0:
                # No space to place a stone
                return PASS_STONE
            move = vacancy[0]
            # print(move)
            # print(Judge.is_legal_move(board, move, self.player))
            vacancy.remove(move)

            if Judge.is_legal_move(board, move, self.player):
                print("true")
                return move
            else:
                continue

    def is_policy_legal(self, move, board):
        return True
