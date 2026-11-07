import ast
import importlib.util
from common import PARENT, SECOND, BACKGROUND, require
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.linalg import expm_frechet

JPAIR = np.array([[0., 1.], [-1., 0.]])
JFULL = np.kron(np.eye(4), JPAIR)


def sup(values):
    return float(np.max(abs(values)))


def norm(values):
    return max(sup(values), 1e-80)


def multiply(matrix, vector):
    return np.einsum("...ij,...j->...i", matrix, vector)


def transpose(matrix):
    return np.swapaxes(matrix, -1, -2)


def load(path):
    with np.load(path) as archive:
        return {name: archive[name].copy() for name in archive.files}


def joint_extractor():
    path = PARENT / "derive_and_test.py"
    module_tree = ast.parse(path.read_text())
    module_tree.body = [node for node in module_tree.body if not (isinstance(node, ast.ImportFrom) and node.module == "symbolic")]
    namespace = dict(__file__=str(path), __name__="retained_joint_math")
    exec(compile(module_tree, str(path), "exec"), namespace)
    function = next(node for node in ast.parse(path.read_text()).body if isinstance(node, ast.FunctionDef) and node.name == "inspect")
    require(isinstance(function.body[-1], ast.Return), "terminal-only extraction")
    names = ["state", "actual", "generated", "predicted", "linear", "hessian", "averaged", "checks", "diagnostics"]
    function.name = "extract_joint"
    function.body[-1] = ast.Return(value=ast.Dict(keys=[ast.Constant(name) for name in names], values=[ast.Name(id=name, ctx=ast.Load()) for name in names]))
    tree = ast.fix_missing_locations(ast.Module(body=[function], type_ignores=[]))
    exec(compile(tree, str(path), "exec"), namespace)
    return namespace["extract_joint"], namespace["matrices"]


class Background:
    def __init__(self, model):
        self.packet = load(BACKGROUND / "runs" / model / "dop-half-cap.npz")
        self.efold = self.packet["efold"]
        self.mass = self.packet["masses"]
        self.other = CubicSpline(self.efold, self.packet["other_density"])
        keep = np.unique(np.r_[np.arange(0, len(self.efold), 2), len(self.efold) - 1])
        self.other_coarse = CubicSpline(self.efold[keep], self.packet["other_density"][keep])
        self.carrier = CubicSpline(self.efold, self.packet["a"] * self.mass[1] / self.packet["H"])
        self.phase = self.carrier.antiderivative()
        self.origin = float(self.phase(self.efold[0]))
        path = SECOND / "common.py"
        function = next(node for node in ast.parse(path.read_text()).body if isinstance(node, ast.FunctionDef) and node.name == "dense_values")
        namespace = dict(np=np, require=require)
        exec(compile(ast.Module(body=[function], type_ignores=[]), str(path), "exec"), namespace)
        self.dense = namespace["dense_values"]

    def evaluate(self, efolds, coarse=False):
        values, rates = self.dense(self.packet, np.atleast_1d(efolds))
        physical, derivative = values * self.packet["units"], rates * self.packet["units"]
        fields = self.packet["initial_fields"] + physical[:, [0, 2]]
        velocities = physical[:, [1, 3]]
        field_rates, velocity_rates = derivative[:, [0, 2]], derivative[:, [1, 3]]
        scale = np.exp(np.atleast_1d(efolds))
        omega = scale[:, None] * self.mass
        density = (velocities**2 + omega**2 * fields**2) / 2
        density_rate = velocities * velocity_rates + omega**2 * (fields**2 + fields * field_rates)
        external = self.other_coarse if coarse else self.other
        hubble = np.sqrt((external(efolds) + density.sum(axis=1)) / 3)
        hlog = (external(efolds, 1) + density_rate.sum(axis=1)) / (6 * hubble**2)
        phase, mu = self.phase(efolds) - self.origin, self.carrier(efolds)
        rotation = np.exp(1j * phase)
        amplitude = scale * (np.sqrt(omega[:, 1]) * fields[:, 1] + 1j * velocities[:, 1] / np.sqrt(omega[:, 1])) * rotation
        amplitude_rate = rotation * (scale * np.sqrt(omega[:, 1]) * (1.5 * fields[:, 1] + field_rates[:, 1])
                         + 1j * scale / np.sqrt(omega[:, 1]) * (.5 * velocities[:, 1] + velocity_rates[:, 1])) + 1j * mu * amplitude
        return dict(scale=scale, hubble=hubble, hlog=hlog, omega_s=omega[:, 0], velocity_s=velocities[:, 0],
                    velocity_s_rate=velocity_rates[:, 0], omega_h=omega[:, 1], background=amplitude,
                    background_rate=amplitude_rate, phase=phase, mu=mu, mu_rate=self.carrier(efolds, 1))


