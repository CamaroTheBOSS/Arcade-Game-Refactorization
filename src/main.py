import pygame
import sys
from level import Level
from player import Player
from audio import Audio
from HUD import GameHUD, HUDelement


# function used for collision detection
def inequality(a: list, b: list):
    for i in range(b.__len__()):
        if a[i] != b[i]:
            return True
    return False


class PyWindow:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((1024, 820))
        self.gameWindow = Game(self.window)
        self.menuWindow = Menu()
        self.levelEditor = LevelEditor()
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


class LevelEditor:
    pass


class Menu:
    pass


class SummaryWindow:
    def __init__(self, window):
        self.window = window
        self.score = 0
        self.deathCounter = 0
        self.timer = 0
        self.ScoreDeathTimeHUDRepresentation = HUDelement()
        self.img = pygame.image.load("./Graphics/level_summary.png").convert()

    def SetAttributes(self, score, deaths, time):
        self.score = score
        self.deathCounter = deaths
        self.timer = time

    def SetText(self, font):
        self.ScoreDeathTimeHUDRepresentation.textToRender = [
            font.render(f"Score: {self.score}", False, (255, 255, 255)),
            font.render(f"Deaths: {self.deathCounter}", False, (255, 255, 255)),
            font.render(f"Time: %.2f" % self.timer, False, (255, 255, 255)),
            font.render("Press C to continue", False, (255, 255, 255))
        ]

    def show(self):
        self.window.blit(self.img, (270, 270))
        for i, text in enumerate(self.ScoreDeathTimeHUDRepresentation.textToRender):
            self.window.blit(text, (310, 335 + i * 63))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                    return


