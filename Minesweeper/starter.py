import pygame
from Minesweeper.menu_fields import *
from Minesweeper import Game


def show_game_menu(game: Game):
    pygame.init()
    pygame.display.init()
    game.window = pygame.display.set_mode((300, 300))
    game.window.fill((255, 255, 255))

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
                game.close()

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
                pygame.draw.rect(game.window, field.color, field)

                text_surface = base_font.render(field.user_text, True, (255, 255, 255))

                # render at position stated in arguments
                game.window.blit(text_surface, (field.x + 5, field.y + 5))

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
                    pygame.draw.rect(game.window, (255, 255, 255), button)
                    button.x += round(button.w * 0.05)
                    button.y += round(button.h * 0.05)
                    button.w = round(0.9 * button.w)
                    button.h = round(0.9 * button.h)
                    pressed = True
                if event.type == pygame.MOUSEBUTTONUP:
                    button.w = round(button.w / 0.9)
                    button.h = round(button.h / 0.9)
                    button.x -= round(button.w * 0.05)
                    button.y -= round(button.h * 0.05)
                    if button.collidepoint(event.pos):
                        match button.button_type:
                            case 'Start':
                                game.height = int(input_fields[0].user_text)
                                game.width = int(input_fields[1].user_text)
                                game.mines = int(input_fields[2].user_text)
                                start_game(game, game.height, game.width, game.mines)
                pygame.draw.rect(game.window, button.color, button)
                text_surface = base_font.render(button.text_on_button, True, (255, 255, 255))
                game.window.blit(text_surface, (button.x + 5, button.y + 5))
                pygame.display.flip()


def start_game(game: Game, height: int, width: int, mines: int) -> None:
    game.set_desks(height, width, mines)
    game.render_game_desk()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                right_click(game, event.pos[1], event.pos[0])
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game.end_game:
                    show_result_window(game)
                else:
                    left_click(game, event.pos[1], event.pos[0])
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                game.close()


def show_result_window(game: Game):
    pygame.init()
    pygame.display.init()
    game.window = pygame.display.set_mode((300, 150))
    game.window.fill((255, 255, 255))
    base_font = pygame.font.Font(None, 32)
    text_surface = base_font.render(game.end_game_message, True, (0, 0, 0))
    game.window.blit(text_surface, (10, 10))
    pygame.display.update()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                game.close()


def right_click(game: Game, x, y):
    x //= game.cell_size
    y //= game.cell_size
    if game.playerDesk[x][y] == -2:
        game.playerDesk[x][y] = -3
        game.continue_render(x, y, 'Flag')
    elif game.playerDesk[x][y] == -3:
        game.playerDesk[x][y] = -2
        game.continue_render(x, y, 'NotOpened')


def left_click(game, x, y) -> bool:
    x //= game.cell_size
    y //= game.cell_size
    return game.step(x, y)
