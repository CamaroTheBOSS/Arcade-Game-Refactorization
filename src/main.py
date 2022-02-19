import pygame
from level import Level
from player import Player


class LevelEditor:
    pass


class Menu:
    pass


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((1024, 720))
        self.level = None
        self.player = None

    def loadLevel(self, file):
        self.level = Level(file)
        self.player = Player(self.level.playerStartPosition[0],
                             self.level.playerStartPosition[1],
                             "./Graphics/player.png")

    def update(self):  # Render graphics
        self.window.blit(self.level.layout, (0, 0))
        self.window.blit(self.player.img, (self.player.hitbox.x, self.player.hitbox.y))
        pygame.display.flip()

    def run(self):
        running = True

        # Main game loop
        while running:
            # Check for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    print(pygame.key.name(event.key))

            self.update()


if __name__ == '__main__':
    game = Game()
    game.loadLevel("1.txt")
    game.run()
