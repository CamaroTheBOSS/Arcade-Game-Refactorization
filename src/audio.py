import pygame


class Audio:
    def __init__(self):
        # Music
        self.Music = []

        # Effects
        self.Death = None
        self.CoinCollection = None
        self.KeyCollection = None
        self.DoorOpening = None
        self.LevelWin = None

    def SetMusicVolume(self, volume):
        pass

    def SetEffectsVolume(self, volume):
        self.Death.set_volume(volume)
        self.CoinCollection.set_volume(volume)
        self.KeyCollection.set_volume(volume)
        self.DoorOpening.set_volume(volume)
        self.LevelWin.set_volume(volume)


