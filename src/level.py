from const import *
from utils import *
from pather import *
import pygame
import random


class Level(object):
    def __init__(self, level):
        self.map = []
        self.dynamicObjIndexes = {
            SpriteType.GOAL: [],
            SpriteType.BOX: [],
            SpriteType.PLAYER: []
        }
        self.row = 1
        self.col = 1
        self.level = level
        self.pressTime = {}
        self.pather = Pather()
        self.load_level()

    def load_level(self):
        self.map = []
        goalIndexes = []
        boxIndexes = []
        playerIndexes = []
        with open('data/level/' + str(self.level) + '.x', 'r') as f:
            lines = f.readlines()
            r, c = lines[0].split(' ')
            self.row = int(r)
            self.col = int(c)
            r = 0
            for line in lines[1:]:
                mapRow = []
                for c in range(self.col):
                    if line[c] == SpriteType.BOX:
                        mapRow.append(SpriteType.FLOOR)
                        boxIndexes.append([r, c])
                    elif line[c] == SpriteType.PLAYER:
                        mapRow.append(SpriteType.FLOOR)
                        playerIndexes.append([r, c])
                    elif line[c] == SpriteType.GOAL:
                        mapRow.append(SpriteType.FLOOR)
                        goalIndexes.append((r, c))
                    else:
                        mapRow.append(line[c])

                self.map.append(mapRow)
                r += 1
        self.dynamicObjIndexes = {
            SpriteType.GOAL: goalIndexes,
            SpriteType.BOX: boxIndexes,
            SpriteType.PLAYER: playerIndexes
        }
        self.pather.start_record(self.level)
        self.autoMoveIndx = 0
        self.lastAutoMoveTime = get_current_time()

    def get_map(self):
        return self.map

    def get_dynamic_obj_indexes(self, sType):
        return self.dynamicObjIndexes[sType]

    def check_and_set_press_time(self, key):
        ret = False
        if get_current_time() - self.pressTime.get(key, 0) > 150:
            ret = True
            self.pressTime[key] = get_current_time()
        return ret

    def keydown_handler(self):
        pressed = pygame.key.get_pressed()
        for i, key in enumerate(DIR_KEY):
            if pressed[key] and self.check_and_set_press_time(key):
                self.move(i)

    def move(self, i):
        playerIndex = self.get_dynamic_obj_indexes(SpriteType.PLAYER)[0]
        r, c = playerIndex[0], playerIndex[1]
        nr = r + DIR[i][0]
        nc = c + DIR[i][1]
        if self.is_floor(nr, nc):
            self.set_player_index(nr, nc)
            self.pather.add_record(i)
        elif self.is_box(nr, nc):
            if self.can_push(nr, nc, i):
                self.push_box(nr, nc, i)
                self.pather.add_record(i)

    def auto_move(self):
        if get_current_time() - self.lastAutoMoveTime > random.randint(500, 1000):
            self.lastAutoMoveTime = get_current_time()
            if self.autoMoveIndx < len(self.pather.get_records()):
                self.move(self.pather.get_records()[self.autoMoveIndx])
                self.autoMoveIndx += 1
            else:
                self.move(random.randint(0, 3))

    def set_player_index(self, r, c):
        playerPos = self.get_dynamic_obj_indexes(SpriteType.PLAYER)
        playerPos[0] = (r, c)

    def is_floor(self, r, c):
        if r < 0 or c < 0:
            return False
        if r >= self.row or c >= self.col:
            return False
        if self.map[r][c] == SpriteType.WALL:
            return False
        for box in self.get_dynamic_obj_indexes(SpriteType.BOX):
            if box[0] == r and box[1] == c:
                return False
        return True

    def is_box(self, r, c):
        for box in self.get_dynamic_obj_indexes(SpriteType.BOX):
            if box[0] == r and box[1] == c:
                return True
        return False

    def can_push(self, r, c, d):
        nr = r + DIR[d][0]
        nc = c + DIR[d][1]
        return self.is_floor(nr, nc)

    def push_box(self, r, c, d):
        for box in self.get_dynamic_obj_indexes(SpriteType.BOX):
            if box[0] == r and box[1] == c:
                nr = r + DIR[d][0]
                nc = c + DIR[d][1]
                if self.is_floor(nr, nc):
                    box[0] = nr
                    box[1] = nc
                    self.set_player_index(r, c)

    def check_finish(self):
        for box in self.get_dynamic_obj_indexes(SpriteType.BOX):
            find = False
            for goal in self.get_dynamic_obj_indexes(SpriteType.GOAL):
                if box[0] == goal[0] and box[1] == goal[1]:
                    find = True
                    break
            if find == False:
                return False
        return True

    def check_level(self):
        if self.check_finish():
            self.pather.dump_record()
            self.level += 1
            self.load_level()
            return True
        return False
