from common234 import *
import assemble234


def dot(values, coefficients):
    return mp.fsum(scalar(value) * coefficient for value, coefficient in zip(values, coefficients))


def probes():
    return [
        ('broad_photon', np.r_[np.sin(np.arange(98) * .43 + .1), 0.]),
        ('two_tails', np.r_[np.zeros(96), 1., .5, 0.]),
        ('gas', np.r_[np.zeros(98), 1.]),
        ('mixed', np.r_[np.cos(np.arange(98) * .29 + .3), .3]),
    ]


def main():
    modest()
    config, assembly = assemble234.protocol_assembly()
    target = ROOT / 'results/product-controls.json'
    assert not target.exists()
    controls = dict(frozen_at=now(), script_sha256=digest(Path(__file__)),
        background_step='1e-8', wave_step='1e-18', tolerance=1e-10,
        probes={name: values.tolist() for name, values in probes()},
        scope='Independent raw-product finite differences on four fixed coefficient directions, every angular component; not every individual matrix entry',
        block_sha256=digest(ROOT / 'results/virtual-mixed-blocks.npz'))
    write(ROOT / 'controls-configuration.json', controls)
    original, features, models = setup(config)
    blocks = packet(ROOT / 'results/virtual-mixed-blocks.npz')
    checks, records = [], []
    maximum = dict(product=0., medium=0., assembled=0., assembled_medium=0.)
    with mp.workdps(80):
        background_step, wave_step = mp.mpf(controls['background_step']), mp.mpf(controls['wave_step'])
        for row in config['events']:
            parameters, weight = source.physics.parameters_and_weight(row['theta'], row['node'])
            event = geometry(parameters)
            tests = models[0]['difference'].tests.evaluate(np.array(event['frequencies']))
            vacuum = angular.inherited.vacuum.finite_virtual_ratio(mp.mpf(str(parameters['energy'])), mp.mpf(str(parameters['cosine'])))
            vacuum += angular.inherited.vacuum.soft_constant(mp.mpf(str(parameters['energy'])), mp.mpf(str(parameters['cosine'])))
            equilibrium_kernel = vacuum + scalar(read(row['loop_path'])['scalar'])
            for join in config['joins']:
                basis = features.evaluate(np.array(event['frequencies']), join)
                maps = packet(ROOT / 'response' / f'{row["label"]}-join{join}-order6.npz')['mueller'][:98, :, 0, 0]
                for state in config['states']:
                    physical = [scalar(config['heat']) * mp.mpf(value) for value in state['coefficients']]
                    background_photons = [dot(line, physical[:98]) for line in basis]
                    stats = statistics(event, background_photons, physical[-1])
                    kernel_background = dot(maps[:, 0], physical[:98])
                    for degree, start in [(0, 0), (1, 1), (2, 4)]:
                        harmonic = angular.angular_feature(np.array(event['directions']), degree)
                        unused, unused, left, unused = projected(event, tests, basis, stats['equilibrium'], degree)
                        prefix = f'{row["label"]}:join{join}:{state["model"]}:{state["history"]}:l{degree}:order6'
                        for name, wave in probes():
                            measured_components, medium_components = [], []
                            for component in range(harmonic.shape[1]):
                                photons = [dot(line, list(map(scalar, wave[:98]))) * scalar(harmonic[index, component]) for index, line in enumerate(basis)]
                                gas = scalar(wave[-1]) if degree == 0 else mp.mpf(0)
                                velocity = [scalar(wave[-1]) * int(degree == 1 and component == axis) for axis in range(3)]
                                kernel_wave = dot(maps[:, start + component], list(map(scalar, wave[:98])))
                                wave_linear = prior.scalar_product(stats['equilibrium'], photons, gas, velocity, mp.mpf(0))
                                mixed_statistical = prior.scalar_product(stats['mixed'], photons, gas, velocity, mp.mpf(0))
                                medium = kernel_background * wave_linear + kernel_wave * stats['linear_source']
                                expected = equilibrium_kernel * mixed_statistical + medium
                                scale = max(abs(equilibrium_kernel * mixed_statistical) + abs(kernel_background * wave_linear)
                                    + abs(kernel_wave * stats['linear_source']), mp.mpf('1e-300'))
                                medium_scale = max(abs(kernel_background * wave_linear) + abs(kernel_wave * stats['linear_source']), mp.mpf('1e-300'))
                                sampled_full, sampled_medium = [], []
                                for background_sign, wave_sign in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                                    amplitude, disturbance = background_sign * background_step, wave_sign * wave_step
                                    flux = raw_flux(event,
                                        [amplitude * value + disturbance * change for value, change in zip(background_photons, photons)],
                                        amplitude * physical[-1] + disturbance * gas,
                                        [disturbance * value for value in velocity])
                                    kernel_change = amplitude * kernel_background + disturbance * kernel_wave
                                    sampled_full.append((equilibrium_kernel + kernel_change) * flux)
                                    sampled_medium.append(kernel_change * flux)
                                def mixed_difference(values):
                                    return (values[0] - values[1] - values[2] + values[3]) / (4 * background_step * wave_step)
                                measured, measured_medium = mixed_difference(sampled_full), mixed_difference(sampled_medium)
                                error, medium_error = float(abs(measured - expected) / scale), float(abs(measured_medium - medium) / medium_scale)
                                check(checks, prefix + f':{name}:component{component}:raw product derivative', error)
                                check(checks, prefix + f':{name}:component{component}:raw medium derivative', medium_error)
                                maximum['product'] = max(maximum['product'], error)
                                maximum['medium'] = max(maximum['medium'], medium_error)
                                measured_components.append(float(measured))
                                medium_components.append(float(measured_medium))
                            full_vector = .5 * weight * (left @ np.array(measured_components)) / (2 * degree + 1)
                            medium_vector = .5 * weight * (left @ np.array(medium_components)) / (2 * degree + 1)
                            expected_vector = blocks[prefix + ':total'] @ wave
                            expected_medium = blocks[prefix + ':medium'] @ wave
                            error, medium_error = relative(full_vector, expected_vector), relative(medium_vector, expected_medium)
                            check(checks, prefix + f':{name}:saved full block', error)
                            check(checks, prefix + f':{name}:saved medium block', medium_error)
                            maximum['assembled'] = max(maximum['assembled'], error)
                            maximum['assembled_medium'] = max(maximum['assembled_medium'], medium_error)
                print(json.dumps(dict(product_anchor=row['label'], join=join, checks=len(checks), maximum=maximum)), flush=True)
        for join in config['joins']:
            radial = packet(ROOT / 'radial' / f'join{join}-order6.npz')
            for anchor, row in enumerate(config['events']):
                errors = []
                wrong_errors = []
                for ray in range(8):
                    for pole in range(2):
                        location = scalar(radial['locations'][anchor, ray, pole])
                        occupation = 1 / mp.expm1(location)
                        expected = -mp.pi * int(radial['signs'][anchor, ray, pole]) * location * occupation * (1 + occupation) / 2
                        actual = scalar(radial['poles'][anchor, ray, pole, -1].imag)
                        error = float(abs(actual / expected - 1))
                        wrong_error = float(abs(-actual / expected - 1))
                        check(checks, f'join{join}:{row["label"]}:ray{ray}:pole{pole}:absorptive derivative sign', error)
                        check(checks, f'join{join}:{row["label"]}:ray{ray}:pole{pole}:wrong absorptive sign rejected', int(wrong_error <= 1e-10), 0)
                        errors.append(error)
                        wrong_errors.append(wrong_error)
                records.append(dict(join=join, anchor=row['label'], maximum_absorptive_identity_error=max(errors),
                    minimum_wrong_sign_error=min(wrong_errors),
                    scope='Analytic h=x thermal control at the complex radial kernel; no claim that unpolarized intensity detects every absorptive change'))
    failed = [entry for entry in checks if not entry['passed']]
    report = dict(state='complete', qualified=not failed, checks=checks, failed=failed, maximum=maximum,
        records=records, finished_at=now(), arithmetic_digits=80, scope=controls['scope'])
    write(target, report)
    print(json.dumps(dict(checks=len(checks), failed=failed, maximum=maximum)), flush=True)
    assert not failed, failed


if __name__ == '__main__':
    main()
