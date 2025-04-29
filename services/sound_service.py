import pygame

class SoundService:
    def __init__(self):
        self.sounds = {
            "click": pygame.mixer.Sound("assets/66878__mikemunkie__click1.wav"),
            "place": pygame.mixer.Sound("assets/66878__mikemunkie__click1.wav")
        }

    def play(self, name):
        sound = self.sounds.get(name)
        if sound:
            sound.play()
