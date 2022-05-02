import pygame
from game.game import Game
from editor.leveleditor import LevelEditor
from game.summary import SummaryWindow
from menus.menu import Menu


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


if __name__ == '__main__':
    app = PyWindow()
    x = "menu"
    while True:
        if x == "menu":
            x = app.menuWindow.run()
        elif x == "chooseLevel":
            pass
        elif x == "editLevel":
            app.levelEditor.run()

        # app.loadAndRunLevel("1.txt")
        # app.showSummaryWindow()
        # app.loadAndRunLevel("2.txt")
        # app.showSummaryWindow()
