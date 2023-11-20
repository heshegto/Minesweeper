import pygame


class InputField(pygame.Rect):
    def __init__(self, left, top, width, height, information_type, default_value='15'):
        super().__init__(left, top, width, height)
        self.information_type = information_type

        self.active = False
        self.text = default_value
        self.default_value = default_value
        self.color_active = pygame.Color('lightskyblue3')
        self.color_passive = pygame.Color('chartreuse4')

        self.color = self.color_passive
    
    def field_logic(self, event: pygame.event):
        # Making Field active
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.collidepoint(event.pos):
                self.active = True
                self.text = ''
            else:
                self.active = False
                if self.text == '':
                    self.text = self.default_value

        # Logic when player typing something in Input Fields
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and self.active:
                self.text = self.text[:-1]
            elif event.unicode.isdigit() and self.active:
                self.text += event.unicode

            elif event.key == pygame.K_KP_ENTER:
                self.active = False
                if self.text == '':
                    self.text = self.default_value

        # Max number that Field can contain in itself
        if self.information_type != 'mines' and self.text.isdigit() and int(self.text) > 50:
            self.text = "50"
        if self.information_type == 'mines' and self.text.isdigit() and int(self.text) > 100:
            self.text = "100"

        # Coloring active and passive Fields
        if self.active:
            self.color = self.color_active
        else:
            self.color = self.color_passive
    

class Button(pygame.Rect):
    def __init__(self, left, top, width, height, text_on_button, button_type):
        super().__init__(left, top, width, height)
        self.text = text_on_button
        self.button_type = button_type
        self.active = False
        self.pressed = False
        self.active_color = (170, 170, 170)
        self.passive_color = (100, 100, 100)
        self.color = self.passive_color

    def is_pressed(self, window: pygame.display, event: pygame.event):
        if event.type == pygame.MOUSEMOTION:
            if self.collidepoint(event.pos):
                self.active = True
                self.color = self.active_color
            else:
                self.active = False
                self.color = self.passive_color
        if event.type == pygame.MOUSEBUTTONDOWN and self.collidepoint(event.pos):
            pygame.draw.rect(window, (255, 255, 255), self)
            self.x += round(self.w * 0.05)
            self.y += round(self.h * 0.05)
            self.w = round(0.9 * self.w)
            self.h = round(0.9 * self.h)
            self.pressed = True
        if event.type == pygame.MOUSEBUTTONUP:
            if self.pressed:
                self.w = round(self.w / 0.9)
                self.h = round(self.h / 0.9)
                self.x -= round(self.w * 0.05)
                self.y -= round(self.h * 0.05)
                self.pressed = False
            if self.collidepoint(event.pos):
                return True
        return False
