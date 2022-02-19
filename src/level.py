import pygame
import csv


class Level:
    def __init__(self, file):
        self.layout = None
        self.playerStartPosition = None
        self.checkpointRespawnPosition = None
        self.Enemies = []
        self.Coins = []
        self.Key = None
        self.Doors = None
        self.InterpretateFile(file)

    def InterpretateFile(self, file):
        with open(f"./Levels/{file}") as data:
            csv_reader = csv.reader(data, delimiter=',')
            for line in csv_reader:
                if line[0] == 'layoutPath':
                    self.layout = pygame.image.load(line[1]).convert()
                elif line[0] == 'playerStartPosition':
                    self.playerStartPosition = (int(line[1]), int(line[2]))
                elif line[0] == 'checkpointRespawnPosition':
                    self.checkpointRespawnPosition = (int(line[1]), int(line[2]))

