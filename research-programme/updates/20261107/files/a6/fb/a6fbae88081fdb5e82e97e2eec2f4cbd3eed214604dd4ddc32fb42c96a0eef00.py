from source231 import *


def bdf(values, step):
    return (1.5 * values[2:] - 2 * values[1:-1] + .5 * values[:-2]) / step


def paired_defects(system, saved, component):
    rows = saved['rows']
    scale = system.background.start_scale * np.exp(rows[:, 0])
    fields = saved['fields']
    if component == 1:
        base = fields[:, :, :, 0]
        hubble = rows[:, 12]
    else:
        base = fields[:, :, :, 0] + fields[:, :, :, 1]
        hubble = rows[:, 12] * (1 + rows[:, 13])
    delta = fields[:, :, :, component]
    fraction = rows[:, 12 + component]
    delta_hubble = hubble * fraction
    velocity_energy = np.sum(base[:, 1] * delta[:, 1] + .5 * delta[:, 1]**2, axis=1) / scale**2
    potential = np.sum(system.mass**2 * (base[:, 0] * delta[:, 0] + .5 * delta[:, 0]**2), axis=1)
    reference = system.background.parent.photons / scale**4
    density = velocity_energy + potential + reference * rows[:, 7 + component]
    pressure = velocity_energy - potential + reference * rows[:, 9 + component]
    raychaudhuri = (hubble[2:] * (1 + fraction[2:]) * bdf(delta_hubble, system.step)
        + delta_hubble[2:] * bdf(hubble, system.step)
        - hubble[2:]**2 * fraction[2:] * (2 + fraction[2:]) + scale[2:]**2 * (density[2:] + pressure[2:]) / 2)
    field_defects = (hubble[2:, None, None] * ((1 + fraction[2:, None, None]) * bdf(delta, system.step)
        + fraction[2:, None, None] * bdf(base, system.step)))
    field_defects[:, 0] -= delta[2:, 1]
    field_defects[:, 1] += (2 * hubble[2:, None] * ((1 + fraction[2:, None]) * delta[2:, 1]
        + fraction[2:, None] * base[2:, 1]) + scale[2:, None]**2 * system.mass**2 * delta[2:, 0])
    normalization = np.max(abs(hubble**2 * fraction) + scale**2 * (abs(density) + abs(pressure)))
    return dict(expansion=rows[2:, 0], raychaudhuri=raychaudhuri, field_defects=field_defects,
        normalization=normalization, raychaudhuri_relative=float(np.max(abs(raychaudhuri)) / normalization))


def constraint_identity_probes(checks):
    mp.mp.dps = 80
    for label, amplitude in [('ordinary', '1'), ('small_EOS', '1e-13')]:
        amplitude = mp.mpf(amplitude)
        hubble, scale, wave = mp.mpf('3.1'), mp.mpf('1e-5'), mp.mpf('.1')
        background_sum = mp.mpf('2.7e11')
        metric, transverse, longitudinal, density, current, stress_t, stress_l = [amplitude * mp.mpf(value) for value in ('.3', '-.2', '.7', '1e8', '2e7', '-1e7', '5e6')]
        ray_defect = mp.mpf('1e-8')
        energy_defect, current_defect = amplitude * mp.mpf('.13'), amplitude * mp.mpf('.27')
        trace = 2 * transverse + longitudinal
        hubble_prime = hubble**2 - scale**2 * background_sum / 2 + ray_defect
        transverse_prime = -4 * hubble * transverse - hubble * longitudinal - wave**2 * metric / 2 + scale**2 * (density - stress_l) / 2
        longitudinal_prime = -2 * hubble * transverse - 3 * hubble * longitudinal - wave**2 * metric + scale**2 * (density + stress_l - 2 * stress_t) / 2
        density_prime = -3 * hubble * density - hubble * (2 * stress_t + stress_l) - mp.j * wave * current - background_sum * trace + energy_defect
        current_prime = -4 * hubble * current - mp.j * wave * stress_l + current_defect
        hamiltonian = 2 * wave**2 * metric + 4 * hubble * trace - 2 * scale**2 * density
        momentum = 2 * mp.j * wave * transverse - scale**2 * current
        hamiltonian_prime = (4 * wave**2 * transverse + 4 * hubble_prime * trace + 4 * hubble * (2 * transverse_prime + longitudinal_prime)
            - 4 * hubble * scale**2 * density - 2 * scale**2 * density_prime)
        momentum_prime = 2 * mp.j * wave * transverse_prime - 2 * hubble * scale**2 * current - scale**2 * current_prime
        actual = [hamiltonian_prime + 4 * hubble * hamiltonian + 2 * mp.j * wave * momentum,
                  momentum_prime + 2 * hubble * momentum + mp.j * wave * hamiltonian / 2]
        expected = constraint_forcing(scale, trace, ray_defect, energy_defect, current_defect)
        for name, left, right in zip(('Hamiltonian', 'momentum'), actual, expected):
            check(checks, label + ': independent direct ' + name + ' defect forcing', float(abs(left / right - 1)), 1e-10)
            check(checks, label + ': omitting forcing detected in ' + name, int(abs(left / right) < mp.mpf('.99')), 0)


def main():
    modest()
    protocol()
    config = read(ROOT / 'supplement-configuration.json')
    for name, expected in config['hashes'].items():
        assert digest(ROOT / name) == expected
    checks, results = [], []
    inputs = read(ROOT / 'results/inputs-complete.json')
    constraint_identity_probes(checks)
    for model in ('heavy', 'cold'):
        resolutions = {}
        for count in (3200, 6400):
            system = prior.System(model, count, inputs)
            with np.load(register(inputs, PREVIOUS / f'runs/{model}-{count}/history.npz')) as archive:
                saved = dict(archive)
            resolutions[count] = {}
            for name, component in (('NR', 1), ('EOS', 2)):
                values = paired_defects(system, saved, component)
                resolutions[count][name] = values['raychaudhuri_relative']
                save_npz(ROOT / f'results/{model}-{count}-{name}-background-defects.npz', **values)
                check(checks, f'{model}:{count}:{name}: background Raychaudhuri defect versus small source', values['raychaudhuri_relative'], .01)
        for name in ('NR', 'EOS'):
            ratio = resolutions[6400][name] / resolutions[3200][name]
            check(checks, f'{model}:{name}: backward-difference Raychaudhuri defect convergence', ratio, .8)
            results.append(dict(model=model, component=name, coarse=resolutions[3200][name], fine=resolutions[6400][name], ratio=ratio))
    add_modules(inputs)
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    assert not (ROOT / 'results/background-defects.json').exists()
    report = dict(stage=231, state='complete', finished_at=now(), qualified=all(row['passed'] for row in checks),
        checks=checks, failed=[row for row in checks if not row['passed']], results=results,
        scope='Exact forced constraint checks and paired BDF background-defect estimates, not continuous interpolation or propagated wave certification')
    write(ROOT / 'results/background-inputs.json', inputs)
    write(ROOT / 'results/background-defects.json', report)
    print(json.dumps(dict(checks=len(checks), failed=report['failed'], results=results)), flush=True)


if __name__ == '__main__':
    main()
