import mpmath as mp
import numpy as np

import factors236 as retained
from full_tail_factors import FullTailFactors
from full_tail_integrand import panel_block, separator_logarithm
from retained_column_differences import difference_using_retained_splines


class SplitColumns:
    def __init__(self, high, low):
        self.high = np.asarray(high, dtype=float).copy()
        self.low = np.asarray(low, dtype=float).copy()
        if self.high.ndim != 2 or self.high.shape != self.low.shape or self.high.shape[0] != 578:
            raise ValueError("All577 photon coordinates and gas are required")
        if not self.high.shape[1] or not np.isfinite(self.high).all() or not np.isfinite(self.low).all():
            raise ValueError("Finite nonempty split coefficient columns required")
        self.high.flags.writeable = False
        self.low.flags.writeable = False
        self.count = self.high.shape[1]

    def photon(self, rows):
        return retained.precise.stable_dot(rows, self.high[:-1], self.low[:-1])

    def gas(self, harmonic):
        return retained.precise.stable_dot(np.asarray(harmonic)[:, None], self.high[-1:], self.low[-1:]).T

    def right(self, values):
        return np.swapaxes(retained.precise.stable_dot(np.swapaxes(values, -1, -2), self.high, self.low), -1, -2)

    def matrix(self, values):
        return retained.precise.stable_dot(values, self.high, self.low)


class FullTailActionFactors(FullTailFactors):
    def __init__(self, owner, bundle, tests, projections):
        if set(projections) != {0, 1} or projections[0].count != projections[1].count:
            raise ValueError("Two matching full-coordinate join projections required")
        super().__init__(owner, bundle, tests)
        self.projections = projections
        self.full_right = self.right
        self.right = {key: projections[key[0]].right(np.asarray(value)) for key, value in self.full_right.items()}
        self.projected_basis = {join: projections[join].photon(self.basis_base[join]) for join in (0, 1)}

    def evaluate(self, soft_values, event_values, sign):
        if mp.mp.dps < 60:
            raise ValueError("Source factors require at least60 decimal arithmetic digits")
        if sign not in (-1, 1) or len(soft_values) != len(event_values) or not len(soft_values):
            raise ValueError("Paired nonempty soft events and physical sign required")
        owner = self.owner
        frequencies = np.array([float(abs(retained.scalar(value)) * owner.doppler / owner.temperature) for value in soft_values])
        shifts = np.array([float(event["hard_shift"] * owner.hard_doppler / owner.temperature) for event in event_values])
        test_delta = np.column_stack([shifts, retained.spline_difference(self.tests.spline, self.frequency[1], shifts)])
        test_delta[:, 1] = 0.
        test_delta[:, 2] = shifts / self.tests.basis.norms[1]
        test_soft = self.tests.evaluate(frequencies)
        feature_soft = {join: self.features.evaluate(frequencies, join) for join in (0, 1)}
        feature_delta = {join: difference_using_retained_splines(self.features, self.frequency[1], shifts, join, retained.spline_difference) for join in (0, 1)}
        potential_soft = {join: retained.precise.stable_dot(feature_soft[join], self.high[join], self.low[join]) for join in (0, 1)}
        potential_delta = {join: retained.precise.stable_dot(feature_delta[join], self.high[join], self.low[join]) for join in (0, 1)}
        projected_soft = {join: self.projections[join].photon(feature_soft[join]) for join in (0, 1)}
        projected_delta = {join: self.projections[join].photon(feature_delta[join]) for join in (0, 1)}
        output, coefficients = {}, {join: [] for join in (0, 1)}
        recoil_delta, photon_delta = [], []
        for node_index, event in enumerate(event_values):
            transfer = owner.transform * mp.matrix([event["kinetic"], *event["recoil"]])
            transfer_delta = owner.transform * mp.matrix([event["kinetic_shift"], *event["recoil_shift"]])
            photon_shift = owner.transform * mp.matrix([event["hard_shift"] + event["soft"], *(-event["recoil_shift"])])
            recoil_delta.append(list(map(float, transfer_delta / owner.temperature)))
            photon_delta.append(list(map(float, photon_shift / owner.temperature)))
            current = dict(self.event, frequencies=[self.event["frequencies"][0], self.event["frequencies"][1] + retained.scalar(shifts[node_index]), retained.scalar(frequencies[node_index])],
                electron_transfer=list(transfer), signs=[-1, 1, sign])
            for join in (0, 1):
                values = [retained.equilibrium(current)]
                for state_index in range(self.state_count):
                    potential = [self.background[join][state_index][0], self.background[join][state_index][1] + retained.scalar(potential_delta[join][node_index, state_index]),
                        retained.scalar(potential_soft[join][node_index, state_index])]
                    values.append(retained.coefficient_state(current, potential, self.gas[join][state_index]))
                coefficients[join].append(values)
        recoil_delta, photon_delta = np.array(recoil_delta), np.array(photon_delta)
        for degree in (0, 1, 2):
            harmonic = self.harmonics[degree]
            delta_left = test_delta[:, :, None] * harmonic[1] + sign * test_soft[:, :, None] * harmonic[2]
            if degree < 2:
                delta_left[:, 0] = photon_delta[:, :1] if degree == 0 else photon_delta[:, 1:]
                if degree == 0:
                    delta_left[:, 1] = sign / self.tests.basis.norms[0]
                    delta_left[:, 2] = (photon_delta[:, :1] - self.tests.basis.mean * sign) / self.tests.basis.norms[1]
            gas_delta = recoil_delta[:, :1] if degree == 0 else recoil_delta[:, 1:] if degree == 1 else np.zeros((len(shifts), 9))
            output[degree, "left_delta"] = np.concatenate([delta_left, gas_delta[:, None, :]], axis=1)
            for join in (0, 1):
                projection = self.projections[join]
                right_delta = np.zeros((len(shifts), self.state_count + 1, projection.count, harmonic.shape[-1]))
                reference = np.zeros_like(right_delta)
                for node_index, frequency in enumerate(frequencies):
                    occupation = 1 / mp.expm1(retained.scalar(frequency))
                    coupling = 2 * occupation * (1 + occupation) / (1 + 2 * occupation)
                    soft_wave = projected_soft[join][node_index, :, None] * harmonic[2]
                    for state_index in range(self.state_count + 1):
                        actual = coefficients[join][node_index][state_index]
                        born = self.coefficients[join][state_index]
                        soft_background = mp.mpf(0) if state_index == 0 else retained.scalar(potential_soft[join][node_index, state_index - 1])
                        background_source = mp.mpf(0) if state_index == 0 else born["density"]
                        extra = float(coupling * soft_background) * self.right[join, degree][0] + float(coupling * background_source) * soft_wave
                        reference[node_index, state_index] = self.right[join, degree][state_index] + extra
                        difference = [actual["photon"][index] - born["photon"][index] - coupling * soft_background * self.equilibrium["photon"][index] for index in (0, 1)]
                        difference_soft = actual["photon"][2] - coupling * background_source
                        photon = np.einsum("n,nc,ni->ci", list(map(float, difference)), self.projected_basis[join], harmonic[:2])
                        photon += float(actual["photon"][1]) * projected_delta[join][node_index, :, None] * harmonic[1]
                        photon += float(difference_soft) * projected_soft[join][node_index, :, None] * harmonic[2]
                        gas = [actual["gas"] - born["gas"] - coupling * soft_background * self.equilibrium["gas"]] if degree == 0 else [value - old - coupling * soft_background * normal
                            for value, old, normal in zip(actual["velocity"], born["velocity"], self.equilibrium["velocity"])] if degree == 1 else [0.] * 9
                        right_delta[node_index, state_index] = photon + projection.gas(list(map(float, gas)))
                output[join, degree, "right_delta"] = right_delta
                output[join, degree, "reference"] = reference
        return output


