import pygame
from Minesweeper import Game, show_game_menu
import sys
sys.setrecursionlimit(5000)


if __name__ == '__main__':
    a = Game()
    show_game_menu(a)
