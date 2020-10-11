_intervals = [1, 256 / 243, 9 / 8, 6 / 5, 5 / 4, 4 / 3, 25 / 18, 3 / 2, 8 / 5, 5 / 3, 9 / 5, 15 / 8, 2]


class State:
    def __init__(self, frequency, note):
        self.frequency = frequency
        self.note = note

    def __call__(self, note):
        n_semitones = note - self.note
        interval = _compute_interval(n_semitones)
        self.note = note
        self.frequency *= interval
        return self.frequency


def _compute_interval(n_semitones):
    is_negative = n_semitones < 0
    n_semitones = abs(n_semitones)
    n_octaves = n_semitones // 12
    n_semitones = n_semitones % 12
    octave_modifier = 2 ** n_octaves
    interval_ratio = _intervals[
        n_semitones
    ]
    ratio = octave_modifier * interval_ratio
    if is_negative:
        ratio = 1 / ratio

    return ratio
