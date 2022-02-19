import pygame


class LevelEditor:
    pass


class Menu:
    pass


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((1024, 720))
        self.level = None

    def loadLevel(self):
        pass

    def run(self, level):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    print(pygame.key.name(event.key))

            self.window.fill((255, 255, 255))


if __name__ == '__main__':
    game = Game()
    game.run()

