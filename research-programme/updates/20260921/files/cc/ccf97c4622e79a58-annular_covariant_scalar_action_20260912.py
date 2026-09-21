import numpy as np

from annular_gram_joint_action_20260909 import gram_matrices
from annular_metric_flux_jets_20260909 import SecondJet
from annular_nonlinear_history_20260912 import HistoryAction


def full_spatial_factors(count, include_gram):
    factors = np.diff(np.eye(count), axis=0)
    sampling = (np.eye(count)[:-1] + np.eye(count)[1:]) / 2
    if include_gram:
        extra_factors, extra_sampling = gram_matrices(count)
        factors = np.concatenate([factors, extra_factors])
        sampling = np.concatenate([sampling, extra_sampling])
    return factors, sampling


class CovariantScalarAction(HistoryAction):
    def __init__(self, history, include_gram):
        super().__init__(history)
        self.include_gram = include_gram
        self.factors, self.sampling = full_spatial_factors(self.radii.size, include_gram)
        self.factor, self.node = np.nonzero((self.factors != 0) | (self.sampling != 0))
        self.anchors = (self.sampling @ self.radii)[self.factor]
        self.targets = self.radii[self.node]
        self.distance = self.targets - self.anchors
        self.factor_weight = self.factors[self.factor, self.node]
        self.sample_weight = self.sampling[self.factor, self.node]
        self.node_weights = np.full(self.radii.size, self.spacing)
        self.node_weights[[0, -1]] /= 2

    def kinetic(self, times, direction, amplitude=0):
        fields, rates, second, delta, delta_rate, unused_second = self.history.evaluate(times[:, None], self.radii, direction, amplitude)
        geometry = self.geometry.evaluate(self.radii, fields)
        coefficient = self.radii**4 / geometry['C']
        coefficient_first = -coefficient * np.sum(geometry['C_y'] * rates[:3], axis=0) / geometry['C']
        coefficient_variation = -coefficient * np.sum(geometry['C_y'] * delta[:3], axis=0) / geometry['C']
        action = (.5 * coefficient * rates[3]**2) @ self.node_weights
        raw = (.5 * coefficient_variation * rates[3]**2 + coefficient * rates[3] * delta_rate[3]) @ self.node_weights
        interior = (.5 * coefficient_variation * rates[3]**2 - (coefficient_first * rates[3] + coefficient * second[3]) * delta[3]) @ self.node_weights
        boundary = (coefficient * rates[3] * delta[3]) @ self.node_weights
        return {'action': action, 'raw': raw, 'interior': interior, 'boundary': boundary, 'coefficient': coefficient}

    def full_integrated(self, direction, amplitude=0, order=20):
        spatial = self.integrated(direction, amplitude, order)
        points, weights = np.polynomial.legendre.leggauss(order)
        times = np.concatenate([.05 + .35 * points, [-.3, .4]])
        kinetic = self.kinetic(times, direction, amplitude)
        integration = .35 * weights
        kinetic_boundary = float(kinetic['boundary'][-1] - kinetic['boundary'][-2])
        return {'action': spatial['action'] + float(integration @ kinetic['action'][:-2]), 'raw': spatial['raw'] + float(integration @ kinetic['raw'][:-2]), 'adjoint': spatial['adjoint'] + float(integration @ kinetic['interior'][:-2]) + kinetic_boundary, 'spatial_action': spatial['action'], 'kinetic_action': float(integration @ kinetic['action'][:-2]), 'spatial_time_boundary': spatial['boundary'], 'kinetic_time_boundary': kinetic_boundary, 'minimum_J': spatial['minimum_J'], 'minimum_F': spatial['F_min'], 'minimum_chart_d': spatial['chart_min'], 'maximum_nonzero_P': spatial['P_max'], 'weighted_current_error': spatial['weighted_current_error']}


class TimePullbackHistory:
    def __init__(self, base):
        self.base = base
        self.soluble = False

    def map(self, time, radius):
        offset = radius - 6
        scale = np.exp(.4 * offset)
        displacement = .11 * offset + .2 * offset**2
        radial = .4 * scale * time + .11 + .4 * offset
        return scale * time + displacement, scale, radial, .4 * scale

    def evaluate(self, time, radius, direction, amplitude=0):
        if amplitude != 0 or np.any(direction):
            raise ValueError('Finite coordinate pullback is a separate manufactured covariance control.')
        moved_time, clock_scale, clock_radial, clock_radial_time = self.map(time, radius)
        fields, rates, second, unused_delta, unused_delta_rate, unused_delta_second = self.base.evaluate(moved_time, radius, [0, 0, 0, 0])
        jets = [SecondJet(fields[index], rates[index] * clock_scale, second[index] * clock_scale**2) for index in range(4)]
        geometry = 1 - 2 * jets[0] / radius
        shift = .1 * jets[1] * geometry**1.5 * jets[2]
        metric_tt = -jets[1] * jets[1] + shift * shift / geometry
        metric_tr = shift / geometry
        clock_r = SecondJet(clock_radial, np.broadcast_to(clock_radial_time, fields[0].shape))
        transformed_rr = 1 / geometry + 2 * metric_tr * clock_r + metric_tt * clock_r * clock_r
        transformed_tr = clock_scale * (metric_tr + metric_tt * clock_r)
        transformed_tt = clock_scale**2 * metric_tt
        new_geometry = 1 / transformed_rr
        new_shift = transformed_tr / transformed_rr
        new_lapse = (-transformed_tt + transformed_tr * transformed_tr / transformed_rr)**.5
        new_mass = radius * (1 - new_geometry) / 2
        new_momentum = new_shift / (.1 * new_lapse * new_geometry**1.5)
        transformed = [new_mass, new_lapse, new_momentum, jets[3]]
        values = np.stack([item.value for item in transformed])
        first = np.stack([item.first for item in transformed])
        acceleration = np.stack([item.second for item in transformed])
        zeros = np.zeros_like(values)
        return [values, first, acceleration, zeros, zeros, zeros]