def reference_action(factors, frequency, measure, mode, join, degree, event_weight, angular_weight):
    if mp.mp.dps < 60 or mode not in ("control", "difference") or join not in (0, 1) or degree not in (0, 1, 2):
        raise ValueError("Retained high precision source arguments required")
    frequency, measure = np.asarray(frequency, dtype=float), np.asarray(measure, dtype=float)
    if frequency.ndim != 1 or not len(frequency) or measure.shape != frequency.shape or not np.isfinite(frequency).all() or np.any(frequency <= 0) or not np.isfinite(measure).all():
        raise ValueError("Matching finite positive frequency and measure vectors required")
    if not np.isfinite(float(event_weight)) or not np.isfinite(float(angular_weight)):
        raise ValueError("Finite source weights required")
    basis = factors.features.evaluate(frequency, join)
    potential = retained.precise.stable_dot(basis, factors.high[join], factors.low[join])
    wave = factors.projections[join].photon(basis)[:, :, None] * factors.harmonics[degree][2]
    occupation = 1 / np.expm1(frequency)
    base = factors.right[join, degree]
    medium = np.zeros((len(frequency), *base.shape))
    for state in range(1, factors.state_count + 1):
        medium[:, state] = potential[:, state - 1, None, None] * base[0]
        medium[:, state] += float(factors.coefficients[join][state]["density"]) * wave
    weight = -2 * float(factors.owner.pole[mode]) * measure * occupation / frequency
    right_sum = base * np.sum(weight) + np.einsum("n,nvci->vci", weight * (1 + occupation), medium)
    result = np.einsum("ai,vci->vac", factors.left[degree], right_sum, optimize=True)
    return result * (.5 * event_weight * angular_weight / (2 * degree + 1))


def panel_action(factors, frequency, measure, densities, factors_data, mode, join, degree,
                 event_weight, angular_weight, emission_allowed, absorption_allowed):
    if not isinstance(factors, FullTailActionFactors):
        raise ValueError("Explicit full-coordinate action factors required")
    if not emission_allowed and not absorption_allowed:
        return reference_action(factors, frequency, measure, mode, join, degree, event_weight, angular_weight)
    return panel_block(factors, frequency, measure, densities, factors_data, mode, join, degree,
        event_weight, angular_weight, emission_allowed, absorption_allowed)


def logarithm_action(factors, mode, join, degree, event_weight, angular_weight):
    if not isinstance(factors, FullTailActionFactors):
        raise ValueError("Explicit full-coordinate action factors required")
    return separator_logarithm(factors, mode, join, degree, event_weight, angular_weight)
