import pytest

_intervals = [1, 256 / 243, 9 / 8, 6 / 5, 5 / 4, 4 / 3, 25 / 18, 3 / 2, 8 / 5, 5 / 3, 9 / 5, 15 / 8, 2]


def test_intervals():
    last = _intervals[0]
    for interval in _intervals[1:]:
        assert interval > last
        last = interval


def _compute_interval(n_semitones):
    is_negative = n_semitones < 0
    n_semitones = abs(n_semitones)
    n_octaves = n_semitones // 12
    n_semitones = n_semitones % 12
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


@pytest.mark.parametrize(
    "note, ratio",
    [
        (14, 18 / 8),
        (-14, 9 / 16)
    ]
)
def test_octaves(
        state,
        note,
        ratio
):
    assert state(note) == ratio


@pytest.mark.parametrize(
    "note, ratio",
    [
        (0, 1),
        (2, 9 / 8),
        (4, 5 / 4),
        (5, 4 / 3),
        (7, 3 / 2),
        (9, 5 / 3),
        (11, 15 / 8),
        (12, 2),
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
        (-2, 8 / 9),
        (-4, 4 / 5),
        (-5, 3 / 4),
        (-7, 2 / 3),
        (-9, 3 / 5),
        (-11, 8 / 15),
        (-12, 0.5),
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
