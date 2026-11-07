import mpmath as mp
import numpy as np

import factors236 as retained
from retained_column_differences import difference_using_retained_splines


def scalar(value):
    return mp.mpf(float(value)) if isinstance(value, (float, np.floating)) else mp.mpf(value)


class PreciseEpochResponse:
    def __init__(self, factors, high, low):
        if mp.mp.dps < 60:
            raise ValueError('At least60 digits required before source contraction')
        if high.shape != low.shape or high.shape != (578, 18):
            raise ValueError('All18 actual history/difference columns and578 coordinates required')
        self.factors = factors
        self.columns = [[scalar(upper) + scalar(lower) for upper, lower in zip(high[:, column], low[:, column])] for column in range(18)]
        self.gas = [column[-1] for column in self.columns]
        self.base = {join: self.contract(factors.basis_base[join]) for join in (0, 1)}
        self.born_coefficients = {join: [retained.equilibrium(factors.event)] + [retained.coefficient_state(factors.event,
            [row[column] for row in self.base[join]], self.gas[column]) for column in range(18)] for join in (0, 1)}

    def contract(self, rows):
        values = np.asarray(rows)
        return [[mp.fsum(scalar(value) * coefficient for value, coefficient in zip(row, column[:-1]))
            for column in self.columns] for row in values]

    def projected(self, coefficients, values, degree, harmonic):
        result = []
        for column in range(18):
            vector = []
            for axis in range(harmonic.shape[-1]):
                photon = mp.fsum(coefficient * values[node][column] * scalar(harmonic[node, axis])
                    for node, coefficient in enumerate(coefficients['photon']))
                gas = coefficients['gas'] if degree == 0 else coefficients['velocity'][axis] if degree == 1 else mp.mpf(0)
                vector.append(photon + gas * self.gas[column])
            result.append(vector)
        return result

    def born(self, join, degree):
        return [self.projected(coefficients, self.base[join], degree, self.factors.harmonics[degree])
            for coefficients in self.born_coefficients[join]]

    def current(self, join, degree, soft_value, event, sign):
        factors, owner = self.factors, self.factors.owner
        frequency = float(abs(scalar(soft_value)) * owner.doppler / owner.temperature)
        shift = float(event['hard_shift'] * owner.hard_doppler / owner.temperature)
        basis_soft = factors.features.evaluate(np.array([frequency]), join)
        basis_delta = difference_using_retained_splines(factors.features, factors.frequency[1], np.array([shift]), join, retained.spline_difference)
        potential_soft = self.contract(basis_soft)[0]
        potential_delta = self.contract(basis_delta)[0]
        transfer = owner.transform * mp.matrix([event['kinetic'], *event['recoil']])
        current = dict(factors.event, frequencies=[factors.event['frequencies'][0], factors.event['frequencies'][1] + scalar(shift), scalar(frequency)],
            electron_transfer=list(transfer), signs=[-1, 1, sign])
        values = [self.base[join][0], [before + change for before, change in zip(self.base[join][1], potential_delta)], potential_soft]
        coefficients = [retained.equilibrium(current)] + [retained.coefficient_state(current,
            [row[column] for row in values], self.gas[column]) for column in range(18)]
        harmonic = factors.harmonics[degree]
        complete = [self.projected(value, values, degree, harmonic) for value in coefficients]
        born = self.born(join, degree)
        equilibrium = born[0]
        occupation = 1 / mp.expm1(scalar(frequency))
        coupling = 2 * occupation * (1 + occupation) / (1 + 2 * occupation)
        reference, delta = [], []
        for state in range(19):
            background = mp.mpf(0) if state == 0 else potential_soft[state - 1]
            density = mp.mpf(0) if state == 0 else self.born_coefficients[join][state]['density']
            state_reference, state_delta = [], []
            for column in range(18):
                vector = [born[state][column][axis] + coupling * (background * equilibrium[column][axis]
                    + density * potential_soft[column] * scalar(harmonic[2, axis])) for axis in range(harmonic.shape[-1])]
                state_reference.append(vector)
                state_delta.append([actual - before for actual, before in zip(complete[state][column], vector)])
            reference.append(state_reference)
            delta.append(state_delta)
        return dict(complete=complete, reference=reference, right_delta=delta, coefficients=coefficients,
            basis=[factors.basis_base[join][0], factors.basis_base[join][1] + basis_delta[0], basis_soft[0]],
            basis_base=factors.basis_base[join], basis_delta=basis_delta[0], basis_soft=basis_soft[0],
            values=values, current_event=current, coupling=coupling, potential_soft=potential_soft)

    def response(self, left, right, degree):
        return [[[mp.fsum(scalar(value) * coefficient for value, coefficient in zip(row, right[state][column])) / (2 * degree + 1)
            for column in range(18)] for row in left] for state in range(19)]

    def expanded_equilibrium_delta(self, event_data, join, degree, harmonic):
        coefficients = event_data['coefficients'][0]
        born = self.born_coefficients[join][0]
        rows = []
        for coordinate in range(578):
            axes = []
            for axis in range(harmonic.shape[-1]):
                if coordinate == 577:
                    value = coefficients['gas'] - born['gas'] if degree == 0 else coefficients['velocity'][axis] - born['velocity'][axis] if degree == 1 else mp.mpf(0)
                else:
                    value = mp.fsum((coefficients['photon'][node] - born['photon'][node]) * scalar(event_data['basis_base'][node, coordinate]) * scalar(harmonic[node, axis]) for node in (0, 1))
                    value += coefficients['photon'][1] * scalar(event_data['basis_delta'][coordinate]) * scalar(harmonic[1, axis])
                    value += coefficients['photon'][2] * scalar(event_data['basis_soft'][coordinate]) * scalar(harmonic[2, axis])
                axes.append(value)
            rows.append(axes)
        return [[mp.fsum(row[axis] * coefficient for row, coefficient in zip(rows, column))
            for axis in range(harmonic.shape[-1])] for column in self.columns]


def split_array(values):
    objects = np.asarray(values, dtype=object)
    high = np.array([float(value) for value in objects.flat]).reshape(objects.shape)
    low = np.array([float(value - scalar(upper)) for value, upper in zip(objects.flat, high.flat)]).reshape(objects.shape)
    return high, low
