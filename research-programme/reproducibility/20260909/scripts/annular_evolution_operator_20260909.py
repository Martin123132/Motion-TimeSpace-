import math
import numpy as numerical
import sympy as symbolic

from annular_fifth_order_jet_20260909 import Jet, KEYS, INDEX, MAX_ORDER, jet_log


def equations(fields, radius, coupling, case):
    kappa = float(symbolic.sympify(case["normalization_kappa"]))
    constants = {key: float(symbolic.sympify(value)) for key, value in case["parameters"].items()}
    mass = fields["mass_ref"] + coupling * fields["mass_response"]
    shift = fields["shift_ref"] + coupling * fields["shift_response"]
    scalar = fields["scalar_ref"] + coupling * fields["scalar_response"]
    lapse = 1 - 2 * mass / radius - constants["Lambda"] * radius**2 / 3
    inverse_exp = (-shift).exp()
    exp_shift = shift.exp()
    lapse_radial = lapse.derivative(2)
    shift_radial = shift.derivative(2)
    shift_mixed = shift_radial.derivative(1)
    curvature = -lapse_radial.derivative(2) - 3 * lapse_radial * shift_radial - 2 * lapse * (shift_radial.derivative(2) + shift_radial**2) - 2 * inverse_exp * shift_mixed + 2 * (lapse_radial + lapse * shift_radial) / radius + 2 * (1 - lapse) / radius**2
    weyl = curvature**2 / 3
    scalar_time = scalar.derivative(1)
    scalar_radial = scalar.derivative(2)
    kinetic = 2 * inverse_exp * scalar_time * scalar_radial + lapse * scalar_radial**2
    principal = 1 - 4 * constants["b2"] * kinetic - 6 * constants["b3"] * kinetic**2
    weighted = principal + 2 * coupling * weyl
    potential = constants["m_chi"]**2 * scalar**2 / 2
    multiplier = -2 * coupling * radius**2 * kinetic * curvature / 3
    multiplier_radial = multiplier.derivative(2)
    bg = 2 * lapse / radius - lapse_radial - 2 * lapse * shift_radial
    boundary = 2 * lapse * multiplier_radial + 2 * inverse_exp * multiplier.derivative(1) + bg * multiplier
    improved = mass - kappa * boundary
    time_current = radius**2 * weighted * scalar_radial
    radial_current = radius**2 * weighted * scalar_time + exp_shift * radius**2 * weighted * lapse * scalar_radial
    scalar_residual = inverse_exp * (time_current.derivative(1) + radial_current.derivative(2)) / radius**2 - constants["m_chi"]**2 * scalar
    energy = radius**2 * weighted * scalar_time * (inverse_exp * scalar_time + lapse * scalar_radial) - lapse.derivative(1) * multiplier_radial - bg.derivative(1) * multiplier
    radial_energy = radius**2 * (principal * lapse * scalar_radial**2 / 2 + potential + constants["b2"] * kinetic**2 + 2 * constants["b3"] * kinetic**3) + coupling * radius**2 * weyl * lapse * scalar_radial**2 + shift_radial * boundary - 2 * inverse_exp * shift_mixed * multiplier
    lapse_source = kappa * radius * weighted * scalar_radial**2 + 2 * kappa * (multiplier_radial.derivative(2) + 2 * multiplier_radial / radius - shift_radial * multiplier_radial) / radius
    radial_box = lapse_radial + lapse * shift_radial
    base_curvature = curvature - 2 * radial_box / radius - 2 * (1 - lapse) / radius**2
    multiplier_box = 2 * inverse_exp * multiplier_radial.derivative(1) + lapse * multiplier_radial.derivative(2) + radial_box * multiplier_radial
    angular_source = -kinetic / 2 - potential + constants["b2"] * kinetic**2 + constants["b3"] * kinetic**3 - coupling * kinetic * weyl + multiplier_box / radius**2 - 2 * multiplier / radius**4
    angular_residual = radial_box / radius - base_curvature / 2 + constants["Lambda"] - 2 * kappa * angular_source
    return {"scalar": scalar_residual, "mass_time": improved.derivative(1) - kappa * energy, "mass_radial": improved.derivative(2) - kappa * radial_energy, "lapse_radial": shift_radial - lapse_source, "angular_metric": angular_residual, "lapse_time_source_error": (shift_radial - lapse_source).derivative(1), "scalar_density": exp_shift * radius**2 * scalar_residual}, lapse.extract(), weyl.extract()



