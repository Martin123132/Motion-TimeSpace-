from angular232 import *
import source231 as gas_source


def photon_mass(order):
    nodes, weights = special.roots_laguerre(order)
    radial = inherited.functions(nodes)
    measure = weights * nodes**2 / ((-np.expm1(-nodes))**2 * (np.pi**4 / 15))
    return (radial.T * measure) @ radial


def main():
    modest()
    config = protocol()
    frozen = read(ROOT / 'assessment-configuration.json')
    for name, expected in frozen['hashes'].items():
        assert digest(ROOT / name) == expected
    inputs = read(ROOT / 'results/preflight-inputs.json')
    checks, results = [], []
    mass = photon_mass(160)
    check(checks, 'Regular photon susceptibility mass quadrature', relative(photon_mass(96), mass), 1e-10)
    check(checks, 'Photon temperature susceptibility equals four', mass[0, 0] - 4, 1e-10)
    mp.mp.dps = 80
    for model in ('heavy', 'cold'):
        background, mixture = gas_source.prior.prior.prior.load_background(model, inputs)
        for probe in config['probes']:
            temperature = probe['temperature']
            scale = background.theta0 / temperature
            reference = background.parent.photons / scale**4
            rest = background.parent.baryons / scale**3 / reference
            heat = background.chi
            eos = gas_source.eos_at(mixture, temperature, 1.)
            nodes, weights = gas_source.prior.prior.radial_rule(48)
            measure = weights * (1 + temperature * nodes) * np.sqrt(2 + temperature * nodes)
            measure /= measure.sum()
            mean = float(measure @ nodes)
            variance = float(measure @ (nodes - mean)**2)
            velocity_susceptibility = float(measure @ (nodes * (2 + temperature * nodes)) / 3)
            enthalpy = 1 + temperature * (mean + 1)
            check(checks, f'{model}:{probe["label"]}: electron kinetic boost susceptibility equals enthalpy', velocity_susceptibility / enthalpy - 1, 1e-10)
            check(checks, f'{model}:{probe["label"]}: electron energy variance heat capacity', (2 / 3) * mixture.fractions[0] * variance + (1 - mixture.fractions[0]) - eos['C'], 1e-10)
            for kind, capacity, inertia in [('NR', 1., rest + 5 * heat / 3), ('EOS', eos['C'], rest + heat * (eos['A'] + 2 / 3))]:
                for degree in (0, 1):
                    folder = ROOT / 'runs' / f'{probe["label"]}-l{degree}-8-56-original'
                    path = register(inputs, folder / 'matrix.npz')
                    with np.load(path) as archive:
                        correction = archive['total'].copy()
                        born = archive['born'].copy()
                    susceptibility = heat * capacity if degree == 0 else inertia
                    augmented_mass = np.zeros((4, 4))
                    augmented_mass[:3, :3] = mass / (2 * degree + 1)
                    augmented_mass[-1, -1] = susceptibility
                    for label, weak in [('Born', born), ('matched_increment', correction)]:
                        generator = -np.linalg.solve(augmented_mass, weak)
                        photon_source = mass[0] @ generator[:3] / (2 * degree + 1)
                        reconstructed_gas = -photon_source / susceptibility
                        error = relative(generator[-1], reconstructed_gas)
                        check(checks, f'{model}:{probe["label"]}:{kind}:l{degree}:{label}: actual EOS gas port from common photon moment', error, 2e-7)
                        if degree == 1:
                            common = np.array([1., 0., 0., 1.])
                            check(checks, f'{model}:{probe["label"]}:{kind}:{label}: common velocity has no collision acceleration', np.linalg.norm(generator @ common) / np.linalg.norm(generator), 2e-7)
                        results.append(dict(model=model, probe=probe['label'], gas=kind, degree=degree, component=label,
                            susceptibility=susceptibility, photon_gas_pairing=error,
                            scope='Common Planck/Juttner reference susceptibility; conditional event normalization, not a wave evolution'))
    add_modules(inputs)
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    report = dict(stage=232, state='complete', finished_at=now(), qualified=all(row['passed'] for row in checks),
        checks=checks, failed=[row for row in checks if not row['passed']], results=results,
        scope='Same matched photon block paired to NR/EOS heat and enthalpy on both calibrated parents at the common equilibrium reference')
    assert not (ROOT / 'results/interface.json').exists()
    write(ROOT / 'results/interface-inputs.json', inputs)
    write(ROOT / 'results/interface.json', report)
    print(json.dumps(dict(checks=len(checks), failed=report['failed'])), flush=True)


if __name__ == '__main__':
    main()
