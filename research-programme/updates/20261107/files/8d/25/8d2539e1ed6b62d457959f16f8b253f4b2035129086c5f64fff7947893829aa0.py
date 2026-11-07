from run233 import *


def main():
    modest()
    config, frozen = run_protocol()
    target = ROOT / 'results/components.json'
    assert not target.exists()
    write(ROOT / 'components-configuration.json', dict(frozen_at=now(), script_sha256=digest(Path(__file__)),
        event_indices=[0, 1, 4], states='all original/half/quarter, both parents and joins', tolerance=1e-10))
    original, features, models = setup(config)
    checks, maxima = [], dict(exact=0., mixed=0.)
    with mp.workdps(80):
        step, background_step = mp.mpf('1e-20'), mp.mpf('1e-12')
        for row in config['events']:
            parameters, unused = source.physics.parameters_and_weight(row['theta'], row['node'])
            for index, (tag, event) in enumerate(selected_events(parameters, config)):
                if index not in (0, 1, 4):
                    continue
                for state in config['states']:
                    for join in config['joins']:
                        values = features.evaluate(np.array(event['frequencies']), join)
                        coefficients = list(map(mp.mpf, state['coefficients']))
                        potential = [scalar(config['heat']) * mp.fsum(scalar(value) * coefficient for value, coefficient in zip(line, coefficients[:98])) for line in values]
                        gas = scalar(config['heat']) * coefficients[-1]
                        stats = statistics(event, potential, gas)
                        count = len(potential)
                        for component in range(count + 5):
                            photon_wave = [mp.mpf(int(component == offset)) for offset in range(count)]
                            gas_wave = mp.mpf(int(component == count))
                            velocity_wave = [mp.mpf(int(component == count + 1 + axis)) for axis in range(3)]
                            density_wave = mp.mpf(int(component == count + 4))
                            def sampled(amplitude, wave):
                                return raw_flux(event, [amplitude * value + wave * change for value, change in zip(potential, photon_wave)],
                                    amplitude * gas + wave * gas_wave, [wave * value for value in velocity_wave], wave * density_wave)
                            measured = (sampled(1, step) - sampled(1, -step)) / (2 * step)
                            mixed_measured = (sampled(background_step, step) - sampled(background_step, -step)
                                - sampled(-background_step, step) + sampled(-background_step, -step)) / (4 * step * background_step)
                            for label, actual in [('exact', measured), ('mixed', mixed_measured)]:
                                expected = scalar_product(stats[label], photon_wave, gas_wave, velocity_wave, density_wave)
                                scale = max(mp.sqrt(mp.fsum(value**2 for value in vector(stats[label]))), mp.mpf('1e-300'))
                                error = float(abs(actual - expected) / scale)
                                maxima[label] = max(maxima[label], error)
                                check(checks, f'{row["label"]}:{tag}:{state["model"]}:{state["history"]}:{join}:component{component}:{label}', error)
    failed = [row for row in checks if not row['passed']]
    write(target, dict(state='complete', qualified=not failed, checks=checks, failed=failed, maxima=maxima,
        normalization='Each coefficient error divided by the full coefficient-vector norm; no division by an identically zero transverse component', finished_at=now()))
    print(json.dumps(dict(component_checks=len(checks), failed=failed, maxima=maxima)), flush=True)
    assert not failed, failed


if __name__ == '__main__':
    main()
