import mpmath as mp
import numpy as np

import factors236 as retained
from event_coupling import EventCoupling
from precise_epoch_response import PreciseEpochResponse, scalar
from retained_column_differences import difference_using_retained_splines


class FactoredEpochResponse(PreciseEpochResponse):
    def __init__(self, factors, high, low):
        if mp.mp.dps < 60 or high.shape != low.shape or high.shape != (578, 18):
            raise ValueError('Use all578 coordinates and18 physical/difference columns at least at60 digits')
        self.precision = mp.mp.prec
        self.factors = factors
        self.columns = [[scalar(upper) + scalar(lower) for upper, lower in zip(high[:, column], low[:, column])] for column in range(18)]
        self.gas = [column[-1] for column in self.columns]
        self.base = {join: self.contract(factors.basis_base[join]) for join in (0, 1)}
        self.born_operator = EventCoupling(factors.event)
        self.born_coefficients = {join: [self.born_operator.equilibrium()] + [self.born_operator.coefficients(
            [row[column] for row in self.base[join]], self.gas[column]) for column in range(18)] for join in (0, 1)}
        self.born_cache = {}
        self.current_operators = {}
        self.current_readouts = {}

    def born(self, join, degree):
        self.born_operator.check_precision()
        key = (join, degree)
        if key not in self.born_cache:
            unused, self.born_cache[key] = self.born_operator.evaluate(self.base[join], self.gas, self.factors.harmonics[degree], degree)
        return self.born_cache[key]

    def current(self, join, degree, soft_value, event, sign):
        self.born_operator.check_precision()
        if sign not in (-1, 1) or event['soft'] != sign * scalar(soft_value):
            raise ValueError('Soft event and signed source node disagree')
        factors, owner = self.factors, self.factors.owner
        frequency = float(abs(scalar(soft_value)) * owner.doppler / owner.temperature)
        shift = float(event['hard_shift'] * owner.hard_doppler / owner.temperature)
        transfer = tuple(owner.transform * mp.matrix([event['kinetic'], *event['recoil']]))
        key = (scalar(soft_value), sign, scalar(event['hard_shift']), *transfer)
        current = dict(factors.event, frequencies=[factors.event['frequencies'][0], factors.event['frequencies'][1] + scalar(shift), scalar(frequency)],
            electron_transfer=list(transfer), signs=[-1, 1, sign])
        if key not in self.current_operators:
            self.current_operators[key] = EventCoupling(current)
        operator = self.current_operators[key]
        readout_key = (key, join)
        if readout_key not in self.current_readouts:
            basis_soft = factors.features.evaluate(np.array([frequency]), join)
            basis_delta = difference_using_retained_splines(factors.features, factors.frequency[1], np.array([shift]), join, retained.spline_difference)
            potential_soft = self.contract(basis_soft)[0]
            potential_delta = self.contract(basis_delta)[0]
            values = [self.base[join][0], [before + change for before, change in zip(self.base[join][1], potential_delta)], potential_soft]
            self.current_readouts[readout_key] = (basis_soft, basis_delta, potential_soft, values)
        basis_soft, basis_delta, potential_soft, values = self.current_readouts[readout_key]
        harmonic = factors.harmonics[degree]
        coefficients, complete = operator.evaluate(values, self.gas, harmonic, degree)
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
