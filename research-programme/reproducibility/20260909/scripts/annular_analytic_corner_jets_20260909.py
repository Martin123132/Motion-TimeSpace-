import math

import numpy as numerical

from annular_fifth_order_jet_20260909 import Jet, KEYS, INDEX, MAX_ORDER


def refresh(data):
    return Jet(data, [position for position in range(len(KEYS)) if numerical.any(data[position] != 0)])


def constitutive_jets(primitive, radius, evaluator):
    scalar, velocity, gradient, mass, shift = primitive
    exponential = shift.exp()
    lapse = 1 - 2 * mass / radius - evaluator.constants["Lambda"] * radius**2 / 3
    radial = gradient - evaluator.sigma * velocity
    kinetic = 2 * velocity * radial / exponential + lapse * radial**2
    principal = 1 - 4 * evaluator.constants["b2"] * kinetic - 6 * evaluator.constants["b3"] * kinetic**2
    slope = -4 * evaluator.constants["b2"] - 12 * evaluator.constants["b3"] * kinetic
    sigma = evaluator.sigma
    canonical_momentum = sigma * (2 - sigma * exponential * lapse) * velocity - (1 - sigma * exponential * lapse) * gradient
    flux_base = velocity + exponential * lapse * radial
    kinetic_velocity = 2 * (gradient - 2 * sigma * velocity) / exponential - 2 * sigma * lapse * radial
    kinetic_gradient = 2 * velocity / exponential + 2 * lapse * radial
    kinetic_exponential = -2 * velocity * radial / exponential**2
    alpha = principal * sigma * (2 - sigma * exponential * lapse) + slope * kinetic_velocity * canonical_momentum
    mixed = principal * (1 - sigma * exponential * lapse) + slope * kinetic_velocity * flux_base
    wave = principal * exponential * lapse + slope * kinetic_gradient * flux_base
    momentum_lapse = slope * radial**2 * canonical_momentum + principal * sigma * exponential * radial
    momentum_exponential = slope * kinetic_exponential * canonical_momentum + principal * sigma * lapse * radial
    flux_lapse = slope * radial**2 * flux_base + principal * exponential * radial
    flux = principal * flux_base
    time_source = evaluator.kappa * radius**2 * velocity * flux / exponential
    radial_source = evaluator.kappa * radius**2 * (principal * lapse * radial**2 / 2 + evaluator.constants["m_chi"]**2 * scalar**2 / 2 + evaluator.constants["b2"] * kinetic**2 + 2 * evaluator.constants["b3"] * kinetic**3)
    return {"E": exponential, "F": lapse, "P": principal, "Q": principal + 2 * kinetic * slope, "alpha": alpha, "B": mixed, "c": wave, "h_mu": -2 * momentum_lapse / radius, "h_delta": exponential * momentum_exponential, "f_mu": -2 * flux_lapse / radius, "h": principal * canonical_momentum, "f": flux, "C0": time_source, "G0": radial_source + sigma * time_source, "D0": evaluator.kappa * radius * principal * radial**2, "potential_force": exponential * evaluator.constants["m_chi"]**2 * scalar}


def background_jets(evaluator, radii, time=0., epsilon=.1):
    Jet.numpy, Jet.count = numerical, radii.size
    radius = Jet.variable(radii, 2)
    advanced = Jet.variable(numerical.full_like(radii, time), 1) + evaluator.sigma * (radius - 4)
    coefficient_values = [entry if isinstance(entry, Jet) else Jet.constant(entry) for entry in evaluator.evaluator(advanced, radius)]
    harmonics = {}
    for kind, mode in set((entry[2], entry[3]) for entry in evaluator.metadata):
        phase = mode * advanced.extract() / epsilon
        increment = (advanced - advanced.extract()) * (mode / epsilon)
        harmonic = Jet.constant(0)
        power = Jet.constant(1)
        for degree in range(MAX_ORDER + 1):
            coefficient = (numerical.cos(phase + degree * numerical.pi / 2) if kind == "cos" else numerical.sin(phase + degree * numerical.pi / 2)) / math.factorial(degree)
            harmonic = harmonic + coefficient * power
            power = power * increment
        harmonics[kind, mode] = harmonic
    fields = {name: Jet.constant(0) for name in evaluator.case["fields"]}
    for (name, order, kind, mode), coefficient in zip(evaluator.metadata, coefficient_values):
        fields[name] = fields[name] + epsilon**order * coefficient * harmonics[kind, mode]
    scalar, mass, shift = [fields[name] for name in ["scalar_ref", "mass_ref", "shift_ref"]]
    primitive = [scalar, scalar.derivative(1), scalar.derivative(2), mass, shift]
    data = constitutive_jets(primitive, radius, evaluator)
    current = [scalar, primitive[2], data["h"], mass, shift]
    return radius, primitive, data, current


