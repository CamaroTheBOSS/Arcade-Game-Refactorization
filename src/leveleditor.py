import sys
import pygame
import easygui
from level import LevelToEdit
from sprite import Sprite


class Button(Sprite):
    def __init__(self, x, y, pathImg: str, text="", font=None, dx=0, dy=0):
        super().__init__(x, y, pathImg)

        if font is not None:
            self.text = font.render(text, False, (255, 255, 255))
        else:
            self.text = pygame.font.SysFont('Calibri', 30, bold=True).render(text, False, (255, 255, 255))

        # dx, dy for text translation relative to the img graphic
        self.dx = dx
        self.dy = dy

    def show(self, window: pygame.Surface):
        window.blit(self.img, (self.hitbox.x, self.hitbox.y))
        window.blit(self.text, (self.hitbox.x + self.dx,
                                self.hitbox.y + self.dy))

    def leftClick(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.hitbox.collidepoint(x, y):
                    return self.onLeftClick()
        return 0

    def onLeftClick(self):
        return 0

    def setPos(self, position: list):
        self.hitbox.x = position[0]
        self.hitbox.y = position[1]
        self.center[0] = self.img.get_rect().center[0] + position[0]
        self.center[1] = self.img.get_rect().center[1] + position[1]


class ImportLayoutButton(Button):
    def __init__(self, x, y, pathImg: str, text="", font=None, dx=0, dy=0):
        super().__init__(x, y, pathImg, text=text, font=font, dx=dx, dy=dy)

    def onLeftClick(self):
        pathToLayout = easygui.fileopenbox()
        if pathToLayout is None:
            return 0
        return pathToLayout


class LevelEditor:
    def __init__(self, window):
        # Utility
        self.window = window
        self.screenH = self.window.get_height()
        self.screenW = self.window.get_width()
        self.clock = pygame.time.Clock()
        self.running = False

        # Buttons
        self.font = pygame.font.SysFont('Calibri', 30, bold=True)
        self.importLayout = ImportLayoutButton(390, 100, "./Graphics/button.png", "Import layout", self.font, 40, 16)

        # Level's data to save
        self.level = LevelToEdit()

    def checkImportLayoutEvent(self, event):
        pathToLayout = self.importLayout.leftClick(event)
        if pathToLayout:
            self.level.setLayout(pathToLayout)
            if any(ext in pathToLayout[-3:] for ext in ["jpg", "png"]):
                if self.level.layout.get_height() != self.screenH - 100 or \
                        self.level.layout.get_width() != self.screenW:
                    self.level.layout = None
                else:
                    self.importLayout.setPos([-300, -300])

    def update(self):
        self.window.fill((0, 0, 0))

        if self.level.layout is None:
            self.importLayout.show(self.window)
        else:
            self.window.blit(self.level.layout, (0, 0))
        pygame.display.flip()

    def run(self):
        self.running = True

        # Editor main loop
        while self.running:
            self.clock.tick(60 * 3)
            mouse = pygame.mouse.get_pos()
            # Check for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                self.checkImportLayoutEvent(event)

            self.update()
