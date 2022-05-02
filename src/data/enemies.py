from data.sprite import MovingSprite


class SimpleEnemy(MovingSprite):
    def __init__(self, x, y, pathImg):
        super().__init__(x, y, pathImg)
