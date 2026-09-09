import math

import numpy as numerical
from numpy.polynomial import chebyshev

from annular_continuum_initial_data_20260909 import lift, profiles
from annular_fifth_order_jet_20260909 import Jet, KEYS as OLD_KEYS, INDEX as OLD_INDEX, MAX_ORDER
from sbp4_derived_operator_20260909 import derivative


KEYS = [(direction, time, radius) for direction in range(3) for time in range(4) for radius in range(4 - time)]
INDEX = {key: position for position, key in enumerate(KEYS)}
PRODUCTS = [(left, right, INDEX[target]) for left, first in enumerate(KEYS) for right, second in enumerate(KEYS) if (target := tuple(first[index] + second[index] for index in range(3))) in INDEX]


class TransferJet:
    __array_priority__ = 1000

    def __init__(self, data):
        self.data = numerical.asarray(data)

    @classmethod
    def constant(cls, values, count):
        data = numerical.zeros((len(KEYS), count), dtype=numerical.result_type(values, float))
        data[0] = values
        return cls(data)

    def coerce(self, other):
        return other if isinstance(other, TransferJet) else self.constant(other, self.data.shape[-1])

    def __add__(self, other):
        return TransferJet(self.data + self.coerce(other).data)

    __radd__ = __add__

    def __neg__(self):
        return TransferJet(-self.data)

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        if not isinstance(other, TransferJet):
            return TransferJet(self.data * other)
        data = numerical.zeros_like(self.data, dtype=numerical.result_type(self.data, other.data))
        for left, right, target in PRODUCTS:
            data[target] += self.data[left] * other.data[right]
        return TransferJet(data)

    __rmul__ = __mul__

    def __truediv__(self, other):
        return self * other**-1 if isinstance(other, TransferJet) else TransferJet(self.data / other)

    def __rtruediv__(self, other):
        return self**-1 * other

    def __pow__(self, exponent):
        if isinstance(exponent, int) and exponent >= 0:
            result = self.coerce(1)
            for degree in range(exponent):
                result = result * self
            return result
        if numerical.any(self.data[0] == 0):
            raise ZeroDivisionError("Zero Taylor denominator")
        relative = self.data / self.data[0]
        relative[0] = 0
        relative = TransferJet(relative)
        power = self.coerce(1)
        result = power
        coefficient = 1.0
        for degree in range(1, 6):
            power = power * relative
            coefficient *= (exponent - degree + 1) / degree
            result = result + coefficient * power
        return result * self.data[0]**exponent

    def exp(self):
        remainder = self.data.copy()
        remainder[0] = 0
        remainder = TransferJet(remainder)
        power = self.coerce(1)
        result = power
        for degree in range(1, 6):
            power = power * remainder
            result = result + power / math.factorial(degree)
        return result * numerical.exp(self.data[0])

    def derivative(self, axis):
        result = numerical.zeros_like(self.data)
        for position, key in enumerate(KEYS):
            if key[axis]:
                target = list(key)
                target[axis] -= 1
                result[INDEX[tuple(target)]] = key[axis] * self.data[position]
        return TransferJet(result)

    def extract(self, degree=0):
        return self.data[INDEX[degree, 0, 0]]


def background_fields(evaluator, time, radii, epsilon=0.1):
    Jet.numpy, Jet.count = numerical, radii.size
    advanced = time + evaluator.sigma * (radii - 4)
    time_jet, radius_jet = Jet.variable(advanced, 1), Jet.variable(radii, 2)
    coefficients = [entry if isinstance(entry, Jet) else Jet.constant(entry) for entry in evaluator.evaluator(time_jet, radius_jet)]
    harmonics = {}
    for kind, mode in set((entry[2], entry[3]) for entry in evaluator.metadata):
        data = numerical.zeros((len(OLD_KEYS), radii.size))
        active = []
        for degree in range(MAX_ORDER + 1):
            position = OLD_INDEX[0, degree, 0]
            angle = mode * advanced / epsilon + degree * numerical.pi / 2
            data[position] = (numerical.cos(angle) if kind == "cos" else numerical.sin(angle)) * (mode / epsilon)**degree / math.factorial(degree)
            active.append(position)
        harmonics[kind, mode] = Jet(data, active)
    fields = {field: Jet.constant(0) for field in evaluator.case["fields"]}
    for (field, order, kind, mode), value in zip(evaluator.metadata, coefficients):
        fields[field] = fields[field] + epsilon**order * value * harmonics[kind, mode]
    result = {}
    for name in ["scalar_ref", "mass_ref", "shift_ref"]:
        data = numerical.zeros((len(KEYS), radii.size))
        for position, key in enumerate(KEYS):
            if key[0] == 0:
                data[position] = fields[name].data[OLD_INDEX[key]]
        result[name] = TransferJet(data)
    return result


