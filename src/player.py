from sprite import Sprite


class Player(Sprite):
    def __init__(self, x, y, path):
        super().__init__(x, y, path)
        self.lu = None
        self.ru = None
        self.ld = None
        self.rd = None

    def calculateCornerCoordinates(self):
        self.lu = [self.hitbox.x,
                   self.hitbox.y]
        self.ru = [self.center[0] + int(self.size[1] / 2) - 1,
                   self.center[1] - int(self.size[0] / 2)]
        self.ld = [self.center[0] - int(self.size[1] / 2),
                   self.center[1] + int(self.size[0] / 2) - 1]
        self.rd = [self.center[0] + int(self.size[1] / 2) - 1,
                   self.center[1] + int(self.size[0] / 2) - 1]
