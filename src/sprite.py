import pygame


class Sprite:
    def __init__(self, x, y, path):
        self.img = pygame.image.load(path).convert_alpha()
        self.hitbox = self.img.get_rect()
        self.hitbox.x = x
        self.hitbox.y = y
        self.center = [self.img.get_rect().center[0] + self.hitbox.x, self.img.get_rect().center[1] + self.hitbox.y]
        self.size = self.img.get_size()
        print(".")
