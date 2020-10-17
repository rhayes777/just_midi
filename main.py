import time

import mido
import pygame
from pygame import midi

pygame.init()
midi.init()
mido.set_backend("mido.backends.pygame")

output = mido.open_output()


def play_note(channel=0, note=50, velocity=50):
    output.send(mido.Message("note_on", channel=channel, note=note, velocity=velocity))


def stop_note(channel=0, note=50):
    output.send(mido.Message("note_off", channel=channel, note=note))


def pitch_bend(value, channel=0):
    output.send(mido.Message('pitchwheel', pitch=value, channel=channel))


if __name__ == "__main__":
    pitch_bend(0)
    play_note()
    time.sleep(1)
    stop_note()
    pitch_bend(8191)
    play_note()
    time.sleep(1)
    stop_note()
