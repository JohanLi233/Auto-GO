from enum import Enum


class StoneChain:

    def __init__(self, player, stones, liberties):
        self.belonging = player
        self.stones = set(stones)
        self.liberties = set(liberties)

    @classmethod
    def merge(cls, chain1, chain2):
        assert chain1.belonging == chain2.belonging
        allStones = chain1.stones | chain2.stones
        liberties = (chain1.liberties | chain2.liberties) - allStones
        return StoneChain(chain1.belonging, allStones, liberties)


class Player(Enum):
    black = 0
    white = 1

    def other(self):
        return Player.white if self == Player.black else Player.black
