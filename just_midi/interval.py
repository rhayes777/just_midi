from abc import abstractmethod


class State:
    def __init__(self, frequency, note):
        self.frequency = frequency
        self.note = note

    def __call__(self, note):
        n_semitones = note - self.note
        self.note = note
        self.frequency *= JustRatio(n_semitones)
        return self.frequency


class AbstractRatio:
    def __init__(self, n_semitones):
        self._n_semitones = n_semitones

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
