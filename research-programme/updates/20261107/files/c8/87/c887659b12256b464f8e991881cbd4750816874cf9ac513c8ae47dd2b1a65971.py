from thermal_wave_common import *
from thermal_wave_system import ThermalWaveSystem, CoupledSystem
import sympy as symbolic


def exact_identities():
    hubble, scale, wave = symbolic.symbols('H a k', nonzero=True)
    heat, reference, ratio, ratio_prime = symbolic.symbols('chi rho_star R R_prime', nonzero=True)
    density, temperature, velocity, trace_rate = symbolic.symbols('delta_b delta_r v S')
    source_energy, source_momentum = symbolic.symbols('C_E C_F')
    rest, inertia, inertia_prime = symbolic.symbols('rho_b B B_prime', nonzero=True)
    gradient = symbolic.I * wave
    divergence = gradient * velocity
    density_prime = -divergence - trace_rate
    background_heat = heat * (ratio_prime + hubble * ratio)
    temperature_prime = (-hubble * temperature - symbolic.Rational(2, 3) * ratio * (divergence + trace_rate)
                         - source_energy / heat - background_heat * density / heat)
    internal = heat * reference * ratio
    delta_internal = heat * reference * (ratio * density + temperature)
    delta_internal_prime = heat * reference * ((ratio_prime - 4 * hubble * ratio) * density
                                               + ratio * density_prime + temperature_prime - 4 * hubble * temperature)
    gas_pressure = symbolic.Rational(2, 3) * delta_internal
    velocity_prime = (-source_momentum - inertia_prime * velocity - gradient * gas_pressure / reference) / inertia
    gas_current_prime = reference * (inertia * velocity_prime + (inertia_prime - 4 * hubble * inertia) * velocity)
    identities = {
        'Gas internal-energy continuity including background heat dilution':
            delta_internal_prime + 5 * hubble * delta_internal + symbolic.Rational(5, 3) * internal * (divergence + trace_rate) + reference * source_energy,
        'Gas rest-mass continuity': rest * density_prime + rest * (divergence + trace_rate),
        'Gas momentum including evolving thermal enthalpy':
            gas_current_prime + 4 * hubble * reference * inertia * velocity + gradient * gas_pressure + reference * source_momentum,
    }
    photon_density, monopole, dipole, quadrupole = symbolic.symbols('rho_gamma E0 E1 E2')
    redshift_energy = 4 * photon_density / reference
    monopole_prime = source_energy - gradient * dipole / 3 - redshift_energy * trace_rate / 3
    dipole_prime = 3 * source_momentum - gradient * (monopole + symbolic.Rational(2, 5) * quadrupole)
    identities['Photon energy continuity with distorted background redshift'] = (
        reference * monopole_prime + gradient * reference * dipole / 3
        + symbolic.Rational(4, 3) * photon_density * trace_rate - reference * source_energy)
    identities['Photon momentum with anisotropic stress'] = (
        reference * dipole_prime / 3 + gradient * reference * (monopole / 3 + symbolic.Rational(2, 15) * quadrupole)
        - reference * source_momentum)
    field, prime, field_delta, prime_delta, mass2 = symbolic.symbols('phi pi delta_phi delta_pi m_squared')
    field_prime = prime
    prime_prime = -2 * hubble * prime - scale ** 2 * mass2 * field
    field_delta_prime = prime_delta
    prime_delta_prime = -2 * hubble * prime_delta - (wave ** 2 + scale ** 2 * mass2) * field_delta - trace_rate * prime
    scalar_density = prime * prime_delta / scale ** 2 + mass2 * field * field_delta
    scalar_pressure = prime * prime_delta / scale ** 2 - mass2 * field * field_delta
    scalar_current = -gradient * prime * field_delta / scale ** 2
    scalar_density_prime = ((prime_prime * prime_delta + prime * prime_delta_prime - 2 * hubble * prime * prime_delta) / scale ** 2
                            + mass2 * (field_prime * field_delta + field * field_delta_prime))
    scalar_current_prime = -gradient * (prime_prime * field_delta + prime * prime_delta - 2 * hubble * prime * field_delta) / scale ** 2
    identities['Retained canonical-field energy continuity'] = (
        scalar_density_prime + 3 * hubble * (scalar_density + scalar_pressure)
        + gradient * scalar_current + prime ** 2 * trace_rate / scale ** 2)
    identities['Retained canonical-field momentum continuity'] = (
        scalar_current_prime + 4 * hubble * scalar_current + gradient * scalar_pressure)
    total_density, total_pressure, delta_energy, current, stress_t, stress_l = symbolic.symbols('rho p delta_rho j S_T S_L')
    metric_t, rate_t, rate_l = symbolic.symbols('h_T sigma_T sigma_L')
    total_rate = 2 * rate_t + rate_l
    hubble_prime = hubble ** 2 - scale ** 2 * (total_density + total_pressure) / 2
    rate_t_prime = -4 * hubble * rate_t - hubble * rate_l - wave ** 2 * metric_t / 2 + scale ** 2 * (delta_energy - stress_l) / 2
    rate_l_prime = -2 * hubble * rate_t - 3 * hubble * rate_l - wave ** 2 * metric_t + scale ** 2 * (delta_energy + stress_l - 2 * stress_t) / 2
    delta_energy_prime = -3 * hubble * delta_energy - hubble * (2 * stress_t + stress_l) - gradient * current - (total_density + total_pressure) * total_rate
    current_prime = -4 * hubble * current - gradient * stress_l
    hamiltonian = 2 * wave ** 2 * metric_t + 4 * hubble * total_rate - 2 * scale ** 2 * delta_energy
    momentum = 2 * gradient * rate_t - scale ** 2 * current
    hamiltonian_prime = (4 * wave ** 2 * rate_t + 4 * hubble_prime * total_rate + 4 * hubble * (2 * rate_t_prime + rate_l_prime)
                        - 4 * hubble * scale ** 2 * delta_energy - 2 * scale ** 2 * delta_energy_prime)
    momentum_prime = 2 * gradient * rate_t_prime - 2 * hubble * scale ** 2 * current - scale ** 2 * current_prime
    identities['Hamiltonian propagation: C_H_prime = -4H C_H - 2ik C_M'] = hamiltonian_prime + 4 * hubble * hamiltonian + 2 * gradient * momentum
    identities['Momentum propagation: C_M_prime = -2H C_M - ik C_H/2'] = momentum_prime + 2 * hubble * momentum + gradient * hamiltonian / 2
    checks = [dict(name=name, passed=symbolic.expand(expression) == 0, residual=str(symbolic.expand(expression)))
              for name, expression in identities.items()]
    checks += [
        dict(name='Removing background heat dilution leaves nonzero Qbar delta_b',
             passed=symbolic.simplify(reference * background_heat * density) != 0),
        dict(name='Removing enthalpy derivative leaves nonzero rho_star B_prime v',
             passed=symbolic.simplify(reference * inertia_prime * velocity) != 0),
        dict(name='Removing gas pressure force leaves nonzero pressure gradient',
             passed=symbolic.simplify(gradient * gas_pressure) != 0),
    ]
    return checks


