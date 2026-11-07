import sys
from common import *
sys.path.extend([str(TIMECHAIN), str(PREVIOUS)])
from canonical_math import JFULL, joint_extractor, multiply, norm, sup
import numpy as np


class NativeRest:
    def __init__(self, context, model, wave):
        self.context, self.model, self.wave = context, model, wave
        self.background = context["activate_background"]("dop-half-cap")
        self.dimension = context["dimension"]
        self.mapping = context["state_map"]
        self.signature = context["signature_values"]
        self.position = context["position"]
        self.matrices = joint_extractor()[1]
        signature = self.signature
        require(all(signature[index] == 0 for index in (11, 12, 13, 14, 16, 18, 21, 22, 23, 24, 25, 70)), "unowned approximation or thermal perturbation")
        require(signature[20] == 1 and signature[30] == 5 and signature[40] > 2, "explicit native momentum hierarchy")
        scalar_start = int(signature[2])
        excluded = [1, 2, scalar_start, scalar_start + 1]
        if model == "heavy":
            excluded += [scalar_start + 2, scalar_start + 3]
        self.scalar_positions = [self.position(index) for index in excluded[2:]]
        self.rest_positions = np.array([index for index, native in enumerate(self.mapping) if native not in excluded])
        self.expansion = np.zeros(self.dimension)
        self.shear = np.zeros(self.dimension)
        self.expansion[self.position(3)] = -wave
        for monopole in (int(signature[3]), int(signature[4])):
            self.expansion[self.position(monopole)] = -4 * wave / 3
            self.shear[self.position(monopole + 2)] = 8 * wave / 15
        for node in range(5):
            monopole = int(signature[50]) + node * (int(signature[40]) + 1)
            self.expansion[self.position(monopole)] = -4 * wave / 3
            self.shear[self.position(monopole + 2)] = 8 * wave / 15
        self.active = np.arange(8) if model == "heavy" else np.array([0, 1, 4, 5, 6, 7])
        self.maximum = 192
        self.native_order = int(signature[40])
        require(self.maximum >= self.native_order, "retained hierarchy order")
        self.native_rest_size = len(self.rest_positions)
        self.extra_size = 5 * (self.maximum - self.native_order)
        self.rest_size = self.native_rest_size + self.extra_size
        def rest_index(native):
            return int(np.flatnonzero(self.rest_positions == self.position(native))[0])
        self.tail_indices = np.array([[rest_index(int(signature[50]) + node * (self.native_order + 1) + degree)
                                       for node in range(5)] for degree in range(3, self.native_order + 1)])
        self.low_indices = np.array([rest_index(int(signature[50]) + node * (self.native_order + 1) + 2) for node in range(5)])
        self.rest_units = np.r_[context["normalization"][self.rest_positions], np.tile(context["tail_units"], self.maximum - self.native_order)]
        from scipy.interpolate import CubicSpline
        mass = self.background["masses"][1] if model == "heavy" else 1.
        self.carrier_rate = CubicSpline(self.background["efold"], self.background["a"] * mass / self.background["H"])
        self.carrier_integral = self.carrier_rate.antiderivative()
        self.carrier_origin = self.carrier_integral(self.background["efold"][0])

    def phase(self, efold):
        return float(self.carrier_integral(efold) - self.carrier_origin), float(self.carrier_rate(efold))

    def encode(self, efold, physical):
        point = self.context["point"](efold)
        scale, stamp = point[10:12]
        observer = self.context["observe"](stamp, physical)
        terms, meta = self.context["stress"](stamp, physical)
        source = meta[5] * meta[9]
        if self.model == "heavy":
            source += meta[15] * meta[19]
            phase, mu = self.phase(efold)
            omega = scale * meta[18]
            amplitude = scale * (np.sqrt(omega) * meta[19] + 1j * meta[20] / np.sqrt(omega)) * np.exp(1j * phase)
        else:
            amplitude = 0j
        current = terms[:, 1].sum()
        state = np.array([meta[9], scale**2 * meta[10], amplitude.real, amplitude.imag,
                          -2 * physical[self.position(2)], scale**2 * (current / (2 * self.wave) - source / 2),
                          physical[self.position(1)] / self.wave,
                          scale**2 * (2 * self.wave * meta[2] + 3 * current / self.wave)])
        return state, np.r_[physical[self.rest_positions], np.zeros(self.extra_size)], observer, terms, meta

    def decode(self, efold, state, rest):
        point = self.context["point"](efold)
        scale = point[10]
        physical = np.zeros(self.dimension)
        physical[self.rest_positions] = rest[:self.native_rest_size]
        physical[self.position(1)], physical[self.position(2)] = self.wave * state[6], -state[4] / 2
        physical[self.scalar_positions[0]], physical[self.scalar_positions[1]] = state[0], state[1] / scale**2
        if self.model == "heavy":
            phase, _ = self.phase(efold)
            omega = scale * self.background["masses"][1]
            amplitude = complex(*state[2:4]) * np.exp(-1j * phase)
            physical[self.scalar_positions[2]] = amplitude.real / (scale * np.sqrt(omega))
            physical[self.scalar_positions[3]] = amplitude.imag * np.sqrt(omega) / scale
        return physical

    def geometry(self, efold, state):
        point = self.context["point"](efold)
        scale = point[10]
        source = point[1] * state[0]
        if self.model == "heavy":
            phase, _ = self.phase(efold)
            omega = scale * self.background["masses"][1]
            source += point[3] * (complex(*state[2:4]) * np.exp(-1j * phase)).real / (scale * np.sqrt(omega))
        expansion = (state[7] - 6 * state[5]) / (2 * self.wave * scale**2) - 3 * source / (2 * self.wave)
        shear = state[7] / (2 * self.wave * scale**2)
        return expansion, shear

    def rest_operator(self, efold, state, rest):
        point = self.context["point"](efold)
        stamp, hubble = point[11:13]
        physical = self.decode(efold, state, rest)
        original = self.context["original_rhs"](stamp, physical)
        observed = self.context["observe"](stamp, physical)
        native_shear = observed[5]
        native_expansion = native_shear - 1.5 * observed[3] / self.wave**2
        expansion, shear = self.geometry(efold, state)
        corrected = original + self.expansion * (expansion - native_expansion) + self.shear * (shear - native_shear)
        return corrected[self.rest_positions] / hubble

    def source_only(self, efold, rest):
        point = self.context["point"](efold)
        physical = np.zeros(self.dimension)
        physical[self.rest_positions] = rest[:self.native_rest_size]
        stamp, hubble = point[11:13]
        observed = self.context["observe"](stamp, physical)
        original = self.context["original_rhs"](stamp, physical)
        terms, meta = self.context["stress"](stamp, physical)
        native_shear = observed[5]
        native_expansion = native_shear - 1.5 * observed[3] / self.wave**2
        internal = original - self.expansion * native_expansion - self.shear * native_shear
        scale = point[10]
        linear = np.zeros(8)
        linear[4] = -scale**2 / hubble * (terms[:5, 2].sum() / 2 - observed[4] / 3)
        linear[6] = 2 * scale**2 * observed[4] / hubble
        return internal[self.rest_positions] / hubble, linear, observed, terms

    def exact_hessian(self, efold):
        point = self.context["point"](efold)
        scale, hubble = point[10], point[12]
        omega_s = scale * self.background["masses"][0]
        if self.model == "heavy":
            omega_h = scale * self.background["masses"][1]
            phase, mu = self.phase(efold)
            field = self.background["initial_fields"][1] + point[2]
            amplitude = scale * (np.sqrt(omega_h) * field + 1j * point[3] / np.sqrt(omega_h)) * np.exp(1j * phase)
        else:
            omega_h, phase, mu, amplitude = scale, 0., scale / hubble, 0j
        arrays = [np.atleast_1d(value) for value in (scale, hubble, omega_s, point[1], omega_h, amplitude, mu, phase)]
        return self.matrices(*arrays, self.wave)[0][0]

    def extend_tail(self, efold, rest, native_rate):
        point = self.context["point"](efold)
        speeds = self.context["kinetic"](point[11])[1]
        tail = np.vstack([rest[self.tail_indices], rest[self.native_rest_size:].reshape(-1, 5)])
        degrees = np.arange(3, self.maximum + 1)
        lower = self.wave * degrees / (2 * degrees + 1)
        upper = -self.wave * (degrees + 1) / (2 * degrees + 1)
        derivative = np.zeros_like(tail)
        derivative[1:] += lower[1:, None] * tail[:-1]
        derivative[:-1] += upper[:-1, None] * tail[1:]
        derivative *= speeds
        derivative[0] += 3 * self.wave / 7 * speeds * rest[self.low_indices]
        derivative /= point[12]
        result = np.r_[native_rate, derivative[self.native_order - 2:].ravel()]
        result[self.tail_indices] = derivative[:self.native_order - 2]
        return result

    def full_rhs(self, efold, state, rest):
        internal, linear, observed, terms = self.source_only(efold, rest)
        expansion, shear = self.geometry(efold, state)
        hubble = self.context["point"](efold)[12]
        rest_rate = internal + (self.expansion[self.rest_positions] * expansion + self.shear[self.rest_positions] * shear) / hubble
        state_rate = JFULL @ (self.exact_hessian(efold) @ state + linear)
        return state_rate, self.extend_tail(efold, rest, rest_rate)
