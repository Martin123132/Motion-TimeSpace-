from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_physical_native_kernel_20260928 import decimals
from annular_position_reaction_20260929 import second_radial
from annular_old_field_reaction_20260929 import coefficient_data
from derive_annular_native_shape_stress_20260928 import physical_data
from bisect import bisect_right
from decimal import Decimal
import numpy as np


ZERO = Decimal(0)
ONE = Decimal(1)


class Directional:
    def __init__(self, value, tangent=ZERO):
        self.value = value if isinstance(value, Decimal) else Decimal(value)
        self.tangent = tangent if isinstance(tangent, Decimal) else Decimal(tangent)

    @staticmethod
    def lift(value):
        return value if isinstance(value, Directional) else Directional(value)

    def __add__(self, other):
        other = self.lift(other)
        return Directional(self.value + other.value, self.tangent + other.tangent)

    __radd__ = __add__

    def __neg__(self):
        return Directional(-self.value, -self.tangent)

    def __sub__(self, other):
        return self + (-self.lift(other))

    def __rsub__(self, other):
        return self.lift(other) - self

    def __mul__(self, other):
        other = self.lift(other)
        return Directional(self.value * other.value,
            self.tangent * other.value + self.value * other.tangent)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self.lift(other)
        quotient = self.value / other.value
        return Directional(quotient, (self.tangent - quotient * other.tangent) / other.value)

    def __rtruediv__(self, other):
        return self.lift(other) / self

    def __pow__(self, exponent):
        if not isinstance(exponent, int):
            raise TypeError('Only integer powers are needed by the native kernel')
        if exponent == 0:
            return Directional(ONE)
        return Directional(self.value ** exponent,
            exponent * self.value ** (exponent - 1) * self.tangent)

    def sqrt(self):
        root = self.value.sqrt()
        return Directional(root, self.tangent / (2 * root))

    def __lt__(self, other):
        return self.value < self.lift(other).value

    def __le__(self, other):
        return self.value <= self.lift(other).value

    def __gt__(self, other):
        return self.value > self.lift(other).value

    def __ge__(self, other):
        return self.value >= self.lift(other).value


def chebyshev_value(coefficients, coordinate):
    future, following = ZERO, ZERO
    for coefficient in coefficients[:0:-1]:
        future, following = coefficient + 2 * coordinate * future - following, future
    return coefficients[0] + coordinate * future - following


def chebyshev_derivative(coefficients):
    degree = len(coefficients) - 1
    if degree == 0:
        return [ZERO]
    output = [ZERO] * degree
    for index in range(degree - 1, -1, -1):
        output[index] = 2 * (index + 1) * coefficients[index + 1]
        if index + 2 < degree:
            output[index] += output[index + 2]
    output[0] /= 2
    return output


class DecimalMetric:
    def __init__(self, solver, solution):
        self.solver, self.solution = solver, solution
        self.edges = list(decimals(solver.edges))
        self.centers = decimals(solver.centers)
        self.lengths = decimals(solver.lengths)
        self.cache = {}

    def coefficients(self, component, cell):
        key = component, cell
        if key not in self.cache:
            primitive = list(decimals(self.solution['primitives'][component, cell]))
            radial = list(decimals(self.solution['rhs_coefficients'][component, cell]))
            left = Decimal.from_float(float(self.solution['left'][component, cell]))
            self.cache[key] = primitive, radial, chebyshev_derivative(radial), left
        return self.cache[key]

    def at(self, radii):
        values, radial, second = [np.empty((2, len(radii)), dtype=object) for unused in range(3)]
        for index, radius in enumerate(radii):
            cell = min(max(bisect_right(self.edges, radius) - 1, 0), len(self.lengths) - 1)
            coordinate = 2 * (radius - self.centers[cell]) / self.lengths[cell]
            for component in range(2):
                primitive, derivative, twice, left = self.coefficients(component, cell)
                values[component, index] = left + chebyshev_value(primitive, coordinate)
                radial[component, index] = chebyshev_value(derivative, coordinate)
                second[component, index] = chebyshev_value(twice, coordinate) * 2 / self.lengths[cell]
        return values, radial, second


def metric_coefficients(radius, values, radial, second, movement, variation, variation_r):
    mass, lapse_log = values
    mass_r, lapse_log_r = radial
    moved_mass = variation[0] + mass_r * movement
    moved_lapse = variation[1] + lapse_log_r * movement
    moved_mass_r = variation_r[0] + second[0] * movement
    moved_lapse_r = variation_r[1] + second[1] * movement
    metric = 1 - 2 * mass / radius
    metric_r = -2 * mass_r / radius + 2 * mass / radius ** 2
    metric_change = -2 * moved_mass / radius + 2 * mass * movement / radius ** 2
    radial_change = -2 * moved_mass_r / radius + 2 * mass_r * movement / radius ** 2
    radial_change += 2 * moved_mass / radius ** 2 - 4 * mass * movement / radius ** 3
    beta = radius ** 2 * lapse_log.exp() * metric.sqrt()
    log_gradient = 2 / radius + lapse_log_r + metric_r / (2 * metric)
    beta_r = beta * log_gradient
    beta_change = beta * (2 * movement / radius + moved_lapse + metric_change / (2 * metric))
    beta_r_change = beta_change * log_gradient + beta * (-2 * movement / radius ** 2
        + moved_lapse_r + radial_change / (2 * metric) - metric_r * metric_change / (2 * metric ** 2))
    return beta, beta_r, beta_change, beta_r_change


