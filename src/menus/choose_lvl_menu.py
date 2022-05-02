import pygame
import sys
import os
from data.HUD import HUDelement
import glob


def readFolder(pathToFolder):
    fileNames = []
    pathToFiles = pathToFolder + f"/*.txt"
    for file in glob.glob(pathToFiles):
        normalized_path = os.path.normpath(file)
        fileNames.append(normalized_path.split(os.sep)[-1])

    return fileNames


class ChooseLevelMenu:
    def __init__(self, window):
        self.window = window
        self.optionPointer = 0
        self.options = HUDelement()
        self.font = pygame.font.SysFont('Calibri', 30, bold=True)

        self.levels = readFolder("./Levels")
        self.options.textToRender = []
        self.colors = []
        self.initLevels()

        self.running = True
        self.clock = pygame.time.Clock()

    def initLevels(self):
        self.levels = readFolder("./Levels")
        self.options.textToRender = []
        self.colors = []
        for name in self.levels:
            self.options.textToRender.append(self.font.render(name, True, (255, 255, 255)))
            self.colors.append((255, 255, 255))

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
        for i, name in enumerate(self.levels):
            self.options.textToRender[i] = self.font.render(name, True, self.colors[i])

        for i, option in enumerate(self.options.textToRender):
            self.window.blit(option, (50, 50 + i * 50))
        pygame.display.flip()

    def run(self):
        self.running = True
        self.initLevels()

        # Editor main loop
        while self.running:
            self.clock.tick(60 * 3)
            # Check for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        if len(self.options.textToRender):
                            self.selectUp()
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if len(self.options.textToRender):
                            self.selectDown()
                    elif event.key == pygame.K_RETURN:
                        level = self.levels[self.optionPointer]
                        return level
                    elif event.key == pygame.K_ESCAPE:
                        return "menu"
            self.update()
