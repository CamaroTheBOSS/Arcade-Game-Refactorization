import sys
import pygame
from level import LevelToEdit
from buttons import ImportLayoutButton, AddEnemyButton, AddCoinButton, PlayerButton, KeyButton, DoorsButton, \
    DeleteButton, EnemyButton, CoinButton


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
        smallFont = pygame.font.SysFont('Calibri', 18)
        self.importLayout = ImportLayoutButton(390, 100, "./Graphics/button.png", "Import layout", self.font, 40, 16)
        self.enemyAdder = AddEnemyButton(10, 730, "./Graphics/enemy.png", "Add enemy", smallFont, 40, 10)
        self.coinAdder = AddCoinButton(10, 775, "./Graphics/coin.png", "Add coin", smallFont, 40, 10)
        self.deleteButton = DeleteButton(300, 752, "./Graphics/delete.png", "Delete object", smallFont, 40, 10)
        self.playerButton = PlayerButton(100, 100, "./Graphics/player.png")
        self.keyButton = KeyButton(100, 150, "./Graphics/key.png")
        self.doorsButton = DoorsButton(100, 200, "./Graphics/doors.png")

        # Draggable and selectable objects containers
        self.draggable = [self.playerButton,  self.keyButton, self.doorsButton]
        self.selectable = [self.playerButton, self.keyButton, self.doorsButton]
        self.selectPNG = pygame.image.load("./Graphics/select32x32.png").convert_alpha()

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
            self.draggable.append(newEnemy)
            self.selectable.append(newEnemy)
            print("Enemy has been added")

    def addCoinEvent(self, event):
        newCoin = self.coinAdder.leftClickDown(event)
        if newCoin:
            self.draggable.append(newCoin)
            self.selectable.append(newCoin)
            print("Coin has been added")

    def deleteObjectEvent(self, event):
        if self.deleteButton.leftClickDown(event):
            for i, draggable in enumerate(self.draggable):
                if draggable.selected:
                    del self.draggable[i]
                    break

            for i, selectable in enumerate(self.selectable):
                if selectable.selected:
                    del self.selectable[i]
                    break

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
                selectable.selected = True
                self.selectable.reverse()
                return 1
        return 0

    def update(self):
        self.window.fill((0, 0, 0))

        # Render layout or import layout button
        if self.level.layout is None:
            self.importLayout.show(self.window)
        else:
            self.window.blit(self.level.layout, (0, 0))

        # Render buttons for adding enemies and coins
        self.enemyAdder.show(self.window)
        self.coinAdder.show(self.window)
        self.deleteButton.show(self.window)

        # Render draggable
        reverse = self.draggable.copy().__reversed__()
        for draggable in reverse:
            self.window.blit(draggable.img, (draggable.hitbox.x, draggable.hitbox.y))

        # Render selection
        for selectable in self.selectable:
            if selectable.selected:
                self.window.blit(self.selectPNG, (selectable.hitbox.x - 6, selectable.hitbox.y - 6))

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
                self.draggingEvent(event)
                self.selectingEvent(event)
                self.deleteObjectEvent(event)

            self.update()