def coefficients(state, radius, constants, kappa, sigma):
    scalar, velocity, radial, mass, shift = state
    exponential = numerical.exp(shift)
    lapse = 1 - 2 * mass / radius - constants["Lambda"] * radius**2 / 3
    kinetic = 2 * velocity * radial + lapse * radial**2
    principal = 1 - 4 * constants["b2"] * kinetic - 6 * constants["b3"] * kinetic**2
    principal_x = -4 * constants["b2"] - 12 * constants["b3"] * kinetic
    rho = exponential * radius**2
    raised = velocity + lapse * radial
    density_a = 2 * radius**2 * principal_x * radial**2 / exponential
    density_b = radius**2 * (principal + 2 * principal_x * radial * raised)
    density_c = rho * (principal * lapse + 2 * principal_x * raised**2)
    density_time = density_a - 2 * sigma * density_b + sigma**2 * density_c
    source_delta = kappa * radius * principal * radial**2
    source_time = kappa * radius**2 * exponential * principal * velocity * raised
    source_radial = kappa * radius**2 * (principal * lapse * radial**2 / 2 + constants["m_chi"]**2 * scalar**2 / 2 + constants["b2"] * kinetic**2 + 2 * constants["b3"] * kinetic**3)
    current_mass_v = -2 * radius * principal_x * radial**3
    current_mass_r = -2 * radius * exponential * (principal_x * radial**2 * raised + principal * radial)
    current_r = rho * principal * raised
    explicit_lapse_r = 2 * mass / radius**2 - 2 * constants["Lambda"] * radius / 3
    explicit_current_r = exponential * (2 * radius * principal * raised + radius**2 * explicit_lapse_r * (principal_x * radial**2 * raised + principal * radial))
    return {"E": exponential, "F": lapse, "rho": rho, "P": principal, "Px": principal_x, "a": density_a, "b": density_b, "c": density_c, "at": density_time, "D": source_delta, "C": source_time, "R": source_radial, "jmu_v": current_mass_v, "jmu_r": current_mass_r, "jr": current_r, "jr_explicit": explicit_current_r}


def reference_rhs(state, spatial, radius, constants, kappa, sigma):
    data = coefficients(state, radius, constants, kappa, sigma)
    scalar, velocity, radial, mass, shift = state
    scalar_r, velocity_r, radial_r, mass_r, shift_r = spatial
    source = data["rho"] * constants["m_chi"]**2 * scalar - data["jmu_v"] * data["C"] - data["jmu_r"] * data["R"] - ((data["b"] - sigma * data["c"]) * data["E"] * velocity + data["jr"]) * data["D"] - data["jr_explicit"]
    velocity_time = (source - data["E"] * (2 * data["b"] - sigma * data["c"]) * velocity_r - data["c"] * radial_r) / (data["E"] * data["at"])
    radial_time = data["E"] * velocity_r - sigma * data["E"] * velocity_time + data["E"] * velocity * data["D"]
    return numerical.stack([data["E"] * velocity, velocity_time, radial_time, data["C"], (shift_r - data["D"]) / sigma])


def local_jacobians(state, spatial, radius, constants, kappa, sigma):
    zero_order, first_order = [], []
    step = 1e-30
    for component in range(5):
        varied = state.astype(complex)
        varied[component] += 1j * step
        zero_order.append(reference_rhs(varied, spatial, radius, constants, kappa, sigma).imag / step)
        varied_spatial = spatial.astype(complex)
        varied_spatial[component] += 1j * step
        first_order.append(reference_rhs(state, varied_spatial, radius, constants, kappa, sigma).imag / step)
    return numerical.stack(zero_order, axis=1), numerical.stack(first_order, axis=1)


