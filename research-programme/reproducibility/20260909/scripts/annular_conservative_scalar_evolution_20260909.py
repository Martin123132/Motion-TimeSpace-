import math

import numpy as numerical

from sbp4_derived_operator_20260909 import derivative
from sbp4_compatible_second_operator_20260909 import norm_weights


def metric(time, radii, constants, dynamic=False):
    mass = 1 + (0.005 * numerical.sin(0.7 * time) if dynamic else 0)
    mass_time = 0.0035 * numerical.cos(0.7 * time) if dynamic else 0
    exponential = numerical.exp(0.01 * numerical.sin(time)) if dynamic else 1 + 0 * radii
    exponential_time = 0.01 * numerical.cos(time) * exponential if dynamic else 0 * radii
    lapse = 1 - 2 * mass / radii - constants["Lambda"] * radii**2 / 3
    lapse_time = -2 * mass_time / radii
    lapse_radial = 2 * mass / radii**2 - 2 * constants["Lambda"] * radii / 3
    return exponential, lapse, exponential_time, lapse_time, lapse_radial


def constitutive(velocity, gradient, exponential, lapse, constants, sigma=0.05):
    radial = gradient - sigma * velocity
    kinetic = 2 * velocity * radial / exponential + lapse * radial**2
    principal = 1 - 4 * constants["b2"] * kinetic - 6 * constants["b3"] * kinetic**2
    slope = -4 * constants["b2"] - 12 * constants["b3"] * kinetic
    canonical_alpha = sigma * (2 - sigma * exponential * lapse)
    canonical_mixed = 1 - sigma * exponential * lapse
    canonical_momentum = canonical_alpha * velocity - canonical_mixed * gradient
    kinetic_velocity = 2 * (gradient - 2 * sigma * velocity) / exponential - 2 * sigma * lapse * radial
    kinetic_gradient = 2 * velocity / exponential + 2 * lapse * radial
    kinetic_exponential = -2 * velocity * radial / exponential**2
    momentum = principal * canonical_momentum
    flux_base = velocity + exponential * lapse * radial
    flux = principal * flux_base
    alpha = principal * canonical_alpha + slope * kinetic_velocity * canonical_momentum
    mixed = principal * canonical_mixed + slope * kinetic_velocity * flux_base
    wave = principal * exponential * lapse + slope * kinetic_gradient * flux_base
    discriminant = principal * (principal + 2 * kinetic * slope)
    momentum_exponential = slope * kinetic_exponential * canonical_momentum + principal * sigma * lapse * radial
    momentum_lapse = slope * radial**2 * canonical_momentum + principal * sigma * exponential * radial
    flux_exponential = slope * kinetic_exponential * flux_base + principal * lapse * radial
    flux_lapse = slope * radial**2 * flux_base + principal * exponential * radial
    return {"momentum": momentum, "flux": flux, "X": kinetic, "P": principal, "Q": principal + 2 * kinetic * slope, "alpha": alpha, "B": mixed, "c": wave, "D": discriminant, "h_E": momentum_exponential, "h_F": momentum_lapse, "flux_E": flux_exponential, "flux_F": flux_lapse, "s": radial}


def invert_momentum(momentum, gradient, exponential, lapse, constants, sigma=0.05):
    canonical_alpha = sigma * (2 - sigma * exponential * lapse)
    if numerical.any(canonical_alpha <= 0):
        raise ValueError("Canonical seed leaves the declared time branch")
    velocity = (momentum + (1 - sigma * exponential * lapse) * gradient) / canonical_alpha
    scale = numerical.maximum(numerical.maximum(numerical.abs(momentum), numerical.abs(gradient)), 1e-6)
    for iteration in range(12):
        values = constitutive(velocity, gradient, exponential, lapse, constants, sigma)
        healthy = (values["alpha"] > 0) & (values["P"] > 0) & (values["Q"] > 0)
        if not numerical.all(healthy):
            raise ValueError("Legendre inversion leaves the sampled healthy branch")
        residual = values["momentum"] - momentum
        if numerical.all(numerical.abs(residual) <= 2e-13 * scale + 1e-15):
            return velocity, values, iteration, float(numerical.max(numerical.abs(residual)))
        correction = residual / values["alpha"]
        damping = 1.0
        for attempt in range(16):
            proposed = velocity - damping * correction
            trial = constitutive(proposed, gradient, exponential, lapse, constants, sigma)
            acceptable = (trial["alpha"] > 0) & (trial["P"] > 0) & (trial["Q"] > 0)
            if numerical.all(acceptable) and numerical.all(numerical.abs(trial["momentum"] - momentum) <= numerical.abs(residual) + 1e-15):
                velocity = proposed
                break
            damping /= 2
        else:
            raise ValueError("Safeguarded Legendre step failed")
    raise ValueError("Legendre inversion did not converge")


