import pytest

_intervals = [1, 9 / 8, 5 / 4, 4 / 3, 3 / 2, 5 / 3, 15 / 8, 2]


def _compute_interval(n_semitones):
    ratio = _intervals[
        abs(n_semitones)
    ]
    if n_semitones < 0:
        return 1 / ratio
    return ratio


@pytest.fixture(
    name="state"
)
def make_state():
    return State(100, 0)


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
        (0, 1),
        (1, 9 / 8),
        (2, 5 / 4),
        (3, 4 / 3),
        (4, 3 / 2),
        (5, 5 / 3),
        (6, 15 / 8),
        (7, 2),
    ]
)
def test_octave(
        note,
        ratio,
        state
):
    assert state(note) == 100 * ratio
    assert state.frequency == 100 * ratio
    assert state.note == note


@pytest.mark.parametrize(
    "note, ratio",
    [
        (0, 1),
        (-1, 8 / 9),
        (-2, 4 / 5),
        (-3, 3 / 4),
        (-4, 2 / 3),
        (-5, 3 / 5),
        (-6, 8 / 15),
        (-7, 0.5),
    ]
)
def test_inverse(
        note,
        ratio,
        state
):
    state = State(100, 0)
    assert state(note) == 100 * ratio
    assert state.frequency == 100 * ratio
    assert state.note == note


def test_shift(state):
    state(2)
    state(1)
    assert state(0) != 100
