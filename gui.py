import pygame
from settings import *


class Gui:

    def __init__(self):
        if GUI_ON:
            pygame.init()
            self.screen = pygame.display.set_mode(BOARD_SIZE)
            pygame.display.set_caption("Go Game")
            self.font = pygame.font.SysFont(None, FONT_SIZE)

    def draw_board(self):
        self.screen.fill(BOARD_COLOR)
        for i in range(HEIGHT):
            # Draw horizontal lines with margins
            pygame.draw.line(
                self.screen,
                LINE_COLOR,
                (
                    BOARD_MARGIN,
                    BOARD_MARGIN
                    + i * (BOARD_SIZE[0] - 2 * BOARD_MARGIN) / (HEIGHT - 1),
                ),
                (
                    BOARD_SIZE[0] - BOARD_MARGIN,
                    BOARD_MARGIN
                    + i * (BOARD_SIZE[1] - 2 * BOARD_MARGIN) / (HEIGHT - 1),
                ),
                LINE_WIDTH,
            )
            for j in range(WIDTH):
                # Draw vertical lines with margins
                pygame.draw.line(
                    self.screen,
                    LINE_COLOR,
                    (
                        BOARD_MARGIN
                        + j * (BOARD_SIZE[0] - 2 * BOARD_MARGIN) / (WIDTH - 1),
                        BOARD_MARGIN,
                    ),
                    (
                        BOARD_MARGIN
                        + j * (BOARD_SIZE[1] - 2 * BOARD_MARGIN) / (WIDTH - 1),
                        BOARD_SIZE[1] - BOARD_MARGIN,
                    ),
                    LINE_WIDTH,
                )

            row_label = self.font.render(str(HEIGHT - i), True, FONT_COLOR)
            self.screen.blit(
                row_label,
                (
                    BOARD_MARGIN / 2,
                    BOARD_MARGIN + i * GRID_SIZE[1] - row_label.get_height() / 2,
                ),
            )

            col_label = self.font.render(str(1 + i), True, FONT_COLOR)  # number column
            self.screen.blit(
                col_label,
                (
                    BOARD_MARGIN + i * GRID_SIZE[0] - col_label.get_width() / 2,
                    BOARD_SIZE[1] - BOARD_MARGIN / 2,
                ),
            )

            # Alphabet column
            # col_label = self.font.render(
            #     chr(65 + i), True, FONT_COLOR
            # )  # 65 is ASCII for 'A'
            # self.screen.blit(
            #     col_label,
            #     (
            #         BOARD_MARGIN + i * GRID_SIZE[0] - col_label.get_width() / 2,
            #         BOARD_SIZE[1] - BOARD_MARGIN / 2,
            #     ),
            # )

    def draw_stones(self, board):
        board_array = board.to_numpy()
        for row in range(board.height):
            for col in range(board.width):
                stone = board_array[row, col]
                if stone != 0:  # There's a stone at this position
                    color = (0, 0, 0) if stone == 1 else (255, 255, 255)

                    # Flip the y-coordinate by subtracting from the maximum row index
                    pixel_y = BOARD_MARGIN + (board.height - 1 - row) * GRID_SIZE[1]

                    # x-coordinate remains the same
                    pixel_x = BOARD_MARGIN + col * GRID_SIZE[0]

                    pygame.draw.circle(
                        self.screen,
                        color,
                        (int(pixel_x), int(pixel_y)),
                        STONE_RADIUS,
                    )

    def update(self, board):
        self.draw_board()
        self.draw_stones(board)
        pygame.display.flip()

    def quit(self):
        pygame.quit()
