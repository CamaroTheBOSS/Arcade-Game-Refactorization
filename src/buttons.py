import pygame
import easygui
from sprite import Sprite


class TextInputBox:
    def __init__(self, x, y, w, h):
        self.box = pygame.Rect(x, y, w, h)
        self.active = False
        self.text = "Level name"


class Button(Sprite):
    def __init__(self, x, y, pathImg: str, text="", font=None, dx=0, dy=0):
        super().__init__(x, y, pathImg)
        self.drag = False  # For drag and dropping
        self.selected = False

        if font is not None:
            self.text = font.render(text, False, (255, 255, 255))
        else:
            self.text = pygame.font.SysFont('Calibri', 30, bold=True).render(text, False, (255, 255, 255))

        self.strText = text
        # dx, dy for text translation relative to the img graphic
        self.dx = dx
        self.dy = dy

    def changeText(self, text, font=None):
        self.strText = text
        if font is not None:
            self.text = font.render(text, False, (255, 255, 255))
        else:
            self.text = pygame.font.SysFont('Calibri', 30, bold=True).render(text, False, (255, 255, 255))

    def changeFont(self, font=None):
        self.text = font.render(self.strText, False, (255, 255, 255))

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
                    self.onSelecting()
        return 0

    def onLeftClickDown(self):
        return 0

    def onLeftClickHold(self):
        return 0

    def onDragging(self):
        return 0

    def onSelecting(self):
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

    def changePos(self, position: list):
        self.hitbox.x -= position[0]
        self.hitbox.y -= position[1]
        self.center[0] -= position[0]
        self.center[1] -= position[1]


class ImportLayoutButton(Button):
    def __init__(self, x, y, pathImg: str, text="", font=None, dx=0, dy=0):
        super().__init__(x, y, pathImg, text=text, font=font, dx=dx, dy=dy)

    def onLeftClickDown(self):
        pathToLayout = easygui.fileopenbox()
        if pathToLayout is None:
            return 0
        return pathToLayout


class SaveLevelButton(Button):
    def __init__(self, x, y, pathImg: str, text="", font=None, dx=0, dy=0):
        super().__init__(x, y, pathImg, text=text, font=font, dx=dx, dy=dy)

    def onLeftClickDown(self):

        return 1


class AddEnemyButton(Button):
    def __init__(self, x, y, pathImg: str, text="", font=None, dx=0, dy=0):
        super().__init__(x, y, pathImg, text=text, font=font, dx=dx, dy=dy)

    def onLeftClickDown(self):
        return EnemyButton(0, 0, "./Graphics/enemy.png")


class AddPathPointButton(Button):
    def __init__(self, x, y, pathImg: str, text="", font=None, dx=0, dy=0):
        super().__init__(x, y, pathImg, text=text, font=font, dx=dx, dy=dy)

    def onLeftClickDown(self):
        return 1


class AddCoinButton(Button):
    def __init__(self, x, y, pathImg: str, text="", font=None, dx=0, dy=0):
        super().__init__(x, y, pathImg, text=text, font=font, dx=dx, dy=dy)

    def onLeftClickDown(self):
        return CoinButton(0, 0, "./Graphics/coin.png")


class DeleteButton(Button):
    def __init__(self, x, y, pathImg: str, text="", font=None, dx=0, dy=0):
        super().__init__(x, y, pathImg, text=text, font=font, dx=dx, dy=dy)

    def onLeftClickDown(self):
        return 1


class SwitchPathTypeButton(Button):
    def __init__(self, x, y, pathImg: str, text="", font=None, dx=0, dy=0):
        super().__init__(x, y, pathImg, text=text, font=font, dx=dx, dy=dy)

    def onLeftClickDown(self):
        return 1


# Class for objects we can drag
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
        return 1


