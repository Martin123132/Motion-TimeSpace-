from common import *
import numpy as np
import sympy as sp


def symbolic():
    hubble, hubble_prime, omega, field, velocity, potential = sp.symbols("H Hp omega phi v Psi", real=True)
    velocity_prime = -2 * hubble * velocity - omega**2 * field
    velocity_second = -2 * hubble_prime * velocity - 2 * hubble * velocity_prime - 2 * hubble * omega**2 * field - omega**2 * velocity
    alpha_coefficient = hubble * velocity_prime - 2 * hubble**2 * velocity + omega**2 * velocity + velocity_second + 2 * hubble_prime * velocity + hubble * omega**2 * field
    wave, full = sp.symbols("k Omega", positive=True)
    density_first = omega**2 * field / full
    density_first_rate = (2 - omega**2 / full**2) * density_first + omega**2 * velocity / (hubble * full)
    scalar_free = sp.Matrix([[omega**2 / full**2, full / hubble], [-full / hubble, -2]])
    density = sp.Matrix([[density_first, velocity]])
    density_rate = sp.Matrix([[density_first_rate, velocity_prime / hubble]])
    expected = sp.Matrix([[2 * density_first - wave**2 * velocity / (hubble * full), -4 * velocity]])
    free_residual = (density_rate + density * scalar_free - expected).applyfunc(lambda value: sp.factor(value.subs(wave**2, full**2 - omega**2)))
    injection_psi = sp.Matrix([full * velocity / hubble, -omega**2 * field / hubble])
    injection_phi = sp.Matrix([0, 3 * velocity])
    total, defect, source, metric_rate = sp.symbols("Wq DeltaW L0 PhiN", real=True)
    denominator = 2 * wave**2 + 3 * total
    phi_rate = -(source - 3 * defect * potential / (2 * wave**2)) / denominator
    checks = dict(normal_scalar_alpha=sp.factor(alpha_coefficient),
                  normal_scalar_psi=sp.factor(velocity_prime + 2 * hubble * velocity + omega**2 * field),
                  free_density=free_residual,
                  scalar_density_psi=sp.simplify((density * injection_psi)[0]),
                  scalar_density_phi=sp.simplify((density * injection_phi)[0] - 3 * velocity**2),
                  implicit_metric=sp.simplify(denominator * phi_rate + source - 3 * defect * potential / (2 * wave**2)))
    require(all(value == sp.zeros(*value.shape) if isinstance(value, sp.MatrixBase) else value == 0 for value in checks.values()), "symbolic channel derivation")
    return {name: str(value) for name, value in checks.items()}