def outer(left, right):
    return left[:, :, None] * right[:, None, :]


def coefficients(background, wave):
    scale, hubble, hlog = background["scale"], background["hubble"], background["hlog"]
    omega_s, omega_h, mu = background["omega_s"], background["omega_h"], background["mu"]
    amplitude, amplitude_rate = background["background"], background["background_rate"]
    count = len(scale)
    values, rates = np.zeros((count, 5, 8, 8)), np.zeros((count, 5, 8, 8))
    gamma = wave**2 / (2 * omega_h * hubble)
    gamma_rate = -(1 + hlog) * gamma
    values[:, 0, 0, 0] = scale**2 * (wave**2 + omega_s**2) / hubble
    rates[:, 0, 0, 0] = (2 - hlog) * values[:, 0, 0, 0] + 2 * scale**2 * omega_s**2 / hubble
    for first, second, factor in ((1, 1, 1.), (5, 5, -6.), (5, 7, 1.), (7, 5, 1.)):
        values[:, 0, first, second] = factor / (scale**2 * hubble)
        rates[:, 0, first, second] = -(2 + hlog) * values[:, 0, first, second]
    values[:, 0, 6, 6] = -2 * scale**2 * wave**2 / hubble
    rates[:, 0, 6, 6] = (2 - hlog) * values[:, 0, 6, 6]
    frequency = omega_h / hubble - mu + gamma
    frequency_rate = (1 - hlog) * omega_h / hubble - background["mu_rate"] + gamma_rate
    values[:, 0, 2, 2] = values[:, 0, 3, 3] = frequency
    rates[:, 0, 2, 2] = rates[:, 0, 3, 3] = frequency_rate
    values[:, 1, 2, 2], values[:, 1, 3, 3] = gamma, -gamma
    rates[:, 1, 2, 2], rates[:, 1, 3, 3] = gamma_rate, -gamma_rate
    values[:, 1, 2, 3] = values[:, 1, 3, 2] = 1.5
    values[:, 2, 2, 2], values[:, 2, 3, 3] = -1.5, 1.5
    values[:, 2, 2, 3] = values[:, 2, 3, 2] = gamma
    rates[:, 2, 2, 3] = rates[:, 2, 3, 2] = gamma_rate

    vectors, derivatives = np.zeros((3, count, 8)), np.zeros((3, count, 8))
    vectors[0, :, 0], derivatives[0, :, 0] = background["velocity_s"], background["velocity_s_rate"]
    normal_amplitude = amplitude / (2 * scale**2)
    normal_rate = (amplitude_rate - 2 * amplitude) / (2 * scale**2)
    for container, amplitude_value in ((vectors, normal_amplitude), (derivatives, normal_rate)):
        container[0, :, 2], container[0, :, 3] = amplitude_value.imag, -amplitude_value.real
        container[1, :, 2], container[1, :, 3] = amplitude_value.imag, amplitude_value.real
        container[2, :, 2], container[2, :, 3] = -amplitude_value.real, amplitude_value.imag
    geometry = np.zeros((count, 8))
    geometry[:, 5], geometry[:, 7] = -6., 1.
    factor = -3 * scale**2 / (2 * hubble)
    factor_rate = (2 - hlog) * factor
    for harmonic in range(3):
        cross = (outer(geometry, vectors[harmonic]) + outer(vectors[harmonic], geometry)) / (2 * hubble[:, None, None])
        cross_rate = (outer(geometry, derivatives[harmonic]) + outer(derivatives[harmonic], geometry)) / (2 * hubble[:, None, None]) - hlog[:, None, None] * cross
        values[:, harmonic] += cross
        rates[:, harmonic] += cross_rate
    products = []
    product_rates = []
    for left, right in ((0, 0), (1, 1), (2, 2), (0, 1), (1, 0), (0, 2), (2, 0), (1, 2), (2, 1)):
        products.append(outer(vectors[left], vectors[right]))
        product_rates.append(outer(derivatives[left], vectors[right]) + outer(vectors[left], derivatives[right]))
    def combinations(items):
        return [items[0] + (items[1] + items[2]) / 2, items[3] + items[4],
                items[5] + items[6], (items[1] - items[2]) / 2, (items[7] + items[8]) / 2]
    for harmonic, (product, derivative) in enumerate(zip(combinations(products), combinations(product_rates))):
        values[:, harmonic] += factor[:, None, None] * product
        rates[:, harmonic] += factor_rate[:, None, None] * product + factor[:, None, None] * derivative
    return values, rates