def native_force_tangent(native, data, field_change, edge_change, beta_change, beta_r_change):
    if not native.enabled:
        zero = np.full(native.count + 1, ZERO, dtype=object)
        return zero.copy(), zero.copy()
    lift = lambda values, tangent: np.array([Directional(value, derivative)
        for value, derivative in zip(values, tangent)], dtype=object)
    result = native.evaluate(lift(data['edges'], edge_change), lift(data['field'], field_change),
        lift(data['beta'], beta_change))
    source = -sum(result['edge_gradient'] * data['displacement'], ZERO)
    source -= sum(result['load'] * lift(data['beta_radial'], beta_r_change)
        * data['displacement'][native.native_edges], ZERO)
    force = np.r_[-result['field_gradient'], source]
    return (np.array([Directional.lift(value).tangent for value in force], dtype=object),
        np.array([Directional.lift(value).value for value in force], dtype=object))


class NativePrecision:
    def __init__(self, native, loads, action, field_direction, source_direction, edge_vertices, position):
        self.native, self.loads, self.action = native, loads, action
        self.field_direction, self.source_direction, self.edge_vertices = field_direction, source_direction, edge_vertices
        self.position = position
        self.decimal_fields = decimals(field_direction)
        self.decimal_source = decimals(source_direction)
        self.decimal_edges = decimals(edge_vertices)
        self.cardinal_coefficients = decimals(action.owner.layer_rule.inverse)
        self.source = decimals(action.source)
        self.metric = DecimalMetric(action.solver, action.solution)
        self.responses = [DecimalMetric(item.solver, item.solution) for item in position.responses]

    def cardinal(self, label):
        label = label if isinstance(label, Decimal) else Decimal.from_float(float(label))
        return np.array([chebyshev_value(column, 2 * label)
            for column in self.cardinal_coefficients.T], dtype=object)

    def packet(self, label, mode):
        if mode not in ['legacy', 'decimal_geometry', 'decimal_metric', 'decimal_all']:
            raise ValueError('Unknown isolated precision mode')
        native, action = self.native, self.action
        data = physical_data(native, self.loads, action, float(label))
        cardinal = decimals(data['cardinal']) if mode != 'decimal_all' else self.cardinal(label)
        if mode != 'legacy':
            source = sum(cardinal * self.source, ZERO)
            label_value = label if isinstance(label, Decimal) else Decimal.from_float(float(label))
            width = Decimal.from_float(float(action.owner.width))
            lower, upper = native.references[0] + width * label_value, native.references[-1] + width * label_value
            data['edges'] = np.array([lower + (source - lower) * fraction if index <= native.anchor
                else upper + (source - upper) * fraction for index, fraction in enumerate(data['displacement'])], dtype=object)
            data['field'] = self.loads.coordinates[:, :-1].T @ cardinal
            field_change = cardinal @ self.decimal_fields
            edge_change = cardinal @ self.decimal_edges + data['displacement'] * sum(cardinal * self.decimal_source, ZERO)
        else:
            field_change = decimals(data['cardinal'] @ self.field_direction)
            edge_change = decimals(data['cardinal'] @ self.edge_vertices) + data['displacement'] * Decimal.from_float(float(data['cardinal'] @ self.source_direction))
        radius = data['edges'][native.native_edges]
        movement = edge_change[native.native_edges]
        if mode in ['legacy', 'decimal_geometry']:
            radius_float, movement_float = np.asarray(radius, float), np.asarray(movement, float)
            values, radial = action.solver.values(action.solution, radius_float)
            second = second_radial(action.solver, action.solution, radius_float)
            variation, variation_r = self.position.at(radius_float)
            unused, beta, unused2, beta_r = coefficient_data(radius_float + 1e-25j * movement_float,
                values + 1e-25j * (variation + radial * movement_float),
                radial + 1e-25j * (variation_r + second * movement_float))
            beta_change, beta_r_change = decimals(beta.imag / 1e-25), decimals(beta_r.imag / 1e-25)
            if mode != 'legacy':
                unused, original_beta, unused2, original_beta_r = coefficient_data(radius_float, values, radial)
                data['beta'], data['beta_radial'] = decimals(original_beta), decimals(original_beta_r)
        else:
            values, radial, second = self.metric.at(radius)
            response_pairs = [response.at(radius) for response in self.responses]
            variation, variation_r = [sum(pair[component] for pair in response_pairs) for component in [0, 1]]
            coefficients = np.array([metric_coefficients(radius[index], values[:, index], radial[:, index],
                second[:, index], movement[index], variation[:, index], variation_r[:, index])
                for index in range(len(radius))], dtype=object).T
            data['beta'], data['beta_radial'], beta_change, beta_r_change = coefficients
        data['cardinal'] = cardinal
        return data, field_change, edge_change, beta_change, beta_r_change

    def evaluate(self, label, mode):
        packet = self.packet(label, mode)
        derivative, base = native_force_tangent(self.native, *packet)
        return derivative, base, packet[0]['cardinal']
