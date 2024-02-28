from settings import PASS_STONE, SURRENDER_STONE
from utilities import *


class GameState(Enum):
    g_over = -1
    g_continue = 1
    g_surrender = 0


class Judge:  # Judge class

    @classmethod
    def is_legal_move(cls, board, stone, player):
        # Check for pass or surrender
        if stone in [PASS_STONE, SURRENDER_STONE]:
            return True
        # Check if the move is inside the board and the position is empty
        if not board.is_on_board(stone) or board.stones.get(stone) is not None:
            return False
        # Check for no liberties or repeat of board state
        no_liberties, zobrist = board.evaluate(player, stone)
        if no_liberties == 0 or (player, zobrist) in board.board_records:
            return False
        return True

    @classmethod
    def next_state(cls, player_current, move, board):
        if move == SURRENDER_STONE:  # Surrender
            return GameState.g_surrender, player_current.other()
        if move == PASS_STONE and board.move_records[-1][1] == PASS_STONE:
            return GameState.g_over, None  # Both players passed
        return GameState.g_continue, player_current.other()

    @classmethod
    def calculate_result(cls, board):
        # Komi is a fixed bonus score given to white to compensate for black's first move advantage
        komi = 7.5
        # Initialize sets to track territories
        black_territory, white_territory, neutral_territory = set(), set(), set()

        def find_borders(board, stone, visited_stones):
            """Recursive function to identify the borders of a given territory."""
            borders = set()
            neighbours = board.get_neighboring_stones(stone)
            for neighbour in neighbours:
                # Skip if the neighbour is not on the board or has already been visited
                if not board.is_on_board(neighbour) or neighbour in visited_stones:
                    continue
                # If the neighbour is empty, it's part of the territory
                if board.stones.get(neighbour) is None:
                    visited_stones.add(neighbour)
                    borders |= find_borders(board, neighbour, visited_stones)
                else:
                    # If the neighbour has a stone, it defines the border of the territory
                    borders.add(board.stones.get(neighbour).belonging)
            return borders

        # Iterate over every point on the board to determine territory ownership
        for i in range(board.height):
            for j in range(board.width):
                point = (i, j)
                if board.stones.get(point) is None and point not in neutral_territory:
                    visited_stones = {point}
                    borders = find_borders(board, point, visited_stones)
                    if len(borders) == 1:
                        # Assign the territory to the respective player
                        (
                            black_territory
                            if Player.black in borders
                            else white_territory
                        ).update(visited_stones)
                    else:
                        # If borders contain both players, it's neutral territory
                        neutral_territory.update(visited_stones)

        # Count the stones and territories for each player
        black_scores = len(
            [p for p in board.stones if board.stones[p].belonging == Player.black]
        ) + len(black_territory)
        white_scores = len(
            [p for p in board.stones if board.stones[p].belonging == Player.white]
        ) + len(white_territory)

        # Return the game result by calculating black's score minus white's score adjusted with komi
        return black_scores - (white_scores + komi)