class AnalyticCornerJets:
    def __init__(self, evaluator, families):
        self.evaluator, self.families = evaluator, families
        self.radii = numerical.tile([4., 8.], families)
        self.radius, self.primitive, self.data, self.background = background_jets(evaluator, self.radii)
        self.background_rhs = self.rhs([Jet.constant(0) for component in range(5)])
        self.defect = [value.derivative(1) - derivative for value, derivative in zip(self.background, self.background_rhs)]
        self.background_constraint = self.primitive[3].derivative(2) - self.data["G0"]

    def rhs(self, error):
        velocity_error = (error[2] + self.data["B"] * error[1] - self.data["h_mu"] * error[3] - self.data["h_delta"] * error[4]) / self.data["alpha"]
        velocity = self.primitive[1] + velocity_error
        fields = [self.background[0] + error[0], velocity, self.background[1] + error[1], self.background[3] + error[3], self.background[4] + error[4]]
        data = constitutive_jets(fields, self.radius, self.evaluator)
        constraint = fields[3].derivative(2) - data["G0"]
        return [velocity, velocity.derivative(2), (self.radius**2 * data["f"]).derivative(2) / self.radius**2 - data["potential_force"] - data["f_mu"] * constraint, data["C0"], (fields[4].derivative(2) - data["D0"]) / self.evaluator.sigma]

    def evaluate(self, initial_derivatives, forcing_weights):
        Jet.numpy, Jet.count = numerical, self.radii.size
        forcing = numerical.repeat(numerical.asarray(forcing_weights), 2)
        if len(forcing_weights) != self.families or numerical.shape(initial_derivatives) != (5, self.families, 4, 2):
            raise ValueError("Need initial coordinate derivatives zero through four at both endpoints")
        coordinate = []
        for component in range(4):
            values = numerical.zeros((len(KEYS), self.radii.size))
            for order in range(5):
                if component != 2 or order == 0:
                    values[INDEX[1, 0, order]] = initial_derivatives[order, :, component].ravel() / math.factorial(order)
            coordinate.append(refresh(values))
        for order in range(3):
            fields = [self.primitive[0] + coordinate[0], self.primitive[1] + coordinate[1], self.primitive[2] + coordinate[0].derivative(2), self.primitive[3] + coordinate[2], self.primitive[4] + coordinate[3]]
            source = constitutive_jets(fields, self.radius, self.evaluator)["G0"]
            values = coordinate[2].data.copy()
            values[INDEX[1, 0, order + 1]] = (source.data[INDEX[1, 0, order]] - forcing * self.background_constraint.data[INDEX[0, 0, order]]) / (order + 1)
            coordinate[2] = refresh(values)
        momentum = self.data["alpha"] * coordinate[1] - self.data["B"] * coordinate[0].derivative(2) + self.data["h_mu"] * coordinate[2] + self.data["h_delta"] * coordinate[3]
        initial = [coordinate[0], coordinate[0].derivative(2), momentum, coordinate[2], coordinate[3]]
        error = []
        for value in initial:
            selected = numerical.zeros_like(value.data)
            for order in range(4):
                selected[INDEX[1, 0, order]] = value.data[INDEX[1, 0, order]]
            error.append(refresh(selected))
        for time_order in range(3):
            rhs = self.rhs(error)
            updated = []
            for component in range(5):
                values = error[component].data.copy()
                for radial_order in range(3 - time_order):
                    values[INDEX[1, time_order + 1, radial_order]] = (rhs[component].data[INDEX[1, time_order, radial_order]] - forcing * self.defect[component].data[INDEX[0, time_order, radial_order]]) / (time_order + 1)
                updated.append(refresh(values))
            error = updated
        impedance = (self.data["P"] * self.data["Q"])**.5
        sign = numerical.tile([-1., 1.], self.families)
        slope = -(self.data["B"] + sign * impedance) / self.data["c"]
        velocity_error = (error[2] + self.data["B"] * error[1] - self.data["h_mu"] * error[3] - self.data["h_delta"] * error[4]) / self.data["alpha"]
        boundary = error[1] - slope * velocity_error + (slope - self.evaluator.sigma) * self.primitive[1] * error[4]
        corners = []
        for order in range(4):
            scalar = boundary.data[INDEX[1, order, 0]].reshape((self.families, 2)) * math.factorial(order)
            lapse = error[4].data[INDEX[1, order, 0]].reshape((self.families, 2))[:, 1] * math.factorial(order)
            corners.append(numerical.column_stack([scalar, lapse]))
        return numerical.stack(corners, axis=1), error
