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
