from common import *
import numpy as np


class PhysicalEnergyMap:
    def __init__(self, system):
        self.system = system
        self.size = len(system.core)
        self.heavy = np.array(system.slots if system.model == "heavy" else [], dtype=int)
        self.rest = np.array([index for index in range(self.size) if index not in self.heavy])
        self.quadrupoles = np.array([self.moment_slot(2, node) for node in range(5)])
        first = float(system.background["efold"][0])
        point = system.context["point"](first)
        observed = system.context["observe"](point[11], system.zero_native)
        self.origin_scale = point[10]
        self.fluid_origin = observed[12:16]
        self.speeds_origin = system.context["kinetic"](point[11])[1]
        self.massive_origin = []
        for node in range(5):
            native = np.zeros(system.context["dimension"])
            native[system.context["all_moments"][0, node]] = 1.
            terms, _ = system.context["stress"](point[11], native)
            self.massive_origin.append(float(terms[4, 0]))
        require(min(*self.fluid_origin, *self.massive_origin) > 0, "positive retained energy weights")

    def slot(self, native):
        return int(np.flatnonzero(self.system.core == self.system.context["position"](native))[0])

    def moment_slot(self, degree, node):
        return int(np.flatnonzero(self.system.core == self.system.context["all_moments"][degree, node])[0])

    def blocks(self, efold):
        system = self.system
        point = system.context["point"](efold)
        scale, hubble = point[10], point[12]
        hubble_rate = float(system.background_spline(efold, 1)[0])
        density = self.fluid_origin * (self.origin_scale / scale)**np.array([1., 1., 2., 2.])
        units = system.units[:self.size]
        alpha_unit = units[system.alpha_slot]
        direct = np.zeros((self.size, self.size))
        inverse_direct = np.zeros_like(direct)
        logarithmic = np.zeros_like(direct)
        shift, shift_rate = np.zeros(self.size), np.zeros(self.size)
        assigned = np.zeros(self.size, dtype=bool)

        def set_scalar(slot, weight, rate, gauge=0., gauge_rate=0.):
            require(weight > 0 and np.isfinite(weight), "positive physical energy weight")
            direct[slot, slot] = weight * units[slot]
            inverse_direct[slot, slot] = 1 / direct[slot, slot]
            logarithmic[slot, slot] = rate
            shift[slot] = weight * gauge * alpha_unit
            shift_rate[slot] = weight * (rate * gauge + gauge_rate) * alpha_unit
            assigned[slot] = True

        set_scalar(system.alpha_slot, np.sqrt(density[0]) * system.wave, -.5)
        set_scalar(self.slot(2), np.sqrt(density[0]) * hubble / system.wave, -.5 + hubble_rate / hubble, -3 * hubble, -3 * hubble_rate)
        set_scalar(self.slot(3), np.sqrt(density[1]) * hubble / system.wave, -.5 + hubble_rate / hubble, -3 * hubble, -3 * hubble_rate)
        set_scalar(self.slot(4), np.sqrt(density[1]), -.5, system.wave, 0.)
        signature = system.context["signature_values"]
        for species, beginning, maximum in ((2, int(signature[3]), int(signature[6])),
                                            (3, int(signature[4]), 2 if signature[12] else int(signature[8]))):
            for degree in range(maximum + 1):
                angular = 2 * degree + 1.
                if degree == maximum and maximum > 2:
                    angular = float(maximum)
                if species == 3 and signature[12] and degree == 2:
                    angular = 2.
                weight = np.sqrt(density[species] * angular / 4)
                gauge = -4 * hubble if degree == 0 else (4 * system.wave / 3 if degree == 1 else 0.)
                gauge_rate = -4 * hubble_rate if degree == 0 else 0.
                set_scalar(self.slot(beginning + degree), weight, -1., gauge, gauge_rate)
        maximum = int(signature[7])
        for degree in range(2, maximum + 1):
            angular = (2 * degree + 1) * (degree + 1) * (degree + 2) / (degree * (degree - 1))
            if degree == maximum and maximum > 2:
                previous = (2 * degree - 1) * degree * (degree + 1) / ((degree - 1) * (degree - 2))
                upper = (degree + 2) * (degree - 2) / (degree * (2 * degree - 1))
                lower = degree / (degree - 2)
                angular = previous * upper / lower
            set_scalar(self.slot(int(signature[5]) + degree), np.sqrt(density[2] * angular / 4), -1.)
        speeds = system.context["kinetic"](point[11])[1]
        massive = np.array(self.massive_origin) * (self.origin_scale / scale)**2 * self.speeds_origin / speeds
        massive_rate = -(1 + speeds**2) / 2
        self.tail_weights = np.sqrt(massive[None, :] * (2 * np.arange(3, 193)[:, None] + 1) / 4) * system.units[self.size:].reshape(190, 5)
        self.tail_rate = float(np.max(massive_rate))
        for node in range(5):
            for degree in range(3):
                weight = np.sqrt(massive[node] * (2 * degree + 1) / 4)
                gauge = -4 * hubble if degree == 0 else (4 * system.wave / (3 * speeds[node]) if degree == 1 else 0.)
                gauge_rate = -4 * hubble_rate if degree == 0 else (gauge * (1 - speeds[node]**2) if degree == 1 else 0.)
                set_scalar(self.moment_slot(degree, node), weight, massive_rate[node], gauge, gauge_rate)
        conditions = []
        for species in range(2 if system.model == "heavy" else 1):
            slots = np.array([int(np.flatnonzero(system.core == value)[0]) for value in system.owner.scalar_positions[2 * species:2 * species + 2]])
            omega = scale * system.background["masses"][species]
            full_frequency = np.sqrt(system.wave**2 + omega**2)
            omega_ratio = omega**2 / full_frequency**2
            field = system.background["initial_fields"][species] + point[2 * species]
            velocity, velocity_rate = point[2 * species + 1], point[2 * species + 6]
            velocity_second = -2 * velocity_rate - omega**2 / hubble * ((2 - hubble_rate / hubble) * field + velocity / hubble)
            if species == 0:
                block = np.diag([full_frequency * units[slots[0]], units[slots[1]]])
                inverse = np.diag(1 / np.diag(block))
                rate_block = np.diag([omega_ratio, 0.])
            else:
                phase, mu = system.owner.phase(efold)
                cosine, sine = np.cos(phase), np.sin(phase)
                rotation = np.array([[cosine, sine], [-sine, cosine]])
                factors = np.array([full_frequency / (scale * np.sqrt(omega)), np.sqrt(omega) / scale])
                block = np.diag(factors) @ rotation @ np.diag(units[slots])
                inverse = np.diag(1 / units[slots]) @ rotation.T @ np.diag(1 / factors)
                rate_block = np.diag([omega_ratio - 1.5, -.5]) - mu * np.diag(factors) @ np.array([[0., -1.], [1., 0.]]) @ np.diag(1 / factors)
            selection = np.ix_(slots, slots)
            direct[selection], inverse_direct[selection], logarithmic[selection] = block, inverse, rate_block
            shift[slots] = np.array([full_frequency * velocity, hubble * (velocity_rate - velocity)]) * alpha_unit
            shift_rate[slots] = np.array([full_frequency * (omega_ratio * velocity + velocity_rate),
                                          hubble_rate * (velocity_rate - velocity) + hubble * (velocity_second - velocity_rate)]) * alpha_unit
            assigned[slots] = True
            conditions.append(float(full_frequency / omega))
        require(np.all(assigned), "complete physical energy map")
        transform = direct.copy()
        transform[:, system.alpha_slot] += shift
        inverse = inverse_direct.copy()
        inverse[:, system.alpha_slot] -= inverse_direct @ shift / direct[system.alpha_slot, system.alpha_slot]
        derivative = logarithmic.copy()
        derivative[:, system.alpha_slot] += (shift_rate - logarithmic @ shift) / direct[system.alpha_slot, system.alpha_slot]
        return transform, inverse, derivative, conditions

    def generator(self, efold, core):
        transform, inverse, derivative, conditions = self.blocks(efold)
        return transform @ core @ inverse + derivative, transform, inverse, conditions

    def comparison(self, matrix):
        remainder = matrix[np.ix_(self.rest, self.rest)]
        remainder_rate = max(self.tail_rate, float(np.linalg.eigvalsh((remainder + remainder.T) / 2)[-1]))
        if len(self.heavy):
            heavy = matrix[np.ix_(self.heavy, self.heavy)]
            heavy_rate = float(np.linalg.eigvalsh((heavy + heavy.T) / 2)[-1])
            to_heavy = float(np.linalg.norm(matrix[np.ix_(self.heavy, self.rest)], ord=2))
            to_rest = float(np.linalg.norm(matrix[np.ix_(self.rest, self.heavy)], ord=2))
        else:
            heavy_rate, to_heavy, to_rest = 0., 0., 0.
        return np.array([[heavy_rate, to_heavy], [to_rest, remainder_rate]])

    def hierarchy_skew(self, operator, efold):
        transform, inverse, _, _ = self.blocks(efold)
        _, into_core, into_tail, speed, _, _ = operator.blocks(efold, 0)
        weights = np.diag(transform)[self.quadrupoles]
        boundary = into_core * weights / self.tail_weights[0] + into_tail * self.tail_weights[0] / weights
        lower = operator.lower[1:, None] * speed[None, :] * self.tail_weights[1:] / self.tail_weights[:-1]
        upper = operator.upper[:-1, None] * speed[None, :] * self.tail_weights[:-1] / self.tail_weights[1:]
        scale = max(float(np.max(abs(lower))), float(np.max(abs(upper))), 1e-80)
        return max(float(np.max(abs(boundary))), float(np.max(abs(lower + upper)))) / scale

