from agents.agent import Agent
from judge import Judge
from settings import RANDOM_AGENT_STRATEGY, SURRENDER_STONE, PASS_STONE
from utilities import *
import random
import sys


class RandomPolicyAgent(Agent):
    """An agent that plays randomly and following some simple rules"""

    def __init__(self, player):
        super().__init__(player)
        seed = random.randrange(sys.maxsize)
        self.rng = random.Random(seed)
        self.ignore_efficiency = False
        # print("Seed was:", seed)

    def choose_move(self, board):
        self.step += 1
        vacancy = board.find_vacancy()
        self.rng.shuffle(vacancy)

        for _ in range(2):
            for i in vacancy:
                if self.ignore_efficiency:
                    if Judge.is_legal_move(board, i, self.player):
                        self.ignore_efficiency = False
                        return i
                    else:
                        continue

                if self.is_move_efficient(i, board):
                    if Judge.is_legal_move(board, i, self.player):
                        return i

            self.ignore_efficiency = True

        return PASS_STONE

    def is_move_efficient(self, move, board):  # use some simple rules
        if self.step < 5:
            return True
        # 0 for using all strategy
        # 1 for using move_on_eye only
        # 2 for using strength only
        if RANDOM_AGENT_STRATEGY == 0:
            if self.move_on_eye(move, board):
                return False
            elif not self.is_extending_from_strength(move, board):
                return False
            else:
                return True
        elif RANDOM_AGENT_STRATEGY == 1:
            if self.move_on_eye(move, board):
                return False
            else:
                return True
        elif RANDOM_AGENT_STRATEGY == 2:
            if self.is_extending_from_strength(move, board):
                return True
            else:
                return False
        else:
            # Unknown strategy
            return True

    def move_on_eye(self, move, board):  # not to place on eye
        neighbours = board.get_neighboring_stones(move)
        for i in neighbours:
            if not board.is_on_board(i):
                continue
            if board.stones.get(i) == None:
                return False
            elif board.stones.get(i).belonging != self.player:
                return False
            elif len(board.stones.get(i).liberties) <= 1:
                return False
            else:
                pass
        return True

    def is_extending_from_strength(self, move, board):
        friendly_neighbors = 0
        empty_neighbors = 0
        strong_groups_nearby = False

        neighbors = board.get_neighboring_stones(move)
        for n in neighbors:
            if board.is_on_board(n):
                if board.stones.get(n) is None:
                    empty_neighbors += 1
                elif board.stones.get(n).belonging == self.player:
                    friendly_neighbors += 1
                    # Check if the friendly group is strong
                    if len(board.stones.get(n).liberties) > 2:
                        strong_groups_nearby = True

        # A move is considered as extending from strength if it's next to at least one strong friendly group,
        # and it's not completely surrounded by friendly stones (to avoid filling in one's own eyes)
        # this is checked using move_one_eye method
        if strong_groups_nearby and empty_neighbors > 0:
            return True
        else:
            return False
