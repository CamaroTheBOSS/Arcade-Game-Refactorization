import pygame
from game.game import Game
from editor.leveleditor import LevelEditor
from game.summary import SummaryWindow
from menus.menu import Menu
from menus.choose_lvl_menu import ChooseLevelMenu


class PyWindow:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((1024, 820))
        self.gameWindow = Game(self.window)
        self.menuWindow = Menu(self.window)
        self.chooseLevelMenu = ChooseLevelMenu(self.window)
        self.levelEditor = LevelEditor(self.window)
        self.summaryWindow = SummaryWindow(self.window)

    def loadAndRunLevel(self, File):
        self.gameWindow.loadLevel(File)
        w = self.gameWindow.run()
        return w

    def showSummaryWindow(self):
        self.summaryWindow.SetAttributes(self.gameWindow.HUD.score,
                                         self.gameWindow.HUD.deathCounter,
                                         self.gameWindow.HUD.timer)
        self.summaryWindow.SetText(self.gameWindow.font)
        w = self.summaryWindow.show()
        return w


if __name__ == '__main__':
    app = PyWindow()
    x = "menu"
    while True:
        if x == "menu":
            x = app.menuWindow.run()
        elif x == "chooseLevel":
            x = app.chooseLevelMenu.run()
        elif x == "editLevel":
            x = app.levelEditor.run()
        else:
            x = app.loadAndRunLevel(x)
            if x == "WIN":
                x = app.showSummaryWindow()
