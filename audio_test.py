import pygame
import time

pygame.mixer.pre_init(
    frequency=44100,
    size=-16,
    channels=2,
    buffer=4096
)
pygame.init()

pygame.mixer.music.load("test.mp3")
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    time.sleep(1)