import pygame
import sys
from data.HUD import HUDelement


def readFolder(pathToFolder)
    pass


class ChooseLevelMenu:
    def __init__(self, window):
        self.window = window
        self.optionPointer = 0
        self.options = HUDelement()
        self.font = pygame.font.SysFont('Calibri', 30, bold=True)
        self.options.textToRender = []
        self.names = []
        self.colors = []
        self.running = True
        self.clock = pygame.time.Clock()

    def selectDown(self):
        if self.optionPointer >= len(self.options.textToRender) - 1:
            self.optionPointer = 0
        else:
            self.optionPointer += 1

        self.colors[self.optionPointer] = (0, 0, 0)
        self.colors[self.optionPointer - 1] = (255, 255, 255)

    def selectUp(self):
        if self.optionPointer == 0:
            self.optionPointer = len(self.options.textToRender) - 1
            self.colors[self.optionPointer] = (0, 0, 0)
            self.colors[0] = (255, 255, 255)
        else:
            self.optionPointer -= 1
            self.colors[self.optionPointer] = (0, 0, 0)
            self.colors[self.optionPointer + 1] = (255, 255, 255)

    def update(self):
        self.window.fill((23, 125, 105))
        self.options.textToRender = [
            self.font.render(f"Start game", True, self.colors[0]),
            self.font.render(f"Edit level", True, self.colors[1]),
            self.font.render(f"Quit", True, self.colors[2])
        ]
        for i, option in enumerate(self.options.textToRender):
            self.window.blit(option, (50, 50 + i * 50))
        pygame.display.flip()

    def run(self):
        self.running = True

        # Editor main loop
        while self.running:
            self.clock.tick(60 * 3)
            # Check for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.selectUp()
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.selectDown()
                    elif event.key == pygame.K_RETURN:
                        if self.optionPointer == 0:
                            print("start")
                            return "chooseLevel"
                        elif self.optionPointer == 1:
                            print("edit level")
                            return "editLevel"
                        elif self.optionPointer == 2:
                            sys.exit()
            self.update()