def initial_third(payload, radii):
    amplitudes = numerical.array(payload["amplitudes"])
    result = numerical.zeros((2, 4, radii.size))
    shapes = profiles(radii, 3)
    result[:, 0] = amplitudes[:, :2] @ shapes[:2]
    result[:, 3] = amplitudes[:, 2, None] * shapes[2]
    for panel in payload["panels"]:
        mask = (radii >= panel["left"]) & (radii <= panel["right"])
        coefficients = chebyshev.chebder(numerical.array(panel["mass_coefficients"]).T, m=3, axis=0) * 8
        result[:, 2, mask] = chebyshev.chebval(2 * (radii[mask] - panel["left"]) - 1, coefficients)
    return result


def spatial_derivatives(values, spacing, maximum, method):
    result = [values]
    if method == "sbp":
        for order in range(1, maximum + 1):
            result.append(derivative(result[-1], spacing))
        return result
    width = int(method.removeprefix("poly"))
    count = values.shape[-1]
    indices = numerical.clip(numerical.arange(count) - width // 2, 0, count - width)[:, None] + numerical.arange(width)
    nodes = indices - numerical.arange(count)[:, None]
    weights = {}
    for location in numerical.unique(nodes[:, 0]):
        offsets = numerical.arange(width) + location
        matrix = offsets[None, :].astype(float)**numerical.arange(width)[:, None]
        directions = numerical.zeros((width, maximum))
        for order in range(1, maximum + 1):
            directions[order, order - 1] = math.factorial(order)
        weights[int(location)] = numerical.linalg.solve(matrix, directions)
    for order in range(1, maximum + 1):
        stencil = numerical.stack([weights[int(node)][..., order - 1] for node in nodes[:, 0]])
        result.append(numerical.einsum("...nw,nw->...n", values[..., indices] - values[..., :, None], stencil) / spacing**order)
    return result


def error_fields(time_jets, payload, radii, sigma, method):
    spacing = float(radii[1] - radii[0])
    initial = list(lift(payload, radii)) + [initial_third(payload, radii)]
    mixed = {}
    for time_order in range(4):
        values = time_jets[time_order, 0].copy()
        if time_order == 0:
            values -= initial[0][0]
        for radius_order, derivative_value in enumerate(spatial_derivatives(values, spacing, 3 - time_order, method)):
            mixed[time_order, radius_order] = derivative_value + (initial[radius_order][0] if time_order == 0 else 0)
    result = {}
    for name, component in [("scalar_ref", 0), ("mass_ref", 2), ("shift_ref", 3)]:
        data = numerical.zeros((len(KEYS), radii.size))
        for position, (direction, time_order, radius_order) in enumerate(KEYS):
            if direction == 0:
                data[position] = sum(math.comb(radius_order, index) * (-sigma)**index * mixed[time_order + index, radius_order - index][component] for index in range(radius_order + 1)) / (math.factorial(time_order) * math.factorial(radius_order))
        result[name] = TransferJet(data)
    return result, mixed


def along_segment(background, error, position):
    result = {}
    for name, base in background.items():
        data = base.data + position * error[name].data
        data = data.copy()
        for index, key in enumerate(KEYS):
            if key[0] == 0:
                data[INDEX[1, key[1], key[2]]] = error[name].data[index]
        result[name] = TransferJet(data)
    return result


def radius_field(radii):
    result = TransferJet.constant(radii, radii.size)
    result.data[INDEX[0, 0, 1]] = 1
    return result


def geometry(fields, radius, constants, kappa):
    scalar, mass, shift = [fields[name] for name in ["scalar_ref", "mass_ref", "shift_ref"]]
    exponential, inverse = shift.exp(), (-shift).exp()
    lapse = 1 - 2 * mass / radius - constants["Lambda"] * radius**2 / 3
    radial = lapse.derivative(2)
    shift_radial = shift.derivative(2)
    scalar_radial, scalar_time = scalar.derivative(2), scalar.derivative(1)
    kinetic = 2 * inverse * scalar_time * scalar_radial + lapse * scalar_radial**2
    principal = 1 - 4 * constants["b2"] * kinetic - 6 * constants["b3"] * kinetic**2
    potential = constants["m_chi"]**2 * scalar**2 / 2
    curvature = -radial.derivative(2) - 3 * radial * shift_radial - 2 * lapse * (shift_radial.derivative(2) + shift_radial**2) - 2 * inverse * shift_radial.derivative(1) + 2 * (radial + lapse * shift_radial) / radius + 2 * (1 - lapse) / radius**2
    proxy = 12 * mass / radius**3 + 4 * kappa * (kinetic / 2 - 3 * constants["b2"] * kinetic**2 - 5 * constants["b3"] * kinetic**3 - potential)
    mass_source = kappa * radius**2 * (principal * lapse * scalar_radial**2 / 2 + potential + constants["b2"] * kinetic**2 + 2 * constants["b3"] * kinetic**3)
    mass_residual = mass.derivative(2) - mass_source
    lapse_residual = shift_radial - kappa * radius * principal * scalar_radial**2
    time_current = radius**2 * principal * scalar_radial
    radial_current = radius**2 * principal * scalar_time + exponential * radius**2 * principal * lapse * scalar_radial
    scalar_residual = inverse * (time_current.derivative(1) + radial_current.derivative(2)) / radius**2 - constants["m_chi"]**2 * scalar
    terms = [-8 * mass_residual / radius**2, 2 * mass_residual.derivative(2) / radius, -2 * inverse * lapse_residual.derivative(1), -2 * lapse * lapse_residual.derivative(2), (2 * lapse / radius - 3 * radial - 2 * lapse * shift_radial) * lapse_residual, -2 * kappa * radius * scalar_radial * scalar_residual]
    defect = sum(terms)
    boundary = 2 * lapse / radius - radial - 2 * lapse * shift_radial

    def restore(multiplier):
        return kappa * (2 * lapse * multiplier.derivative(2) + 2 * inverse * multiplier.derivative(1) + boundary * multiplier)

    multiplier = -2 * radius**2 * kinetic * curvature / 3
    proxy_multiplier = -2 * radius**2 * kinetic * proxy / 3
    residual_multiplier = -2 * radius**2 * kinetic * defect / 3
    result = {"Z": curvature, "Zalg": proxy, "defect": defect, "Weyl2": curvature**2 / 3, "M1": multiplier, "K1": restore(multiplier), "K1alg": restore(proxy_multiplier), "K1residual": restore(residual_multiplier), "Rm": mass_residual, "Dl": lapse_residual, "Fchi": scalar_residual, "Rm_r": mass_residual.derivative(2), "Dl_v": lapse_residual.derivative(1), "Dl_r": lapse_residual.derivative(2), "X": kinetic, "F": lapse}
    result.update({"defect_term_" + str(index): term for index, term in enumerate(terms)})
    return result


def quadratic_majorants(background, error, radii, constants, kappa):
    fields = {}
    for name, base in background.items():
        data = numerical.abs(base.data) + numerical.abs(error[name].data)
        for index, key in enumerate(KEYS):
            if key[0] == 0:
                data[INDEX[1, key[1], key[2]]] = numerical.abs(error[name].data[index])
        fields[name] = TransferJet(data)
    scalar, mass, shift = [fields[name] for name in ["scalar_ref", "mass_ref", "shift_ref"]]
    radius = radius_field(radii)
    inverse_radius = TransferJet(numerical.abs((radius**-1).data))
    exponent_base = numerical.abs(error["shift_ref"].extract())
    nonconstant = shift.data.copy()
    nonconstant[0] = 0
    exponential_rest = TransferJet(nonconstant).exp()
    inverse = exponential_rest * numerical.exp(-background["shift_ref"].extract() + exponent_base)
    exponential = exponential_rest * numerical.exp(background["shift_ref"].extract() + exponent_base)
    lapse = 1 + 2 * mass * inverse_radius + abs(constants["Lambda"]) * radius**2 / 3
    radial, shift_radial = lapse.derivative(2), shift.derivative(2)
    scalar_radial, scalar_time = scalar.derivative(2), scalar.derivative(1)
    kinetic = 2 * inverse * scalar_time * scalar_radial + lapse * scalar_radial**2
    principal = 1 + 4 * abs(constants["b2"]) * kinetic + 6 * abs(constants["b3"]) * kinetic**2
    potential = constants["m_chi"]**2 * scalar**2 / 2
    curvature = radial.derivative(2) + 3 * radial * shift_radial + 2 * lapse * (shift_radial.derivative(2) + shift_radial**2) + 2 * inverse * shift_radial.derivative(1) + 2 * (radial + lapse * shift_radial) * inverse_radius + 2 * (1 + lapse) * inverse_radius**2
    proxy = 12 * mass * inverse_radius**3 + 4 * abs(kappa) * (kinetic / 2 + 3 * abs(constants["b2"]) * kinetic**2 + 5 * abs(constants["b3"]) * kinetic**3 + potential)
    mass_source = abs(kappa) * radius**2 * (principal * lapse * scalar_radial**2 / 2 + potential + abs(constants["b2"]) * kinetic**2 + 2 * abs(constants["b3"]) * kinetic**3)
    mass_residual = mass.derivative(2) + mass_source
    lapse_residual = shift_radial + abs(kappa) * radius * principal * scalar_radial**2
    time_current = radius**2 * principal * scalar_radial
    radial_current = radius**2 * principal * scalar_time + exponential * radius**2 * principal * lapse * scalar_radial
    scalar_residual = inverse * (time_current.derivative(1) + radial_current.derivative(2)) * inverse_radius**2 + constants["m_chi"]**2 * scalar
    boundary = 2 * lapse * inverse_radius + radial + 2 * lapse * shift_radial
    multiplier = 2 * radius**2 * kinetic * curvature / 3
    restoration = abs(kappa) * (2 * lapse * multiplier.derivative(2) + 2 * inverse * multiplier.derivative(1) + boundary * multiplier)
    return {"Z": curvature.extract(2), "Zalg": proxy.extract(2), "Weyl2": (curvature**2 / 3).extract(2), "M1": multiplier.extract(2), "K1": restoration.extract(2), "Rm": mass_residual.extract(2), "Dl": lapse_residual.extract(2), "Fchi": scalar_residual.extract(2)}
