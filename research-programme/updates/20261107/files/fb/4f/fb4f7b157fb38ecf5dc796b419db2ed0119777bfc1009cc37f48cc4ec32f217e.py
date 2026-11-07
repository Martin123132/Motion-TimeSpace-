from source231 import *


def symbolic(checks):
    hubble, reference, heat, ratio, energy, capacity, capacity_R, rest, transfer = sp.symbols('H rho_star chi R A C C_R rest Q', nonzero=True)
    density, temperature, velocity, spatial_trace, wave, source_energy, source_current, defect = sp.symbols('b r v S k CE CF f_R')
    gradient = sp.I * wave
    ratio_prime = hubble * ratio - (2 * hubble * ratio + transfer / heat) / capacity
    observed_prime = ratio_prime + defect
    energy_prime = hubble * (energy - ratio * capacity) + capacity * observed_prime
    capacity_prime = capacity_R * (observed_prime - hubble * ratio)
    physical_capacity_prime = capacity_R * (ratio_prime - hubble * ratio)
    inertia = rest + heat * (energy + 2 * ratio / 3)
    inertia_prime = hubble * rest + heat * (energy_prime + sp.Rational(2, 3) * observed_prime)
    physical_inertia_prime = inertia_prime.subs(defect, 0)
    compression = gradient * velocity + spatial_trace
    density_prime = -compression
    temperature_prime = ((hubble - 2 * hubble / capacity - physical_capacity_prime / capacity) * temperature
        - 2 * ratio * compression / (3 * capacity) - (source_energy - transfer * density) / (heat * capacity))
    pressure = 2 * heat * (ratio * density + temperature) / 3
    velocity_prime = (-source_current - physical_inertia_prime * velocity - gradient * pressure) / inertia
    density_gas = (rest + heat * energy) * density + heat * capacity * temperature
    density_gas_prime = (rest * (density_prime - 3 * hubble * density)
        + heat * ((energy_prime - 4 * hubble * energy) * density + energy * density_prime
        + (capacity_prime - 4 * hubble * capacity) * temperature + capacity * temperature_prime))
    current_prime = inertia * velocity_prime + (inertia_prime - 4 * hubble * inertia) * velocity
    energy_residual = density_gas_prime + 3 * hubble * (density_gas + pressure) + inertia * compression + source_energy
    current_residual = current_prime + 4 * hubble * inertia * velocity + gradient * pressure + source_current
    identities = dict(
        gas_off_shell_energy=energy_residual - heat * defect * (capacity * density + capacity_R * temperature),
        gas_off_shell_momentum=current_residual - heat * (capacity + sp.Rational(2, 3)) * defect * velocity,
        gas_on_shell_energy=energy_residual.subs(defect, 0),
        gas_on_shell_momentum=current_residual.subs(defect, 0),
        NR_temperature=temperature_prime.subs({capacity: 1, capacity_R: 0}) + hubble * temperature + 2 * ratio * compression / 3 + (source_energy - transfer * density) / heat)
    adiabatic_temperature = 2 * ratio * density / (3 * capacity)
    sound_squared = 2 * heat * ratio * (1 + 2 / (3 * capacity)) / (3 * inertia)
    identities['isentropic_density_variation'] = density_gas.subs(temperature, adiabatic_temperature) - inertia * density
    identities['isentropic_pressure_characteristic'] = pressure.subs(temperature, adiabatic_temperature) - sound_squared * inertia * density
    frequency = sp.symbols('omega')
    acoustic = sp.Matrix([[-sp.I * frequency, 0, gradient], [0, -sp.I * frequency, 2 * ratio * gradient / (3 * capacity)],
        [gradient * 2 * heat * ratio / (3 * inertia), gradient * 2 * heat / (3 * inertia), -sp.I * frequency]])
    identities['entropy_and_acoustic_characteristic_polynomial'] = acoustic.det() - sp.I * frequency * (frequency**2 - wave**2 * sound_squared)
    scale, background_density, background_pressure, delta_density, current, stress_t, stress_l = sp.symbols('a rho p drho j ST SL')
    metric_t, rate_t, rate_l, ray_defect, energy_defect, momentum_defect = sp.symbols('hT sigT sigL RH E_def M_def')
    trace = 2 * rate_t + rate_l
    hubble_prime = hubble**2 - scale**2 * (background_density + background_pressure) / 2 + ray_defect
    transverse_prime = -4 * hubble * rate_t - hubble * rate_l - wave**2 * metric_t / 2 + scale**2 * (delta_density - stress_l) / 2
    longitudinal_prime = -2 * hubble * rate_t - 3 * hubble * rate_l - wave**2 * metric_t + scale**2 * (delta_density + stress_l - 2 * stress_t) / 2
    density_prime = -3 * hubble * delta_density - hubble * (2 * stress_t + stress_l) - gradient * current - (background_density + background_pressure) * trace + energy_defect
    current_prime = -4 * hubble * current - gradient * stress_l + momentum_defect
    hamiltonian = 2 * wave**2 * metric_t + 4 * hubble * trace - 2 * scale**2 * delta_density
    momentum = 2 * gradient * rate_t - scale**2 * current
    hamiltonian_prime = (4 * wave**2 * rate_t + 4 * hubble_prime * trace + 4 * hubble * (2 * transverse_prime + longitudinal_prime)
        - 4 * hubble * scale**2 * delta_density - 2 * scale**2 * density_prime)
    momentum_prime = 2 * gradient * transverse_prime - 2 * hubble * scale**2 * current - scale**2 * current_prime
    identities['forced_Hamiltonian_constraint'] = hamiltonian_prime + 4 * hubble * hamiltonian + 2 * gradient * momentum - 4 * trace * ray_defect + 2 * scale**2 * energy_defect
    identities['forced_momentum_constraint'] = momentum_prime + 2 * hubble * momentum + gradient * hamiltonian / 2 + scale**2 * momentum_defect
    phi, prime, delta_phi, delta_prime, mass2, defect_phi, defect_prime = sp.symbols('phi pi dphi dpi m2 fphi fpi')
    prime_rate = -2 * hubble * prime - scale**2 * mass2 * phi + defect_prime
    perturbation_rate = -2 * hubble * delta_prime - (wave**2 + scale**2 * mass2) * delta_phi - trace * prime
    scalar_density = prime * delta_prime / scale**2 + mass2 * phi * delta_phi
    scalar_pressure = prime * delta_prime / scale**2 - mass2 * phi * delta_phi
    scalar_current = -gradient * prime * delta_phi / scale**2
    scalar_density_prime = (prime_rate * delta_prime + prime * perturbation_rate - 2 * hubble * prime * delta_prime) / scale**2 + mass2 * ((prime + defect_phi) * delta_phi + phi * delta_prime)
    scalar_current_prime = -gradient * (prime_rate * delta_phi + prime * delta_prime - 2 * hubble * prime * delta_phi) / scale**2
    identities['canonical_field_off_shell_energy'] = scalar_density_prime + 3 * hubble * (scalar_density + scalar_pressure) + gradient * scalar_current + prime**2 * trace / scale**2 - defect_prime * delta_prime / scale**2 - mass2 * defect_phi * delta_phi
    identities['canonical_field_off_shell_momentum'] = scalar_current_prime + 4 * hubble * scalar_current + gradient * scalar_pressure + gradient * defect_prime * delta_phi / scale**2
    for name, expression in identities.items():
        residual = sp.factor(expression)
        check(checks, name, int(residual != 0), 0)
    controls = dict(missing_background_heat_dilution=transfer * density,
        missing_enthalpy_derivative=physical_inertia_prime * velocity,
        wrong_NR_pressure=2 * heat * ((energy - ratio) * density + (capacity - 1) * temperature) / 3,
        missing_background_forcing=4 * trace * ray_defect - 2 * scale**2 * energy_defect)
    for name, residual in controls.items():
        check(checks, 'detect_' + name, int(sp.simplify(residual) == 0), 0)
    return dict(exact_identities=len(identities), negative_controls=len(controls))


