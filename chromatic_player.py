import pygame
import glob

# mixer config
freq = 44100  # audio CD quality
bitsize = -16   # unsigned 16 bit
channels = 2  # 1 is mono, 2 is stereo
buffer = 1024   # number of samples
pygame.mixer.init(freq, bitsize, channels, buffer)
pygame.mixer.music.set_volume(0.8)


def play_music(midi_filename):
  '''Stream music_file in a blocking manner'''
  # listen for interruptions
  try:
    clock = pygame.time.Clock()
    pygame.mixer.music.load(midi_filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        clock.tick(30) # check if playback has finished
  except:
    # if user hits Ctrl/C then exit
    # (works only in console mode)
    pygame.mixer.music.fadeout(1000)
    pygame.mixer.music.stop()
    raise SystemExit

# gl = glob.glob(r"C:\Users\Alex\Google Drive\Projects\perfectpitch\mynotes\*.mid")

# midi_filename = r"C:\Users\Alex\Google Drive\Projects\perfectpitch\mynotes\A-2.mid"

# for i in gl:
#     play_music(i)