def generator(background, wave):
    values, rates = coefficients(background, wave)
    phase, mu = background["phase"], background["mu"]
    hessian, generating, fast, slow = values[:, 0].copy(), np.zeros_like(values[:, 0]), np.zeros_like(values[:, 0]), np.zeros_like(values[:, 0])
    for harmonic, cosine, sine in ((2, 1, 2), (4, 3, 4)):
        cos, sin = np.cos(harmonic * phase)[:, None, None], np.sin(harmonic * phase)[:, None, None]
        oscillating = cos * values[:, cosine] + sin * values[:, sine]
        hessian += oscillating
        fast += oscillating
        generating += (sin * values[:, cosine] - cos * values[:, sine]) / (harmonic * mu[:, None, None])
        slow += (sin * (rates[:, cosine] - (background["mu_rate"] / mu)[:, None, None] * values[:, cosine])
                - cos * (rates[:, sine] - (background["mu_rate"] / mu)[:, None, None] * values[:, sine])) / (harmonic * mu[:, None, None])
    return hessian, generating, fast + slow, fast


def transform(background, wave, include_fast=True):
    hessian, generating, derivative, fast = generator(background, wave)
    scale = background["scale"]
    slow_scale = scale * (wave**2 + background["omega_s"]**2)**.25
    metric_scale = scale * np.sqrt(wave)
    balancing = np.column_stack([1 / slow_scale, slow_scale, np.ones(len(scale)), np.ones(len(scale)),
                                1 / metric_scale, metric_scale, 1 / metric_scale, metric_scale])
    matrices = np.empty_like(hessian)
    rates = np.empty_like(hessian)
    fast_rates = np.empty_like(hessian) if include_fast else None
    for index, units in enumerate(balancing):
        generator_scaled = (JFULL @ generating[index]) * units[None, :] / units[:, None]
        derivative_scaled = (JFULL @ derivative[index]) * units[None, :] / units[:, None]
        matrices[index], rates[index] = expm_frechet(generator_scaled, derivative_scaled)
        if include_fast:
            fast_scaled = (JFULL @ fast[index]) * units[None, :] / units[:, None]
            fast_rates[index] = expm_frechet(generator_scaled, fast_scaled, compute_expm=False)
    return dict(hessian=hessian, balance=balancing, transform=matrices, rate=rates, fast_rate=fast_rates)


def physical_matrix(matrix, units):
    return matrix * units[:, :, None] / units[:, None, :]

