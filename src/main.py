import pygame
from game.game import Game
from editor.leveleditor import LevelEditor
from game.summary import SummaryWindow
import sys
import os


class PyWindow:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((1024, 820))
        self.gameWindow = Game(self.window)
        self.menuWindow = Menu(self.window)
        self.levelEditor = LevelEditor(self.window)
        self.summaryWindow = SummaryWindow(self.window)

    def loadAndRunLevel(self, File):
        self.gameWindow.loadLevel(File)
        self.gameWindow.run()

    def showSummaryWindow(self):
        self.summaryWindow.SetAttributes(self.gameWindow.HUD.score,
                                         self.gameWindow.HUD.deathCounter,
                                         self.gameWindow.HUD.timer)
        self.summaryWindow.SetText(self.gameWindow.font)
        self.summaryWindow.show()


class Menu:
    def __init__(self, window):
        self.window = window
        self.optionPointer = 0
        self.options = []
        self.running = False
        self.clock = pygame.time.Clock()

    def selectUp(self):
        if self.optionPointer >= len(self.options) - 1:
            self.optionPointer = 0
        else:
            self.optionPointer += 1

    def selectDown(self):
        if self.optionPointer == 0:
            self.optionPointer = len(self.options) - 1
        else:
            self.optionPointer -= 1

    def update(self):
        pass

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

            self.update()


if __name__ == '__main__':
    app = PyWindow()
    # app.levelEditor.run()

    app.loadAndRunLevel("1.txt")
    app.showSummaryWindow()
    app.loadAndRunLevel("2.txt")
    app.showSummaryWindow()
