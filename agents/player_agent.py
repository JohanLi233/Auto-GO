from agents.agent import Agent
from judge import Judge


class PlayerAgent(Agent):

    def choose_move(self, board):
        while True:
            column = int(input("column")) - 1
            row = int(input("row")) - 1

            if Judge.is_legal_move(board, (row, column), self.player):
                return (row, column)
            else:
                print("Iilegal move")
