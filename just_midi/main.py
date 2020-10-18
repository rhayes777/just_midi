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

    def _get_state(self, note):
        if self._state is None:
            self._state = i.State(
                frequency=i.frequency_for_note_number(
                    note
                ),
                note=note
            )
        return self._state

    def _bend(self, new_note, message):
        bend = int(
            new_note.remainder * PITCHWHEEL_SEMITONE
        )
        self._output.send(
            mido.Message(
                'pitchwheel',
                pitch=bend,
                channel=message.channel
            )
        )

    def _send_note(self, new_note, message):
        self._output.send(
            mido.Message(
                message.type,
                note=int(new_note),
                velocity=message.velocity,
                channel=message.channel
            )
        )

    def send(self, message):
        note = message.note
        state = self._get_state(note)
        frequency = state(note)
        state.note = note
        new_note = i.Note(frequency)
        self._bend(
            new_note=new_note,
            message=message
        )
        self._send_note(
            new_note=int(new_note),
            message=message
        )


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
