from common import *
from poisson_driver import open_system
from scipy.interpolate import make_interp_spline
import numpy as np

BRANCHES = ("poisson-spatial", "newton-dust-force")


def sup(value):
    return float(np.max(abs(np.asarray(value))))


def relative(value, scale):
    return sup(value) / max(sup(scale), 1e-80)


def open_owned(model, folder):
    system = open_system(model, folder)
    path = POISSON / "preflight-v2/backgrounds" / (model + ".npz")
    require(digest(path) == read(POISSON / "preflight-v2" / (model + "-preflight.json"))["units_sha256"], "background packet")
    system.install_background(load(path))
    return system


def extract(system, efold):
    size = len(system.core)
    units = system.units[:size]
    point = system.context["point"](efold)
    scale, hubble = point[10], point[12]
    expansion = system.metric_kernels(efold)[0]
    injection = np.zeros((size, 2))
    injection[system.alpha_slot, 0] = 1 / (hubble * units[system.alpha_slot])
    injection[:, 1] = expansion[system.core] / (hubble * units)
    injection[system.alpha_slot, 1] = 0.
    if system.model == "heavy":
        phase = system.owner.phase(efold)[0]
        omega = scale * system.background["masses"][1]
        carrier = -1j * scale * system.wave * point[3] * np.exp(1j * phase) / (hubble * np.sqrt(omega))
        injection[system.slots, 1] = np.array([carrier.real, carrier.imag]) / units[system.slots]
    base = np.empty((size, size))
    channels = np.empty((2, 2, size))
    rows = np.empty((2, size))
    gravity_rate = hubble * system.background_spline(efold, 1)[1]
    for column in range(size):
        state = np.zeros(len(system.units))
        state[column] = units[column]
        derivative, values, rates, info, _, _ = system.evaluate(efold, state, "gr")
        base[:, column] = derivative[:size] / units
        rows[:, column] = [values["D"], values["delta_c"]]
        psi_new = -values["D"] / (2 * system.wave**2)
        alpha_rate = psi_new - hubble * info["alpha"]
        density_base = rates["density_sync"] + system.wave * info["quadrature_enthalpy"] * info["z"]
        gravity = 3 * hubble * info["enthalpy"] / (2 * system.wave**2)
        for branch, factor in enumerate((1., 0.)):
            phi_base = factor * (-density_base / (2 * system.wave**2) + gravity_rate * info["alpha"] + gravity * alpha_rate)
            denominator = 1 + 3 * factor * info["quadrature_enthalpy"] / (2 * system.wave**2)
            expansion_new = (system.wave * info["alpha"] - 3 * (phi_base + info["H_rate"] * info["alpha"] + hubble * alpha_rate) / system.wave) / denominator
            channels[branch, :, column] = [psi_new - values["Psi"], expansion_new - info["z"]]
    speeds = system.context["kinetic"](point[11])[1] / hubble
    return base, injection, channels, rows, speeds


class AdjointOperator:
    def __init__(self, packet):
        self.packet = packet
        self.size = int(packet["core_size"])
        self.dimension = len(packet["units"])
        self.units = packet["units"]
        self.wave = float(packet["wave"])
        self.quadrupoles = packet["quadrupoles"]
        self.degree = np.arange(3, 193)
        self.lower = self.wave * self.degree / (2 * self.degree + 1)
        self.upper = -self.wave * (self.degree + 1) / (2 * self.degree + 1)
        self.upper[-1] = 0.
        self.splines = {name: make_interp_spline(packet["efold"], packet[name], k=5, axis=0)
                        for name in ("base", "injection", "channels", "rows", "speeds")}

    def blocks(self, efold, branch):
        injection = self.splines["injection"](efold)
        channel = self.splines["channels"](efold)[branch]
        core = self.splines["base"](efold) + injection @ channel
        speed = self.splines["speeds"](efold)
        tail_units = self.units[self.size:self.size + 5]
        low_units = self.units[self.quadrupoles]
        tail_to_core = -3 * self.wave * speed * tail_units / (5 * low_units)
        core_to_tail = 3 * self.wave * speed * low_units / (7 * tail_units)
        return core, tail_to_core, core_to_tail, speed, injection, channel

    def apply(self, efold, vector, branch, transpose=False):
        core, tail_to_core, core_to_tail, speed, _, _ = self.blocks(efold, branch)
        values = vector.reshape(self.dimension, -1)
        core_values = values[:self.size]
        tail_values = values[self.size:].reshape(190, 5, -1)
        result_core = (core.T if transpose else core) @ core_values
        result_tail = np.zeros_like(tail_values)
        lower = self.lower[:, None, None] * speed[None, :, None]
        upper = self.upper[:, None, None] * speed[None, :, None]
        if transpose:
            result_core[self.quadrupoles] += core_to_tail[:, None] * tail_values[0]
            result_tail[0] += tail_to_core[:, None] * core_values[self.quadrupoles]
            result_tail[:-1] += lower[1:] * tail_values[1:]
            result_tail[1:] += upper[:-1] * tail_values[:-1]
        else:
            result_core[self.quadrupoles] += tail_to_core[:, None] * tail_values[0]
            result_tail[0] += core_to_tail[:, None] * core_values[self.quadrupoles]
            result_tail[1:] += lower[1:] * tail_values[:-1]
            result_tail[:-1] += upper[:-1] * tail_values[1:]
        result = np.concatenate([result_core, result_tail.reshape(-1, values.shape[1])])
        return result.reshape(vector.shape)
