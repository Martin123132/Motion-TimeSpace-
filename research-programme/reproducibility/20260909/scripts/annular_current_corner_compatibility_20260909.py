import numpy as numerical
import sympy as symbolic

from annular_coupled_current_operator_20260909 import primitive_data, snapshot_coefficients


def explicit_gradients(data):
    zero = numerical.zeros_like(data["alpha"])
    velocity = numerical.stack([zero, data["B"] / data["alpha"], 1 / data["alpha"], -data["h_mu"] / data["alpha"], -data["h_delta"] / data["alpha"]])
    flux = data["B"] * velocity + numerical.stack([zero, data["c"], zero, data["f_mu"], data["E"] * data["flux_E"]])
    return velocity, flux


def continuous_operator(snapshot, radii, evaluator):
    current = snapshot_coefficients(snapshot, radii, evaluator)
    state, spatial, second = [snapshot[name][0] for name in ["state", "state_space", "state_second"]]
    primitive = numerical.stack([state[0], state[1], spatial[0], state[2], state[3]])
    radial = numerical.stack([spatial[0], spatial[1], second[0], spatial[2], spatial[3]])
    data = primitive_data(primitive, radii, evaluator.constants, evaluator.kappa, evaluator.sigma)
    varied = primitive_data(primitive.astype(complex) + 1j * 1e-30 * radial, radii.astype(complex) + 1j * 1e-30, evaluator.constants, evaluator.kappa, evaluator.sigma)
    velocity, flux = explicit_gradients(varied)
    velocity_radial, flux_radial = velocity.imag / 1e-30, flux.imag / 1e-30
    zero_order = numerical.zeros_like(current["principal"])
    zero_order[0] = current["q_gradient"]
    zero_order[1] = velocity_radial
    zero_order[2] = flux_radial + 2 * current["flux_gradient"] / radii - current["V_gradient"] + current["f_mu"] * current["constraint_gradient"] - snapshot["initial_constraint"][0] * current["fmu_gradient"]
    zero_order[3] = current["C_gradient"]
    zero_order[4] = -current["D_gradient"] / evaluator.sigma
    return zero_order, current["principal"], current["independent_defect"], current, data, varied


def convert_initial(initial, radial, second, data, data_radial):
    momentum = data["alpha"] * initial[:, 1] - data["B"] * radial[:, 0] + data["h_mu"] * initial[:, 2] + data["h_delta"] * initial[:, 3]
    momentum_radial = data["alpha"] * radial[:, 1] - data["B"] * second[:, 0] + data["h_mu"] * radial[:, 2] + data["h_delta"] * radial[:, 3]
    momentum_radial += data_radial["alpha"] * initial[:, 1] - data_radial["B"] * radial[:, 0] + data_radial["h_mu"] * initial[:, 2] + data_radial["h_delta"] * initial[:, 3]
    values = numerical.stack([initial[:, 0], radial[:, 0], momentum, initial[:, 2], initial[:, 3]], axis=1)
    first = numerical.stack([radial[:, 0], second[:, 0], momentum_radial, radial[:, 2], radial[:, 3]], axis=1)
    return values, first


class CornerCompatibility:
    def __init__(self, evaluator, space_step=0.01, time_step=0.002, count=7):
        self.evaluator = evaluator
        self.space_step, self.time_step, self.count = space_step, time_step, count
        self.weights_first = numerical.array([float(value) for value in symbolic.finite_diff_weights(2, list(range(count)), 0)[1][-1]])
        self.weights_second = numerical.array([float(value) for value in symbolic.finite_diff_weights(2, list(range(count)), 0)[2][-1]])
        self.radii = numerical.stack([4 + space_step * numerical.arange(count), 8 - space_step * numerical.arange(count)])
        spatial_snapshot = evaluator.evaluate(numerical.zeros(2 * count), self.radii.ravel(), 0.1)
        self.spatial_operator = continuous_operator(spatial_snapshot, self.radii.ravel(), evaluator)
        self.times = time_step * numerical.arange(count)
        self.endpoints = numerical.array([4., 8.])
        time_snapshot = evaluator.evaluate(self.times[:, None], self.endpoints[None, :], 0.1)
        self.time_operator = continuous_operator(time_snapshot, self.endpoints[None, :], evaluator)

    def evaluate(self, initial_provider, forcing_weights):
        zero_order, principal, defect, current, data, varied_data = self.spatial_operator
        initial, radial, second = initial_provider(self.radii.ravel())
        data_radial = {key: value.imag / 1e-30 for key, value in varied_data.items()}
        initial_y, initial_y_radial = convert_initial(initial, radial, second, data, data_radial)
        first_time = numerical.einsum("ijn,bjn->bin", zero_order, initial_y) + numerical.einsum("ijn,bjn->bin", principal, initial_y_radial) - forcing_weights[:, None, None] * defect
        first_time = first_time.reshape((len(forcing_weights), 5, 2, self.count))
        first_time_radial = numerical.einsum("bicn,n->bic", first_time, self.weights_first) / self.space_step
        first_time_radial[:, :, 1] *= -1
        first_time_at_boundary = first_time[:, :, :, 0]
        initial_boundary = initial_y.reshape((len(forcing_weights), 5, 2, self.count))[:, :, :, 0]
        initial_radial_boundary = initial_y_radial.reshape((len(forcing_weights), 5, 2, self.count))[:, :, :, 0]
        time_zero, time_principal, time_defect, time_current, unused_data, unused_varied = self.time_operator
        fixed_data_rhs = numerical.einsum("ijtn,bjn->bitn", time_zero, initial_boundary) + numerical.einsum("ijtn,bjn->bitn", time_principal, initial_radial_boundary) - forcing_weights[:, None, None, None] * time_defect
        explicit_time = numerical.einsum("bitn,t->bin", fixed_data_rhs, self.weights_first) / self.time_step
        second_time = explicit_time + numerical.einsum("ijn,bjn->bin", time_zero[:, :, 0], first_time_at_boundary) + numerical.einsum("ijn,bjn->bin", time_principal[:, :, 0], first_time_radial)
        impedance = numerical.sqrt(time_current["P"] * time_current["Q"])
        slope = -(time_current["B"] + numerical.array([-1., 1.]) * impedance) / time_current["c"]
        boundary = -slope * time_current["q_gradient"]
        boundary[1] += 1
        boundary[4] += (slope - self.evaluator.sigma) * time_current["q0"]
        boundary_first = numerical.einsum("itn,t->in", boundary, self.weights_first) / self.time_step
        boundary_second = numerical.einsum("itn,t->in", boundary, self.weights_second) / self.time_step**2
        zeroth = numerical.einsum("in,bin->bn", boundary[:, 0], initial_boundary)
        first = numerical.einsum("in,bin->bn", boundary[:, 0], first_time_at_boundary) + numerical.einsum("in,bin->bn", boundary_first, initial_boundary)
        second = numerical.einsum("in,bin->bn", boundary[:, 0], second_time) + 2 * numerical.einsum("in,bin->bn", boundary_first, first_time_at_boundary) + numerical.einsum("in,bin->bn", boundary_second, initial_boundary)
        return numerical.stack([numerical.column_stack([zeroth, initial_boundary[:, 4, 1]]), numerical.column_stack([first, first_time_at_boundary[:, 4, 1]]), numerical.column_stack([second, second_time[:, 4, 1]])], axis=1)
