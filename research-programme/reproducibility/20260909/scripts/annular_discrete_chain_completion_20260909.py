import numpy as numerical
from scipy.linalg import solve_banded

from annular_discrete_constraint_transport_20260909 import explicit_mass_gradients
from annular_noether_source_projection_20260909 import transpose_band
from sbp4_derived_operator_20260909 import derivative


def chain_coefficients(snapshot, radii, evaluator):
    state, radial, second = [snapshot[name][0] for name in ["state", "state_space", "state_second"]]
    primitive = numerical.stack([state[0], state[1], radial[0], state[2], state[3]])
    direction = numerical.stack([radial[0], radial[1], second[0], radial[2], radial[3]])
    varied = explicit_mass_gradients(primitive.astype(complex) + 1j * 1e-30 * direction, radii.astype(complex) + 1j * 1e-30, evaluator)
    return {"mass_flux_radial": varied[1].imag / 1e-30, "velocity_radial": varied[2].imag / 1e-30, "weighted_flux_radial": 2 * radii * varied[3].real + radii**2 * varied[3].imag / 1e-30}


def bulk_commutator(current, values, spacing, radii):
    radial = derivative(values, spacing)
    defects = []
    for coefficient, coefficient_radial in [(current["C_gradient"], current["mass_flux_radial"]), (current["q_gradient"], current["velocity_radial"]), (radii**2 * current["flux_gradient"], current["weighted_flux_radial"])]:
        flux = numerical.einsum("in,in->n", coefficient, values)
        defects.append(derivative(flux, spacing) - numerical.einsum("in,in->n", coefficient, radial) - numerical.einsum("in,in->n", coefficient_radial, values))
    gradient = current["constraint_gradient"]
    return defects[0] - gradient[1] * defects[1] - gradient[2] * defects[2] / radii**2


def complete_with_target(sources, gradient, band, outer_derivative, scalar_energy_weight, target):
    anchored = band.copy()
    anchored[3] -= gradient[2]
    anchored[3, -1] = 1
    full_outer = outer_derivative.copy()
    full_outer[-1] -= gradient[2, -1]
    normal = solve_banded((3, 3), transpose_band(anchored), full_outer, check_finite=False)
    normal[-1] = -1
    normal /= numerical.max(numerical.abs(normal))
    covector = normal * gradient[1]
    covector[[0, -1]] = 0
    denominator = float(numerical.sum(covector**2 / scalar_energy_weight))
    forcing = gradient[1] * sources[1] + gradient[3] * sources[3] + target
    mismatch = float(numerical.dot(normal, forcing))
    completed = sources.copy()
    if denominator > 0:
        completed[1] -= mismatch * covector / (denominator * scalar_energy_weight)
    elif mismatch != 0:
        raise ValueError("No boundary-fixed scalar direction for the derived chain target")
    forcing = gradient[1] * completed[1] + gradient[3] * completed[3] + target
    forcing[-1] = 0
    completed[2] = solve_banded((3, 3), anchored, forcing, check_finite=False)
    return completed, {"denominator": denominator, "mismatch": mismatch, "projection_energy_norm": abs(mismatch) / numerical.sqrt(denominator) if denominator > 0 else 0.}
