from agents.agent import Agent
from judge import Judge
from settings import SURRENDER_STONE, PASS_STONE
from utilities import *
import random
import sys


class RandomPolicyAgent(Agent):
    """An agent that plays randomly and following some simple rules"""

    def __init__(self, player):
        super().__init__(player)
        seed = random.randrange(sys.maxsize)
        self.rng = random.Random(seed)
        print("Seed was:", seed)

    def choose_move(self, board):
        self.step += 1
        vacancy = board.find_vacancy()

        # Giving up when a lot behind
        # Might cost too long for a game if agents play towards the real end for a large board
        # if self.should_surrender(board):
        #     return SURRENDER_STONE

        while True:
            # No space to place a stone
            if len(vacancy) == 0:
                return PASS_STONE
            move = self.rng.choice(vacancy)
            vacancy.remove(move)

            if Judge.is_legal_move(board, move, self.player) and self.is_policy_legal(
                move, board
            ):
                return move
            else:
                continue

    def is_policy_legal(self, move, board):  # use some simple rules
        neighbours = board.get_neighboring_stones(move)
        is_eye = True
        for i in neighbours:
            if not board.is_on_board(i):
                continue
            if board.stones.get(i) == None:
                is_eye = False
                break
            elif board.stones.get(i).belonging != self.player:
                is_eye = False
                break
            elif len(board.stones.get(i).liberties) <= 1:
                is_eye = False
                break
            else:
                pass
        if is_eye:
            return False
        return True
