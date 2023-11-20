import pygame
from Minesweeper.menu_fields import InputField, Button
from Minesweeper import Game

background_color = (255, 255, 255)


def show_game_menu(game: Game):
    pygame.init()
    pygame.display.init()
    game.window = pygame.display.set_mode((300, 300))
    game.window.fill(background_color)
    # basic font for user typed
    base_font = pygame.font.Font(None, 32)

    greetings_font = pygame.font.Font(None, 40)
    greetings_text = greetings_font.render("Minesweeper", True, (0, 0, 0))

    text_1 = base_font.render("Height", True, (0, 0, 0))
    text_2 = base_font.render("Width", True, (0, 0, 0))
    text_3 = base_font.render("Mines", True, (0, 0, 0))

    game.window.blit(greetings_text, (75, 10))
    game.window.blit(text_1, (25, 105))
    game.window.blit(text_2, (25, 155))
    game.window.blit(text_3, (25, 205))

    # Fields in which player set desk height, desk width and amount of mines
    input_fields = [InputField(142, 100, 140, 32, 'height'),
                    InputField(142, 150, 140, 32, 'width'),
                    InputField(142, 200, 140, 32, 'mines')
                    ]

    buttons = [Button(80, 250, 130, 32, text_on_button="Start game", button_type='Start'),
               Button(25, 50, 62, 32, text_on_button="Easy", button_type='Easy'),
               Button(107, 50, 92, 32, text_on_button="Medium", button_type='Medium'),
               Button(219, 50, 62, 32, text_on_button="Hard", button_type='Hard'),
               ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                game.close()

            # Input fields logic
            for field in input_fields:
                # Making field active
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if field.collidepoint(event.pos):
                        field.active = True
                        field.text = ''
                    else:
                        field.active = False
                        if field.text == '':
                            field.text = field.default_value

                # Logic when player typing something in Input Fields
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE and field.active:
                        field.text = field.text[:-1]
                    elif event.unicode.isdigit() and field.active:
                        field.text += event.unicode

                    elif event.key == pygame.K_KP_ENTER:
                        field.active = False
                        if field.text == '':
                            field.text = field.default_value

                # Max number that field can contain in itself
                if field.information_type != 'mines' and field.text.isdigit() and int(field.text) > 50:
                    field.text = "50"
                if field.information_type == 'mines' and field.text.isdigit() and int(field.text) > 100:
                    field.text = "100"

                # Coloring active and passive fields
                if field.active:
                    field.color = field.color_active
                else:
                    field.color = field.color_passive

                # draw rectangle and argument passed which should be on screen
                draw(game.window, field.color, field)

            for button in buttons:
                if event.type == pygame.MOUSEMOTION:
                    if button.collidepoint(event.pos):
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
                    button.pressed = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if button.pressed:
                        button.w = round(button.w / 0.9)
                        button.h = round(button.h / 0.9)
                        button.x -= round(button.w * 0.05)
                        button.y -= round(button.h * 0.05)
                        button.pressed = False
                    if button.collidepoint(event.pos):
                        match button.button_type:
                            case 'Start':
                                game.height = int(input_fields[0].text)
                                game.width = int(input_fields[1].text)
                                game.mines = int(input_fields[2].text)
                                start_game(game, game.height, game.width, game.mines)
                            case 'Easy':
                                input_fields[0].text, input_fields[1].text, input_fields[2].text = '8', '10', '10'
                                draw(game.window, input_fields[0].color, input_fields[0])
                                draw(game.window, input_fields[1].color, input_fields[1])
                                draw(game.window, input_fields[2].color, input_fields[2])
                            case 'Medium':
                                input_fields[0].text, input_fields[1].text, input_fields[2].text = '14', '18', '40'
                                draw(game.window, input_fields[0].color, input_fields[0])
                                draw(game.window, input_fields[1].color, input_fields[1])
                                draw(game.window, input_fields[2].color, input_fields[2])
                            case 'Hard':
                                input_fields[0].text, input_fields[1].text, input_fields[2].text = '20', '24', '99'
                                draw(game.window, input_fields[0].color, input_fields[0])
                                draw(game.window, input_fields[1].color, input_fields[1])
                                draw(game.window, input_fields[2].color, input_fields[2])

                draw(game.window, button.color, button)


def draw(window, color, thing):
    base_font = pygame.font.Font(None, 32)
    pygame.draw.rect(window, color, thing)
    text_surface = base_font.render(thing.text, True, (255, 255, 255))

    # render at position stated in arguments
    window.blit(text_surface, (thing.x + 5, thing.y + 5))

    # set width of textfield so that text cannot get outside of user's text input
    # field.w = max(140, text_surface.get_width() + 10)
    pygame.display.flip()


def start_game(game: Game, height: int, width: int, mines: int) -> None:
    game.set_desks(height, width, mines)
    game.render_game_desk()

    ac_x = 0  # x dimension of active cell
    ac_y = 0  # y dimension of active cell

    # Logic when you push cells with different mouse buttons
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                ac_x = event.pos[1] // game.cell_size
                ac_y = event.pos[0] // game.cell_size
                if game.playerDesk[ac_x][ac_y] == -2:
                    game.continue_render(ac_x, ac_y, 'ActiveCell')
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos[1], event.pos[0]
                x //= game.cell_size
                y //= game.cell_size

                # This variable makes sure that button pushed and released at the same cell
                cell_activated = (ac_x == x) and (ac_y == y)

                # Push any mouse button to leave the game in the end
                if game.end_game and event.button:
                    show_result_window(game)

                if event.button == 3:
                    right_click(game, x, y)
                elif event.button == 1 and cell_activated:
                    left_click(game, x, y)
                elif game.playerDesk[ac_x][ac_y] == -2:
                    game.continue_render(ac_x, ac_y, 'NotOpened')

            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                game.close()


def show_result_window(game: Game):
    pygame.init()
    pygame.display.init()
    game.window = pygame.display.set_mode((252, 150))
    game.window.fill(background_color)
    base_font = pygame.font.Font(None, 32)
    text_surface = base_font.render(game.end_game_message, True, (0, 0, 0))

    restart_button = Button(80, 50, 92, 32, text_on_button="Restart", button_type='Restart')
    exit_button = Button(95, 100, 62, 32, text_on_button="Exit", button_type='Exit')

    game.window.blit(text_surface, (10, 10))
    pygame.display.update()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                game.close()
            for button in [restart_button, exit_button]:
                if event.type == pygame.MOUSEMOTION:
                    if button.collidepoint(event.pos):
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
                    button.pressed = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if button.pressed:
                        button.w = round(button.w / 0.9)
                        button.h = round(button.h / 0.9)
                        button.x -= round(button.w * 0.05)
                        button.y -= round(button.h * 0.05)
                        button.pressed = False
                    if button.collidepoint(event.pos):
                        match button.button_type:
                            case 'Restart':
                                show_game_menu(game)
                            case 'Exit':
                                running = False
                                game.close()
                draw(game.window, button.color, button)



def right_click(game: Game, x, y):
    if game.playerDesk[x][y] == -2:
        game.playerDesk[x][y] = -3
        game.continue_render(x, y, 'Flag')
    elif game.playerDesk[x][y] == -3:
        game.playerDesk[x][y] = -2
        game.continue_render(x, y, 'NotOpened')


def left_click(game, x, y) -> bool:
    return game.step(x, y)
