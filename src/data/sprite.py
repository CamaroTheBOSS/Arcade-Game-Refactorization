import pygame


class Sprite:
    def __init__(self, x, y, pathImg):
        self.img = pygame.image.load(pathImg).convert_alpha()
        self.hitbox = self.img.get_rect()
        self.hitbox.x = x
        self.hitbox.y = y
        self.center = [self.img.get_rect().center[0] + self.hitbox.x, self.img.get_rect().center[1] + self.hitbox.y]
        self.size = self.img.get_size()
        print(".")


class MovingSprite(Sprite):
    def __init__(self, x, y, pathImg):
        super().__init__(x, y, pathImg)
        self.pathway = []
        self.pathType = None
        self.currentPathPoint = 0
        self.reverse = False

    def buildPath(self, startPos: tuple, waypoints: list, pathType='reverse'):
        self.pathType = pathType
        self.pathway.append([startPos[0], startPos[1]])
        # waypoints are stored in relative form, so firstly it is needed to add enemy start position to each waypoint
        for way in waypoints:
            way[0] += startPos[0]
            way[1] += startPos[1]
            self.pathway.append(way)

        # if we want enemy to repeat the path we  need to add one more point to the path start
        if self.pathType == 'repeat':
            self.pathway.append([startPos[0], startPos[1]])

    def nextPathPoint(self):
        if self.hitbox.x < self.pathway[self.currentPathPoint][0]:
            self.hitbox.x += 1
        elif self.hitbox.x > self.pathway[self.currentPathPoint][0]:
            self.hitbox.x -= 1
        if self.hitbox.y < self.pathway[self.currentPathPoint][1]:
            self.hitbox.y += 1
        elif self.hitbox.y > self.pathway[self.currentPathPoint][1]:
            self.hitbox.y -= 1

        if self.hitbox.x == self.pathway[self.currentPathPoint][0] and \
                self.hitbox.y == self.pathway[self.currentPathPoint][1]:

            if self.currentPathPoint == len(self.pathway) - 1:
                if self.pathType == 'repeat':
                    self.currentPathPoint = 0
                else:
                    self.reverse = True
            elif self.currentPathPoint == 0:
                self.reverse = False

            if not self.reverse:
                self.currentPathPoint += 1
            else:
                self.currentPathPoint -= 1


# Class for interactive lists of objects
class ObjectsContainer:
    def __init__(self):
        self.ListOfObjects = []
        self.ListOfHitboxes = []
