import pygame
import time
import pygame.midi
from PyQt5.QtCore import *
from PyQt5.QtGui  import *
from PyQt5.QtWidgets import *

# mixer config
# freq = 44100  # audio CD quality
# bitsize = -16   # unsigned 16 bit
# channels = 2  # 1 is mono, 2 is stereo
# buffer = 1024   # number of samples
# pygame.mixer.init(freq, bitsize, channels, buffer)
# pygame.mixer.music.set_volume(0.8)

pygame.midi.init()
fps = 60
timer = pygame.time.Clock()
player= pygame.midi.Output(0)
player.set_instrument(1,1) #127 is max

major=[0,4,7,12]

def go(note):
    player.note_on(note, 127, 1)
    QTimer.singleShot(1000, lambda: player.note_off(note, 127, 1))

# def go(note):
#     player.note_on(note, 127,1)
#     time.sleep(1)
#     player.note_off(note,127,1)

# def arp(base,ints):
#     for n in ints:
#         go(base+n)

# def chord(base, ints):
#     player.note_on(base,127,1)
#     player.note_on(base+ints[1],127,1)
#     player.note_on(base+ints[2],127,1)
#     player.note_on(base+ints[3],127,1)
#     time.sleep(1)
#     player.note_off(base,127,1)
#     player.note_off(base+ints[1],127,1)
#     player.note_off(base+ints[2],127,1)
#     player.note_off(base+ints[3],127,1)

def end():
       pygame.quit()

#go(61)
