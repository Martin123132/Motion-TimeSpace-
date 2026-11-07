from source231 import *


def effective(matrix):
    return np.triu(matrix) + np.triu(matrix, 1).T


def process_columns(system, theta, opacity, profile, gas):
    scattering = system.ladder.at(theta, 0)
    dc = system.emission.at(theta, 'dc')
    br = system.emission.at(theta, 'dcbr') - dc
    matrices = dict(Compton=scattering, DC=-dc, BR=-br)
    factor = linalg.cho_factor(system.effective_mass, lower=False)
    source = {name: system.heat * opacity * linalg.cho_solve(factor,
        effective(matrix) @ profile - (matrix @ system.basis.temperature) * gas) for name, matrix in matrices.items()}
    common = sum(source.values())
    density = common + source['BR']
    return dict(processes=source, background=common, density=density)


def boost_port(system, source):
    basis = system.basis
    values = basis.values
    derivative = basis.derivative(basis.nodes)
    weak = ((2 * values + basis.nodes[:, None] * derivative).T * basis.measure) @ values
    edges = np.array([basis.minimum, basis.maximum])
    edge_values = basis.evaluate(edges)
    occupations = 1 / np.expm1(edges)
    edge_measure = edges**3 * occupations * (1 + occupations) / (np.pi**4 / 15)
    edge_source = edge_values @ source
    surface = edge_values[1] * edge_measure[1] * edge_source[1] - edge_values[0] * edge_measure[0] * edge_source[0]
    solved = linalg.solve(system.effective_mass, np.column_stack([weak @ source, surface]), assume_a='pos')
    boundary_energy = (edges[1] * edge_measure[1] * edge_source[1] - edges[0] * edge_measure[0] * edge_source[0]) / 3
    return dict(boost=solved[:, 0] - solved[:, 1], bulk=solved[:, 0], surface=solved[:, 1],
                boundary_momentum=boundary_energy)


def main():
    modest()
    protocol()
    config = read(ROOT / 'port-configuration.json')
    for name, expected in config['hashes'].items():
        assert digest(ROOT / name) == expected
    inputs = read(ROOT / 'results/background-inputs.json')
    for name in ('DERIVATION.md', 'emission_response.py', 'density_tangent.py', 'verify_frame_pairing.py'):
        register(inputs, BRANCH / 'emitting-wave-response-20261008' / name)
    checks, records = [], []
    mp.mp.dps = 80
    for model in ('heavy', 'cold'):
        system = prior.System(model, 6400, inputs)
        with np.load(register(inputs, PREVIOUS / f'runs/{model}-6400/history.npz')) as archive:
            saved = dict(archive)
        for index in (400, 1600, 3200, 4800, 6400):
            scale = system.background.start_scale * math.exp(float(system.coordinates[index]))
            opacity = system.background.parent.opacity_constant / scale**2
            reference = system.background.parent.photons / scale**4
            rest = system.background.parent.baryons / scale**3 / reference
            for kind, component in (('NR', 0), ('EOS', 1)):
                profile = saved['profiles'][index, :, 0] + component * saved['profiles'][index, :, 1]
                gas = saved['rows'][index, 3] + component * saved['rows'][index, 4]
                hubble = saved['rows'][index, 12] * (1 + saved['rows'][index, 13]) * (1 + component * saved['rows'][index, 14])
                ports = process_columns(system, system.theta[index], opacity, profile, gas)
                energy = system.basis.energy
                moments = {name: float(energy @ value) for name, value in ports['processes'].items()}
                total = sum(moments.values())
                density = float(energy @ ports['density'])
                eos = eos_at(system.mixture, system.theta[index], 1 + system.heat * gas, kind)
                local = gas_coefficients(float(hubble), rest, system.heat, 1 + system.heat * gas, eos, total)
                label = f'{model}:{index}:{kind}'
                mp_moments = {name: mp.mpf(value) for name, value in moments.items()}
                def varied_transfer(fraction):
                    return fraction * (mp_moments['Compton'] + mp_moments['DC']) + fraction**2 * mp_moments['BR']
                derivative = mp.diff(varied_transfer, 1)
                check(checks, label + ': physical density column includes two BR factors', float((mp.mpf(density) - derivative) / max(abs(derivative), mp.mpf('1e-100'))), 1e-9)
                heat, capacity = mp.mpf(system.heat), mp.mpf(eos['C'])
                def gas_transfer(fraction):
                    return -varied_transfer(fraction) / (heat * fraction * capacity)
                expected = -mp_moments['BR'] / (heat * capacity)
                actual = mp.diff(gas_transfer, 1)
                check(checks, label + ': source per gas particle retains ion-density term', float(actual / expected - 1), 1e-10)
                check(checks, label + ': omitted ion term is detected against its own response', int(abs(actual / expected) < mp.mpf('.99')), 0)
                basis_rows = np.eye(6, dtype=complex)
                density_row, temperature_row, velocity_row, trace_row, energy_extra, current_extra = basis_rows
                momentum = current_extra.copy()
                monopole = density * density_row + energy_extra
                rows = source_rows(local, density_row, trace_row + .1j * velocity_row, temperature_row, velocity_row, monopole, momentum, .1)
                expected_density_heating = -(density - total) / (system.heat * eos['C'])
                check(checks, label + ': implemented gas density column matches physical BR term',
                    abs(rows['temperature'][0] - expected_density_heating) / max(abs(expected_density_heating), 1e-100), 1e-9)
                boost = boost_port(system, ports['background'])
                momentum_bulk = float(energy @ boost['bulk'] / 3)
                momentum_surface = float(energy @ boost['surface'] / 3)
                boost_moment = float(energy @ boost['boost'] / 3)
                check(checks, label + ': weak common-boost bulk moment', (momentum_bulk - total) / max(abs(total), 1e-100), 1e-9)
                check(checks, label + ': explicit finite-window boost surface moment', (momentum_surface - boost['boundary_momentum']) / max(abs(boost['boundary_momentum']), 1e-100), 1e-9)
                check(checks, label + ': boost energy-momentum identity including boundary', (boost_moment - total + boost['boundary_momentum']) / max(abs(total), 1e-100), 1e-9)
                records.append(dict(model=model, index=index, kind=kind, photon_process_energy=moments,
                    density_heating=float(expected), omitted_ion_relative_error=1.,
                    boundary_momentum=float(boost['boundary_momentum']), boundary_over_bulk=float(boost['boundary_momentum'] / total),
                    common_boost_momentum=boost_moment, scope='Common boost of retained isotropic source, not angular drag or a polarized angular Jacobian'))
        print(json.dumps(dict(model=model, checks=len(checks), failed=sum(not row['passed'] for row in checks))), flush=True)
    add_modules(inputs)
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    report = dict(stage=231, state='complete', finished_at=now(), qualified=all(row['passed'] for row in checks),
        checks=checks, failed=[row for row in checks if not row['passed']], records=records,
        scope='Stage80 density/common-boost ports applied to unchanged Stage230 bank and EOS gas rows; no inferred angular redistribution')
    assert not (ROOT / 'results/collision-ports.json').exists()
    write(ROOT / 'results/port-inputs.json', inputs)
    write(ROOT / 'results/collision-ports.json', report)
    print(json.dumps(dict(checks=len(checks), failed=report['failed'])), flush=True)


if __name__ == '__main__':
    main()
