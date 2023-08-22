import pygame
from Minesweeper import Game
import sys
sys.setrecursionlimit(5000)

if __name__ == '__main__':
    a = Game()
    a.show_menu()
    # a.start_game(50, 95, 500)
