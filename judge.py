from settings import PASS_STONE, SURRENDER_STONE
from utilities import *
import numpy as np


class GameState(Enum):
    gameover = 1
    surrender = 2
    game_continue = 3
    black_win = 4
    white_win = 5


class Judge:  # Judge class

    @classmethod
    def get_result(cls, board, player, game_state):
        result = Judge.calculate_result(board)
        who_win = None
        if game_state == GameState.surrender:
            if player == Player.black:
                who_win = Player.black
            else:
                who_win = Player.white
        if game_state == GameState.gameover:
            if result > 0:
                who_win = Player.black
            elif result < 0:
                who_win = Player.white
            # not possible for tie
        if game_state == GameState.black_win:
            who_win = Player.black

        if game_state == GameState.white_win:
            who_win = Player.white

        return who_win

    @classmethod
    def is_legal_move(cls, board, stone, player):
        liberties, zobrist = board.evaluate(player, stone)
        # Check for pass or surrender
        if stone in [PASS_STONE, SURRENDER_STONE]:
            return True
        # Check if the move is inside the board and the position is empty
        elif not board.is_on_board(stone) or board.stones.get(stone) is not None:
            return False
        # Check for no liberties or repeat of board state
        elif liberties == 0 or (player, zobrist) in board.board_records:
            return False
        else:
            return True

    @classmethod
    def next_state(cls, current_player, move, board):
        if move == SURRENDER_STONE:  # Surrender
            return GameState.surrender, current_player.other()

        if (
            len(board.move_records) >= 2
            and move == PASS_STONE
            and board.move_records[-1][1] == PASS_STONE
        ):
            return GameState.gameover, None  # Both players passed

        # Check for three consecutive passes by the same player
        consecutive_passes = 0

        for record in reversed(board.move_records):
            if record[0] == current_player and record[1] == PASS_STONE:
                consecutive_passes += 1
            elif record[0] != current_player:
                continue
            else:
                break  # Stop counting if a move is not a pass or made by the other player

        if move == PASS_STONE:
            consecutive_passes += 1

        if consecutive_passes >= 3:  # Three consecutive passes by the same player
            if current_player == Player.black:
                return GameState.white_win, None
            else:
                return GameState.black_win, None

        return GameState.game_continue, current_player.other()

    @classmethod
    def calculate_result(cls, board):
        # Komi is a fixed bonus score given to white to compensate for black's first move advantage using Chinese rule
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

    @classmethod
    def evaluate(cls, board):
        board_array = board.to_numpy()
        eval_array = np.zeros(board_array.shape)
        board_size = board_array.shape[0]
        edge_threshold = 3
        corner_influence = 3.5
        edge_influence = 3
        center_influence = 2.5

        for i in range(board_size):
            for j in range(board_size):
                for x in range(board_size):
                    for y in range(board_size):
                        if board_array[x, y] == 0:
                            continue
                        L = abs(i - x) + abs(j - y)
                        max_influence, basis = cls.calculate_influence(
                            x,
                            y,
                            board_size,
                            edge_threshold,
                            corner_influence,
                            edge_influence,
                            center_influence,
                        )
                        influence = basis ** (max_influence - L) * board_array[x, y]
                        eval_array[i, j] += influence
        return eval_array

    @staticmethod
    def calculate_influence(
        x,
        y,
        board_size,
        edge_threshold,
        corner_influence,
        edge_influence,
        center_influence,
    ):
        max_influence = 2
        basis = center_influence
        if (x <= edge_threshold or x >= board_size - edge_threshold) and (
            y <= edge_threshold or y >= board_size - edge_threshold
        ):  # Corner
            corner_x = min(x, board_size - x - 1)
            corner_y = min(y, board_size - y - 1)
            max_influence = (corner_x + corner_y) / 2 + 1
            basis = corner_influence
        elif (x <= edge_threshold or x >= board_size - edge_threshold) or (
            y <= edge_threshold or y >= board_size - edge_threshold
        ):  # Edge
            if x <= edge_threshold or x >= board_size - edge_threshold:
                max_influence = min(x, board_size - x - 1)
            else:
                max_influence = min(y, board_size - y - 1)
            basis = edge_influence
        return max_influence, basis

    @classmethod
    def who_has_advantage(cls, board):
        komi = 7.5
        board_array = cls.evaluate(board)
        count_b = np.sum(board_array[board_array >= 1])
        count_w = abs(np.sum(board_array[board_array <= -1]))
        if count_b > count_w + komi:
            return Player.black, count_b - count_w
        elif count_b < count_w + komi:
            return Player.white, count_w - count_b
        else:
            return None, 0