def cold_rhs_check(system, expansion):
    local = system.background(expansion)
    inherited = CoupledSystem(system.geometry.parent, system.maximum)
    moment = system.geometry.parent.time_at(local['scale'])
    state, _ = system.initial()
    random = np.random.default_rng(714)
    state[:11] += random.normal(size=11) * 1e-5
    for degree, names in enumerate(system.names):
        for name in names:
            state[system.mode_slice(degree, name)] = system.basis.temperature * random.normal() * 1e-5
    state[system.neutrino] = random.normal(size=system.maximum + 1) * 1e-5
    photon = np.zeros((inherited.count, 3, 3), complex)
    neutrino = np.zeros(inherited.count, complex)
    tensors_list = []
    for degree, names in enumerate(system.names):
        tensors, _ = prior.modal_tensors(inherited.directions, np.array([1., 0., 0.]), degree)
        tensors_list.append(tensors)
        for name, tensor in zip(names, tensors):
            coefficient = system.basis.energy @ state[system.mode_slice(degree, name)] / 4
            photon += 2 * coefficient * tensor
        neutrino += state[system.neutrino.start + degree] * special.eval_legendre(degree, inherited.directions[:, 0])
    packed = inherited.pack(np.diag([state[1], state[0], state[0]]), np.diag([state[3], state[2], state[2]]),
                            state[4:6], state[6:8], state[8], np.array([state[9], 0., 0.]), photon, neutrino)
    all_states = np.zeros((4, inherited.size), complex)
    all_states[0] = packed
    old = inherited.unpack((inherited.slow_rhs(moment, all_states) + inherited.collision_rhs(moment, all_states))[0])
    old_projected = np.zeros(system.size, complex)
    old_projected[:4] = [old['metric'][1, 1], old['metric'][0, 0], old['rate'][1, 1], old['rate'][0, 0]]
    old_projected[4:10] = np.r_[old['field'], old['prime'], old['number'], old['velocity'][0]]
    for degree, names in enumerate(system.names):
        coefficients = (2 * degree + 1) / 4 * np.einsum('n,anij,nji->a', inherited.weights, tensors_list[degree], old['photon'])
        for name, coefficient in zip(names, coefficients):
            old_projected[system.mode_slice(degree, name)] = coefficient * system.basis.temperature
        old_projected[system.neutrino.start + degree] = (2 * degree + 1) * np.dot(
            inherited.weights * special.eval_legendre(degree, inherited.directions[:, 0]), old['neutrino'])
    _, _, generator = system.matrices(expansion)
    new = generator @ state
    new[10] = 0.
    blocks = [slice(0, 4), slice(4, 8), slice(8, 10), slice(11, system.neutrino.start), system.neutrino]
    return {name: float(np.linalg.norm(new[section] - old_projected[section]) / max(np.linalg.norm(old_projected[section]), 1e-100))
            for name, section in zip(['metric', 'fields', 'gas', 'polarized_photons', 'neutrinos'], blocks)}


