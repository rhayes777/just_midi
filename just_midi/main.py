import mido
import pygame
from pygame import midi

from just_midi.control import StopPlay, Input

clock = pygame.time.Clock()

pygame.init()
midi.init()
mido.set_backend("mido.backends.pygame")

output = mido.open_output()


def pitch_bend(value, channel=0):
    output.send(mido.Message('pitchwheel', pitch=value, channel=channel))


class Runner:
    def __init__(self, input_, output_):
        self._input = input_
        self._output = output_
        self.velocity = 50
        self.channel = 0

    def run(self):
        play = True
        while play:
            clock.tick(40)
            try:
                for message in self._input():
                    self._output.send(message)
            except StopPlay:
                play = False


if __name__ == "__main__":
    runner = Runner(
        input_=Input(),
        output_=output
    )
    runner.run()
