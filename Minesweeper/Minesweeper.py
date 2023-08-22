import pygame
import sys
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
        # -3 -cell with flag (only on player desk)
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

        # Do moves on player desk and show it on screen
        if self.playerDesk[x][y] != -3:
            self.playerDesk[x][y] = self.desk[x][y]
            if self.window is not None:
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
            self.show_other_mines(x, y)
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

    def render_game_desk(self):
        """This function should be called to start render game window"""
        pygame.init()
        # Creating display
        pygame.display.init()
        self.window = pygame.display.set_mode((self.window_width, self.window_height))

        # Filling window with not opened cells
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
        all_sprites.add(cell)  # PyCharm shows problem here, but everything ok
        all_sprites.draw(canvas)

    def __continue_render(self, x, y, cell_type):
        """This function should be called to update window"""
        x, y = self.cell_size // 2 + self.cell_size * x, self.cell_size // 2 + self.cell_size * y
        self.__draw_cell(self.window, x, y, cell_type)
        pygame.display.flip()

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
            sys.exit()

    def show_other_mines(self, x, y):
        for i in range(self.height):
            for j in range(self.width):
                x_, y_ = self.cell_size // 2 + self.cell_size * i, self.cell_size // 2 + self.cell_size * j
                if not (j == x and i == y) and self.desk[i][j] == -1:
                    if self.playerDesk[i][j] == -3:
                        self.__draw_cell(self.window, x_, y_, 'Flag')
                    if self.playerDesk[i][j] == -2:
                        self.__draw_cell(self.window, x_, y_, 'Mine')
                if self.desk[i][j] != -1 and self.playerDesk[i][j] == -3:
                    self.__draw_cell(self.window, x_, y_, 'NotMine')
        pygame.event.pump()
        pygame.display.update()

    def show_menu(self):
        pygame.init()
        pygame.display.init()
        self.window = pygame.display.set_mode((300, 300))
        self.window.fill((255, 255, 255))

        # basic font for user typed
        base_font = pygame.font.Font(None, 32)
        Fields = [TextField(100,100,'height'), TextField(100,150,'width'), TextField(100,200,'mines')]

        color_active = pygame.Color('lightskyblue3')
        color_passive = pygame.Color('chartreuse4')
        color = color_passive

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                    # self.close()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for field in Fields:
                        if field.input_rect.collidepoint(event.pos):
                            field.active = True
                        else:
                            field.active = False

                if event.type == pygame.KEYDOWN:
                    for field in Fields:
                        if event.key == pygame.K_BACKSPACE and field.active:
                            field.user_text = field.user_text[:-1]
                        elif event.key == pygame.K_KP_ENTER:
                            field.active = False
                        elif event.unicode.isdigit() and field.active:
                            field.user_text += event.unicode
            for field in Fields:
                if field.active:
                    color = color_active
                else:
                    color = color_passive

            # draw rectangle and argument passed which should
            # be on screen
                pygame.draw.rect(self.window, color, field.input_rect)

                text_surface = base_font.render(field.user_text, True, (255, 255, 255))

                # render at position stated in arguments
                self.window.blit(text_surface, (field.input_rect.x + 5, field.input_rect.y + 5))

                # set width of textfield so that text cannot get
                # outside of user's text input
                field.input_rect.w = max(100, text_surface.get_width() + 10)
                pygame.display.flip()

        self.height = int(Fields[0].user_text)
        self.width = int(Fields[1].user_text)
        self.mines = int(Fields[2].user_text)
        self.start_game(self.height, self.width, self.mines)

    def start_game(self, height: int, width: int, mines: int) -> None:
        self.set_desks(height, width, mines)
        self.render_game_desk()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    self.right_click(event.pos[1], event.pos[0])
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.left_click(event.pos[1], event.pos[0])
                if event.type == pygame.QUIT:
                    running = False
                    self.close()

    def show_result_window(self):
        pass


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


class TextField:
    def __init__(self, x, y, type):
        self.active = False
        self.user_text = ''
        self.input_rect = pygame.Rect(x, y, 140, 32)
