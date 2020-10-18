import mido
import pygame
from pygame import midi

from just_midi import interval as i
from just_midi.control import StopPlay, Input

clock = pygame.time.Clock()

pygame.init()
midi.init()
mido.set_backend("mido.backends.pygame")

output = mido.open_output()

PITCHWHEEL_SEMITONE = mido.MAX_PITCHWHEEL / 2


class JustOutput:
    def __init__(self, output_):
        self._state = None
        self._output = output_

    def send(self, message):
        note = message.note
        if self._state is None:
            self._state = i.State(
                frequency=i.frequency_for_note_number(
                    note
                ),
                note=note
            )
        frequency = self._state(note)
        note_number = i.note_number_for_frequency(
            frequency
        )
        remainder = note_number % 1
        note = int(note_number)
        bend = int(
            remainder * PITCHWHEEL_SEMITONE
        )
        self._output.send(
            mido.Message(
                'pitchwheel',
                pitch=bend,
                channel=message.channel
            )
        )
        self._output.send(
            mido.Message(
                message.type,
                note=note,
                velocity=message.velocity
            )
        )


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
        output_=JustOutput(output)
    )
    runner.run()
