import pytest

_intervals = [1, 9 / 8, 5 / 4, 4 / 3, 3 / 2, 5 / 3, 15 / 8, 2]


def _compute_interval(n_semitones):
    is_negative = n_semitones < 0
    n_semitones = abs(n_semitones)
    n_octaves = n_semitones // 7
    n_semitones = n_semitones % 7
    octave_modifier = 2 ** n_octaves
    ratio = octave_modifier * _intervals[
        n_semitones
    ]
    if is_negative:
        ratio = 1 / ratio

    return ratio


@pytest.fixture(
    name="state"
)
def make_state():
    return State(1, 0)


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


def test_octaves(
        state
):
    assert state(8) == 1 * 18 / 8


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
def test_simple(
        note,
        ratio,
        state
):
    assert state(note) == ratio
    assert state.frequency == ratio
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
    state = State(1, 0)
    assert state(note) == ratio
    assert state.frequency == ratio
    assert state.note == note


def test_shift(state):
    state(2)
    state(1)
    assert state(0) != 1
