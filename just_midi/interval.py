import math
from abc import abstractmethod


class State:
    def __init__(self, frequency, note):
        self._frequency = frequency
        self._note = note

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.note} {self.frequency}>"

    @property
    def frequency(self):
        return self._frequency

    @property
    def note(self):
        return self._note

    @note.setter
    def note(self, note):
        self._frequency = self._compute_frequency(note)
        self._note = note

    def _compute_frequency(self, note):
        n_semitones = note - self.note
        return self.frequency * JustRatio(n_semitones)

    def __call__(self, note):
        return self._compute_frequency(note)


class AbstractRatio:
    def __init__(self, n_semitones):
        self._n_semitones = n_semitones

    def __repr__(self):
        return f"<{self.__class__.__name__} {self._n_semitones} -> {self.ratio}>"

    @property
    def _abs_semitones(self):
        return abs(self._n_semitones)

    @property
    def is_negative(self):
        return self._n_semitones < 0

    @property
    def n_octaves(self):
        return self._abs_semitones // 12

    @property
    def remainder(self):
        return self._abs_semitones % 12

    @property
    def octave_modifier(self):
        return 2 ** self.n_octaves

    @property
    @abstractmethod
    def interval_ratio(self):
        pass

    @property
    def ratio(self):
        ratio = self.octave_modifier * self.interval_ratio
        if self.is_negative:
            ratio = 1 / ratio

        return ratio

    def __float__(self):
        return self.ratio

    def __mul__(self, other):
        return float(self) * other

    def __rmul__(self, other):
        return other * float(self)


class JustRatio(AbstractRatio):
    @property
    def interval_ratio(self):
        return self._intervals[
            self.remainder
        ]

    _intervals = [1., 256 / 243, 9 / 8, 6 / 5, 5 / 4, 4 / 3, 25 / 18, 3 / 2, 8 / 5, 5 / 3, 9 / 5, 15 / 8, 2.]


class EqualTemperamentRatio(AbstractRatio):
    @property
    def interval_ratio(self):
        return 2 ** (self.remainder / 12)


def frequency_for_note_number(number):
    a_frequency = 440
    a_number = 69
    return a_frequency * EqualTemperamentRatio(
        number - a_number
    )


class Note:
    base_frequency = frequency_for_note_number(0)

    def __init__(self, frequency):
        self.frequency = frequency

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.frequency}>"

    def __float__(self):
        return 12 * (math.log2(self.frequency) - math.log2(self.base_frequency))

    def __eq__(self, other):
        return float(self) == other

    def __int__(self):
        return int(float(self))

    @property
    def remainder(self):
        return float(self) - int(self)
