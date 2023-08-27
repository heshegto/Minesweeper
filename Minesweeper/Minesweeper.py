import pygame
import sys
import numpy as np


class MinesweeperGame:
    def __init__(self) -> None:
        self.end_game = False  # End game flag
        self.end_game_message = ''
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
            i = int(np.random.random_integers(0, self.height - 1, size=1))
            j = int(np.random.random_integers(0, self.width - 1, size=1))
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
            self.end_game_message = "You lose"

        # Checking if there is any available moves, if No player win
        is_end = True
        for i in range(self.height):
            for j in range(self.width):
                if self.playerDesk[i][j] == -2 and self.desk[i][j] >= 0:
                    is_end = False
        if is_end:
            self.end_game = True
            self.end_game_message = "You win"

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

    def left_click(self, x, y) -> bool:
        x //= self.cell_size
        y //= self.cell_size
        return self.step(x, y)

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
        # Fields in which player set desk height, desk width and amount of mines
        input_fields = [InputField(120, 100, 140, 32, 'height'),
                        InputField(120, 150, 140, 32, 'width'),
                        InputField(120, 200, 140, 32, 'mines')
                        ]

        buttons = [Button(80, 250, 200, 32, text_on_button="Start game", button_type='Start'),
                   ]

        running = True
        while running:
            for event in pygame.event.get():
                print(event)
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                    self.close()

                # Input fields logic
                for field in input_fields:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if field.collidepoint(event.pos):
                            field.active = True
                            field.user_text = ''
                        else:
                            field.active = False
                            if field.user_text == '':
                                field.user_text = field.default_value

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE and field.active:
                            field.user_text = field.user_text[:-1]
                        elif event.key == pygame.K_KP_ENTER:
                            field.active = False
                            if field.user_text == '':
                                field.user_text = field.default_value
                        elif event.unicode.isdigit() and field.active:
                            field.user_text += event.unicode
                    if field.user_text.isdigit() and int(field.user_text) > 50:
                        field.user_text = "50"
                    if field.active:
                        field.color = field.color_active
                    else:
                        field.color = field.color_passive

                    # draw rectangle and argument passed which should
                    # be on screen
                    pygame.draw.rect(self.window, field.color, field)

                    text_surface = base_font.render(field.user_text, True, (255, 255, 255))

                    # render at position stated in arguments
                    self.window.blit(text_surface, (field.x + 5, field.y + 5))

                    # set width of textfield so that text cannot get
                    # outside of user's text input
                    field.w = max(140, text_surface.get_width() + 10)
                    pygame.display.flip()

                for button in buttons:
                    pressed = False
                    if event.type == pygame.MOUSEMOTION and button.collidepoint(event.pos):
                        button.active = True
                        button.color = button.active_color
                    else:
                        button.active = False
                        button.color = button.passive_color
                    if event.type == pygame.MOUSEBUTTONDOWN and button.collidepoint(event.pos):
                        pygame.draw.rect(self.window, (255, 255, 255), button)
                        button.x += round(button.w * 0.05)
                        button.y += round(button.h * 0.05)
                        button.w = round(0.9 * button.w)
                        button.h = round(0.9* button.h)
                        pressed = True
                    if event.type == pygame.MOUSEBUTTONUP:
                        button.w = round(button.w / 0.9)
                        button.h = round(button.h / 0.9)
                        button.x -= round(button.w * 0.05)
                        button.y -= round(button.h * 0.05)
                        if button.collidepoint(event.pos):
                            match button.button_type:
                                case 'Start':
                                    self.height = int(input_fields[0].user_text)
                                    self.width = int(input_fields[1].user_text)
                                    self.mines = int(input_fields[2].user_text)
                                    self.start_game(self.height, self.width, self.mines)
                    pygame.draw.rect(self.window, button.color, button)
                    text_surface = base_font.render(button.text_on_button, True, (255, 255, 255))
                    self.window.blit(text_surface, (button.x + 5, button.y + 5))
                    pygame.display.flip()

    def start_game(self, height: int, width: int, mines: int) -> None:
        self.set_desks(height, width, mines)
        self.render_game_desk()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    self.right_click(event.pos[1], event.pos[0])
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.end_game:
                        self.show_result_window()
                    else:
                        self.left_click(event.pos[1], event.pos[0])
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                    self.close()

    def show_result_window(self):
        pygame.init()
        pygame.display.init()
        self.window = pygame.display.set_mode((300, 150))
        self.window.fill((255, 255, 255))
        base_font = pygame.font.Font(None, 32)
        text_surface = base_font.render(self.end_game_message, True, (0, 0, 0))
        self.window.blit(text_surface, (10, 10))
        pygame.display.update()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                    self.close()


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


class InputField(pygame.Rect):
    def __init__(self, left, top, width, height, information_type, default_value='15'):
        super().__init__(left, top, width, height)
        self.information_type = information_type

        self.active = False
        self.user_text = default_value
        self.default_value = default_value
        self.color_active = pygame.Color('lightskyblue3')
        self.color_passive = pygame.Color('chartreuse4')

        self.color = self.color_passive


class Button(pygame.Rect):
    def __init__(self, left, top, width, height, text_on_button, button_type):
        super().__init__(left, top, width, height)
        self.text_on_button = text_on_button
        self.button_type = button_type
        self.active = False
        self.active_color = (170, 170, 170)
        self.passive_color = (100, 100, 100)
        self.color = self.passive_color
