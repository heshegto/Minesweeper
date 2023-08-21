import pygame
import numpy as np


class MinesweeperGame:
    def __init__(self) -> None:
        self.end_game = False  # End game flag
        self.height, self.width, self.mines = 5, 5, 5

        # Creating player's desk (only this desk player sees)
        self.playerDesk = [[]]

        # Creating game desk
        self.desk = [[]]

        # Counting window size
        self.cell_size = 20
        self.window_height = self.cell_size * self.height
        self.window_width = self.cell_size * self.width

        # Variables that will be needed in render function
        self.window = None
        self.clock = None
        self.render_fps = 8

    def reset_desks(self, height=5, width=5, mines=5) -> None:
        """Resets all desks using input height, width and mines"""
        self.end_game = False
        self.height, self.width, self.mines = height, width, mines
        self.window_height = self.cell_size * self.height
        self.window_width = self.cell_size * self.width

        # What numbers on desks mean:
        # -2 -cell isn't opened (only on player desk)
        # -1 -cell with mine
        # >=0 -number of mines around cell

        # Creating new desks
        self.playerDesk = [[-2 for _ in range(self.width)] for _ in range(self.height)]
        self.desk = [[0 for _ in range(self.width)] for _ in range(self.height)]

        # Putting mines randomly
        count = 0
        while count < self.mines:
            i = int(np.random.random_integers(0, self.height-1, size=1))
            j = int(np.random.random_integers(0, self.width-1, size=1))
            if self.desk[i][j] != 0:
                continue
            self.desk[i][j] = -1
            count += 1

        # Counting how many mines are around each cell
        for i in range(self.height):
            for j in range(self.width):
                if self.desk[i][j] != -1:
                    self.desk[i][j] = self.__get_mines_around(i, j)

    def __get_mines_around(self, x: int, y: int) -> int:
        """Get amount of mines around cell with coordinates x and y"""
        amount = 0
        for x_ in range(-1, 2):
            for y_ in range(-1, 2):
                x_neighbor = x + x_
                y_neighbor = y + y_
                if x_neighbor in range(self.height) and y_neighbor in range(self.width):
                    if self.desk[x_neighbor][y_neighbor] == -1:
                        amount += 1
        return amount

    def step(self, x: int, y: int) -> bool:
        """Makes a move on player's game desk"""

        # Checking if input step is correct
        if x not in range(self.height) or y not in range(self.width):
            raise Exception("Coordinates are out of range")
        if self.end_game:
            raise Exception("Game over. Start new one")
        if self.playerDesk[x][y] != -2:
            print("This cell is already opened")
            return False

        self.playerDesk[x][y] = self.desk[x][y]

        # Additional moves if a player steps onto a cell without mines nearby
        if self.desk[x][y] == 0:
            for x_ in range(-1, 2):
                for y_ in range(-1, 2):
                    x_neighbor = x + x_
                    y_neighbor = y + y_
                    if x_neighbor in range(self.height) and y_neighbor in range(self.width):
                        if self.playerDesk[x_neighbor][y_neighbor] == -2:
                            self.step(x_neighbor, y_neighbor)

        # If player made move on mine
        if self.desk[x][y] == -1:
            self.end_game = True
            print("You lose")

        # Checking if there is any available moves, if No player win
        is_end = True
        for i in range(self.height):
            for j in range(self.width):
                if self.playerDesk[i][j] == -2 and self.desk[i][j] >= 0:
                    is_end = False
        if is_end:
            self.end_game = True
            print("You win")

        return self.end_game

    def start_render(self):
        """This function should be called to start render game window"""
        pygame.init()
        # Creating display
        pygame.display.init()
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        self.clock = pygame.time.Clock()


    def continue_render(self):
        """This function should be called to update window"""
        # Creating blank canvas
        canvas = pygame.Surface((self.window_width, self.window_height))
        canvas.fill((255, 255, 255))

        # Add some gridlines to canvas
        for x in range(self.width + 1):
            pygame.draw.line(
                canvas,
                0,
                (self.cell_size * x, 0),
                (self.cell_size * x, self.window_height),
                width=2,
            )
        for x in range(self.height + 1):
            pygame.draw.line(
                canvas,
                0,
                (0, self.cell_size * x),
                (self.window_width, self.cell_size * x),
                width=2,
            )

        # Printing result of step on canvas
        font = pygame.font.Font(None, 20)

        def draw_symbol(digit, xs, y):
            digit_text = str(digit)
            text_surface = font.render(digit_text, True, (0, 0, 0))
            canvas.blit(text_surface, (xs, y))

        for i in range(self.height):
            for j in range(self.width):
                if self.playerDesk[i][j] == -1:
                    draw_symbol('B', (0.1 + i) * self.cell_size, (0.1 + j) * self.cell_size)
                elif self.playerDesk[i][j] != -2:
                    draw_symbol(self.playerDesk[i][j], (0.1 + i) * self.cell_size, (0.1 + j) * self.cell_size)

        # The following line copies our drawings from `canvas` to the visible window
        self.window.blit(canvas, canvas.get_rect())
        pygame.event.pump()
        pygame.display.update()

        # We need to ensure that human-rendering occurs at the predefined framerate.
        # The following line will automatically add a delay to keep the framerate stable.
        self.clock.tick(self.render_fps)

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
