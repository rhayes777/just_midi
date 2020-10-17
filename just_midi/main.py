import mido
import pygame
from pygame import midi

clock = pygame.time.Clock()

pygame.init()
midi.init()
mido.set_backend("mido.backends.pygame")

output = mido.open_output()


def pitch_bend(value, channel=0):
    output.send(mido.Message('pitchwheel', pitch=value, channel=channel))


class StopPlay(Exception):
    pass


class Input:
    note_map = {
        pygame.K_a: 65,
        pygame.K_w: 66,
        pygame.K_s: 67,
        pygame.K_e: 68,
        pygame.K_d: 69,
        pygame.K_r: 70,
        pygame.K_f: 71,
        pygame.K_g: 72,
        pygame.K_y: 73,
        pygame.K_h: 74,
        pygame.K_u: 75,
        pygame.K_j: 76,
        pygame.K_k: 77,
        pygame.K_o: 78,
        pygame.K_l: 79,
        pygame.K_p: 80,
        pygame.K_SEMICOLON: 81,
        pygame.K_LEFTBRACKET: 82,
        pygame.K_QUOTE: 83,
        pygame.K_BACKSLASH: 84
    }

    type_map = {
        pygame.KEYDOWN: "note_on",
        pygame.KEYUP: "note_off"
    }

    def __init__(
            self,
            channel=0,
            velocity=50
    ):
        self.channel = channel
        self.velocity = velocity

    def __call__(self):
        messages = list()
        events = pygame.event.get()
        for event in events:
            if event.type in self.type_map and event.key in self.note_map:
                message_type = self.type_map[event.type]
                note = self.note_map[event.key]
                messages.append(
                    mido.Message(
                        message_type,
                        channel=self.channel,
                        note=note,
                        velocity=self.velocity
                    )
                )
            if event.key == pygame.K_ESCAPE:
                raise StopPlay()
        return messages


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
