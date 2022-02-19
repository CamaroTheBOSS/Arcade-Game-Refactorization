import pygame
from level import Level


class LevelEditor:
    pass


class Menu:
    pass


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((1024, 720))
        self.level = None

    def loadLevel(self, file):
        self.level = Level(file)

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    print(pygame.key.name(event.key))

            self.window.blit(self.level.layout, (0, 0))
            pygame.display.flip()


if __name__ == '__main__':
    game = Game()
    game.loadLevel("1.txt")
    game.run()