def manufactured(time, radii, constants, domain, dynamic=False, amplitude=0.03, sigma=0.05):
    wave_number = 2 * numerical.pi / (domain[1] - domain[0])
    frequency = 2.3
    phase = wave_number * (radii - domain[0]) + 0.27
    angle = frequency * time + 0.17
    scalar = amplitude * numerical.sin(phase) * numerical.cos(angle)
    velocity = -amplitude * frequency * numerical.sin(phase) * numerical.sin(angle)
    gradient = amplitude * wave_number * numerical.cos(phase) * numerical.cos(angle)
    velocity_time = -frequency**2 * scalar
    gradient_time = -amplitude * wave_number * frequency * numerical.cos(phase) * numerical.sin(angle)
    gradient_radial = -wave_number**2 * scalar
    exponential, lapse, exponential_time, lapse_time, lapse_radial = metric(time, radii, constants, dynamic)
    values = constitutive(velocity, gradient, exponential, lapse, constants, sigma)
    momentum_time = values["alpha"] * velocity_time - values["B"] * gradient_time + values["h_E"] * exponential_time + values["h_F"] * lapse_time
    flux_radial = values["B"] * gradient_time + values["c"] * gradient_radial + values["flux_F"] * lapse_radial
    forcing = momentum_time - flux_radial - 2 * values["flux"] / radii + exponential * constants["m_chi"]**2 * scalar
    return {"state": numerical.stack([scalar, gradient, values["momentum"]]), "velocity": velocity, "forcing": forcing, "momentum_time": momentum_time, "flux_radial": flux_radial, "metric": (exponential, lapse, exponential_time, lapse_time, lapse_radial), "constitutive": values}


