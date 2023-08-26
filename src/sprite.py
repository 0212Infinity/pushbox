import pygame
import const


class Sprite(pygame.sprite.Sprite):
    def __init__(self, imagePath, rowIdx, colIdx, relativePos):
        super(Sprite, self).__init__()
        self.image = pygame.image.load(imagePath)
        self.image = pygame.transform.scale(self.image, (const.SPRITE_SIZE_W, const.SPRITE_SIZE_H))

        self.rect = self.image.get_rect()
        self.relativePos = relativePos
        self.rowIdx = rowIdx
        self.colIdx = colIdx
        self.update_row_idx(rowIdx)
        self.update_col_idx(colIdx)

    def update_row_idx(self, rowIdx):
        self.rowIdx = rowIdx
        self.rect.y = self.relativePos[0] + rowIdx * self.rect.height

    def update_col_idx(self, colIdx):
        self.colIdx = colIdx
        self.rect.x = self.relativePos[1] + colIdx * self.rect.width

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update_idx(self, rowIdx, colIdx):
        self.update_row_idx(rowIdx)
        self.update_col_idx(colIdx)
