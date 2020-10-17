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
                        channel=channel,
                        note=note,
                        velocity=velocity
                    )
                )
            if event.key == pygame.K_ESCAPE:
                raise StopPlay()
        return messages


if __name__ == "__main__":
    velocity = 50
    channel = 0
    play = True
    input_ = Input()
    while play:
        clock.tick(40)
        try:
            for message in input_():
                output.send(message)
        except StopPlay:
            play = False
