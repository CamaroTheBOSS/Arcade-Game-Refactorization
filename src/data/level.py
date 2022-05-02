import pygame
import csv
import shutil
import cv2
import os
import numpy as np
from PIL import Image
from data.enemies import *
from data.collectable import *
from data.sprite import ObjectsContainer, Sprite


class ColorSet:
    def __init__(self):
        self.wall = np.array([0, 0, 0])             # Black
        self.win = np.array([34, 177, 76])          # Green
        self.checkpoint = np.array([255, 127, 39])  # Orange


class LevelTemplate:
    def __init__(self):
        self.layout = None  # layout picture
        self.playerStartPosition = None
        self.checkpointRespawnPosition = None
        self.Enemies = ObjectsContainer()
        self.Coins = ObjectsContainer()
        self.Doors = None


class Level(LevelTemplate):
    def __init__(self, file):
        super().__init__()
        self.layoutData = None  # contains information about walls from the given layout
        self.wallData = None  # contains information about solid objects at the layout
        self.color = ColorSet()  # used for checking win/checkpoint/collision with walls conditions
        self.checkpointReached = False

        self.InterpretateFile(file)

    def Wall(self, solidObject: Sprite, wallType="create"):
        x = solidObject.hitbox.x + 1
        y = solidObject.hitbox.y + 1
        w = solidObject.hitbox[2] - 2
        h = solidObject.hitbox[3] - 2
        value = 0
        if wallType == "delete":
            value = 255
        self.wallData[x:x + w, y:y + h] = value

    def InterpretateFile(self, file):
        with open(f"./Levels/{file}") as data:
            csv_reader = csv.reader(data, delimiter=',')
            for line in csv_reader:
                if line[0] == 'layoutPath':
                    level_np = Image.open(line[1])
                    self.layoutData = np.transpose(np.asarray(level_np), axes=(1, 0, 2))
                    self.layoutData = self.layoutData[:, :, :3]
                    self.layout = pygame.image.load(line[1]).convert()
                    self.wallData = cv2.imread(line[1])
                    self.wallData = np.transpose(cv2.cvtColor(self.wallData, cv2.COLOR_RGB2GRAY))

                elif line[0] == 'playerStartPosition':
                    self.playerStartPosition = (int(line[1]), int(line[2]))

                elif line[0] == 'checkpointRespawnPosition':
                    self.checkpointRespawnPosition = (int(line[1]), int(line[2]))

                elif line[0] == 'simpleEnemy':
                    self.Enemies.ListOfObjects.append(SimpleEnemy(int(line[1]), int(line[2]), "./Graphics/enemy.png"))
                    self.Enemies.ListOfHitboxes.append(self.Enemies.ListOfObjects[-1].hitbox)
                    # Extrude enemy's path points coordinates
                    temp = []
                    for i in range(int((len(line) - 4) / 2)):
                        temp.append([int(line[2 * i + 3]), int(line[2 * i + 4])])
                    self.Enemies.ListOfObjects[-1].buildPath((int(line[1]), int(line[2])), temp, pathType=line[-1])

                elif line[0] == 'coin':
                    self.Coins.ListOfObjects.append(Coin(int(line[1]), int(line[2]), "./Graphics/coin.png"))
                    self.Coins.ListOfHitboxes.append(self.Coins.ListOfObjects[-1].hitbox)

                elif line[0] == 'doorsAndKey':
                    self.Doors = Doors(int(line[1]), int(line[2]), "./Graphics/doors.png",
                                       int(line[3]), int(line[4]), "./Graphics/key.png")
                    self.Wall(self.Doors)


class LevelToEdit(LevelTemplate):
    def __init__(self):
        super().__init__()
        self.key = None
        self.levelPath = ""
        self.Enemies = []
        self.Coins = []

    def setLayout(self, pathToLayout):
        self.layout = pygame.image.load(pathToLayout).convert()

    def saveLevel(self, name: str):
        try:
            shutil.copy2(self.levelPath, f"./Levels")
        except shutil.SameFileError:
            pass
        normalized_path = os.path.normpath(self.levelPath)
        fileName = normalized_path.split(os.sep)[-1]
        fileFormat = fileName[-3:]

        try:
            os.rename(f"./Levels/{fileName}", f"./Levels/{name}.{fileFormat}")
        except FileExistsError:
            os.remove(f"./Levels/{name}.{fileFormat}")
            os.rename(f"./Levels/{fileName}", f"./Levels/{name}.{fileFormat}")

        with open(f"./Levels/{name}.txt", "w+") as f:
            f.write(f"layoutPath,./Levels/{name}.{fileFormat}\n")
            f.write(f"playerStartPosition,{self.playerStartPosition[0]},{self.playerStartPosition[1]}\n")
            f.write(f"checkpointRespawnPosition,{self.checkpointRespawnPosition[0]},{self.checkpointRespawnPosition[1]}\n")
            for simpleEnemy in self.Enemies:
                r = f"simpleEnemy,{simpleEnemy.hitbox.x},{simpleEnemy.hitbox.y},"
                for pathPoint in simpleEnemy.path.pathPoints:
                    x = pathPoint.hitbox.x - simpleEnemy.hitbox.x
                    y = pathPoint.hitbox.y - simpleEnemy.hitbox.y
                    r += f"{x},{y},"
                r += f"{simpleEnemy.path.pathType}"
                f.write(f"{r}\n")
            for coin in self.Coins:
                f.write(f"coin,{coin.hitbox.x},{coin.hitbox.y}\n")
            f.write(f"doorsAndKey,{self.Doors.hitbox.x},{self.Doors.hitbox.y},{self.key.hitbox.x},{self.key.hitbox.y}")
