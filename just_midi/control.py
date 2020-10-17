import mido
import pygame


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