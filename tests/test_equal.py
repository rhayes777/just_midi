import pytest

from just_midi import interval


@pytest.mark.parametrize(
    "n_semitones, ratio",
    [
        (0, 1),
        (12, 2),
        (1, 2 ** (1 / 12)),
        (-1, 1 / (2 ** (1 / 12)))
    ]
)
def test_ratio(n_semitones, ratio):
    assert float(interval.EqualTemperamentRatio(
        n_semitones
    )) == ratio
