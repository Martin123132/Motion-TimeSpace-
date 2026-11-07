from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_moving_Legendre_current_20260921 import samples
from annular_directional_coupled_Euler_20260928 import interpolate_nodal
from annular_physical_native_kernel_20260928 import decimals, maximum
from derive_annular_native_shape_stress_20260928 import physical_data
from decimal import Decimal
from functools import lru_cache
from time import perf_counter
import mpmath as mp
import numpy as np
import sympy as sp


class MixedJet:
    __array_priority__ = 1000

    def __init__(self, value, position=0, time=0, mixed=0):
        self.parts = tuple(np.broadcast_arrays(value, position, time, mixed))

    @staticmethod
    def cast(value):
        return value if isinstance(value, MixedJet) else MixedJet(value)

    def __add__(self, other):
        other = self.cast(other)
        return MixedJet(*[left + right for left, right in zip(self.parts, other.parts)])

    __radd__ = __add__

    def __neg__(self):
        return MixedJet(*[-value for value in self.parts])

    def __sub__(self, other):
        return self + -self.cast(other)

    def __rsub__(self, other):
        return self.cast(other) + -self

    def __mul__(self, other):
        base, position, time, mixed = self.parts
        other_base, other_position, other_time, other_mixed = self.cast(other).parts
        return MixedJet(base * other_base, position * other_base + base * other_position,
            time * other_base + base * other_time,
            mixed * other_base + position * other_time + time * other_position + base * other_mixed)

    __rmul__ = __mul__

    def __pow__(self, power):
        if power == 0:
            return MixedJet(np.ones_like(self.parts[0]))
        if power == 1:
            return self
        base, position, time, mixed = self.parts
        first = power * base**(power - 1)
        second = power * (power - 1) * base**(power - 2)
        return MixedJet(base**power, first * position, first * time,
            first * mixed + second * position * time)

    def __truediv__(self, other):
        return self * self.cast(other)**-1

    def __rtruediv__(self, other):
        return self.cast(other) * self**-1


def symbolic_checks(evidence):
    position, time = sp.symbols('position time')
    base, pos, rate, mixed = sp.symbols('base pos rate mixed')
    family = base + position * pos + time * rate + position * time * mixed
    expression = family**-1
    exact = sp.diff(expression, position, time).subs({position: 0, time: 0})
    evidence.check('mixed_reciprocal_rule', sp.simplify(exact - (2 * pos * rate / base**3 - mixed / base**2)) == 0)
    label, width, displacement, speed = sp.symbols('label width displacement speed', positive=True)
    weight = sp.Rational(3, 2) - 6 * label**2
    interior = sp.integrate(sp.diff(weight, label, 2) * displacement * speed / width**2, (label, -sp.Rational(1, 2), sp.Rational(1, 2)))
    atoms = 12 * displacement * speed / width**2
    evidence.check('translated_collar_mass_requires_endpoint_atoms', sp.simplify(interior + atoms) == 0 and interior != 0)
    radius, load = sp.Function('radius')(position, time), sp.Function('load')(position, time)
    test = sp.Function('test')
    direct = sp.diff(load * test(radius), position, time)
    expected = sp.diff(load, position, time) * test(radius)
    expected += (sp.diff(load, position) * sp.diff(radius, time) + sp.diff(load, time) * sp.diff(radius, position)
        + load * sp.diff(radius, position, time)) * sp.diff(test(radius), radius)
    expected += load * sp.diff(radius, position) * sp.diff(radius, time) * sp.diff(test(radius), radius, 2)
    evidence.check('mixed_material_pushforward_identity', sp.simplify(direct - expected) == 0)


