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


@pytest.mark.parametrize(
    "number, frequency",
    [
        (69, 440),
        (0, 8.18),
        (127, 12543.85)
    ]
)
def test_frequency_for_note_number(
        number, frequency
):
    assert interval.frequency_for_note_number(
        number
    ) == pytest.approx(frequency, rel=0.001)
