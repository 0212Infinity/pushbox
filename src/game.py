from sprite import *
from level import *


class Game(object):
    def __init__(self, surface, relativePos, controlType):
        self.surface = surface
        self.relativePos = relativePos
        self.controlType = controlType
        self.level = Level(1)
        self.load_level()

    @property
    def row(self):
        return self.level.row

    @property
    def col(self):
        return self.level.col

    @property
    def map(self):
        return self.level.get_map()

    def load_level(self):
        self.level.load_level()
        self.load_map_sprites()
        self.load_dynamic_sprites()

    def load_map_sprites(self):
        self.mapSprites = []
        for i in range(self.row):
            mapSpritesRow = []
            for j in range(self.col):
                sType = self.map[i][j]
                res = SPRITE_RES[sType]
                spr = Sprite(res, i, j, self.relativePos)
                mapSpritesRow.append(spr)
            self.mapSprites.append(mapSpritesRow)

    def draw(self):
        self.draw_map()
        self.draw_dynamic_sprites()

    def draw_map(self):
        for i in range(self.row):
            for j in range(self.col):
                self.mapSprites[i][j].draw(self.surface)

    def load_sprites(self, sType, posList):
        spriteList = []
        for pos in posList:
            res = SPRITE_RES[sType]
            spr = Sprite(res, pos[0], pos[1], self.relativePos)
            spriteList.append(spr)
        return spriteList

    def load_dynamic_sprites(self):
        self.goalSprites = self.load_sprites(const.SpriteType.GOAL, self.level.get_dynamic_obj_indexes(SpriteType.GOAL))
        self.boxSprites = self.load_sprites(const.SpriteType.BOX, self.level.get_dynamic_obj_indexes(SpriteType.BOX))
        self.playerSprite = \
            self.load_sprites(const.SpriteType.PLAYER, self.level.get_dynamic_obj_indexes(SpriteType.PLAYER))[0]

    def update_dynamic_sprites(self):
        goalIndexes = self.level.get_dynamic_obj_indexes(SpriteType.GOAL)
        boxIndexes = self.level.get_dynamic_obj_indexes(SpriteType.BOX)
        playerIndex = self.level.get_dynamic_obj_indexes(SpriteType.PLAYER)[0]
        for i, goal in enumerate(self.goalSprites):
            goal.update_idx(*goalIndexes[i])
        for i, box in enumerate(self.boxSprites):
            box.update_idx(*boxIndexes[i])
        self.playerSprite.update_idx(*playerIndex)

    def update(self):
        self.update_dynamic_sprites()
        if self.controlType == ControlType.REN:
            self.level.keydown_handler()
            pressed = pygame.key.get_pressed()
            if pressed[K_r]:
                self.load_level()
        else:
            self.level.auto_move()
        if self.level.check_level():
            self.load_level()

    def draw_dynamic_sprites(self):
        for goal in self.goalSprites:
            goal.draw(self.surface)
        for box in self.boxSprites:
            box.draw(self.surface)
        self.playerSprite.draw(self.surface)
