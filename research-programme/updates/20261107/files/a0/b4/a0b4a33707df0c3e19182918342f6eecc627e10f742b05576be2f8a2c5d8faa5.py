from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_moving_Legendre_current_20260921 import samples, wave_data, dust_data
from annular_candidate_Ward_source_20260921 import fields
from annular_candidate_energy_current_20260921 import richardson
from annular_candidate_coordinate_covectors_20260921 import local_polynomials
from annular_decimal_transport_v2_20260919 import decimal_array
from decimal import localcontext
from math import fsum
from time import perf_counter
import numpy as np


def test_functions(radius):
    coordinate = (np.asarray(radius) - 6) / .9
    envelope = np.maximum(1 - coordinate**2, 0)
    values = np.array([envelope**4 * coordinate**power for power in range(3)])
    slopes = np.array([(-8 * envelope**3 * coordinate**(power + 1)
                       + (power * envelope**4 * coordinate**(power - 1) if power else 0)) / .9
                       for power in range(3)])
    return values, slopes


class ArchivedMetricJet:
    def __init__(self, base, probes, steps):
        self.base, self.probes, self.steps, self.prefixes = base, probes, steps, {}
        for key, action in probes.items():
            increments = np.polynomial.chebyshev.chebval(1., action.solution['primitives'][0].T)
            self.prefixes[key] = np.array([fsum(increments[:index]) for index in range(len(increments))])

    def at(self, radius):
        if radius is getattr(self, 'last_radius', None):
            return self.last_values
        base, spatial = self.base.solver.values(self.base.solution, radius)
        values, derivatives = [], []
        for index in range(3):
            value_pair, derivative_pair = [], []
            for sign in [-1, 1]:
                action = self.probes[index, sign]
                solver, solution = action.solver, action.solution
                value, derivative = solver.values(solution, radius)
                selected = np.clip(np.searchsorted(solver.edges, radius, side='right') - 1, 0, len(solver.edges) - 2)
                mapped = 2 * (radius - solver.centers[selected]) / solver.lengths[selected]
                value = value.copy()
                value[0] = self.prefixes[index, sign][selected] + np.polynomial.chebyshev.chebval(
                    mapped, solution['primitives'][0, selected].T, tensor=False)
                value_pair.append(value)
                derivative_pair.append(derivative)
            values.append(value_pair)
            derivatives.append(derivative_pair)
        rate = richardson(np.array(values), self.steps)[1][-1]
        rate_spatial = richardson(np.array(derivatives), self.steps)[1][-1]
        self.last_radius = radius
        self.last_values = base, spatial, rate, rate_spatial
        return self.last_values


class JetSolver:
    def __init__(self, jet, time):
        self.jet, self.time = jet, time
        self.edges = jet.base.solver.edges

    def values(self, unused, radius):
        base, spatial, rate, rate_spatial = self.jet.at(radius)
        return base + self.time * rate, spatial + self.time * rate_spatial


class JetTangent:
    def __init__(self, jet):
        self.jet = jet

    def at(self, radius):
        unused, unused2, rate, unused3 = self.jet.at(radius)
        return np.broadcast_to(rate[1], (2, len(radius))), np.broadcast_to(-2 * rate[0] / radius, (2, len(radius)))


class KernelPrimitive:
    def __init__(self, action, order):
        self.action = action
        self.edges = action.solver.edges
        self.lengths = np.diff(self.edges)
        self.centers = (self.edges[:-1] + self.edges[1:]) / 2
        nodes = np.polynomial.chebyshev.chebpts1(order)
        radius = (self.centers[:, None] + self.lengths[:, None] * nodes / 2).ravel()
        values = self.at(radius).reshape(3, len(self.lengths), order)
        coefficients = np.polynomial.chebyshev.chebfit(nodes, values.reshape(-1, order).T, order - 1)
        coefficients = coefficients.reshape(order, 3, len(self.lengths))
        self.primitives = np.polynomial.chebyshev.chebint(coefficients, lbnd=-1, axis=0) * self.lengths[None, None, :] / 2
        totals = np.polynomial.chebyshev.chebval(1., self.primitives)
        self.prefix = np.column_stack([np.zeros(3), np.cumsum(totals[:, :-1], axis=1, dtype=np.longdouble)]).astype(float)

    def at(self, radius):
        values, unused = self.action.solver.values(self.action.solution, radius)
        lapse, metric = np.exp(values[1]), 1 - 2 * values[0] / radius
        return test_functions(radius)[0] / (lapse**2 * metric)

    def absolute(self, radius):
        radius = np.atleast_1d(radius)
        selected = np.clip(np.searchsorted(self.edges, radius, side='right') - 1, 0, len(self.lengths) - 1)
        mapped = 2 * (radius - self.centers[selected]) / self.lengths[selected]
        return self.prefix[:, selected] + np.polynomial.chebyshev.chebval(mapped, self.primitives[:, :, selected], tensor=False)

    def anchored(self, radius, source):
        return self.absolute(radius) - self.absolute(np.array([source]))


