from settings import *

import copy
import numpy as np
from utilities import StoneChain, Player


class Board:

    def __init__(self, width=WIDTH, height=HEIGHT):
        # board starts at [0, 0]
        self.width = width
        self.height = height
        self.zobrist = EMPTY_BOARD
        self.stones = (
            {}
        )  # dictionary for location of stones，key：(0,0)，value：StoneString
        self.move_records = []  # [(player,move)]
        self.board_records = set()

    def update_environment(self, player, stone):
        """Updates the game environment based on the player's move."""
        if stone == PASS_STONE:  # Player pass
            self.handle_pass(player)
        elif stone == SURRENDER_STONE:  # Surrender
            self.handle_surrender(player)
        else:
            self.handle_stone_placement(player, stone)

    def handle_pass(self, player):
        """Handles a pass move."""
        self.board_records.add((player, self.zobrist))
        self.move_records.append((player, PASS_STONE))

    def handle_surrender(self, player):
        """Handles surrender."""
        self.move_records.append((player, SURRENDER_STONE))

    def handle_stone_placement(self, player, stone):
        """Handles the placement of a stone on the board."""
        neighbors = self.get_neighboring_stones(stone)
        friendly_chains, enemy_chains, liberties = self.categorize_neighbors(
            player, neighbors
        )

        new_chain = StoneChain(player, [stone], liberties)
        self.update_zobrist(stone, player)

        # Merge with friendly chains
        for chain in friendly_chains:
            new_chain = StoneChain.merge(new_chain, chain)

        # Update board with the new chain
        for stone_position in new_chain.stones:
            self.stones[stone_position] = new_chain

        # Handle captures
        self.handle_captures(enemy_chains, player, stone)

        # Record board state and move
        self.board_records.add((player, self.zobrist))
        self.move_records.append((player, stone))

    def categorize_neighbors(self, player, neighbors):
        """Categorizes neighboring stones into friendly and enemy chains, and identifies liberties."""
        friendly_chains, enemy_chains, liberties = [], [], []
        for neighbor in neighbors:
            if not self.is_on_board(neighbor):
                continue
            chain = self.stones.get(neighbor)
            if chain is None:
                liberties.append(neighbor)
            elif chain.belonging == player:
                if chain not in friendly_chains:
                    friendly_chains.append(chain)
            else:
                if chain not in enemy_chains:
                    enemy_chains.append(chain)
        return friendly_chains, enemy_chains, liberties

    def handle_captures(self, enemy_chains, player, stone):
        """Handles capturing of enemy chains if they have no liberties left."""
        for chain in enemy_chains:
            chain.liberties.discard(stone)
            if len(chain.liberties) == 0:  # Capture
                for captured_stone in chain.stones:
                    self.capture_stone(captured_stone, player)

    def capture_stone(self, stone, player):
        """Removes a captured stone from the board and updates the Zobrist hash."""
        for neighbor in self.get_neighboring_stones(stone):
            neighbor_stone = self.stones.get(neighbor)
            if neighbor_stone is not None:
                if neighbor_stone.belonging == player:
                    neighbor_stone.liberties.add(stone)
        self.stones.pop(stone)
        self.update_zobrist(stone, player.other())

    def get_neighboring_stones(self, stone):
        return [
            (stone[0] - 1, stone[1]),
            (stone[0], stone[1] - 1),
            (stone[0] + 1, stone[1]),
            (stone[0], stone[1] + 1),
        ]  # down, left, up, right

    def is_on_board(self, stone):
        return 0 <= stone[0] < self.height and 0 <= stone[1] < self.width

    def evaluate(self, player, stone):
        zobrist = copy.deepcopy(self.zobrist)
        stones = copy.deepcopy(self.stones)
        neighbors = self.get_neighboring_stones(stone)
        own_chains = []
        enemy_chains = []
        liberties = []

        for neighbor in neighbors:
            if not self.is_on_board(neighbor):
                continue
            chain = stones.get(neighbor)
            if chain is None:
                liberties.append(neighbor)
            elif chain.belonging == player:
                if chain not in own_chains:
                    own_chains.append(chain)
            else:
                if chain not in enemy_chains:
                    enemy_chains.append(chain)

        new_chain = StoneChain(player, [stone], liberties)

        zobrist = self.get_zobrist_hash(stone, player, zobrist)

        for chain in own_chains:
            new_chain = StoneChain.merge(new_chain, chain)
        for stone_position in new_chain.stones:
            stones[stone_position] = new_chain

        for chain in enemy_chains:
            chain.liberties.discard(stone)
            if len(chain.liberties) == 0:
                for captured_stone in chain.stones:
                    for neighbor in self.get_neighboring_stones(captured_stone):
                        neighbor_stone = stones.get(neighbor)
                        if neighbor_stone is not None:
                            if neighbor_stone.belonging == player:
                                neighbor_stone.liberties.add(captured_stone)
                    stones.pop(captured_stone)
                    zobrist = self.get_zobrist_hash(
                        captured_stone, player.other(), zobrist
                    )

        temp = stones.get(stone)
        if temp is None:
            raise ValueError("stone can not be none")

        return len(temp.liberties), zobrist

    def update_zobrist(self, stone, player):
        hash_code = HASH_CODE.get((stone, player))
        if hash_code is None:
            raise ValueError("Can't find hash")
        self.zobrist ^= hash_code

    def get_zobrist_hash(self, stone, player, zobrist):
        """
        Updates the Zobrist hash of the board state.

        This method XORs the current Zobrist hash with the hash value corresponding to the given stone's position
        and the current player. This is used to maintain a unique hash for the current board state.
        """
        hash_code = HASH_CODE.get((stone, player))
        if hash_code is None:
            raise ValueError("Can't find hash")
        return zobrist ^ hash_code

    def print_board(self):
        for row in range(self.height):
            bump = " " if row > 9 else ""
            line = []
            for col in range(self.width):
                stone = self.stones.get((self.height - 1 - row, col))
                if stone is not None:
                    player = stone.belonging
                    line.append(STONE_TO_CHAR.get(player))
                else:
                    line.append(STONE_TO_CHAR.get(None))
            print("%s%d %s" % (bump, self.height - row, "".join(line)))
        print("   " + "  ".join(COLS[: self.width]))

    def to_numpy(self):  # convert to numpy array
        board_array = np.zeros((self.height, self.width), dtype="int")  # 0 for none
        for i in self.stones:
            if self.stones[i].belonging == Player.black:  # 1 for black
                board_array[i[0], i[1]] = 1
            elif self.stones[i].belonging == Player.white:  # -1 for white
                board_array[i[0], i[1]] = -1
            else:
                pass
        return board_array

    def find_vacancy(self):
        vacancies = []
        for i in range(self.width):
            for j in range(self.height):
                if self.stones.get((i, j)) == None:
                    vacancies.append((i, j))
        return vacancies
