import pytest

_intervals = [1, 9 / 8, 5 / 4]


def _compute_interval(n_semitones):
    return _intervals[
        n_semitones
    ]


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


@pytest.mark.parametrize(
    "note, ratio",
    [
        (2, 9 / 8),
        (3, 5 / 4)
    ]
)
def test_modify(
        note,
        ratio
):
    state = State(100, 1)
    assert state(note) == 100 * ratio
    assert state.frequency == 100 * ratio
    assert state.note == note

# 1st - 1
# 2nd - 9/8
# 3rd - 5/4
# 4th - 4/3
# Perfect 5th - 3/2
# Octave - 2
# 6th - 5/3
# 7th - 15/8
# 8th 2/1
