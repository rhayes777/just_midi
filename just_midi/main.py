import mido
import pygame
from pygame import midi

clock = pygame.time.Clock()

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

if __name__ == "__main__":
    velocity = 50
    channel = 0
    play = True
    while play:
        clock.tick(40)
        events = pygame.event.get()
        for event in events:
            if event.type in type_map and event.key in note_map:
                message_type = type_map[event.type]
                note = note_map[event.key]
                output.send(
                    mido.Message(
                        message_type,
                        channel=channel,
                        note=note,
                        velocity=velocity
                    )
                )
            if event.key == pygame.K_ESCAPE:
                play = False
    # pitch_bend(0)
    # print("zero")
    # play_note()
    # time.sleep(1)
    # stop_note()
    # pitch_bend(8191)
    # print("bent")
    # play_note()
    # time.sleep(1)
    # stop_note()
    # pitch_bend(0)
    # print("two")
    # play_note(note=52)
    # time.sleep(1)
    # stop_note(note=52)