class Game:
    def __init__(self, window):
        self.window = window
        self.audio = Audio()
        self.InitSounds()
        self.audio.SetEffectsVolume(0.2)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Calibri', 30, bold=True)
        self.level = None
        self.player = None
        self.running = False
        self.HUD = GameHUD()

    def InitSounds(self):
        self.audio.Death = pygame.mixer.Sound("./Audio/dead.mp3")
        self.audio.LevelWin = pygame.mixer.Sound("./Audio/win.mp3")
        self.audio.KeyCollection = pygame.mixer.Sound("./Audio/mario_key.mp3")
        self.audio.CoinCollection = pygame.mixer.Sound("./Audio/mario_coin.wav")
        self.audio.DoorOpening = pygame.mixer.Sound("./Audio/door.mp3")

    def loadLevel(self, file):
        self.level = Level(file)
        self.player = Player(self.level.playerStartPosition[0],
                             self.level.playerStartPosition[1],
                             "./Graphics/player.png")
        self.HUD.score = 0
        self.HUD.deathCounter = 0
        self.HUD.timer = 0

    def playerCollisions(self):
        self.player.calculateCornerCoordinates()

        # Collisions with walls
        keys = pygame.key.get_pressed()
        ru = self.player.ru
        rd = self.player.rd
        lu = self.player.lu
        ld = self.player.ld
        data = self.level.layoutData

        # Move only when pixels are not in specific color and
        # player is not colliding with solid objects like closed doors
        if self.level.wallData[ru[0] + 1][ru[1]] != 0 and \
                self.level.wallData[rd[0] + 1][rd[1]] != 0 and \
                inequality(data[ru[0] + 1, ru[1]], self.level.color.wall) and \
                inequality(data[rd[0] + 1, rd[1]], self.level.color.wall):
            self.player.center[0] += keys[pygame.K_RIGHT]
            self.player.hitbox.x += keys[pygame.K_RIGHT]

        if self.level.wallData[lu[0] - 1][lu[1]] != 0 and \
                self.level.wallData[ld[0] - 1][ld[1]] != 0 and \
                inequality(data[lu[0] - 1, lu[1]], self.level.color.wall) and \
                inequality(data[ld[0] - 1, ld[1]], self.level.color.wall):
            self.player.center[0] -= keys[pygame.K_LEFT]
            self.player.hitbox.x -= keys[pygame.K_LEFT]

        if self.level.wallData[ld[0]][ld[1] + 1] != 0 and \
                self.level.wallData[rd[0]][rd[1] + 1] != 0 and \
                inequality(data[ld[0], ld[1] + 1], self.level.color.wall) and \
                inequality(data[rd[0], rd[1] + 1], self.level.color.wall):
            self.player.center[1] += keys[pygame.K_DOWN]
            self.player.hitbox.y += keys[pygame.K_DOWN]

        if self.level.wallData[ru[0]][ru[1] - 1] != 0 and \
                self.level.wallData[lu[0]][lu[1] - 1] != 0 and \
                inequality(data[ru[0], ru[1] - 1], self.level.color.wall) and \
                inequality(data[lu[0], lu[1] - 1], self.level.color.wall):
            self.player.center[1] -= keys[pygame.K_UP]
            self.player.hitbox.y -= keys[pygame.K_UP]

        # Collisions with checkpoints
        if not inequality((data[ru[0], ru[1]]), self.level.color.checkpoint) or \
                not inequality((data[lu[0], lu[1]]), self.level.color.checkpoint) or \
                not inequality((data[ld[0], ld[1]]), self.level.color.checkpoint) or \
                not inequality((data[rd[0], rd[1]]), self.level.color.checkpoint):
            self.level.checkpointReached = True
            print("Checkpoint reached")

        # Collisions with win area
        if not inequality((data[ru[0], ru[1]]), self.level.color.win) or \
                not inequality((data[lu[0], lu[1]]), self.level.color.win) or \
                not inequality((data[ld[0], ld[1]]), self.level.color.win) or \
                not inequality((data[rd[0], rd[1]]), self.level.color.win):
            print("WIN")
            self.audio.LevelWin.play()
            self.running = False

        # Collisions with enemies
        if self.player.hitbox.collidelist(self.level.Enemies.ListOfHitboxes) != -1:
            self.audio.Death.play()
            self.HUD.updateDeathCounter()
            self.player.ghost.startReplay()

            if not self.level.checkpointReached:
                self.player.changePosition(self.level.playerStartPosition)
            else:
                self.player.changePosition(self.level.checkpointRespawnPosition)

        # Collisions with coins
        CollisionIndex = self.player.hitbox.collidelist(self.level.Coins.ListOfHitboxes)
        if CollisionIndex != -1:
            self.audio.CoinCollection.play()
            self.HUD.updateScore(100)
            self.level.Coins.ListOfObjects[CollisionIndex].collected = True
            self.level.Coins.ListOfObjects[CollisionIndex].hitbox.x = -40
            self.level.Coins.ListOfObjects[CollisionIndex].hitbox.y = -40

        # Collisions with doorsAndKeys
        if self.level.Doors is not None:
            # Collisions with key
            if self.player.hitbox.collidelist([self.level.Doors.key.hitbox]) != -1:
                self.audio.KeyCollection.play()
                self.level.Doors.key.collected = True
                self.level.Doors.key.hitbox.x = -40
                self.level.Doors.key.hitbox.y = -40

            # Collisions with doors
            if self.player.hitbox.collidelist([self.level.Doors.hitbox]) != -1 and self.level.Doors.key.collected:
                self.audio.DoorOpening.play()
                self.level.Doors.open = True
                self.level.Wall(self.level.Doors, wallType="delete")
                self.level.Doors = None

    def update(self):
        # Rendering layout and player
        self.window.fill((0, 0, 0))
        self.window.blit(self.level.layout, (0, 0))
        self.window.blit(self.player.img, (self.player.hitbox.x, self.player.hitbox.y))

        # Rendering enemies and updating their current position
        for enemy in self.level.Enemies.ListOfObjects:
            self.window.blit(enemy.img, (enemy.hitbox.x, enemy.hitbox.y))
            enemy.nextPathPoint()

        # Rendering coins
        for coin in self.level.Coins.ListOfObjects:
            self.window.blit(coin.img, (coin.hitbox.x, coin.hitbox.y))

        # Rendering doors and key
        if self.level.Doors is not None:
            if not self.level.Doors.open:
                self.window.blit(self.level.Doors.img, (self.level.Doors.hitbox.x,
                                                        self.level.Doors.hitbox.y))
            if not self.level.Doors.key.collected:
                self.window.blit(self.level.Doors.key.img, (self.level.Doors.key.hitbox.x,
                                                            self.level.Doors.key.hitbox.y))

        # Render player's ghost
        frame = self.player.ghost.frame
        if self.player.ghost.isPlaying:
            self.window.blit(self.player.ghost.img, (self.player.ghost.dataToReplay[frame][0],
                                                     self.player.ghost.dataToReplay[frame][1]))
            self.player.ghost.frame += 1
            if frame == len(self.player.ghost.dataToReplay) - 1:
                self.player.ghost.isPlaying = False
                self.player.ghost.dataToReplay = []

        # Render HUD
        for i, text in enumerate(self.HUD.ScoreDeathTimeHUDRepresentation.textToRender):
            self.window.blit(text, (50+i*400, 760))

        pygame.display.flip()

    def run(self):
        self.running = True

        # Main game loop
        while self.running:
            self.clock.tick(60 * 3)
            self.HUD.updateTimer(1 / (60 * 3))
            # Check for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    print(pygame.key.name(event.key))
            self.HUD.updateText(self.font)
            self.player.collectData()
            self.playerCollisions()
            self.update()


if __name__ == '__main__':
    app = PyWindow()

    app.loadAndRunLevel("1.txt")
    app.showSummaryWindow()
    app.loadAndRunLevel("2.txt")





