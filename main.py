import pygame
from Minesweeper import Game

a = Game()
a.reset_desks(20,20,10)
a.start_render()
running = True
while running:
    a.continue_render()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('gay')
            a.continue_render()
            running = False
a.close()
# if __name__ == '__main__':
#     pygame.init()
#     screen = pygame.display.set_mode((800, 600))
#     pygame.display.set_caption("My Pygame Window")
#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#     pygame.quit()