def wave_moments(loads, action, directions, correction, mode_rate, acceleration, order, spatial_order, deadline):
    labels, weights = np.polynomial.legendre.leggauss(order)
    labels, weights = labels / 2, weights / 2
    weights *= 6 * (labels + .5) * (.5 - labels)
    reference_edges = np.array([float(value) for value in action.edges])
    result = np.zeros((2, 3, 4))
    explicit = np.zeros((2, 3))
    field_direction = directions['field_vertices'] - correction[:, :-1]
    source_direction = -correction[:, -1]
    local_error, local_scale, minimum_jacobian = 0., 0., np.inf
    for label, weight in zip(labels, weights):
        if perf_counter() > deadline:
            raise RuntimeError('Safe mixed-wave material boundary')
        row = samples(action, label, spatial_order)
        geometry, quad, cardinal = row['geometry'], row['quadrature'], row['cardinal']
        radius, jacobian = geometry['radius'], geometry['jacobian']
        minimum_jacobian = min(minimum_jacobian, float(np.min(jacobian)))
        indices = np.asarray(action.mesh['elements'])[quad['cells']]
        widths = np.diff(reference_edges)[quad['cells']] * jacobian
        interpolate = lambda values: interpolate_nodal(cardinal @ values, indices, quad['local'], widths)
        unused, field_radial = interpolate(field_direction)
        transported, transported_radial = interpolate(mode_rate[:, :-1])
        field_acceleration = interpolate(acceleration[:, :-1])[0]
        source_mode = float(cardinal @ source_direction)
        source_rate = float(cardinal @ mode_rate[:, -1])
        source_acceleration = float(cardinal @ acceleration[:, -1])
        edge = cardinal @ directions['edge_vertices']
        cells, local = quad['cells'], quad['local']
        eta = (1 - local) * edge[cells] + local * edge[cells + 1]
        eta_radial = (edge[cells + 1] - edge[cells]) / widths
        displacement = geometry['displacement']
        slope = geometry['jacobian_source'] / jacobian
        movement, movement_radial = eta + displacement * source_mode, eta_radial + slope * source_mode
        speed, speed_radial = displacement * row['velocity'], slope * row['velocity']
        mixed_movement, mixed_radial = displacement * source_rate, slope * source_rate
        gradient = row['gradient'] / jacobian
        gradient_time_numerator = row['rate_gradient'] / jacobian
        relative_jacobian = MixedJet(np.ones_like(radius), movement_radial, speed_radial, mixed_radial)
        gradient_jet = MixedJet(gradient, field_radial, gradient_time_numerator, transported_radial) / relative_jacobian
        speed_jet = MixedJet(speed, mixed_movement, displacement * source_acceleration)
        temporal_jet = MixedJet(row['rate'], transported, field_acceleration) - speed_jet * gradient_jet
        radius_jet = MixedJet(radius - 6, movement, speed, mixed_movement)
        gradient_position = field_radial - gradient * movement_radial
        gradient_time = gradient_time_numerator - gradient * speed_radial
        gradient_mixed = transported_radial - gradient_position * speed_radial - gradient_time * movement_radial - gradient * mixed_radial
        temporal = row['rate'] - speed * gradient
        temporal_position = transported - mixed_movement * gradient - speed * gradient_position
        temporal_time = field_acceleration - displacement * source_acceleration * gradient - speed * gradient_time
        temporal_mixed = -mixed_movement * gradient_time - displacement * source_acceleration * gradient_position - speed * gradient_mixed
        measure = quad['measure'] * jacobian
        for channel, jet, value, derivative_pos, derivative_time, derivative_mixed in [
            (0, temporal_jet, temporal, temporal_position, temporal_time, temporal_mixed),
            (1, gradient_jet, gradient, gradient_position, gradient_time, gradient_mixed)]:
            density = value**2
            density_position = movement_radial * density + 2 * value * derivative_pos
            density_time = speed_radial * density + 2 * value * derivative_time
            density_mixed = mixed_radial * density + 2 * movement_radial * value * derivative_time
            density_mixed += 2 * speed_radial * value * derivative_pos + 2 * (derivative_pos * derivative_time + value * derivative_mixed)
            for power in range(3):
                product = relative_jacobian * jet**2 * radius_jet**power
                profile = (radius - 6)**power
                first = np.zeros_like(radius) if power == 0 else power * (radius - 6)**(power - 1)
                second = np.full_like(radius, 2.) if power == 2 else np.zeros_like(radius)
                alternative = profile * density_mixed + first * (movement * density_time + speed * density_position)
                alternative += (second * movement * speed + first * mixed_movement) * density
                local_error = max(local_error, float(np.max(abs(product.parts[3] - alternative))))
                local_scale = max(local_scale, float(np.max(abs(alternative))))
                result[channel, power] += weight * np.array([measure @ item for item in product.parts])
                explicit[channel, power] += weight * (measure @ alternative)
    return dict(moments=result, explicit_mixed=explicit, local_error=local_error,
        local_scale=local_scale, minimum_jacobian=minimum_jacobian)


