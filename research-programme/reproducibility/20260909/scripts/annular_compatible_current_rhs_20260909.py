import numpy as numerical

from annular_compatible_current_restoring_20260909 import restoring_coordinate_source
from annular_volterra_source_completion_20260909 import complete_without_scalar_projection
from sbp4_derived_operator_20260909 import derivative


def compatible_current_rhs(current, state, radii, weights, spacing, sigma, include_forcing=True):
    velocity = numerical.sum(current["q_gradient"] * state, axis=0)
    flux = numerical.sum(current["flux_gradient"] * state, axis=0)
    constraint = derivative(state[3], spacing) - numerical.sum(current["constraint_gradient"] * state, axis=0)
    force = -current["f_mu"] * constraint - numerical.sum(current["fmu_gradient"] * state, axis=0) * current["J0"]
    bulk = numerical.stack([velocity, derivative(velocity, spacing), derivative(radii**2 * flux, spacing) / radii**2 - numerical.sum(current["V_gradient"] * state, axis=0) + force, numerical.sum(current["C_gradient"] * state, axis=0), (derivative(state[4], spacing) - numerical.sum(current["D_gradient"] * state, axis=0)) / sigma])
    if include_forcing:
        bulk -= current["defect"]
    fixed_velocity = velocity - current["q0"] * state[4]
    fixed_gradient = state[1] - sigma * current["q0"] * state[4]
    boundary_flux = current["B"] * fixed_velocity + current["c"] * fixed_gradient
    impedance = numerical.sqrt(current["P"] * current["Q"])
    raw = numerical.zeros((4, radii.size))
    for endpoint, orientation in [(0, 1), (-1, -1)]:
        raw[1, endpoint] = (orientation * boundary_flux[endpoint] - impedance[endpoint] * fixed_velocity[endpoint]) / (current["alpha"][endpoint] * weights[endpoint])
    raw[3, -1] = -state[4, -1] / (sigma * weights[-1])
    raw[1] += restoring_coordinate_source(state[0], radii, current, weights, spacing)
    complete, diagnostics = complete_without_scalar_projection(raw, current["old_gradient"], spacing)
    transformed = numerical.stack([complete[0], numerical.zeros_like(velocity), current["alpha"] * complete[1] + current["h_mu"] * complete[2] + current["h_delta"] * complete[3], complete[2], complete[3]])
    return bulk + transformed, transformed, complete, raw, diagnostics
