import pygame
from Minesweeper import Game
if __name__ == '__main__':
    a = Game()
    a.set_desks(20,10,10)
    a.start_render()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                a.right_click(event.pos[1], event.pos[0])
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                a.left_click(event.pos[1], event.pos[0])
            if event.type == pygame.QUIT:
                running = False

    a.close()
