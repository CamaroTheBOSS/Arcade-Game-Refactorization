import sys
import pygame
from level import LevelToEdit


class LevelEditor:
    def __init__(self, window):
        self.window = window
        self.level = LevelToEdit()
        self.font = pygame.font.SysFont('Calibri', 30, bold=True)
        self.clock = pygame.time.Clock()
        self.running = False

    def update(self):
        self.window.fill((0, 0, 0))
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
            self.update()
