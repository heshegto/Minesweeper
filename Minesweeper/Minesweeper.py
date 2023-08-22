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
        self.cell_size = 16
        self.window_height = self.cell_size * self.height
        self.window_width = self.cell_size * self.width

        # Variables that will be needed in render function
        self.window = None

    def get_player_desk(self):
        return self.playerDesk

    def set_desks(self, height=5, width=5, mines=5) -> None:
        """Resets all desks using input height, width and mines"""
        self.end_game = False
        self.height, self.width, self.mines = height, width, mines
        self.window_height = self.cell_size * self.height
        self.window_width = self.cell_size * self.width

        # What numbers on desks mean:
        # -3 -cell is flaged (only on player desk)
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
        if self.playerDesk[x][y] not in [-2, -3]:
            print("This cell is already opened")
            return False

        if self.playerDesk[x][y] != -3:
            self.playerDesk[x][y] = self.desk[x][y]
            if self.window != None:
                self.__continue_render(x, y, self.desk[x][y])

        # Additional moves if a player steps onto a cell without mines nearby
        if self.playerDesk[x][y] == 0:
            for x_ in range(-1, 2):
                for y_ in range(-1, 2):
                    x_neighbor = x + x_
                    y_neighbor = y + y_
                    if x_neighbor in range(self.height) and y_neighbor in range(self.width):
                        if self.playerDesk[x_neighbor][y_neighbor] == -2:
                            self.step(x_neighbor, y_neighbor)

        # If player made move on mine
        if self.playerDesk[x][y] == -1:
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

        self.window.fill((255, 255, 255))
        for i in range(self.height):
            for j in range(self.width):
                x, y = self.cell_size // 2 + self.cell_size * i, self.cell_size // 2 + self.cell_size * j
                self.__draw_cell(self.window, x, y, 'NotOpened')

        pygame.event.pump()
        pygame.display.update()

    @staticmethod
    def __draw_cell(canvas, x, y, type_of_cell):
        cell = CellSprite(x, y, type_of_cell)
        all_sprites = pygame.sprite.Group()
        all_sprites.add(cell)
        all_sprites.draw(canvas)

    def __continue_render(self, x, y, cell_type):
        """This function should be called to update window"""
        x, y = self.cell_size // 2 + self.cell_size * x, self.cell_size // 2 + self.cell_size * y
        self.__draw_cell(self.window, x, y, cell_type)

        # The following line copies our drawings from `canvas` to the visible window
        pygame.event.pump()
        pygame.display.update()

    def right_click(self, x, y):
        x //= self.cell_size
        y //= self.cell_size
        if self.playerDesk[x][y] == -2:
            self.playerDesk[x][y] = -3
            self.__continue_render(x, y, 'Flag')
        elif self.playerDesk[x][y] == -3:
            self.playerDesk[x][y] = -2
            self.__continue_render(x, y, 'NotOpened')

    def left_click(self, x, y):
        x //= self.cell_size
        y //= self.cell_size
        self.step(x, y)

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()


class CellSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, type_of_cell):
        super().__init__()
        paths = {
            0: "Minesweeper/Textures/num0.png",
            1: "Minesweeper/Textures/num1.png",
            2: "Minesweeper/Textures/num2.png",
            3: "Minesweeper/Textures/num3.png",
            4: "Minesweeper/Textures/num4.png",
            5: "Minesweeper/Textures/num5.png",
            6: "Minesweeper/Textures/num6.png",
            7: "Minesweeper/Textures/num7.png",
            8: "Minesweeper/Textures/num8.png",
            -1: "Minesweeper/Textures/ExplodedMine.png",
            'Flag': "Minesweeper/Textures/Flag.png",
            'Mine': "Minesweeper/Textures/Mine.png",
            'NotMine': "Minesweeper/Textures/NotMine.png",
            'NotOpened': "Minesweeper/Textures/NotOpened.png",
        }

        self.image = pygame.image.load(paths[type_of_cell])
        self.rect = self.image.get_rect()
        self.rect.center = (y, x)  # I don't know why but only in this case everything render correctly