def main():
    modest()
    folder = ROOT / 'results/thermal-identities'
    assert not folder.exists()
    checks, rows, inputs = exact_identities(), [], []
    for model in ['heavy', 'cold']:
        system = ThermalWaveSystem(model, 16, 8, 'physical')
        basis = system.basis
        for name, actual, expected in [
            ('Thermal energy moment of x', basis.energy @ basis.temperature, 4.),
            ('Redshift energy is four times background energy', basis.energy @ system.mass_inverse @ system.redshift_weak, 4 * basis.energy),
            ('Redshift number is three times background number', basis.number @ system.mass_inverse @ system.redshift_weak, 3 * basis.number),
            ('Boosted heat dipole is the background energy source', basis.energy @ system.mass_inverse @ system.boost_weak / 3, basis.energy),
        ]:
            error = float(np.max(abs(actual - expected)) / max(1., float(np.max(abs(expected)))))
            checks.append(dict(name=model + ': ' + name, passed=error < 1e-9, value=error))
        for expansion in [0., .5 * system.geometry.thermal.end, system.geometry.thermal.end]:
            local = system.background(expansion)
            redshift, collision, boost = system.spectral_background(expansion, local)
            redshift_error = abs(basis.energy @ redshift - 4 * local['photon'] / local['photon_reference'])
            heat_error = abs(basis.energy @ collision - local['heat'] * local['hubble'] * local['photon_energy_prime'])
            boost_error = abs(basis.energy @ boost / 3 - basis.energy @ collision)
            source_scale = max(abs(basis.energy @ collision), 1e-100)
            checks.append(dict(name=model + ': conserved distorted-background moments at ' + str(expansion),
                               passed=redshift_error < 1e-12 and heat_error / source_scale < 1e-9 and boost_error / source_scale < 1e-9,
                               redshift=float(redshift_error), heat_relative=float(heat_error / source_scale),
                               boost_relative=float(boost_error / source_scale)))
        inputs.extend([system.geometry.source, system.geometry.parent.source, *system.ladder.inputs])
        cold_system = ThermalWaveSystem(model, 16, 8, 'dust')
        for expansion in [.2, 1., 2.]:
            errors = cold_rhs_check(cold_system, expansion)
            rows.append(dict(model=model, expansion=expansion, errors=errors))
            for sector, error in errors.items():
                checks.append(dict(name=model + ': independent Stage69 cold RHS ' + sector + ' at ' + str(expansion),
                                   passed=error < 1e-9, value=error))
    folder.mkdir(parents=True, exist_ok=False)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
                        exact_conservation_identity_count=9, negative_controls=3,
                        scope='Scalar linear perturbations of conserved expanding ideal-plasma/radiation/canonical-field stress; no constraint projection after initialization.'),
           __file__, [ROOT / 'thermal_wave_system.py', ROOT / 'background_geometry.py', ROOT / 'kernel_ladder.py',
                      WAVES / 'coupled_system.py', WAVES / 'initial_state.py', *sorted(set(inputs))])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    main()
