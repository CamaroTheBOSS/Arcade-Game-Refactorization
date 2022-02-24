from sprite import Sprite


class Player(Sprite):
    def __init__(self, x, y, pathImg):
        super().__init__(x, y, pathImg)
        self.lu = None
        self.ru = None
        self.ld = None
        self.rd = None
        self.ghost = Ghost(0, 0, "./Graphics/player replay.png")

    def calculateCornerCoordinates(self):
        self.lu = [self.hitbox.x,
                   self.hitbox.y]
        self.ru = [self.center[0] + int(self.size[1] / 2) - 1,
                   self.center[1] - int(self.size[0] / 2)]
        self.ld = [self.center[0] - int(self.size[1] / 2),
                   self.center[1] + int(self.size[0] / 2) - 1]
        self.rd = [self.center[0] + int(self.size[1] / 2) - 1,
                   self.center[1] + int(self.size[0] / 2) - 1]

    def changePosition(self, position: list):
        self.hitbox.x = position[0]
        self.hitbox.y = position[1]
        self.center[0] = self.img.get_rect().center[0] + position[0]
        self.center[1] = self.img.get_rect().center[1] + position[1]

    def collectData(self):
        x = self.hitbox.x
        y = self.hitbox.y
        self.ghost.collectedData.append((x, y))


class Ghost(Sprite):
    def __init__(self, x, y, path):
        super().__init__(x, y, path)
        self.collectedData = []
        self.dataToReplay = []
        self.frame = 0
        self.isPlaying = False

    def startReplay(self):
        self.dataToReplay = self.collectedData.copy()
        self.frame = 0
        self.collectedData = []
        self.isPlaying = True

