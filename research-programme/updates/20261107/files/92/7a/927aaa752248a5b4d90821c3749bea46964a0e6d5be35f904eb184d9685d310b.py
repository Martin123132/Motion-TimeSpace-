import mpmath as mp
import numpy as np

import factors236 as retained
from retained_column_differences import difference_using_retained_splines


class FullTailFactors:
    project_right = staticmethod(retained.Factors.project_right)

    def __init__(self, owner, bundle, tests):
        if mp.mp.dps < 60:
            raise ValueError("Source factors require at least60 decimal arithmetic digits")
        if getattr(bundle, "coordinate_convention", None) != "physical-background":
            raise ValueError("Source factors require an explicitly physical background")
        features = bundle.features
        if bundle.high.shape != bundle.low.shape or bundle.high.shape[0] != features.coefficient_count or bundle.high.shape[1] % 2:
            raise ValueError("Expected paired full-tail high/low history coefficients")
        if not np.isfinite(bundle.high).all() or not np.isfinite(bundle.low).all():
            raise ValueError("Nonfinite physical history")
        self.owner, self.features, self.tests = owner, features, tests
        self.spectral_count = features.spectral_count
        self.state_count = bundle.high.shape[1] // 2
        self.physical = {join: [[mp.mpf(float(high)) + mp.mpf(float(low))
            for high, low in zip(bundle.high[:, column], bundle.low[:, column])]
            for column in range(join, bundle.high.shape[1], 2)] for join in (0, 1)}
        self.high = {join: bundle.high[:-1, join::2].copy() for join in (0, 1)}
        self.low = {join: bundle.low[:-1, join::2].copy() for join in (0, 1)}
        self.gas = {join: [values[-1] for values in self.physical[join]] for join in (0, 1)}
        incoming = owner.transform * owner.spin.photon(owner.energy, owner.directions[0])
        outgoing = owner.transform * owner.spin.photon(owner.hard0, owner.directions[1])
        soft_ray = owner.transform * owner.rays[2]
        initial = owner.transform * owner.initial
        transfer = owner.transform * mp.matrix([mp.fsum(value**2 for value in owner.recoil0) / (owner.final0 + 1), *owner.recoil0])
        net = owner.transform * mp.matrix([owner.hard0 - owner.energy, *(-owner.recoil0)])
        self.frequency = np.array([float(incoming[0] / owner.temperature), float(outgoing[0] / owner.temperature)])
        self.directions = np.array([list(map(float, vector[1:])) for vector in (list(incoming), list(outgoing), list(soft_ray))])
        self.directions /= np.linalg.norm(self.directions, axis=1)[:, None]
        self.event = dict(temperature=owner.temperature, frequencies=[incoming[0] / owner.temperature, outgoing[0] / owner.temperature],
            electron_initial=list(initial), electron_transfer=list(transfer), signs=[-1, 1], directions=self.directions[:2].tolist())
        self.equilibrium = retained.equilibrium(self.event)
        self.test_base = tests.evaluate(self.frequency)
        self.basis_base = {join: features.evaluate(self.frequency, join) for join in (0, 1)}
        self.background = {join: [[retained.state235.contraction(line, physical[:self.spectral_count])
            for line in self.basis_base[join]] for physical in self.physical[join]] for join in (0, 1)}
        self.coefficients = {join: [self.equilibrium] + [retained.coefficient_state(self.event, potential, gas)
            for potential, gas in zip(self.background[join], self.gas[join])] for join in (0, 1)}
        self.left, self.right, self.harmonics = {}, {}, {}
        for degree in (0, 1, 2):
            harmonic = retained.angular.angular_feature(self.directions, degree)
            self.harmonics[degree] = harmonic
            photon = np.einsum("n,na,ni->ai", [-1, 1], self.test_base, harmonic[:2])
            if degree < 2:
                photon[0] = list(map(float, mp.matrix(list(net)[:1] if degree == 0 else list(net)[1:]) / owner.temperature))
                if degree == 0:
                    photon[1] = 0.
                    photon[2] = photon[0] / tests.basis.norms[1]
            gas_left = np.array(list(map(float, transfer))) / float(owner.temperature)
            gas_left = gas_left[:1] if degree == 0 else gas_left[1:] if degree == 1 else np.zeros(9)
            self.left[degree] = np.vstack([photon, gas_left])
            for join in (0, 1):
                self.right[join, degree] = [self.project_right(coefficients, self.basis_base[join], harmonic, degree)
                    for coefficients in self.coefficients[join]]

    def evaluate(self, soft_values, event_values, sign):
        if mp.mp.dps < 60:
            raise ValueError("Source factors require at least60 decimal arithmetic digits")
        if sign not in (-1, 1) or len(soft_values) != len(event_values) or not len(soft_values):
            raise ValueError("Paired nonempty soft events and an emission/absorption sign required")
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
                right_delta = np.zeros((len(shifts), self.state_count + 1, self.spectral_count + 1, harmonic.shape[-1]))
                reference = np.zeros_like(right_delta)
                for node_index, frequency in enumerate(frequencies):
                    occupation = 1 / mp.expm1(retained.scalar(frequency))
                    coupling = 2 * occupation * (1 + occupation) / (1 + 2 * occupation)
                    soft_wave = np.vstack([feature_soft[join][node_index, :, None] * harmonic[2], np.zeros((1, harmonic.shape[-1]))])
                    for state_index in range(self.state_count + 1):
                        actual = coefficients[join][node_index][state_index]
                        born = self.coefficients[join][state_index]
                        soft_background = mp.mpf(0) if state_index == 0 else retained.scalar(potential_soft[join][node_index, state_index - 1])
                        background_source = mp.mpf(0) if state_index == 0 else born["density"]
                        extra = float(coupling * soft_background) * self.right[join, degree][0] + float(coupling * background_source) * soft_wave
                        reference[node_index, state_index] = self.right[join, degree][state_index] + extra
                        difference = [actual["photon"][index] - born["photon"][index] - coupling * soft_background * self.equilibrium["photon"][index] for index in (0, 1)]
                        difference_soft = actual["photon"][2] - coupling * background_source
                        photon = np.einsum("n,na,ni->ai", list(map(float, difference)), self.basis_base[join], harmonic[:2])
                        photon += float(actual["photon"][1]) * feature_delta[join][node_index, :, None] * harmonic[1]
                        photon += float(difference_soft) * feature_soft[join][node_index, :, None] * harmonic[2]
                        gas = [actual["gas"] - born["gas"] - coupling * soft_background * self.equilibrium["gas"]] if degree == 0 else [value - old - coupling * soft_background * normal
                            for value, old, normal in zip(actual["velocity"], born["velocity"], self.equilibrium["velocity"])] if degree == 1 else [0.] * 9
                        right_delta[node_index, state_index] = np.vstack([photon, list(map(float, gas))])
                output[join, degree, "right_delta"] = right_delta
                output[join, degree, "reference"] = reference
        return output
