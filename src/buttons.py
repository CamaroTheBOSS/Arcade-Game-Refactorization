import pygame
import easygui
from sprite import Sprite


class Button(Sprite):
    def __init__(self, x, y, pathImg: str, text="", font=None, dx=0, dy=0):
        super().__init__(x, y, pathImg)
        self.drag = False  # For drag and dropping
        self.selected = False

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
                else:
                    pass
        return 0

    def leftClickHold(self):
        if not self.drag:
            x, y = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:
                if self.hitbox.collidepoint(x, y):
                    self.drag = True
                    return self.onLeftClickHold()
                else:
                    pass
        else:
            return self.onDragging()
        return 0

    def leftClickRelease(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.drag = False
                if self.hitbox.collidepoint(x, y):
                    return self.onLeftClickUp()
                else:
                    pass
        return 0

    def rightClickDown(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                if self.hitbox.collidepoint(x, y):
                    return self.onRightClickDown()
                else:
                    self.selected = False
        return 0

    def onLeftClickDown(self):
        return 0

    def onLeftClickHold(self):
        return 0

    def onDragging(self):
        return 0

    def onLeftClickUp(self):
        return 0

    def onRightClickDown(self):
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


class DraggingObjectButton(Button):
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

    def onRightClickDown(self):
        self.selected = True
        return 1


class EnemyButton(DraggingObjectButton):
    def __init__(self, x, y, pathImg: str, text="", font=None, dx=0, dy=0):
        super().__init__(x, y, pathImg, text=text, font=font, dx=dx, dy=dy)

