from sprite import Sprite


class SimpleCollectable(Sprite):
    def __init__(self, x, y, pathImg):
        super().__init__(x, y, pathImg)
        self.collected = False


class Coin(SimpleCollectable):
    def __init__(self, x, y, pathImg):
        super().__init__(x, y, pathImg)


class Key(SimpleCollectable):
    def __init__(self, x, y, pathImg):
        super().__init__(x, y, pathImg)


class Doors(Sprite):
    def __init__(self, doorsX, doorsY, doorsPathImg, keyX, keyY, keyPathImg):
        super().__init__(doorsX, doorsY, doorsPathImg)
        self.open = False
        self.key = Key(keyX, keyY, keyPathImg)



