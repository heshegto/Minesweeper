import pygame


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