# Class for deletable objects like coins and enemies
class Deletable(DraggingObjectButton):
    def __init__(self, x, y, pathImg: str, text="", font=None, dx=0, dy=0):
        super().__init__(x, y, pathImg, text=text, font=font, dx=dx, dy=dy)


class PlayerButton(DraggingObjectButton):
    def __init__(self, x, y, pathImg: str, text="", font=None, dx=0, dy=0):
        super().__init__(x, y, pathImg, text=text, font=font, dx=dx, dy=dy)


class KeyButton(DraggingObjectButton):
    def __init__(self, x, y, pathImg: str, text="", font=None, dx=0, dy=0):
        super().__init__(x, y, pathImg, text=text, font=font, dx=dx, dy=dy)


class DoorsButton(DraggingObjectButton):
    def __init__(self, x, y, pathImg: str, text="", font=None, dx=0, dy=0):
        super().__init__(x, y, pathImg, text=text, font=font, dx=dx, dy=dy)


class CheckPointSpawnerButton(DraggingObjectButton):
    def __init__(self, x, y, pathImg: str, text="", font=None, dx=0, dy=0):
        super().__init__(x, y, pathImg, text=text, font=font, dx=dx, dy=dy)


class CoinButton(Deletable):
    def __init__(self, x, y, pathImg: str, text="", font=None, dx=0, dy=0):
        super().__init__(x, y, pathImg, text=text, font=font, dx=dx, dy=dy)


class EnemyButton(Deletable):
    def __init__(self, x, y, pathImg: str, text="", font=None, dx=0, dy=0):
        super().__init__(x, y, pathImg, text=text, font=font, dx=dx, dy=dy)
        self.path = PathChain(x, y, self)

    def onLeftClickHold(self):
        x, y = pygame.mouse.get_pos()
        dx = self.hitbox.x - x + self.hitbox[2] / 2
        dy = self.hitbox.y - y + self.hitbox[3] / 2

        self.setPos([x - self.hitbox[2] / 2, y - self.hitbox[3] / 2])
        for pathPoint in self.path.pathPoints:
            pathPoint.changePos([dx, dy])

        return 1

    def onDragging(self):
        x, y = pygame.mouse.get_pos()
        dx = self.hitbox.x - x + self.hitbox[2] / 2
        dy = self.hitbox.y - y + self.hitbox[3] / 2

        self.setPos([x - self.hitbox[2] / 2, y - self.hitbox[3] / 2])
        for pathPoint in self.path.pathPoints:
            pathPoint.changePos([dx, dy])

        return 1


class PathPoint(Deletable):
    def __init__(self, x, y, pathImg: str, enemy, text="", font=None, dx=0, dy=0):
        super().__init__(x, y, pathImg, text=text, font=font, dx=dx, dy=dy)
        self.rendered = True
        self.owner = enemy

    def __eq__(self, other):
        if self.center == other.center:
            return True
        return False

    def onDragging(self):
        if self.rendered:
            x, y = pygame.mouse.get_pos()
            self.setPos([x - self.hitbox[2] / 2, y - self.hitbox[3] / 2])
            return 1

    def onLeftClickHold(self):
        if self.rendered:
            x, y = pygame.mouse.get_pos()
            self.setPos([x - self.hitbox[2] / 2, y - self.hitbox[3] / 2])
            return 1


class PathChain:
    def __init__(self, startX, startY, enemy, color=(255, 100, 20)):
        self.owner = enemy
        self.pathPoints = [PathPoint(startX, startY, "./Graphics/pathPointAdd.png", self.owner)]
        self.color = color
        self.pathType = "repeat"

    def addPoint(self):
        point = PathPoint(self.pathPoints[-1].hitbox.x + 100, self.pathPoints[-1].hitbox.y,
                          "./Graphics/pathPointAdd.png", self.owner)
        self.pathPoints.append(point)
        return point

    def delete(self, index):
        del self.pathPoints[index]

    def switchPathType(self):
        self.pathType = "repeat" if self.pathType == "reverse" else "reverse"

