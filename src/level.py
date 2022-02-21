import pygame
import csv
import numpy as np
from PIL import Image
from enemies import *


class ColorSet:
    def __init__(self):
        self.wall = np.array([0, 0, 0, 255])
        self.win = np.array([34, 177, 76, 255])
        self.checkpoint = np.array([255, 127, 39, 255])


class Level:
    def __init__(self, file):
        self.layout = None
        self.layoutData = None
        self.playerStartPosition = None
        self.checkpointRespawnPosition = None
        self.Enemies = []
        self.Coins = []
        self.Key = None
        self.Doors = None
        self.color = ColorSet()
        self.checkpointReached = False

        self.InterpretateFile(file)

    def InterpretateFile(self, file):
        with open(f"./Levels/{file}") as data:
            csv_reader = csv.reader(data, delimiter=',')
            for line in csv_reader:
                if line[0] == 'layoutPath':
                    level_np = Image.open(line[1])
                    self.layoutData = np.transpose(np.asarray(level_np), axes=(1, 0, 2))
                    self.layout = pygame.image.load(line[1]).convert()

                elif line[0] == 'playerStartPosition':
                    self.playerStartPosition = (int(line[1]), int(line[2]))

                elif line[0] == 'checkpointRespawnPosition':
                    self.checkpointRespawnPosition = (int(line[1]), int(line[2]))

                elif line[0] == 'simpleEnemy':
                    self.Enemies.append(SimpleEnemy(int(line[1]), int(line[2]), "./Graphics/enemy.png"))
                    # Extrude enemy's path points coordinates
                    temp = []
                    for i in range(int((len(line) - 4) / 2)):
                        temp.append([int(line[2 * i + 3]), int(line[2 * i + 4])])
                    self.Enemies[-1].buildPath((int(line[1]), int(line[2])), temp, pathType=line[-1])