def derive(system, energy, efold):
    point = system.context["point"](efold)
    scale, hubble = point[10], point[12]
    wave = system.wave
    transform, inverse, derivative, _ = energy.blocks(efold)
    weights = np.diag(transform) / system.units[:energy.size]
    density = energy.fluid_origin * (energy.origin_scale / scale)**np.array([1., 1., 2., 2.])
    speeds = system.context["kinetic"](point[11])[1]
    massive = np.array(energy.massive_origin) * (energy.origin_scale / scale)**2 * energy.speeds_origin / speeds
    observed = system.context["observe"](point[11], system.zero_native)
    enthalpy = float(observed[0] + observed[1])
    hubble_rate, gravity_rate = system.background_spline(efold, 1)
    gravity = 3 * hubble * enthalpy / (2 * wave**2)
    enthalpy_rate = 2 * wave**2 / (3 * hubble) * (gravity_rate - gravity * hubble_rate / hubble)
    quadrature = density[0] + density[1] + 4 / 3 * (density[2] + density[3] + np.sum(massive))
    quadrature_rate = -density[0] - density[1] - 8 / 3 * (density[2] + density[3]) - 4 / 3 * np.sum((1 + speeds**2) * massive)
    for species in range(2 if system.model == "heavy" else 1):
        quadrature += point[2 * species + 1]**2
        quadrature_rate += 2 * point[2 * species + 1] * point[2 * species + 6]
    defect, defect_rate = quadrature - enthalpy, quadrature_rate - enthalpy_rate
    size = energy.size
    density_row, density_row_rate, free_density, current, shear = (np.zeros(size) for count in range(5))
    psi_injection, phi_injection = np.zeros(size), np.zeros(size)
    alpha = system.alpha_slot
    alpha_weight = weights[alpha]
    psi_injection[alpha] = alpha_weight / hubble
    density_row[alpha] = 3 * hubble * defect / alpha_weight
    density_row_rate[alpha] = 3 * (hubble_rate * defect + hubble * defect_rate + .5 * hubble * defect) / alpha_weight
    free_density[alpha] = (-density[0] * wave**2 / hubble + 3 * (hubble_rate * defect + hubble * defect_rate - hubble * defect)) / alpha_weight
    current[alpha] = (density[0] - defect) * wave / alpha_weight
    for native, fluid in ((2, 0), (3, 1)):
        slot = energy.slot(native)
        density_row[slot] = density[fluid] / weights[slot]
        density_row_rate[slot] = density_row[slot] * (-.5 - hubble_rate / hubble)
        free_density[slot] = -density_row[slot]
        phi_injection[slot] = 3 * weights[slot]
    baryon = energy.slot(4)
    free_density[baryon] = -wave * density[1] / (hubble * weights[baryon])
    current[baryon] = density[1] / weights[baryon]
    psi_injection[baryon] = weights[baryon] * wave / hubble
    signature = system.context["signature_values"]
    for species, beginning in ((2, int(signature[3])), (3, int(signature[4]))):
        monopole, dipole, quadrupole = [energy.slot(beginning + degree) for degree in range(3)]
        density_row[monopole] = density[species] / weights[monopole]
        density_row_rate[monopole] = -density_row[monopole]
        free_density[monopole] = -2 * density_row[monopole]
        free_density[dipole] = -wave * density[species] / (hubble * weights[dipole])
        current[dipole] = density[species] / weights[dipole]
        shear[quadrupole] = density[species] / weights[quadrupole]
        phi_injection[monopole] = 4 * weights[monopole]
        psi_injection[dipole] = 4 * wave * weights[dipole] / (3 * hubble)
        if species == 3 and signature[12]:
            phi_injection[quadrupole] = -4 * weights[quadrupole]
            psi_injection[quadrupole] = -4 * weights[quadrupole]
    for node in range(5):
        monopole, dipole, quadrupole = [energy.moment_slot(degree, node) for degree in range(3)]
        density_row[monopole] = massive[node] / weights[monopole]
        density_row_rate[monopole] = -(1 + speeds[node]**2) / 2 * density_row[monopole]
        free_density[monopole] = -(1 + speeds[node]**2) * density_row[monopole]
        free_density[dipole] = -wave * massive[node] * speeds[node] / (hubble * weights[dipole])
        current[dipole] = massive[node] * speeds[node] / weights[dipole]
        shear[quadrupole] = massive[node] * speeds[node]**2 / weights[quadrupole]
        phi_injection[monopole] = 4 * weights[monopole]
        psi_injection[dipole] = 4 * wave * weights[dipole] / (3 * hubble * speeds[node])
    scalars = []
    for species in range(2 if system.model == "heavy" else 1):
        slots = np.array([int(np.flatnonzero(system.core == value)[0]) for value in system.owner.scalar_positions[2 * species:2 * species + 2]])
        omega = scale * system.background["masses"][species]
        full_frequency = np.sqrt(wave**2 + omega**2)
        field = system.background["initial_fields"][species] + point[2 * species]
        velocity = point[2 * species + 1]
        velocity_rate = point[2 * species + 6]
        density_row[slots] = [omega**2 * field / full_frequency, velocity]
        density_row_rate[slots] = [(2 - omega**2 / full_frequency**2) * density_row[slots[0]] + omega**2 * velocity / (hubble * full_frequency), velocity_rate]
        free_density[slots] = [2 * density_row[slots[0]] - wave**2 * velocity / (hubble * full_frequency), -4 * velocity]
        current[slots[0]] = wave * velocity / full_frequency
        psi_injection[slots] = [full_frequency * velocity / hubble, -omega**2 * field / hubble]
        phi_injection[slots] = [0., 3 * velocity]
        internal = np.array([[omega**2 / full_frequency**2, full_frequency / hubble], [-full_frequency / hubble, -2.]])
        scalars.append(dict(species=species, slots=slots, internal=internal, omega=omega,
                            full_frequency=full_frequency, velocity=velocity, field=field,
                            stress_amplitude=np.sqrt(velocity**2 + omega**2 * field**2)))
    denominator = 2 * wave**2 + 3 * quadrature
    require(denominator > 0, "positive solved metric denominator")
    psi_row = -density_row / (2 * wave**2)
    phi_row = -(free_density + 3 * defect * psi_row) / denominator
    return dict(density=density_row, density_rate=density_row_rate, free_density=free_density,
                current=current, shear=shear, psi_injection=psi_injection, phi_injection=phi_injection,
                psi=psi_row, phi_rate=phi_row, quadrature=quadrature, defect=defect, defect_rate=defect_rate,
                hubble=hubble, denominator=denominator, scalars=scalars,
                transform=transform, inverse=inverse, derivative=derivative)
