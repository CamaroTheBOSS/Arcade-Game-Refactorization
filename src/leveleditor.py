import sys
import pygame
from level import LevelToEdit
from buttons import ImportLayoutButton, AddEnemyButton, AddCoinButton, PlayerButton, KeyButton, DoorsButton, \
    DeleteButton, Deletable, AddPathPointButton, EnemyButton, PathPoint, SwitchPathTypeButton, TextInputBox, \
    SaveLevelButton, CheckPointSpawnerButton, CoinButton


class LevelEditor:
    def __init__(self, window):
        # Utility
        self.window = window
        self.screenH = self.window.get_height()
        self.screenW = self.window.get_width()
        self.clock = pygame.time.Clock()
        self.running = False
        self.font = pygame.font.SysFont('Calibri', 30, bold=True)
        self.smallFont = pygame.font.SysFont('Calibri', 18)

        # Buttons
        self.importLayout = ImportLayoutButton(390, 100, "./Graphics/button.png", "Import layout", self.font, 40, 16)
        self.saveLevel = SaveLevelButton(735, 735, "./Graphics/button.png", "Save level", self.font, 60, 16)
        self.enemyAdder = AddEnemyButton(10, 730, "./Graphics/enemy.png", "Add enemy", self.smallFont, 40, 10)
        self.pathPointAdder = AddPathPointButton(200, 730, "./Graphics/pathPointAdd.png", "Add path point",
                                                 self.smallFont, 40, 10)
        self.switchPathTypeButton = SwitchPathTypeButton(500, 730, "./Graphics/switchPathType.png", "Change path type",
                                                         self.smallFont, 40, 10)
        self.coinAdder = AddCoinButton(10, 775, "./Graphics/coin.png", "Add coin", self.smallFont, 40, 10)
        self.deleteButton = DeleteButton(200, 775, "./Graphics/delete.png", "Delete object", self.smallFont, 40, 10)
        self.playerButton = PlayerButton(100, 100, "./Graphics/player.png")
        self.keyButton = KeyButton(100, 150, "./Graphics/key.png")
        self.doorsButton = DoorsButton(100, 200, "./Graphics/doors.png")
        self.checkPointSpawner = CheckPointSpawnerButton(200, 100, "./Graphics/checkPointSpawn.png")

        # Draggable and selectable objects containers
        self.draggable = [self.playerButton,  self.keyButton, self.doorsButton, self.checkPointSpawner]
        self.selectable = [self.playerButton, self.keyButton, self.doorsButton, self.checkPointSpawner]
        self.selectPNG = pygame.image.load("./Graphics/select32x32.png").convert_alpha()

        # Level's data to save
        self.levelNameBox = TextInputBox(350, 775, 200, 35)
        self.level = LevelToEdit()

    def addLayoutEvent(self, event):
        pathToLayout = self.importLayout.leftClickDown(event)
        if pathToLayout:
            self.level.levelPath = pathToLayout
            self.level.setLayout(pathToLayout)
            if any(ext in pathToLayout[-3:] for ext in ["jpg", "png"]):
                if self.level.layout.get_height() != self.screenH - 100 or \
                        self.level.layout.get_width() != self.screenW:
                    self.level.layout = None
                else:
                    self.importLayout.img = pygame.transform.scale(self.importLayout.img, (110, 40))
                    self.importLayout.hitbox = self.importLayout.img.get_rect()
                    self.importLayout.changeFont(self.smallFont)
                    self.importLayout.setPos([590, 770])
                    self.importLayout.dx = 8
                    self.importLayout.dy = 12

    def saveLevelEvent(self, event):
        saveLevel = self.saveLevel.leftClickDown(event)
        if saveLevel:
            if self.level.layout is not None:
                if self.levelNameBox.text != "":
                    self.level.playerStartPosition = (self.playerButton.hitbox.x,
                                                      self.playerButton.hitbox.y)
                    self.level.checkpointRespawnPosition = (self.checkPointSpawner.hitbox.x,
                                                            self.checkPointSpawner.hitbox.y)
                    self.level.Enemies = []
                    self.level.Coins = []
                    self.level.Doors = None
                    for obj in self.draggable:
                        if isinstance(obj, EnemyButton):
                            self.level.Enemies.append(obj)
                        elif isinstance(obj, CoinButton):
                            self.level.Coins.append(obj)
                        elif isinstance(obj, DoorsButton):
                            self.level.Doors = obj
                        elif isinstance(obj, KeyButton):
                            self.level.key = obj
                    self.level.saveLevel(self.levelNameBox.text)

    def addEnemyEvent(self, event):
        newEnemy = self.enemyAdder.leftClickDown(event)
        if newEnemy:
            self.draggable.append(newEnemy)
            self.selectable.append(newEnemy)
            print("Enemy has been added")

    def switchPathTypeEvent(self, event):
        switch = self.switchPathTypeButton.leftClickDown(event)
        if switch:
            for selectable in self.selectable:
                if selectable.selected:
                    if isinstance(selectable, EnemyButton):
                        selectable.path.switchPathType()
                    elif isinstance(selectable, PathPoint):
                        selectable.owner.path.switchPathType()

    def addPathPointEvent(self, event):
        newPathPoint = self.pathPointAdder.leftClickDown(event)
        if newPathPoint:
            for selectable in self.selectable:
                if selectable.selected and isinstance(selectable, EnemyButton):
                    point = selectable.path.addPoint()
                    self.selectable.append(point)
                    self.draggable.append(point)
                    print("Path point has been added")
                    return None

    def addCoinEvent(self, event):
        newCoin = self.coinAdder.leftClickDown(event)
        if newCoin:
            self.draggable.append(newCoin)
            self.selectable.append(newCoin)
            print("Coin has been added")

    def deleteObjectEvent(self, event):
        if self.deleteButton.leftClickDown(event):
            p = None
            for i, draggable in enumerate(self.draggable):
                if draggable.selected:
                    if isinstance(draggable, Deletable):
                        if isinstance(draggable, PathPoint):
                            p = draggable
                            draggable.owner.path.pathPoints.remove(draggable)
                        del self.draggable[i]
                        break

            for i, selectable in enumerate(self.selectable):
                if selectable.selected:
                    if isinstance(selectable, Deletable):
                        if isinstance(selectable, EnemyButton):
                            for point in  selectable.path.pathPoints.copy():
                                if point in selectable.path.pathPoints:
                                    selectable.path.pathPoints.remove(point)
                                if point in self.draggable:
                                    self.draggable.remove(point)
                                if point in self.selectable:
                                    self.selectable.remove(point)
                        del self.selectable[i]
                        break
            if p is not None:
                p.owner.selected = True
                del p

    def writeCoordOfSelected(self, selected):
        self.window.blit(self.smallFont.render(f"X: {selected.hitbox.x}", False, (255, 255, 255)), (350, 742))
        self.window.blit(self.smallFont.render(f"Y: {selected.hitbox.y}", False, (255, 255, 255)), (400, 742))

    def draggingEvent(self, event):
        # Enemy dragging implementation
        for i, draggable in enumerate(self.draggable):
            # 1. leftClickHold returns 1 if enemy is dragged, so first step is to catch this value and
            # check whether it is equal to 1
            dragging = draggable.leftClickHold()
            draggable.leftClickRelease(event)
            if dragging:
                # 2. If enemy is dragged, drag him to the start of the list of enemies
                self.draggable.insert(0, draggable)
                del self.draggable[i + 1]
                break

    def selectingEvent(self, event):
        for i, selectable in enumerate(self.selectable):
            selecting = selectable.rightClickDown(event)
            selectable.leftClickDown(event)
            if selecting:
                for element in self.selectable:
                    element.selected = False
                    if isinstance(selectable, EnemyButton):
                        if isinstance(element, PathPoint):

                            if element in selectable.path.pathPoints:
                                element.rendered = True
                            else:
                                element.rendered = False
                if isinstance(selectable, PathPoint):
                    for point in selectable.owner.path.pathPoints:
                        point.rendered = True
                selectable.selected = True
                self.selectable.reverse()
                return 1
        return 0

    def textInputBoxEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.levelNameBox.active = True if self.levelNameBox.box.collidepoint(event.pos) else False
        if event.type == pygame.KEYDOWN:
            if self.levelNameBox.active:
                if event.key == pygame.K_RETURN:
                    self.levelNameBox.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.levelNameBox.text = self.levelNameBox.text[:-1]
                else:
                    self.levelNameBox.text += event.unicode

    def update(self):
        self.window.fill((0, 0, 0))

        # Render layout or import layout button
        if self.level.layout is None:
            self.importLayout.show(self.window)
        else:
            self.window.blit(self.level.layout, (0, 0))
            self.saveLevel.show(self.window)
            self.importLayout.show(self.window)

        # Render buttons for adding enemies and coins
        self.enemyAdder.show(self.window)
        self.coinAdder.show(self.window)

        # Render draggable
        reverse = self.draggable.copy().__reversed__()
        for draggable in reverse:
            if not isinstance(draggable, PathPoint):
                self.window.blit(draggable.img, (draggable.hitbox.x, draggable.hitbox.y))

        # Render selection and selection HUD
        for selectable in self.selectable:
            if selectable.selected:
                self.window.blit(self.selectPNG, (selectable.hitbox.x - 6, selectable.hitbox.y - 6))
                self.writeCoordOfSelected(selectable)
                if isinstance(selectable, Deletable):
                    self.deleteButton.show(self.window)
                    if isinstance(selectable, EnemyButton) or isinstance(selectable, PathPoint):
                        self.switchPathTypeButton.show(self.window)
                        self.pathPointAdder.show(self.window)
                        enemy = selectable.owner if isinstance(selectable, PathPoint) else selectable
                        if enemy.path.pathType == "repeat":
                            pygame.draw.line(self.window, (255, 100, 20), enemy.path.pathPoints[0].center,
                                             enemy.path.pathPoints[-1].center, width=3)
                        for i in range(len(enemy.path.pathPoints) - 1):
                            point1 = enemy.path.pathPoints[i]
                            point2 = enemy.path.pathPoints[i + 1]
                            pygame.draw.line(self.window, (255, 100, 20), point1.center, point2.center, width=3)
                            self.window.blit(point2.img, (point2.hitbox.x, point2.hitbox.y))
                            self.window.blit(self.font.render(f"{i + 1}", False, (80, 20, 255)),
                                             (point2.center[0] - 6, point2.center[1] - 14))

        # Render level name box
        self.window.blit(self.font.render(self.levelNameBox.text, True, (255, 255, 255)),
                         (self.levelNameBox.box.x + 5, self.levelNameBox.box.y + 5))
        pygame.draw.rect(self.window, (100, 100, 255), self.levelNameBox.box, 2)

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
                self.addCoinEvent(event)
                self.addPathPointEvent(event)
                self.draggingEvent(event)
                self.selectingEvent(event)
                self.deleteObjectEvent(event)
                self.switchPathTypeEvent(event)
                self.saveLevelEvent(event)
                self.textInputBoxEvent(event)

            self.update()
