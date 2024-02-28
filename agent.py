class Agent:

    def __init__(self, player):
        self.player = player

    def chooseMove(self, board):
        raise NotImplementedError

    def isPolicyLegal(self, move, board):
        raise NotImplementedError
