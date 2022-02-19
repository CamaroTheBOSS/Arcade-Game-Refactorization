from sprite import Sprite


class Player(Sprite):
    def __init__(self, x, y, path):
        super().__init__(x, y, path)
