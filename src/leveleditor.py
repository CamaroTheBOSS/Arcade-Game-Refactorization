import sys
import pygame
import easygui
from level import LevelToEdit
from sprite import Sprite


class Button(Sprite):
    def __init__(self, x, y, pathImg: str, text="", font=None, dx=0, dy=0):
        super().__init__(x, y, pathImg)
        self.drag = False  # For drag and dropping

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

    def leftClickDown(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.hitbox.collidepoint(x, y):
                    return self.onLeftClickDown()
        return 0

    def onLeftClickDown(self):
        return 0

    def leftClickHold(self):
        if not self.drag:
            x, y = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:
                if self.hitbox.collidepoint(x, y):
                    self.drag = True
                    return self.onLeftClickHold()
        else:
            return self.onDragging()
        return 0

    def onLeftClickHold(self):
        return 0

    def onDragging(self):
        return 0

    def leftClickRelease(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.drag = False
                if self.hitbox.collidepoint(x, y):
                    return self.onLeftClickUp()
        return 0

    def onLeftClickUp(self):
        return 0

    def setPos(self, position: list):
        self.hitbox.x = position[0]
        self.hitbox.y = position[1]
        self.center[0] = self.img.get_rect().center[0] + position[0]
        self.center[1] = self.img.get_rect().center[1] + position[1]


class ImportLayoutButton(Button):
    def __init__(self, x, y, pathImg: str, text="", font=None, dx=0, dy=0):
        super().__init__(x, y, pathImg, text=text, font=font, dx=dx, dy=dy)

    def onLeftClickDown(self):
        pathToLayout = easygui.fileopenbox()
        if pathToLayout is None:
            return 0
        return pathToLayout


class AddEnemyButton(Button):
    def __init__(self, x, y, pathImg: str, text="", font=None, dx=0, dy=0):
        super().__init__(x, y, pathImg, text=text, font=font, dx=dx, dy=dy)

    def onLeftClickDown(self):
        return EnemyButton(0, 0, "./Graphics/enemy.png")


class EnemyButton(Button):
    def __init__(self, x, y, pathImg: str, text="", font=None, dx=0, dy=0):
        super().__init__(x, y, pathImg, text=text, font=font, dx=dx, dy=dy)

    def onLeftClickHold(self):
        x, y = pygame.mouse.get_pos()
        self.setPos([x - self.hitbox[2] / 2, y - self.hitbox[3] / 2])
        return 1

    def onDragging(self):
        x, y = pygame.mouse.get_pos()
        self.setPos([x - self.hitbox[2] / 2, y - self.hitbox[3] / 2])
        return 1


class LevelEditor:
    def __init__(self, window):
        # Utility
        self.window = window
        self.screenH = self.window.get_height()
        self.screenW = self.window.get_width()
        self.clock = pygame.time.Clock()
        self.running = False
        self.font = pygame.font.SysFont('Calibri', 30, bold=True)

        # Buttons
        self.importLayout = ImportLayoutButton(390, 100, "./Graphics/button.png", "Import layout", self.font, 40, 16)

        smallFont = pygame.font.SysFont('Calibri', 18)
        self.enemyAdder = AddEnemyButton(10, 730, "./Graphics/enemy.png", "Add enemy", smallFont, 40, 10)

        # Level's data to save
        self.level = LevelToEdit()

    def addLayoutEvent(self, event):
        pathToLayout = self.importLayout.leftClickDown(event)
        if pathToLayout:
            self.level.setLayout(pathToLayout)
            if any(ext in pathToLayout[-3:] for ext in ["jpg", "png"]):
                if self.level.layout.get_height() != self.screenH - 100 or \
                        self.level.layout.get_width() != self.screenW:
                    self.level.layout = None
                else:
                    self.importLayout.setPos([-300, -300])

    def addEnemyEvent(self, event):
        newEnemy = self.enemyAdder.leftClickDown(event)
        if newEnemy:
            self.level.Enemies.ListOfObjects.append(newEnemy)
            print("Enemy has been added")

    def update(self):
        self.window.fill((0, 0, 0))

        # Render layout or import layout button
        if self.level.layout is None:
            self.importLayout.show(self.window)
        else:
            self.window.blit(self.level.layout, (0, 0))

        # Render button for adding enemies and enemies
        self.enemyAdder.show(self.window)
        for enemy in self.level.Enemies.ListOfObjects:
            self.window.blit(enemy.img, (enemy.hitbox.x, enemy.hitbox.y))

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
                self.addLayoutEvent(event)
                self.addEnemyEvent(event)

                # Enemy dragging implementation
                for i, enemy in enumerate(self.level.Enemies.ListOfObjects):
                    # 1. leftClickHold returns 1 if enemy is dragged, so first step is to catch this value and
                    # check whether it is equal to 1
                    dragging = enemy.leftClickHold()
                    enemy.leftClickRelease(event)
                    if dragging:
                        # 2. If enemy is dragged, drag him to the start of the list of enemies
                        self.level.Enemies.ListOfObjects.insert(0, enemy)
                        del self.level.Enemies.ListOfObjects[i + 1]
                        break

            self.update()
