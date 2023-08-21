import os
import time
import pygame


def initial():
    pygame.mixer.init()
    print("player has initialed")


def play(address):
    pygame.mixer.music.load(address)
    print(address)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)
    else:
        pygame.mixer.music.unload()


def delete(address):
    os.remove(address)