class ScalarEvolution:
    def __init__(self, radii, constants, domain, dynamic=False, sigma=0.05):
        self.radii, self.constants, self.domain = radii, constants, domain
        self.dynamic, self.sigma = dynamic, sigma
        self.spacing = float(radii[1] - radii[0])
        self.weights = self.spacing * norm_weights(radii.size)
        self.minimum_alpha = math.inf
        self.minimum_P = math.inf
        self.minimum_Q = math.inf
        self.maximum_inversion_iterations = 0
        self.maximum_inversion_residual = 0.0
        self.maximum_speed = 0.0
        self.mode_counts = set()

    def diagnose(self, time, state):
        exponential, lapse, exponential_time, lapse_time, unused_radial = metric(time, self.radii, self.constants, self.dynamic)
        velocity, values, iterations, inversion_residual = invert_momentum(state[2], state[1], exponential, lapse, self.constants, self.sigma)
        self.minimum_alpha = min(self.minimum_alpha, float(numerical.min(values["alpha"])))
        self.minimum_P = min(self.minimum_P, float(numerical.min(values["P"])))
        self.minimum_Q = min(self.minimum_Q, float(numerical.min(values["Q"])))
        self.maximum_inversion_iterations = max(self.maximum_inversion_iterations, iterations)
        self.maximum_inversion_residual = max(self.maximum_inversion_residual, inversion_residual)
        characteristic = numerical.stack([(values["B"] - numerical.sqrt(values["D"])) / values["alpha"], (values["B"] + numerical.sqrt(values["D"])) / values["alpha"]])
        self.maximum_speed = max(self.maximum_speed, float(numerical.max(numerical.abs(characteristic))))
        left_incoming = int(numerical.sum(characteristic[:, 0] < -1e-10))
        right_incoming = int(numerical.sum(characteristic[:, -1] > 1e-10))
        if left_incoming not in [0, 1] or right_incoming != 1:
            raise ValueError("Boundary configuration is outside this controlled evolution implementation")
        self.mode_counts.add((left_incoming, right_incoming))
        return velocity, values, (exponential, lapse, exponential_time, lapse_time), (left_incoming, right_incoming)

    def rhs(self, time, state, diagnostics=False):
        exact = manufactured(time, self.radii, self.constants, self.domain, self.dynamic, sigma=self.sigma)
        velocity, values, metric_values, counts = self.diagnose(time, state)
        exponential, lapse, exponential_time, lapse_time = metric_values
        flux = values["flux"]
        area_flux = self.radii**2 * flux
        source = exact["forcing"].copy()
        for position, incoming, orientation in [(0, counts[0], 1), (-1, counts[1], -1)]:
            if incoming:
                impedance = numerical.sqrt(exact["constitutive"]["D"][position])
                current_difference = flux[position] - exact["constitutive"]["flux"][position]
                velocity_difference = velocity[position] - exact["velocity"][position]
                source[position] += (orientation * current_difference - impedance * velocity_difference) / self.weights[position]
        result = numerical.stack([velocity, derivative(velocity, self.spacing), derivative(area_flux, self.spacing) / self.radii**2 - exponential * self.constants["m_chi"]**2 * state[0] + source])
        lagrangian = -values["X"] / 2 + self.constants["b2"] * values["X"]**2 + self.constants["b3"] * values["X"]**3 - self.constants["m_chi"]**2 * state[0]**2 / 2
        kinetic_exponential = -2 * velocity * values["s"] / exponential**2
        energy_exponential = -self.radii**2 * lagrangian + exponential * self.radii**2 * values["P"] * kinetic_exponential / 2
        energy_lapse = exponential * self.radii**2 * values["P"] * values["s"]**2 / 2
        metric_work = float(numerical.sum(self.weights * (energy_exponential * exponential_time + energy_lapse * lapse_time)))
        boundary_work = float(area_flux[-1] * velocity[-1] - area_flux[0] * velocity[0])
        source_work = float(numerical.sum(self.weights * self.radii**2 * velocity * source))
        energy_power = boundary_work + source_work + metric_work
        if not diagnostics:
            return result, energy_power
        direct_power = float(numerical.sum(self.weights * (exponential * self.radii**2 * self.constants["m_chi"]**2 * state[0] * result[0] + area_flux * result[1] + self.radii**2 * velocity * result[2]))) + metric_work
        energy = float(numerical.sum(self.weights * self.radii**2 * (state[2] * velocity - exponential * lagrangian)))
        product_defect = derivative(area_flux, self.spacing) / self.radii**2 - derivative(flux, self.spacing) - 2 * flux / self.radii
        return result, energy_power, {"energy": energy, "direct_energy_power": direct_power, "balanced_energy_power": energy_power, "metric_work": metric_work, "boundary_work": boundary_work, "source_work": source_work, "weighted_flux_product_defect_max": float(numerical.max(numerical.abs(product_defect))), "velocity": velocity, "boundary_modes": counts}

    def evolve(self, final_time=0.15, cfl=0.15, time_refinement=1):
        state = manufactured(0, self.radii, self.constants, self.domain, self.dynamic, sigma=self.sigma)["state"].copy()
        unused_rhs, unused_power, initial = self.rhs(0, state, diagnostics=True)
        speed = max(self.maximum_speed, 1 / self.sigma) * 1.05
        steps = int(math.ceil(final_time * speed / (cfl * self.spacing)))
        steps = int(math.ceil(steps / 3)) * 3 * time_refinement
        timestep = final_time / steps
        initial_defect = state[1] - derivative(state[0], self.spacing)
        budget = 0.0
        outputs = []
        for step in range(steps):
            time = step * timestep
            first, first_power = self.rhs(time, state)
            second, second_power = self.rhs(time + timestep / 2, state + timestep * first / 2)
            third, third_power = self.rhs(time + timestep / 2, state + timestep * second / 2)
            fourth, fourth_power = self.rhs(time + timestep, state + timestep * third)
            state += timestep * (first + 2 * second + 2 * third + fourth) / 6
            budget += timestep * (first_power + 2 * second_power + 2 * third_power + fourth_power) / 6
            if step + 1 in [steps // 3, steps]:
                current_time = (step + 1) * timestep
                unused_rhs, unused_power, diagnostics = self.rhs(current_time, state, diagnostics=True)
                exact = manufactured(current_time, self.radii, self.constants, self.domain, self.dynamic, sigma=self.sigma)
                actual = numerical.vstack([state, diagnostics.pop("velocity")])
                truth = numerical.vstack([exact["state"], exact["velocity"]])
                outputs.append({"time": current_time, "state": state.copy(), "actual": actual, "exact": truth, "absolute_error": numerical.max(numerical.abs(actual - truth), axis=-1), "L2_error": numerical.sqrt(numerical.sum(self.weights * (actual - truth)**2, axis=-1)), "scale": numerical.max(numerical.abs(truth), axis=-1), "integrability_change": float(numerical.max(numerical.abs(state[1] - derivative(state[0], self.spacing) - initial_defect))), "integrability_initial_max": float(numerical.max(numerical.abs(initial_defect))), "energy_integral_error": diagnostics["energy"] - initial["energy"] - budget, "energy_scale": max(abs(initial["energy"]), abs(budget), abs(diagnostics["energy"]), 1e-30), "diagnostics": diagnostics})
        return outputs, {"steps": steps, "dt": timestep, "maximum_speed": self.maximum_speed, "actual_CFL": timestep * self.maximum_speed / self.spacing, "minimum_alpha": self.minimum_alpha, "minimum_P": self.minimum_P, "minimum_Q": self.minimum_Q, "maximum_inversion_iterations": self.maximum_inversion_iterations, "maximum_inversion_residual": self.maximum_inversion_residual, "mode_counts": sorted(self.mode_counts)}