def native_label(engine, mode_rate, label, step=Decimal('1e-12')):
    image, position, data, edge_direction, field_direction = engine.native_direct(label)
    cardinal = decimals(data['cardinal'])
    rate_direction = decimals(mode_rate[:, :-1].T) @ cardinal
    edge_rate_direction = data['displacement'] * (decimals(mode_rate[:, -1]) @ cardinal)
    edge_rate = data['displacement'] * data['source_velocity']
    time = engine.native.tangent(data['edges'], data['field'], edge_rate, data['rate'])
    mixed = []
    for magnitude in [step, step / 2]:
        pair = []
        for sign in [-1, 1]:
            amount = sign * magnitude
            pair.append(engine.native.tangent(data['edges'] + amount * edge_direction,
                data['field'] + amount * field_direction, edge_rate + amount * edge_rate_direction,
                data['rate'] + amount * rate_direction))
        mixed.append((pair[1] - pair[0]) / (2 * magnitude))
    return np.asarray([image, position, time, mixed[-1]], float), float(maximum(mixed[-1] - mixed[0]))


def native_expansion(engine, mode_rate, degree, progress):
    labels = np.cos(np.arange(degree + 1) * np.pi / degree) / 2
    values, errors = [], []
    for index, label in enumerate(labels):
        if perf_counter() > engine.loads.deadline:
            raise RuntimeError('Safe native mixed shape boundary')
        row, error = native_label(engine, mode_rate, label)
        values.append(row)
        errors.append(error)
        if index % 8 == 0:
            progress('native-mixed-label-' + str(index))
    coefficients = np.array([np.polynomial.chebyshev.chebfit(2 * labels, np.array(values)[:, component], degree)
        for component in range(4)])
    return dict(labels=labels, values=np.array(values), coefficients=coefficients, step_errors=np.array(errors))


def decimal_coefficients(values):
    return decimals(values)


def label_derivative(coefficients):
    count = len(coefficients)
    if count <= 1:
        return np.full_like(coefficients, Decimal(0))
    answer = np.full((count - 1, *coefficients.shape[1:]), Decimal(0), dtype=object)
    for index in range(count - 2, -1, -1):
        answer[index] = 2 * (index + 1) * coefficients[index + 1]
        if index + 2 < len(answer):
            answer[index] += answer[index + 2]
    answer[0] /= 2
    return 2 * answer


def evaluate_polynomial(coefficients, label, derivative=0):
    for unused in range(derivative):
        coefficients = label_derivative(coefficients)
    return np.polynomial.chebyshev.chebval(2 * label, coefficients)


@lru_cache(maxsize=4)
def decimal_rule(order):
    with mp.workdps(80):
        nodes, weights = mp.gauss_quadrature(order, 'legendre')
        return tuple((Decimal(str(nodes[index] / 2)), Decimal(str(weights[index] / 2))) for index in range(order))


def map_coefficients(engine, mode_rate, native):
    inverse = engine.owner.layer_rule.inverse
    source = decimal_coefficients(inverse @ engine.material.coordinates[:, -1])
    source_direction = decimal_coefficients(inverse @ engine.direction[:, -1])
    source_velocity = decimal_coefficients(inverse @ engine.loads.rates[:, -1])
    source_mixed = decimal_coefficients(inverse @ mode_rate[:, -1])
    if not native:
        return tuple(value[:, None] for value in [source, source_direction, source_velocity, source_mixed])
    reference = np.array(engine.native.references, object)[engine.native.native_edges]
    lower, anchor, upper = engine.native.references[0], engine.native.references[engine.native.anchor], engine.native.references[-1]
    displacement = np.array([(point - lower) / (anchor - lower) if point <= anchor else (upper - point) / (upper - anchor) for point in reference], object)
    radius = source[:, None] * displacement
    radius[0] += reference - anchor * displacement
    radius[1] += Decimal.from_float(float(engine.owner.width)) * (1 - displacement) / 2
    support = decimal_coefficients(inverse @ engine.edge_vertices[:, engine.native.native_edges])
    return radius, support + source_direction[:, None] * displacement, source_velocity[:, None] * displacement, source_mixed[:, None] * displacement


