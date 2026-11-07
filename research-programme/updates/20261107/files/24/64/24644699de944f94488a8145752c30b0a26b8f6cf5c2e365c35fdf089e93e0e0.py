import mpmath as mp

import factors236 as retained
from precise_epoch_response import scalar


class EventCoupling:
    def __init__(self, event):
        if mp.mp.dps < 60:
            raise ValueError('Construct event couplings at least at60 digits')
        self.precision = mp.mp.prec
        self.temperature = scalar(event['temperature'])
        self.frequencies = tuple(map(scalar, event['frequencies']))
        self.signs = tuple(event['signs'])
        self.initial = tuple(map(scalar, event['electron_initial']))
        self.transfer = tuple(map(scalar, event['electron_transfer']))
        self.count = len(self.frequencies)
        if self.count not in (2, 3) or len(self.signs) != self.count or any(sign not in (-1, 1) for sign in self.signs):
            raise ValueError('Retained two/three-leg events with signed photon legs required')
        if len(self.initial) != 4 or len(self.transfer) != 4:
            raise ValueError('Complete electron four-vectors required')
        values = (self.temperature, *self.frequencies, *self.initial, *self.transfer)
        if not all(mp.isfinite(value) for value in values) or self.temperature <= 0 or min(self.frequencies) <= 0:
            raise ValueError('Finite positive temperature/frequencies required')
        mean = retained.state235.mean_energy(mp.nstr(self.temperature, 85))
        self.initial_score = (self.initial[0] - mean) / self.temperature
        self.score_difference = -self.transfer[0] / self.temperature
        self.final_score = self.initial_score - self.score_difference
        occupations = tuple(1 / mp.expm1(value) for value in self.frequencies)
        self.forward = tuple(value + int(sign < 0) for value, sign in zip(occupations, self.signs))
        self.reverse = tuple(value + int(sign > 0) for value, sign in zip(occupations, self.signs))
        self.matrix = mp.matrix(self.count + 5, self.count + 1)
        for first in range(self.count):
            for second in range(first + 1, self.count):
                entry = -(self.signs[first] * (self.forward[second] + self.reverse[second])
                    + self.signs[second] * (self.forward[first] + self.reverse[first])) / 2
                self.matrix[first, second] = self.matrix[second, first] = entry
            entry = self.forward[first] * self.score_difference - self.signs[first] * self.final_score
            self.matrix[first, self.count] = self.matrix[self.count, first] = entry
        self.matrix[self.count, self.count] = self.score_difference * (self.initial_score + self.final_score - 2)
        for axis in range(3):
            momentum, transfer = self.initial[axis + 1], self.transfer[axis + 1]
            for photon in range(self.count):
                self.matrix[self.count + 1 + axis, photon] = (-momentum * self.signs[photon] - transfer * self.reverse[photon]) / self.temperature
            self.matrix[self.count + 1 + axis, self.count] = (momentum * self.score_difference
                - transfer * (self.final_score - 1)) / self.temperature
        for photon, sign in enumerate(self.signs):
            self.matrix[self.count + 4, photon] = -sign
        self.matrix[self.count + 4, self.count] = self.score_difference
        self.gradient = mp.matrix([-sign for sign in self.signs] + [self.score_difference]
            + [-value / self.temperature for value in self.transfer[1:]] + [mp.mpf(0)])

    def check_precision(self):
        if mp.mp.prec != self.precision:
            raise ValueError('Rebuild event coupling when arithmetic precision changes')

    def unpack(self, values):
        return dict(photon=[values[index] for index in range(self.count)], gas=values[self.count],
            velocity=[values[self.count + 1 + axis] for axis in range(3)], density=values[self.count + 4])

    def equilibrium(self):
        self.check_precision()
        return self.unpack(self.gradient)

    def coefficients(self, potential, gas):
        self.check_precision()
        if len(potential) != self.count:
            raise ValueError('One potential for every event photon leg required')
        background = mp.matrix([*map(scalar, potential), scalar(gas)])
        if not all(mp.isfinite(value) for value in background):
            raise ValueError('Finite event readout required')
        return self.unpack(self.matrix * background)

    def evaluate(self, values, gas, harmonic, degree):
        self.check_precision()
        if degree not in (0, 1, 2) or len(values) != self.count:
            raise ValueError('Retained angular sector and complete photon legs required')
        columns = len(gas)
        axes = (1, 3, 9)[degree]
        if columns == 0 or any(len(row) != columns for row in values):
            raise ValueError('Inconsistent event background/wave columns')
        if harmonic.shape[0] < self.count or harmonic.shape[1] != axes:
            raise ValueError('Angular harmonics do not match the requested sector')
        background = mp.matrix([[scalar(value) for value in row] for row in values]
            + [[scalar(value) for value in gas]])
        if not all(mp.isfinite(value) for value in background):
            raise ValueError('Finite event readouts required')
        changes = self.matrix * background
        coefficients = [self.equilibrium()] + [self.unpack(changes[:, column]) for column in range(columns)]
        right = mp.matrix(self.count + 5, columns + 1)
        right[:, 0] = self.gradient
        for column in range(columns):
            right[:, column + 1] = changes[:, column]
        output = [[[mp.mpf(0) for axis in range(axes)] for column in range(columns)] for state in range(columns + 1)]
        for axis in range(axes):
            waves = mp.matrix(self.count + 5, columns)
            for photon in range(self.count):
                for column in range(columns):
                    waves[photon, column] = background[photon, column] * scalar(harmonic[photon, axis])
            if degree < 2:
                gas_row = self.count if degree == 0 else self.count + 1 + axis
                for column in range(columns):
                    waves[gas_row, column] = scalar(gas[column])
            projected = right.transpose() * waves
            for state in range(columns + 1):
                for column in range(columns):
                    output[state][column][axis] = projected[state, column]
        return coefficients, output
