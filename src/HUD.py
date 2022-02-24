import pygame

class HUDelement:
    def __init__(self):
        self.textToRender = []


class GameHUD:
    def __init__(self):
        self.score = 0
        self.deathCounter = 0
        self.timer = 0
        self.ScoreDeathTimeHUDRepresentation = HUDelement()

    def updateScore(self, scoreToAdd: int):
        self.score += scoreToAdd

    def updateDeathCounter(self):
        self.deathCounter += 1

    def updateTimer(self, timeToAdd):
        self.timer += timeToAdd

    def updateText(self, font):
        self.ScoreDeathTimeHUDRepresentation.textToRender = [
            font.render(f"Score: {self.score}", False, (255, 255, 255)),
            font.render(f"Deaths: {self.deathCounter}", False, (255, 255, 255)),
            font.render(f"Time: %.2f" % self.timer, False, (255, 255, 255))
        ]
