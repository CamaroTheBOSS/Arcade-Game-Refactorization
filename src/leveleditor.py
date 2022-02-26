import sys
import pygame
from level import LevelToEdit
from buttons import ImportLayoutButton, AddEnemyButton


class LevelEditor:
    def __init__(self, window):
        # Utility
        self.window = window
        self.screenH = self.window.get_height()
        self.screenW = self.window.get_width()
        self.clock = pygame.time.Clock()
        self.running = False
        self.font = pygame.font.SysFont('Calibri', 30, bold=True)

        # Selection variables
        self.selection = pygame.image.load("./Graphics/select32x32.png").convert()

        # Buttons
        smallFont = pygame.font.SysFont('Calibri', 18)
        self.importLayout = ImportLayoutButton(390, 100, "./Graphics/button.png", "Import layout", self.font, 40, 16)
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
            if enemy.selected:
                self.window.blit(self.selection, (enemy.hitbox.x - 6, enemy.hitbox.y - 6))
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
                    enemy.rightClickDown(event)
                    enemy.leftClickRelease(event)

                    if dragging:
                        # 2. If enemy is dragged, drag him to the start of the list of enemies
                        self.level.Enemies.ListOfObjects.insert(0, enemy)
                        del self.level.Enemies.ListOfObjects[i + 1]
                        break

            self.update()