class AnnularFields:
    def __init__(self, case, sigma=0.05):
        self.case = case
        self.sigma = sigma
        self.constants = {key: float(symbolic.sympify(value)) for key, value in case["parameters"].items()}
        self.kappa = float(symbolic.sympify(case["normalization_kappa"]))
        time_symbol, radius_symbol = symbolic.symbols("v r", positive=True)
        self.metadata = []
        expressions = []
        for field, orders in case["fields"].items():
            for order, modes in orders.items():
                for key, expression in modes.items():
                    self.metadata.append((field, int(order), key[:3], int(key[3:])))
                    expressions.append(symbolic.sympify(expression, locals={"v": time_symbol, "r": radius_symbol}))
        self.evaluator = symbolic.lambdify((time_symbol, radius_symbol), expressions, modules=[{"log": jet_log}, "numpy"], cse=True, docstring_limit=0)

    def evaluate(self, times, radii, epsilon):
        Jet.numpy = numerical
        times, radii = numerical.broadcast_arrays(times, radii)
        shape = times.shape
        Jet.count = times.size
        advanced = times.ravel() + self.sigma * (radii.ravel() - 4)
        time_jet = Jet.variable(advanced, 1)
        radius_jet = Jet.variable(radii.ravel(), 2)
        coupling = Jet.variable(0, 0)
        coefficients_values = [value if isinstance(value, Jet) else Jet.constant(value) for value in self.evaluator(time_jet, radius_jet)]
        harmonics = {}
        for kind, mode in set((entry[2], entry[3]) for entry in self.metadata):
            data = numerical.zeros((len(KEYS), Jet.count))
            active = []
            for degree in range(MAX_ORDER + 1):
                position = INDEX[0, degree, 0]
                angle = mode * advanced / epsilon + degree * numerical.pi / 2
                data[position] = (numerical.cos(angle) if kind == "cos" else numerical.sin(angle)) * (mode / epsilon)**degree / math.factorial(degree)
                active.append(position)
            harmonics[kind, mode] = Jet(data, active)
        fields = {field: Jet.constant(0) for field in self.case["fields"]}
        for (field, order, kind, mode), value in zip(self.metadata, coefficients_values):
            fields[field] = fields[field] + epsilon**order * value * harmonics[kind, mode]
        residuals, _, _ = equations(fields, radius_jet, coupling, self.case)
        scalar = fields["scalar_ref"] + coupling * fields["scalar_response"]
        mass = fields["mass_ref"] + coupling * fields["mass_response"]
        shift = fields["shift_ref"] + coupling * fields["shift_response"]
        exponential = shift.exp()
        velocity = (-shift).exp() * scalar.derivative(1)
        radial = scalar.derivative(2)
        state_jets = [scalar, velocity, radial, mass, shift]
        lapse = 1 - 2 * mass / radius_jet - self.constants["Lambda"] * radius_jet**2 / 3
        kinetic = 2 * velocity * radial + lapse * radial**2
        principal = 1 - 4 * self.constants["b2"] * kinetic - 6 * self.constants["b3"] * kinetic**2
        principal_x = -4 * self.constants["b2"] - 12 * self.constants["b3"] * kinetic
        density_a = 2 * radius_jet**2 * principal_x * radial**2 / exponential
        density_b = radius_jet**2 * (principal + 2 * principal_x * radial * (velocity + lapse * radial))
        density_c = exponential * radius_jet**2 * (principal * lapse + 2 * principal_x * (velocity + lapse * radial)**2)
        density_time = density_a - 2 * self.sigma * density_b + self.sigma**2 * density_c
        current_mass_v = -2 * radius_jet * principal_x * radial**3
        current_mass_r = -2 * radius_jet * exponential * (principal_x * radial**2 * (velocity + lapse * radial) + principal * radial)
        current_r = exponential * radius_jet**2 * principal * (velocity + lapse * radial)
        lapse_multiplier = (density_b - self.sigma * density_c) * exponential * velocity + current_r
        defect_velocity = (residuals["scalar_density"] - current_mass_v * residuals["mass_time"] - current_mass_r * residuals["mass_radial"] - lapse_multiplier * residuals["lapse_radial"]) / (exponential * density_time)
        defect_radial = -self.sigma * exponential * defect_velocity + exponential * velocity * residuals["lapse_radial"]
        defects = [Jet.constant(0), defect_velocity, defect_radial, residuals["mass_time"], -residuals["lapse_radial"] / self.sigma]
        result = {}
        for label, jets in [("state", state_jets), ("state_time", [entry.derivative(1) for entry in state_jets]), ("state_space", [entry.derivative(2) + self.sigma * entry.derivative(1) for entry in state_jets]), ("defect", defects)]:
            result[label] = numerical.stack([numerical.stack([entry.extract(degree).reshape(shape) for entry in jets]) for degree in [0, 1]])
        result["initial_constraint"] = numerical.stack([(residuals["mass_radial"] + self.sigma * residuals["mass_time"]).extract(degree).reshape(shape) for degree in [0, 1]])
        return result
