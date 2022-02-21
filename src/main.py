import pygame
from level import Level
from player import Player


# function used for collision detection
def inequality(a: list, b: list):
    for i in range(b.__len__()):
        if a[i] != b[i]:
            return True
    return False


class LevelEditor:
    pass


class Menu:
    pass


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((1024, 720))
        self.clock = pygame.time.Clock()
        self.level = None
        self.player = None

    def loadLevel(self, file):
        self.level = Level(file)
        self.player = Player(self.level.playerStartPosition[0],
                             self.level.playerStartPosition[1],
                             "./Graphics/player.png")

    def playerCollisions(self):
        self.player.calculateCornerCoordinates()

        # Collisions with walls
        keys = pygame.key.get_pressed()
        data = self.level.layoutData
        # Move only when pixels are not in specific color
        if inequality((data[self.player.ru[0] + 1, self.player.ru[1]]), self.level.color.wall) and \
                inequality((data[self.player.rd[0] + 1, self.player.rd[1]]), self.level.color.wall):
            self.player.center[0] += keys[pygame.K_RIGHT]
            self.player.hitbox.x += keys[pygame.K_RIGHT]

        if inequality((data[self.player.lu[0] - 1, self.player.lu[1]]), self.level.color.wall) and \
                inequality((data[self.player.ld[0] - 1, self.player.ld[1]]), self.level.color.wall):
            self.player.center[0] -= keys[pygame.K_LEFT]
            self.player.hitbox.x -= keys[pygame.K_LEFT]

        if inequality((data[self.player.ld[0], self.player.ld[1] + 1]), self.level.color.wall) and \
                inequality((data[self.player.rd[0], self.player.rd[1] + 1]), self.level.color.wall):
            self.player.center[1] += keys[pygame.K_DOWN]
            self.player.hitbox.y += keys[pygame.K_DOWN]

        if inequality((data[self.player.ru[0], self.player.ru[1] - 1]), self.level.color.wall) and \
                inequality((data[self.player.lu[0], self.player.lu[1] - 1]), self.level.color.wall):
            self.player.center[1] -= keys[pygame.K_UP]
            self.player.hitbox.y -= keys[pygame.K_UP]

        # Collisions with checkpoints
        if not inequality((data[self.player.ru[0], self.player.ru[1]]), self.level.color.checkpoint) or \
                not inequality((data[self.player.lu[0], self.player.lu[1]]), self.level.color.checkpoint) or \
                not inequality((data[self.player.ld[0], self.player.ld[1]]), self.level.color.checkpoint) or \
                not inequality((data[self.player.rd[0], self.player.rd[1]]), self.level.color.checkpoint):
            self.level.checkpointReached = True
            print("Checkpoint reached")

        # Collisions with win area
        if not inequality((data[self.player.ru[0], self.player.ru[1]]), self.level.color.win) or \
                not inequality((data[self.player.lu[0], self.player.lu[1]]), self.level.color.win) or \
                not inequality((data[self.player.ld[0], self.player.ld[1]]), self.level.color.win) or \
                not inequality((data[self.player.rd[0], self.player.rd[1]]), self.level.color.win):
            print("WIN")
            self.loadLevel("2.txt")

        # Collisions with enemies
        if self.player.hitbox.collidelist(self.level.Enemies.ListOfHitboxes) != -1:
            if not self.level.checkpointReached:
                self.player.changePosition(self.level.playerStartPosition)
            else:
                self.player.changePosition(self.level.checkpointRespawnPosition)

        # Collisions with coins
        CollisionIndex = self.player.hitbox.collidelist(self.level.Coins.ListOfHitboxes)
        if CollisionIndex != -1:
            self.level.Coins.ListOfObjects[CollisionIndex].collected = True
            self.level.Coins.ListOfObjects[CollisionIndex].hitbox.x = -40
            self.level.Coins.ListOfObjects[CollisionIndex].hitbox.y = -40

        if self.level.Doors is not None:
            # Collisions with key
            if self.player.hitbox.collidelist([self.level.Doors.key.hitbox]) != -1:
                self.level.Doors.key.collected = True
                print("Klucyk")

            # Collisions with doors
            if self.player.hitbox.collidelist([self.level.Doors.hitbox]) != -1 and self.level.Doors.key.collected:
                self.level.Doors.open = True
                self.level.Doors = None

    def update(self):
        # Rendering layout and player
        self.window.blit(self.level.layout, (0, 0))
        self.window.blit(self.player.img, (self.player.hitbox.x, self.player.hitbox.y))

        # Rendering enemies and updating their current position
        for enemy in self.level.Enemies.ListOfObjects:
            self.window.blit(enemy.img, (enemy.hitbox.x, enemy.hitbox.y))
            enemy.nextPathPoint()

        # Rendering coins
        for coin in self.level.Coins.ListOfObjects:
            self.window.blit(coin.img, (coin.hitbox.x, coin.hitbox.y))

        # Rendering doors and key
        if self.level.Doors is not None:
            if not self.level.Doors.open:
                self.window.blit(self.level.Doors.img, (self.level.Doors.hitbox.x,
                                                        self.level.Doors.hitbox.y))
            if not self.level.Doors.key.collected:
                self.window.blit(self.level.Doors.key.img, (self.level.Doors.key.hitbox.x,
                                                            self.level.Doors.key.hitbox.y))

        pygame.display.flip()

    def run(self):
        running = True

        # Main game loop
        while running:
            self.clock.tick(60 * 3)
            # Check for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    print(pygame.key.name(event.key))
            self.playerCollisions()
            self.update()


if __name__ == '__main__':
    game = Game()
    game.loadLevel("1.txt")
    game.run()
