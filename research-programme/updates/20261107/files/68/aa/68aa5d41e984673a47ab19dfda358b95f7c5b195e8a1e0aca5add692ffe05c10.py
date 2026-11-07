from common import *
from native_context import factory
from rest_operator_v2 import NativeRest
import numpy as np
from scipy.interpolate import make_interp_spline


class PoissonDriver:
    def __init__(self, context, model, wave):
        self.context, self.model, self.wave = context, model, wave
        self.owner = NativeRest(context, model, wave)
        self.background = self.owner.background
        self.units, self.initial_raw, self.project, self.native_extended_rhs = context["extension"](192, True)
        self.raw_units = self.units.copy()
        self.core = context["core"]
        self.alpha_slot = int(np.flatnonzero(self.core == context["position"](1))[0])
        self.cdm_slot = int(np.flatnonzero(self.core == context["position"](2))[0])
        self.slots = context["envelope_slots"]
        self.zero_native = np.zeros(context["dimension"])
        first = float(self.background["efold"][0])
        point = context["point"](first)
        if model == "heavy":
            omega = point[10] * self.background["masses"][1]
            normal = point[10] * (np.sqrt(omega) * self.units[self.slots[0]] + self.units[self.slots[1]] / np.sqrt(omega))
            self.units[self.slots] = normal
        alpha_unit = 0.
        for index in range(context["dimension"]):
            basis = np.zeros(context["dimension"])
            basis[index] = context["normalization"][index]
            alpha_unit += abs(context["observe"](point[11], basis)[5] / wave)
        self.units[self.alpha_slot] = max(alpha_unit, 1e-80)
        self.initial = self.encode(first, self.initial_raw)

    def encode(self, efold, raw):
        state = raw.copy()
        physical = self.project(raw)
        point = self.context["point"](efold)
        state[self.alpha_slot] = self.context["observe"](point[11], physical)[5] / self.wave
        if self.model == "heavy":
            phase, _ = self.owner.phase(efold)
            omega = point[10] * self.background["masses"][1]
            amplitude = point[10] * (np.sqrt(omega) * raw[self.slots[0]] + 1j * raw[self.slots[1]] / np.sqrt(omega)) * np.exp(1j * phase)
            state[self.slots] = [amplitude.real, amplitude.imag]
        return state

    def decode(self, efold, state):
        raw = state.copy()
        raw[self.alpha_slot] = 0.
        if self.model == "heavy":
            point = self.context["point"](efold)
            phase, _ = self.owner.phase(efold)
            omega = point[10] * self.background["masses"][1]
            amplitude = complex(*state[self.slots]) * np.exp(-1j * phase)
            raw[self.slots[0]] = amplitude.real / (point[10] * np.sqrt(omega))
            raw[self.slots[1]] = amplitude.imag * np.sqrt(omega) / point[10]
        return raw

    def background_values(self, efold):
        point = self.context["point"](efold)
        observed = self.context["observe"](point[11], self.zero_native)
        enthalpy = observed[0] + observed[1]
        return np.array([point[12], 3 * point[12] * enthalpy / (2 * self.wave**2)])

    def install_background(self, packet):
        self.background_spline = make_interp_spline(packet["efold"], packet["values"], k=5, axis=0)

    def metric_kernels(self, efold):
        point = self.context["point"](efold)
        expansion = self.owner.expansion.copy()
        expansion[self.context["position"](2)] = -self.wave
        expansion[self.owner.scalar_positions[1]] = -self.wave * point[1]
        if self.model == "heavy":
            expansion[self.owner.scalar_positions[3]] = -self.wave * point[3]
        return expansion, self.owner.shear

    def evaluate(self, efold, state, branch):
        raw = self.decode(efold, state)
        physical = self.project(raw)
        original_rate, point = self.native_extended_rhs(efold, raw)
        scale_value, stamp, hubble = point[10:13]
        observed = self.context["observe"](stamp, physical)
        terms, metadata = self.context["stress"](stamp, physical)
        density, current, anisotropy = observed[2:5]
        native_shear = observed[5]
        native_z = native_shear - 1.5 * current / self.wave**2
        enthalpy = observed[0] + observed[1]
        quadrature_enthalpy = terms[:, 5].sum() - terms[4, 5] + metadata[3]
        density_rate_base = terms[:, 3].sum() + self.wave * quadrature_enthalpy * native_z
        current_rate = terms[:, 4].sum()
        hubble_rate, gravity_rate = hubble * self.background_spline(efold, 1)
        alpha = state[self.alpha_slot]
        newton_density = density - 3 * hubble * enthalpy * alpha
        if branch == "gr":
            phi = -density / (2 * self.wave**2) - 3 * hubble * current / (2 * self.wave**3)
            psi = phi - anisotropy / self.wave**2
            alpha_rate = psi - hubble * alpha
            phi_rate_base = -density_rate_base / (2 * self.wave**2) - 3 * (hubble_rate * current + hubble * current_rate) / (2 * self.wave**3)
            factor = 1.
        else:
            require(branch in ("poisson-spatial", "newton-dust-force"), "owned gravity branch")
            psi = -newton_density / (2 * self.wave**2)
            factor = 1. if branch == "poisson-spatial" else 0.
            phi = factor * psi
            alpha_rate = psi - hubble * alpha
            gravity = 3 * hubble * enthalpy / (2 * self.wave**2)
            phi_rate_base = factor * (-density_rate_base / (2 * self.wave**2) + gravity_rate * alpha + gravity * alpha_rate)
        denominator = 1 + 3 * factor * quadrature_enthalpy / (2 * self.wave**2)
        require(denominator > 0 and np.isfinite(denominator), "density-metric solve")
        expansion = (self.wave * alpha - 3 * (phi_rate_base + hubble_rate * alpha + hubble * alpha_rate) / self.wave) / denominator
        phi_rate = phi_rate_base + factor * quadrature_enthalpy * expansion / (2 * self.wave)
        eta = phi + hubble * alpha
        eta_rate = phi_rate + hubble_rate * alpha + hubble * alpha_rate
        source_z, source_shear = self.metric_kernels(efold)
        original_rate[:len(self.core)] += source_z[self.core] * (expansion - native_z) + source_shear[self.core] * (self.wave * alpha - native_shear)
        original_rate[self.alpha_slot] = alpha_rate
        derivative = original_rate / hubble
        if self.model == "heavy":
            phase, mu = self.owner.phase(efold)
            omega = scale_value * self.background["masses"][1]
            amplitude = complex(*state[self.slots])
            gamma = self.wave**2 / (2 * omega * hubble)
            amplitude_rate = 1j * (mu - omega / hubble - gamma) * amplitude
            amplitude_rate += (1.5 - 1j * gamma) * np.exp(2j * phase) * amplitude.conjugate()
            amplitude_rate -= 1j * scale_value * self.wave * point[3] * expansion * np.exp(1j * phase) / (hubble * np.sqrt(omega))
            derivative[self.slots] = [amplitude_rate.real, amplitude_rate.imag]
        projected = physical.copy()
        projected[self.context["position"](1)] = self.wave * eta
        values = dict(Phi=phi, Psi=psi, D=newton_density, Q=current + enthalpy * self.wave * alpha, Pi=anisotropy,
                      theta_c=self.wave**2 * alpha, delta_c=observed[19] - 3 * hubble * alpha,
                      delta_b=observed[20] - 3 * hubble * alpha, delta_gamma=observed[21] - 4 * hubble * alpha,
                      delta_massless=observed[22] - 4 * hubble * alpha)
        rates = dict(density_sync=density_rate_base - self.wave * quadrature_enthalpy * expansion,
                     delta_c=original_rate[self.cdm_slot] - 3 * hubble_rate * alpha - 3 * hubble * alpha_rate,
                     theta_c=self.wave**2 * alpha_rate, eta=eta_rate, Phi=phi_rate)
        diagnostics = dict(alpha=alpha, alpha_rate=alpha_rate, z=expansion, eta=eta,
                           denominator=denominator, H=hubble, H_rate=hubble_rate, scale=scale_value,
                           enthalpy=enthalpy, quadrature_enthalpy=quadrature_enthalpy, density_sync=density)
        return derivative, values, rates, diagnostics, projected, terms

    def density(self, efold, state):
        raw = self.decode(efold, state)
        point = self.context["point"](efold)
        return self.context["observe"](point[11], self.project(raw))[2]


def open_system(model, folder):
    wave = dict(read(WAVELENGTH / "inventory-config.json")["waves"])["balanced"]
    context = factory(folder)(model, "balanced", wave)
    return PoissonDriver(context, model, wave)

