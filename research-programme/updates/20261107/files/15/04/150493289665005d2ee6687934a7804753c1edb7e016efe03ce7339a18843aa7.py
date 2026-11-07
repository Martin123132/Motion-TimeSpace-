from common import *
from metric_channels import derive
import numpy as np
import sympy as sp


def symbolic():
    wave, enthalpy, enthalpy_rate, defect, contraction = sp.symbols("k Wq WqN DeltaW dC", positive=True)
    denominator = 1 + 3 * enthalpy / (2 * wave**2)
    denominator_rate = 3 * enthalpy_rate / (2 * wave**2)
    phi_contraction = -(3 * enthalpy_rate + contraction - 3 * defect * (denominator - 1)) / (2 * wave**2 * denominator)
    actual_phi = -3 * defect / (2 * wave**2 * denominator) + phi_contraction / denominator + denominator_rate / denominator**2
    expected_phi = -(contraction + 3 * defect) / (2 * wave**2 * denominator**2)
    omega, field, velocity, full, hubble = sp.symbols("omega phi v Omega H", real=True, nonzero=True)
    density = sp.Matrix([[omega**2 * field / full, velocity]])
    commutator = sp.Matrix([3 * full * velocity / hubble, 3 * omega**2 * field / hubble])
    checks = dict(metric_derivative_cancellation=sp.simplify(actual_phi - expected_phi),
                  psi_coefficient=sp.simplify(1 - (denominator - 1) / denominator - 1 / denominator),
                  scalar_density_contraction=sp.simplify((density * commutator)[0] - 6 * omega**2 * field * velocity / hubble))
    require(all(value == 0 for value in checks.values()), "exact forcing cancellation")
    return {name: str(value) for name, value in checks.items()}


def explicit(system, energy, efold):
    derived = derive(system, energy, efold)
    point = system.context["point"](efold)
    hubble = derived["hubble"]
    wave = system.wave
    transform, inverse = derived["transform"], derived["inverse"]
    weights = np.diag(transform) / system.units[:energy.size]
    psi, phi = derived["psi_injection"], derived["phi_injection"]
    phi_rate = -phi.copy()
    hubble_rate = system.background_spline(efold, 1)[0]
    for native in (2, 3):
        slot = energy.slot(native)
        phi_rate[slot] = phi[slot] * (-.5 + hubble_rate / hubble)
    speeds = system.context["kinetic"](point[11])[1]
    for node in range(5):
        slot = energy.moment_slot(0, node)
        phi_rate[slot] = -(1 + speeds[node]**2) / 2 * phi[slot]
    commutator = np.zeros(energy.size)
    normalized = np.zeros(len(system.units))
    normalized[:energy.size] = inverse @ phi
    raw = system.decode(efold, normalized * system.units)
    observed = system.context["observe"](point[11], system.project(raw))
    baryon = energy.slot(4)
    commutator[baryon] = weights[baryon] * wave / hubble * observed[18]
    signature = system.context["signature_values"]
    commutator[energy.slot(int(signature[3]) + 1)] = psi[energy.slot(int(signature[3]) + 1)]
    massless_dipole = energy.slot(int(signature[4]) + 1)
    commutator[massless_dipole] = psi[massless_dipole]
    if signature[12]:
        commutator[massless_dipole] *= 3
        quad = energy.slot(int(signature[4]) + 2)
        require(point[11] > 0, "flat outgoing closure time")
        commutator[quad] = 12 * weights[quad] / (hubble * point[11])
    for node in range(5):
        slot = energy.moment_slot(1, node)
        commutator[slot] = speeds[node]**2 * psi[slot]
    contraction = 0.
    contraction_upper = 0.
    for scalar in derived["scalars"]:
        species, slots = scalar["species"], scalar["slots"]
        phi_rate[slots] = [0., 3 * point[2 * species + 6]]
        omega, frequency = scalar["omega"], scalar["full_frequency"]
        field, velocity = scalar["field"], scalar["velocity"]
        commutator[slots] = [3 * frequency * velocity / hubble, 3 * omega**2 * field / hubble]
        contraction += 6 * omega**2 * field * velocity / hubble
        contraction_upper += 3 * omega * scalar["stress_amplitude"]**2 / hubble
    density = energy.fluid_origin * (energy.origin_scale / point[10])**np.array([1., 1., 2., 2.])
    massive = np.array(energy.massive_origin) * (energy.origin_scale / point[10])**2 * energy.speeds_origin / speeds
    quadrature_rate = -density[0] - density[1] - 8 / 3 * (density[2] + density[3]) - 4 / 3 * np.sum((1 + speeds**2) * massive)
    for species in range(2 if system.model == "heavy" else 1):
        quadrature_rate += 2 * point[2 * species + 1] * point[2 * species + 6]
    denominator = derived["denominator"] / (2 * wave**2)
    denominator_rate = 3 * quadrature_rate / (2 * wave**2)
    primitive = phi / denominator
    primitive_rate = phi_rate / denominator - phi * denominator_rate / denominator**2
    shear = psi - 3 * derived["defect"] / (2 * wave**2 * denominator) * phi
    current = (psi + commutator) / denominator - phi * (contraction + 3 * derived["defect"]) / (2 * wave**2 * denominator**2)
    return dict(derived=derived, current=current, shear=shear, primitive=primitive,
                primitive_rate=primitive_rate, commutator=commutator, phi_rate=phi_rate,
                contraction=contraction, contraction_upper=contraction_upper)
