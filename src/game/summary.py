import sys
import pygame
from data.HUD import HUDelement


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