def pushforward_parts(engine, maps, coefficients, label, native):
    radius, movement, speed, mixed_map = [evaluate_polynomial(value, label) for value in maps]
    jacobian, jacobian_label, jacobian_label2 = [evaluate_polynomial(maps[0], label, degree) for degree in [1, 2, 3]]
    if min(jacobian) <= 0:
        raise RuntimeError('Non-positive label Jacobian')
    movement_label, speed_label, mixed_map_label = [evaluate_polynomial(value, label, 1) for value in maps[1:]]
    movement_label2, speed_label2 = [evaluate_polynomial(value, label, 2) for value in maps[1:3]]
    if native:
        image, image_position, image_time, image_mixed = [evaluate_polynomial(value, label) for value in coefficients]
        image_label, image_position_label, image_time_label = [evaluate_polynomial(value, label, 1) for value in coefficients[:3]]
        image_label2 = evaluate_polynomial(coefficients[0], label, 2)
        apply = lambda values: engine.native.apply('sampling', values, True)
        load = apply(image**2 / 2)
        load_position, load_time = apply(image * image_position), apply(image * image_time)
        load_mixed = apply(image_position * image_time + image * image_mixed)
        load_label = apply(image * image_label)
        load_label2 = apply(image_label**2 + image * image_label2)
        load_position_label = apply(image_label * image_position + image * image_position_label)
        load_time_label = apply(image_label * image_time + image * image_time_label)
    else:
        load = np.array([Decimal(1)], object)
        load_position, load_time, load_mixed, load_label, load_label2, load_position_label, load_time_label = [np.array([Decimal(0)], object) for unused in range(7)]
    weight = Decimal('1.5') - 6 * label**2
    weight_label, weight_label2 = -12 * label, Decimal(-12)
    first = load_position * speed + load_time * movement + load * mixed_map
    first_label = load_position_label * speed + load_position * speed_label + load_time_label * movement + load_time * movement_label
    first_label += load_label * mixed_map + load * mixed_map_label
    second = load * movement * speed
    second_label = load_label * movement * speed + load * (movement_label * speed + movement * speed_label)
    second_label2 = load_label2 * movement * speed + 2 * load_label * (movement_label * speed + movement * speed_label)
    second_label2 += load * (movement_label2 * speed + 2 * movement_label * speed_label + movement * speed_label2)
    first_density_label = (weight_label * first + weight * first_label) / jacobian - weight * first * jacobian_label / jacobian**2
    second_density_label = (weight_label * second + weight * second_label) / jacobian - weight * second * jacobian_label / jacobian**2
    second_density_label2 = (weight_label2 * second + 2 * weight_label * second_label + weight * second_label2) / jacobian
    second_density_label2 -= 2 * (weight_label * second + weight * second_label) * jacobian_label / jacobian**2
    second_density_label2 -= weight * second * jacobian_label2 / jacobian**2
    second_density_label2 += 2 * weight * second * jacobian_label**2 / jacobian**3
    regular = weight * load_mixed / jacobian - first_density_label / jacobian
    regular += second_density_label2 / jacobian**2 - second_density_label * jacobian_label / jacobian**3
    weak = []
    for power in range(3):
        profile = (radius - 6)**power
        derivative = np.full_like(radius, Decimal(0)) if power == 0 else power * (radius - 6)**(power - 1)
        derivative2 = np.full_like(radius, Decimal(2) if power == 2 else Decimal(0))
        weak.append(weight * (load_mixed * profile + first * derivative + second * derivative2))
    return dict(radius=radius, jacobian=jacobian, regular=regular, weak=np.array(weak, object),
        endpoint_atom=6 * second / jacobian**2, speed=speed, movement=movement)


def pushforward_moments(engine, mode_rate, expansion, native, order):
    maps = map_coefficients(engine, mode_rate, native)
    coefficients = None if not native else [decimal_coefficients(value) for value in expansion['coefficients']]
    regular, weak = [np.full(3, Decimal(0), object) for unused in range(2)]
    for label, quadrature in decimal_rule(order):
        row = pushforward_parts(engine, maps, coefficients, label, native)
        for power in range(3):
            regular[power] += quadrature * sum(row['regular'] * row['jacobian'] * (row['radius'] - 6)**power, Decimal(0))
            weak[power] += quadrature * sum(row['weak'][power], Decimal(0))
    atoms = np.full(3, Decimal(0), object)
    endpoints = []
    for label in [Decimal('-.5'), Decimal('.5')]:
        row = pushforward_parts(engine, maps, coefficients, label, native)
        for power in range(3):
            atoms[power] += sum(row['endpoint_atom'] * (row['radius'] - 6)**power, Decimal(0))
        for index in range(len(row['radius'])):
            endpoints.append(dict(label=float(label), node=index, radius=float(row['radius'][index]),
                atom=float(row['endpoint_atom'][index]), speed=float(row['speed'][index]),
                movement=float(row['movement'][index])))
    return dict(regular=np.asarray(regular, float), atoms=np.asarray(atoms, float), weak=np.asarray(weak, float),
        total=np.asarray(regular + atoms, float), error=float(maximum(regular + atoms - weak)),
        endpoints=endpoints)
