import numpy as numerical

from annular_coupled_current_operator_20260909 import primitive_data
from annular_current_corner_compatibility_20260909 import continuous_operator, explicit_gradients
from sbp4_derived_operator_20260909 import derivative


def explicit_mass_gradients(primitive, radii, evaluator):
    data = primitive_data(primitive, radii, evaluator.constants, evaluator.kappa, evaluator.sigma)
    velocity, flux = explicit_gradients(data)
    beta = evaluator.kappa * radii**2 * primitive[1] / data["E"]
    gradient = numerical.stack([evaluator.kappa * radii**2 * evaluator.constants["m_chi"]**2 * primitive[0], evaluator.kappa * radii**2 * data["flux"] / data["E"], beta, -data["D0"], -evaluator.sigma * data["C0"]])
    mass_flux = gradient[1] * velocity + beta * flux
    mass_flux[4] -= data["C0"]
    return gradient, mass_flux, velocity, flux, beta * data["f_mu"]


def transport_coefficients(snapshot, radii, evaluator):
    zero, principal, defect, current, data, unused = continuous_operator(snapshot, radii, evaluator)
    state, spatial, second, temporal = [snapshot[name][0] for name in ["state", "state_space", "state_second", "state_time"]]
    primitive = numerical.stack([state[0], state[1], spatial[0], state[2], state[3]])
    radial = numerical.stack([spatial[0], spatial[1], second[0], spatial[2], spatial[3]])
    time_direction = numerical.stack([temporal[0], temporal[1], spatial[1], temporal[2], temporal[3]])
    gradient, mass_flux, velocity, flux, rate = explicit_mass_gradients(primitive, radii, evaluator)
    radial_values = explicit_mass_gradients(primitive.astype(complex) + 1j * 1e-30 * radial, radii.astype(complex) + 1j * 1e-30, evaluator)
    time_values = explicit_mass_gradients(primitive.astype(complex) + 1j * 1e-30 * time_direction, radii, evaluator)
    gradient_time = time_values[0].imag / 1e-30
    mass_flux_radial = radial_values[1].imag / 1e-30
    velocity_radial = radial_values[2].imag / 1e-30
    weighted_flux_radial = 2 * radii * flux + radii**2 * radial_values[3].imag / 1e-30
    lower = mass_flux_radial - gradient_time - numerical.einsum("in,ijn->jn", gradient, zero) + rate * gradient
    inverse = numerical.zeros((5, 5, radii.size))
    inverse[0, 0] = 1
    inverse[1] = velocity
    inverse[2, 1] = 1
    inverse[3, 3] = 1
    inverse[4, 4] = 1
    rate_gradient = numerical.stack([explicit_mass_gradients(primitive.astype(complex) + 1j * 1e-30 * inverse[:, component], radii, evaluator)[4].imag / 1e-30 for component in range(5)])
    primitive_defect = numerical.einsum("ijn,jn->in", inverse, defect)
    hessian_defect = explicit_mass_gradients(primitive.astype(complex) + 1j * 1e-30 * primitive_defect, radii, evaluator)[0].imag / 1e-30
    expected_lower = current["J0"] * rate_gradient - hessian_defect
    return {"gradient": gradient, "gradient_time": gradient_time, "mass_flux": mass_flux, "mass_flux_radial": mass_flux_radial, "velocity": velocity, "velocity_radial": velocity_radial, "weighted_flux": radii**2 * flux, "weighted_flux_radial": weighted_flux_radial, "rate": rate, "lower": lower, "expected_lower": expected_lower, "current": current, "zero": zero, "principal": principal, "defect": defect}


def commutator_with_bound(coefficient, radial_coefficient, values, spacing, stencil=None):
    if stencil is None:
        stencil = derivative(numerical.eye(values.shape[-1]), spacing).T
    residual = derivative(coefficient * values, spacing) - coefficient * derivative(values, spacing) - radial_coefficient * values
    coefficient_error = derivative(coefficient, spacing) - radial_coefficient
    bound = numerical.abs(values * coefficient_error)
    reconstructed = values * coefficient_error
    for component in range(values.shape[0]):
        increments = (coefficient[component, None, :] - coefficient[component, :, None]) * (values[component, None, :] - values[component, :, None])
        reconstructed[component] += numerical.sum(stencil * increments, axis=1)
        bound[component] += numerical.sum(numerical.abs(stencil * increments), axis=1)
    return residual.sum(axis=0), bound.sum(axis=0), reconstructed.sum(axis=0)


def transport_terms(coefficients, values, source, spacing, radii):
    gradient = coefficients["gradient"]
    stencil = derivative(numerical.eye(radii.size), spacing).T
    mass = commutator_with_bound(coefficients["mass_flux"], coefficients["mass_flux_radial"], values, spacing, stencil)
    velocity = commutator_with_bound(coefficients["velocity"], coefficients["velocity_radial"], values, spacing, stencil)
    flux = commutator_with_bound(coefficients["weighted_flux"], coefficients["weighted_flux_radial"], values, spacing, stencil)
    channels = numerical.stack([mass[0], -gradient[1] * velocity[0], -gradient[2] * flux[0] / radii**2])
    bound = mass[1] + numerical.abs(gradient[1]) * velocity[1] + numerical.abs(gradient[2]) * flux[1] / radii**2
    source_residual = derivative(source[3], spacing) - numerical.einsum("in,in->n", gradient, source)
    defect_source = -derivative(coefficients["defect"][3], spacing) + numerical.einsum("in,in->n", gradient, coefficients["defect"])
    perturbation_constraint = derivative(values[3], spacing) - numerical.einsum("in,in->n", gradient, values)
    lower = numerical.einsum("in,in->n", coefficients["lower"], values)
    return {"commutator_channels": channels, "commutator": channels.sum(axis=0), "commutator_bound": bound, "source_residual": source_residual, "defect_source": defect_source, "perturbation_constraint": perturbation_constraint, "lower_term": lower, "rate_term": coefficients["rate"] * perturbation_constraint, "rhs": coefficients["rate"] * perturbation_constraint + lower + defect_source + channels.sum(axis=0) + source_residual, "commutator_reconstruction_error": numerical.array([numerical.max(numerical.abs(entry[0] - entry[2])) for entry in [mass, velocity, flux]])}
