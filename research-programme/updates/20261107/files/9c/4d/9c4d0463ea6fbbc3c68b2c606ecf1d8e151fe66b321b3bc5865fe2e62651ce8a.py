from common import *
from native_context import factory
from rest_operator_v2 import NativeRest, JFULL
from coefficients import metric_polynomial
from mean_math import Background, phase_background, polynomials, action_orders, product, evaluate
import numpy as np
from scipy.interpolate import CubicSpline


def initialize(folder):
    (ROOT / folder).mkdir(exist_ok=False)
    wave = dict(read(WAVELENGTH / "inventory-config.json")["waves"])[LABEL]
    context = factory(folder)("heavy", LABEL, wave)
    system = NativeRest(context, "heavy", wave)
    first = float(system.background["efold"][0])
    canonical_units = np.zeros(8)
    for index in range(system.dimension):
        basis = np.zeros(system.dimension)
        basis[index] = context["normalization"][index]
        canonical_units += abs(system.encode(first, basis)[0])
    canonical_units[canonical_units == 0] = 1.
    units = np.r_[canonical_units, system.rest_units]
    signature = system.signature
    native_support = [3, int(signature[3]), int(signature[3]) + 2,
                      int(signature[4]), int(signature[4]) + 2]
    for node in range(5):
        start = int(signature[50]) + node * (int(signature[40]) + 1)
        native_support.extend([start, start + 2])
    support = np.array([int(np.flatnonzero(system.rest_positions == system.position(native))[0]) for native in native_support])
    require(len(np.unique(support)) == 15, "physical source support")
    vectors = np.zeros((system.rest_size, 2))
    vectors[:system.native_rest_size] = np.column_stack([system.expansion[system.rest_positions], system.shear[system.rest_positions]])
    return context, system, units, support, vectors, wave


def source_rows(system, support, efold):
    result = np.zeros((2, len(support)))
    point = system.context["point"](efold)
    scale_value, stamp, hubble = point[10:13]
    for column, index in enumerate(support):
        physical = np.zeros(system.dimension)
        physical[system.rest_positions[index]] = 1.
        terms, metadata = system.context["stress"](stamp, physical)
        pressure, anisotropy = terms[:5, 2].sum(), terms[:5, 6].sum()
        result[0, column] = -scale_value**2 / hubble * (pressure / 2 - anisotropy / 3)
        result[1, column] = 2 * scale_value**2 * anisotropy / hubble
    return result


def factors(provider, system, support, points, wave):
    original, mean, cosine, sine = phase_background(provider, points)
    hessian, exponent, exponent_rate, balance = polynomials(mean, cosine, sine, wave)
    order = action_orders(hessian, exponent, exponent_rate)[2]
    feedback = product(metric_polynomial(mean, wave, balance), order["coordinate_map"])
    pieces = {}
    for name, polynomial, with_j in (("core", order["hessian"], True), ("source", order["source_map"], True), ("feedback", feedback, False)):
        oscillating = {key: JFULL @ value if with_j else value for key, value in polynomial.items() if key}
        primitive = {key: value / (1j * key * mean["mu"][:, None, None]) for key, value in oscillating.items()}
        for prefix, selected in (("U", primitive), ("V", oscillating)):
            result = evaluate(selected, original["phase"])
            require(np.max(abs(result.imag)) < 1e-10 * max(np.max(abs(result.real)), 1e-80), "real phase factors")
            pieces[prefix + "_" + name] = result.real
    linear = np.array([source_rows(system, support, float(efold)) for efold in points])
    result = {}
    for prefix in ("U", "V"):
        result[prefix + "_A"] = pieces[prefix + "_core"] * balance[:, :, None] / balance[:, None, :]
        source = pieces[prefix + "_source"] * balance[:, :, None] * balance[:, None, :]
        result[prefix + "_B"] = source[:, :, [4, 6]] @ linear
        result[prefix + "_C"] = pieces[prefix + "_feedback"] / balance[:, None, :] / original["hubble"][:, None, None]
    result["linear"] = linear
    result["hessian"] = order["hessian"][0].real / (balance[:, :, None] * balance[:, None, :])
    result["source"] = order["source_map"][0].real * balance[:, None, :] / balance[:, :, None]
    result["feedback"] = feedback[0].real / balance[:, None, :]
    return result


def apply(blocks, vector, support, vectors):
    state, rest = vector[:8], vector[8:]
    return np.r_[blocks[0] @ state + blocks[1] @ rest[support], vectors @ (blocks[2] @ state)]


def inverse(blocks, vector, support, vectors):
    core, source, feedback = blocks
    schur = np.eye(8) + core - source @ vectors[support] @ feedback
    state = np.linalg.solve(schur, vector[:8] - source @ vector[8:][support])
    return np.r_[state, vector[8:] - vectors @ (feedback @ state)]


def infinity_norm(blocks, units, support, vectors):
    core, source, feedback = blocks
    upper = abs(core * units[None, :8] / units[:8, None]).sum(axis=1)
    upper += abs(source * units[None, 8 + support] / units[:8, None]).sum(axis=1)
    lower = abs((vectors @ feedback) * units[None, :8] / units[8:, None]).sum(axis=1)
    return float(max(np.max(upper), np.max(lower)))


def balanced_block(value, name, units, support, vectors):
    if name.endswith("_A"):
        return value * units[None, None, :8] / units[None, :8, None]
    if name.endswith("_B"):
        return value * units[None, None, 8 + support] / units[None, :8, None]
    return (vectors[None] @ value) * units[None, None, :8] / units[None, 8:, None]


class Corrector:
    def __init__(self, packet):
        self.support, self.vectors, self.units = packet["support"], packet["vectors"], packet["units"]
        self.splines = {name: CubicSpline(packet["efold"], packet[name], axis=0)
                        for prefix in ("U", "V") for name in (prefix + "_A", prefix + "_B", prefix + "_C")}

    def blocks(self, efold, prefix="U", derivative=0):
        return tuple(self.splines[prefix + "_" + suffix](efold, derivative) for suffix in ("A", "B", "C"))

    def apply(self, efold, vector, prefix="U", derivative=0):
        return apply(self.blocks(efold, prefix, derivative), vector, self.support, self.vectors)

    def inverse(self, efold, vector):
        return inverse(self.blocks(efold), vector, self.support, self.vectors)