def high_precision_checks(system, checks):
    mp.mp.dps = 80
    electron_fraction = mp.mpf(float(system.mixture.fractions[0]))
    results = []
    for index in (0, system.count // 2, system.count):
        theta = mp.mpf(float(system.theta[index]))
        ratio = mp.mpf(1) - mp.mpf('1.1e-9')
        def exact_A(argument):
            temperature = theta * argument
            heat = mp.besselk(1, 1 / temperature) / mp.besselk(2, 1 / temperature) + 3 * temperature - 1
            return (1 - electron_fraction) * argument + mp.mpf(2) / 3 * electron_fraction * heat / theta
        exact_C = mp.diff(exact_A, ratio)
        exact_CR = mp.diff(exact_A, ratio, 2)
        computed = eos_at(system.mixture, float(theta), float(ratio))
        for name, actual, expected in [('A', computed['A'], exact_A(ratio)), ('C', computed['C'], exact_C), ('C_R', computed['C_R'], exact_CR)]:
            check(checks, f'{system.model}:{index}: independent Bessel {name}', float(mp.mpf(actual) / expected - 1), 1e-10)
        local_background = system.background.at(float(system.coordinates[index]))
        hubble = mp.mpf(float(local_background['hubble']))
        heat = mp.mpf(system.heat)
        photon = system.background.parent.photons / (system.background.start_scale * math.exp(float(system.coordinates[index])))**4
        scale = system.background.start_scale * math.exp(float(system.coordinates[index]))
        rest = mp.mpf(float(system.background.parent.baryons / scale**3 / photon))
        transfer = -mp.mpf('.37') * heat * hubble
        local = gas_coefficients(float(hubble), float(rest), float(heat), float(ratio), computed, float(transfer))
        density, temperature, velocity, compression, exchange = [mp.mpf(value) for value in ('.3', '-.2', '.4', '.7', '.13')]
        def primitive(amplitude):
            local_ratio = ratio + amplitude * temperature
            local_capacity = mp.diff(exact_A, local_ratio)
            return hubble * local_ratio - (mp.mpf(2) / 3 * local_ratio * (3 * hubble + amplitude * compression * hubble)
                + (transfer + amplitude * exchange * heat * hubble) / (heat * (1 + amplitude * density))) / local_capacity
        predicted = (mp.mpf(local['temperature_self']) * temperature - 2 * ratio * compression * hubble / (3 * mp.mpf(local['C']))
            - (exchange * heat * hubble - transfer * density) / (heat * mp.mpf(local['C'])))
        check(checks, f'{system.model}:{index}: derivative of nonlinear gas first law', float((predicted - mp.diff(primitive, 0)) / hubble), 1e-10)
        def density_stress(amplitude):
            return (1 + amplitude * density) * (rest + heat * exact_A(ratio + amplitude * temperature))
        def pressure_stress(amplitude):
            return mp.mpf(2) / 3 * heat * (1 + amplitude * density) * (ratio + amplitude * temperature)
        def current_stress(amplitude):
            shifted_ratio = ratio + amplitude * temperature
            enthalpy = (1 + amplitude * density) * (rest + heat * (exact_A(shifted_ratio) + 2 * shifted_ratio / 3))
            speed = amplitude * velocity
            return enthalpy * speed / (1 - speed**2)
        expected_density = (rest + heat * mp.mpf(computed['A'])) * density + heat * mp.mpf(computed['C']) * temperature
        check(checks, f'{system.model}:{index}: independent kinetic density variation', float((expected_density - mp.diff(density_stress, 0)) / heat), 1e-10)
        check(checks, f'{system.model}:{index}: independent ideal pressure variation', float((2 * heat * (ratio * density + temperature) / 3 - mp.diff(pressure_stress, 0)) / heat), 1e-10)
        check(checks, f'{system.model}:{index}: boosted kinetic enthalpy current', float((mp.mpf(local['B']) * velocity - mp.diff(current_stress, 0)) / rest), 1e-10)
        omitted = exact_A(ratio) - exact_A(1) - mp.diff(exact_A, 1) * (ratio - 1)
        excess = exact_A(1) - 1
        check(checks, f'{system.model}:{index}: omitted quadratic heat versus EOS excess', float(omitted / excess), 1e-10)
        results.append(dict(index=index, quadratic_heat=str(omitted), relative_to_EOS_excess=str(omitted / excess)))
    return results


def local_probe(system, saved, index, kind, checks):
    rows = saved['rows']
    coordinate = float(rows[index, 0])
    scale = system.background.start_scale * math.exp(coordinate)
    photon = system.background.parent.photons / scale**4
    rest = system.background.parent.baryons / scale**3 / photon
    total = 0 if kind == 'NR' else 1
    profiles = saved['profiles'][index, :, 0] + total * saved['profiles'][index, :, 1]
    gas = rows[index, 3] + total * rows[index, 4]
    ratio = 1 + system.heat * gas
    hubble = rows[index, 12] * (1 + rows[index, 13]) * (1 + total * rows[index, 14])
    eos = eos_at(system.mixture, system.theta[index], ratio, kind)
    capacity_ratio = eos['C']
    opacity = system.background.parent.opacity_constant / scale**2
    raw = system.ladder.at(system.theta[index], 0) - system.emission.at(system.theta[index], 'dcbr')
    effective = np.triu(raw) + np.triu(raw, 1).T
    thermal_column = raw @ system.basis.temperature
    factor = linalg.cho_factor(system.effective_mass, lower=False)
    kinetic = opacity * linalg.cho_solve(factor, effective)
    thermal = -opacity * linalg.cho_solve(factor, thermal_column)
    background_collision = system.heat * opacity * linalg.cho_solve(factor, effective @ profiles - thermal_column * gas)
    transfer = float(system.basis.energy @ background_collision)
    local = gas_coefficients(float(hubble), float(rest), system.heat, ratio, eos, transfer)
    size = 6 + system.basis.count
    unit = np.eye(size, dtype=complex)
    density_row, temperature_row, velocity_row, trace_row, extra_energy, extra_momentum = unit[:6]
    compression = trace_row + .1j * velocity_row
    energy_row = extra_energy.copy()
    energy_row[6:] = system.basis.energy @ kinetic
    energy_row[1] += system.basis.energy @ thermal
    momentum_row = extra_momentum.copy()
    sources = source_rows(local, density_row, compression, temperature_row, velocity_row, energy_row, momentum_row, .1)
    derivative = [-compression, sources['temperature'], sources['velocity']]
    density, density_prime, current_prime = stress_chain_derivatives(local,
        [density_row, temperature_row, velocity_row], derivative, local['R_prime'])
    energy_terms = np.array([density_prime, 3 * hubble * (density + sources['pressure']), local['B'] * compression, energy_row])
    momentum_terms = np.array([current_prime, 4 * hubble * sources['current'], .1j * sources['pressure'], momentum_row])
    label = f'{system.model}:{system.count}:{index}:{kind}'
    check(checks, label + ': full gas energy row including opposite bank transfer', np.max(abs(energy_terms.sum(axis=0)) / np.maximum(np.sum(abs(energy_terms), axis=0), 1e-300)), 1e-9)
    check(checks, label + ': full gas momentum row including opposite transfer', np.max(abs(momentum_terms.sum(axis=0)) / np.maximum(np.sum(abs(momentum_terms), axis=0), 1e-300)), 1e-9)
    check(checks, label + ': positive subluminal adiabatic gas characteristic', int(not 0 < local['sound_squared'] < 1), 0)
    mp.mp.dps = 80
    exact_local = {name: mp.mpf(value) for name, value in local.items()}
    defect = mp.mpf(hubble) * mp.mpf('.003')
    variations = [mp.mpf('.7'), mp.mpf('-.3'), mp.mpf('.4')]
    rates = [mp.mpf('-.2'), mp.mpf('1e8'), mp.mpf('-.6')]
    _, base_energy, base_current = stress_chain_derivatives(exact_local, variations, rates, exact_local['R_prime'])
    _, changed_energy, changed_current = stress_chain_derivatives(exact_local, variations, rates, exact_local['R_prime'] + defect)
    expected_energy, expected_momentum = defect_sources(exact_local, defect, *variations)
    check(checks, label + ': injected background energy defect coefficient at80digits', float((changed_energy - base_energy) / expected_energy - 1), 1e-10)
    check(checks, label + ': injected background momentum defect coefficient at80digits', float((changed_current - base_current) / expected_momentum - 1), 1e-10)
    diagnostic = dict(model=system.model, count=system.count, index=index, kind=kind, theta=float(system.theta[index]),
        C=eos['C'], C_R=eos['C_R'], sound_squared=local['sound_squared'], inertia=local['B'],
        photon_transfer_over_chiH=transfer / (system.heat * hubble), ratio_prime_over_H=local['R_prime'] / hubble)
    if index >= 2:
        stencil = (1.5 * saved['profiles'][index] - 2 * saved['profiles'][index - 1] + .5 * saved['profiles'][index - 2]) / system.step
        spectrum_s = stencil[:, 0] + total * stencil[:, 1]
        energy_s = float(system.basis.energy @ spectrum_s)
        gas_s = float((1.5 * rows[index, 3] - 2 * rows[index - 1, 3] + .5 * rows[index - 2, 3]
                      + total * (1.5 * rows[index, 4] - 2 * rows[index - 1, 4] + .5 * rows[index - 2, 4])) / system.step)
        realized_transfer = system.heat * hubble * energy_s
        ratio_s = system.heat * gas_s
        realized_local = gas_coefficients(float(hubble), float(rest), system.heat, ratio, eos, realized_transfer)
        diagnostic.update(represented_vs_discrete_transfer_relative=(transfer - realized_transfer) / max(abs(realized_transfer), 1e-300),
            gas_background_defect_over_H=ratio_s - local['R_prime'] / hubble,
            gas_discrete_background_defect_over_H=ratio_s - realized_local['R_prime'] / hubble,
            eos_representation_delta_C=eos['C'] - (1. if kind == 'NR' else float(saved['C0'][index])))
    return diagnostic


def main():
    modest()
    config = protocol()
    assert not (ROOT / 'results/local-source.json').exists()
    inputs = read(ROOT / 'inputs.json')
    checks, records, precision = [], [], []
    exact = symbolic(checks)
    for model in config['models']:
        for count in config['counts']:
            system = prior.System(model, count, inputs)
            with np.load(register(inputs, PREVIOUS / f'runs/{model}-{count}/history.npz')) as archive:
                saved = dict(archive)
            if count == 6400:
                precision.extend(high_precision_checks(system, checks))
            for index in range(0, count + 1, count // config['sample_divisions']):
                for kind in ('NR', 'EOS'):
                    records.append(local_probe(system, saved, index, kind, checks))
            print(json.dumps(dict(model=model, count=count, completed=True, checks=len(checks), failed=sum(not row['passed'] for row in checks))), flush=True)
    refinements = []
    for model in config['models']:
        selected = {(row['count'], row['index'] / row['count'], row['kind']): row for row in records if row['model'] == model}
        for fraction in np.linspace(0, 1, config['sample_divisions'] + 1):
            for name in ('sound_squared', 'inertia', 'C'):
                coarse = selected[(3200, fraction, 'EOS')][name] - selected[(3200, fraction, 'NR')][name]
                fine = selected[(6400, fraction, 'EOS')][name] - selected[(6400, fraction, 'NR')][name]
                error = abs(coarse - fine) / max(abs(fine), 1e-300)
                check(checks, f'{model}:{fraction}: EOS-minus-NR {name} refinement', error, .01)
                refinements.append(dict(model=model, fraction=fraction, quantity=name, relative_change=error))
    add_modules(inputs)
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'), str(path), 'exec')
    since = datetime.fromisoformat(START).timestamp()
    protected = BRANCH.parent.parent / 'formalization-workbench'
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    check(checks, 'Protected workbench recent-mtime guard', len(changed), 0)
    check(checks, 'No local bytecode', len(list(ROOT.rglob('__pycache__'))), 0)
    write(ROOT / 'results/inputs-complete.json', inputs)
    report = dict(stage=231, state='complete', finished_at=now(), qualified=all(row['passed'] for row in checks),
        exact=exact, checks=checks, failed=[row for row in checks if not row['passed']],
        records=records, precision=precision, refinements=refinements, inputs_rehashed=len(inputs),
        protected_recent_mtime_count=len(changed),
        scope='Derived EOS local source and forced constraint identities; saved-bank interface and coefficient tests, not a closed angular transport evolution')
    write(ROOT / 'results/local-source.json', report)
    print(json.dumps(dict(checks=len(checks), failed=report['failed'], inputs=len(inputs))), flush=True)


if __name__ == '__main__':
    main()
