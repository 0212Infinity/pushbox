import sys
from game import *
import const

pygame.init()
DISPLAYSURF = pygame.display.set_mode((const.GAME_WIDTH_SIZE, const.GAME_HEIGHT_SIZE))
gameRen = Game(DISPLAYSURF, (100, 500), const.ControlType.REN)
gameJi = Game(DISPLAYSURF, (100, 20), const.ControlType.JI)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    gameRen.update()
    gameJi.update()
    DISPLAYSURF.fill((0, 0, 0))
    gameRen.draw()
    gameJi.draw()
    if gameJi.level.level > gameRen.level.level:
        DISPLAYSURF.fill((0, 0, 0))
        image = pygame.image.load('res/lose.png')
        DISPLAYSURF.blit(image, image.get_rect())
    pygame.display.update()