def prepare(action, loads, acceleration):
    with localcontext() as context:
        context.prec = 64
        polynomial, unused = local_polynomials(action.mesh, decimal_array(acceleration[:, :-1].T))
        image_rate = np.asarray(loads.factor.apply(decimal_array(loads.rates[:, :-1].T)), float)
    return polynomial, image_rate


def layer_moments(action, loads, tangent, kernel, acceleration, acceleration_polynomial, image_rates, label, order):
    row = samples(action, label, order)
    quadrature, geometry, cardinal = row['quadrature'], row['geometry'], row['cardinal']
    radius, jacobian, lapse, metric = [geometry[key] for key in ['radius', 'jacobian', 'lapse', 'metric']]
    measure, local, cells = quadrature['measure'], quadrature['local'], quadrature['cells']
    kinetic, spatial, displacement = geometry['kinetic'], geometry['gradient'], geometry['displacement']
    temporal, gradient_ref = row['temporal'], row['gradient']
    gradient = gradient_ref / jacobian
    speed = displacement * row['velocity']
    tests, test_slopes = test_functions(radius)
    primitive = kernel.anchored(radius, row['source'])
    wave = wave_data(row, tangent)
    nu_t, metric_t = tangent.at(radius)
    metric_log = nu_t[-1] + metric_t[-1] / (2 * metric)
    coefficients = np.einsum('cpl,l->cp', acceleration_polynomial, cardinal)[cells]
    acceleration_field = coefficients[:, 0] + local * (coefficients[:, 1] + local * coefficients[:, 2])
    acceleration_source = acceleration[:, -1] @ cardinal
    acceleration_time = acceleration_field + acceleration_source * row['motion']
    temporal_ref_rate = acceleration_time + row['velocity'] * row['motion_rate']
    momentum_rate = wave['momentum_rate'][-1] + kinetic * acceleration_time
    widths = np.diff(np.array([float(value) for value in action.edges]))[cells]
    gradient_coefficients = np.einsum('cpl,l->cp', action.gradient, cardinal)[cells]
    second_gradient = gradient_coefficients[:, 1] / widths
    gradient_ref_rate = (row['rate_gradient'] - geometry['jacobian_source'] * row['velocity'] * gradient) / jacobian
    temporal_radial = (row['rate_gradient'] - row['velocity'] *
        (geometry['jacobian_source'] * gradient_ref + displacement * second_gradient) / jacobian) / jacobian
    temporal_time = temporal_ref_rate - speed * temporal_radial
    gradient_time = gradient_ref_rate - speed * second_gradient / jacobian**2
    coefficient = spatial * jacobian
    coefficient_work = -(kinetic / jacobian) * (temporal * temporal_time - temporal**2 * metric_log)
    coefficient_work -= coefficient * gradient * gradient_time
    regular_moment = -(primitive * (measure * jacobian * coefficient_work)).sum(axis=1)

    nodal = action.geometry(action.knots, row['source'], label)
    node_primitive = kernel.anchored(nodal['radius'], row['source'])
    node_rate = cardinal @ loads.rates[:, :-1]
    nodal_test = node_rate[:, None] * node_primitive.T
    test_values = np.einsum('qi,qip->qp', row['shape'], nodal_test[quadrature['indices']])
    test_gradient = np.einsum('qi,qip->qp', quadrature['radial'], nodal_test[quadrature['indices']])
    weak_force = -(kinetic * temporal * row['velocity'] * displacement / jacobian + spatial * gradient_ref)
    field_moment = (measure * weak_force) @ test_gradient - (measure * momentum_rate) @ test_values
    image, image_rate = action.factor_values @ cardinal, image_rates @ cardinal
    load = np.asarray(action.sampling.T @ (image**2 / 2)).ravel()
    load_rate = np.asarray(action.sampling.T @ (image * image_rate)).ravel()
    with localcontext() as context:
        context.prec = 64
        changed_image = np.asarray(loads.factor.apply(decimal_array(nodal_test)), float)
    gram_field_moment = -((action.sampling @ nodal['gradient']) * image) @ changed_image
    atom_bulk = -nodal['gradient'] * load_rate - row['velocity'] * nodal['gradient_source'] * load
    gram_bulk_moment = -(node_primitive * atom_bulk).sum(axis=1)
    atom_energy = nodal['gradient'] * load
    gram_advection_moment = (kernel.at(nodal['radius']) * (nodal['displacement'] * row['velocity'] * atom_energy)).sum(axis=1)

    edges = np.array([float(value) for value in action.edges])
    cell_indices = np.arange(len(edges) - 1)
    left = fields(action, edges[:-1], cell_indices, np.zeros(len(cell_indices)), label)
    right = fields(action, edges[1:], cell_indices, np.ones(len(cell_indices)), label)
    face_radius = right['radius'][:-1]
    face_speed = (left['speed'][1:] + right['speed'][:-1]) / 2
    edge_work = face_speed * (left['energy'][1:] - right['energy'][:-1])
    face_moment = -(kernel.anchored(face_radius, row['source']) * edge_work).sum(axis=1)
    horizontal_wave = field_moment + regular_moment + face_moment
    horizontal_gram = gram_field_moment + gram_bulk_moment + gram_advection_moment

    dust = dust_data(action, row['source'], row['velocity'], tangent)
    source_test, source_slope = test_functions(row['source'])
    dust_moment = dust['momentum'] * source_test
    dust_rate = dust['momentum_rate'][-1] + dust['inertia'] * acceleration_source
    dust_moment_rate = dust_rate * source_test + dust['momentum'] * row['velocity'] * source_slope
    dust_force = action.dust(row['source'], row['velocity'])[1]
    dust_space = -row['velocity'] * dust['momentum'] * source_slope - dust_force * source_test
    dust_euler = (dust_rate - dust_force) * source_test

    volume = lapse * radius**2 / np.sqrt(metric)
    rho = (temporal**2 / lapse**2 + metric * gradient**2) / 2
    transverse = (temporal**2 / lapse**2 - metric * gradient**2) / 2
    wave_space = (measure * jacobian * volume *
        (-rho * test_slopes + (rho * geometry['lapse_log_radial'] + rho * geometry['metric_radial'] / (2 * metric)
         - 2 * transverse / radius) * tests)).sum(axis=1)
    node_test, node_slope = test_functions(nodal['radius'])
    gram_space = (atom_energy * (-node_slope + (nodal['lapse_log_radial'] + nodal['metric_radial'] / (2 * nodal['metric'])
                 + 2 / nodal['radius']) * node_test)).sum(axis=1)
    omitted_tension = (2 * atom_energy * node_test / nodal['radius']).sum(axis=1)
    minimal_wave = -(measure * kinetic * temporal * gradient * tests).sum(axis=1)
    kinetic_rate = geometry['kinetic_source'] * row['velocity'] - kinetic * metric_log
    minimal_wave_rate = -(measure * ((kinetic_rate * temporal * gradient + kinetic * temporal_ref_rate * gradient
        + kinetic * temporal * gradient_ref_rate) * tests + kinetic * temporal * gradient * speed * test_slopes)).sum(axis=1)
    point = fields(action, quadrature['reference'], cells, local, label)
    cell_source = (measure * (-momentum_rate - point['flux_x']) * gradient * tests).sum(axis=1)
    face_force = (left['beta'][1:] - left['alpha'][1:] * face_speed**2) * (left['gradient'][1:]**2 - right['gradient'][:-1]**2) / 2
    face_source = (test_functions(face_radius)[0] * face_force).sum(axis=1)
    endpoint_source = left['energy'][0] * test_functions(left['radius'][0])[0] - right['energy'][-1] * test_functions(right['radius'][-1])[0]
    return dict(horizontal=horizontal_wave + horizontal_gram + dust_moment,
                horizontal_wave=horizontal_wave, horizontal_gram=horizontal_gram, dust_moment=dust_moment,
                field_moment=field_moment, regular_moment=regular_moment, face_moment=face_moment,
                gram_field_moment=gram_field_moment, gram_bulk_moment=gram_bulk_moment, gram_advection_moment=gram_advection_moment,
                minimal=minimal_wave + dust_moment, minimal_rate=minimal_wave_rate + dust_moment_rate,
                wave_space=wave_space, gram_space=gram_space, dust_space=dust_space,
                cell_source=cell_source, face_source=face_source, endpoint_source=endpoint_source, dust_euler=dust_euler,
                wave_identity_error=minimal_wave_rate + wave_space - cell_source - face_source - endpoint_source,
                dust_identity_error=dust_moment_rate + dust_space - dust_euler, omitted_tension=omitted_tension)


def averaged_moments(action, loads, tangent, kernel, acceleration, spatial_order, material_order, deadline):
    polynomials, image_rates = prepare(action, loads, acceleration)
    labels, weights = np.polynomial.legendre.leggauss(material_order)
    labels, weights = labels / 2, weights / 2
    weights *= 6 * (labels + .5) * (.5 - labels)
    rows = []
    for label in labels:
        if perf_counter() > deadline:
            raise RuntimeError('Saved time boundary in radial-current moments')
        rows.append(layer_moments(action, loads, tangent, kernel, acceleration, polynomials, image_rates, label, spatial_order))
    raw = {key: np.array([row[key] for row in rows]) for key in rows[0]}
    summed = {key: weights @ value for key, value in raw.items()}
    return dict(labels=labels, weights=weights, **{'label_' + key: value for key, value in raw.items()},
                **{'sum_' + key: value for key, value in summed.items()})
