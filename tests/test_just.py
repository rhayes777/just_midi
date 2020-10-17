import pytest

from just_midi.interval import State, JustRatio


def test_intervals():
    last = JustRatio._intervals[0]
    for interval in JustRatio._intervals[1:]:
        assert interval > last
        last = interval


@pytest.fixture(
    name="state"
)
def make_state():
    return State(1, 0)


@pytest.mark.parametrize(
    "note, ratio",
    [
        (14, 18 / 8),
        (-14, 8 / 18)
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
