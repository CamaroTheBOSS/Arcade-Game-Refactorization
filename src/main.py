import pygame
from game import Game
from leveleditor import LevelEditor
from summary import SummaryWindow


class PyWindow:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((1024, 820))
        self.gameWindow = Game(self.window)
        self.menuWindow = Menu()
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
    pass


if __name__ == '__main__':
    app = PyWindow()
    app.levelEditor.run()

    # app.loadAndRunLevel("1.txt")
    # app.showSummaryWindow()
    # app.loadAndRunLevel("2.txt")
    # app.showSummaryWindow()
