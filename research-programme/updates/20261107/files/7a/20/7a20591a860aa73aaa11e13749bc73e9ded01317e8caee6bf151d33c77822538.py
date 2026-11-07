from common235 import *
import radial234
import state235


def profile_moments(features, join, order, profile):
    frequency, weights, numerator = radial234.grid(features, join, order)
    change = -np.expm1(-(frequency / profile)**2)
    occupation = 1 / np.expm1(frequency)
    scalar_moment = weights @ (change * occupation / frequency)
    coordinate_moment = (weights * change / frequency**2) @ numerator[:, :98]
    return scalar_moment, coordinate_moment


def soft_rays(parameters):
    recoil = np.array([0., 0., parameters['energy']]) - parameters['hard'] * parameters['hard_direction']
    final_energy = np.sqrt(1 + recoil @ recoil)
    result = []
    for index, (direction, weight) in enumerate(angular.inherited.source.angular_nodes(4)):
        pole = angular.inherited.source.ALPHA / (4 * np.pi**2) * np.linalg.norm(np.cross(recoil, direction))**2 / (final_energy - recoil @ direction)**2
        lab = parameters['transform'] @ np.r_[1., direction]
        result.append(dict(index=index, direction=lab[1:] / np.linalg.norm(lab[1:]), weight=weight, pole=pole))
    return result


def main():
    modest()
    config = protocol()
    target = ROOT / 'results/soft-product-and-profile.json'
    assert not target.exists()
    controls = dict(frozen_at=now(), script_sha256=digest(Path(__file__)), profiles=[.2, .5],
        orders=[4, 6], soft_frequencies=[1.2e-6, 1e-4, .2, 2., 10., 30.],
        ray_indices=[0, 11, 23], background_step='1e-8', wave_step='1e-18',
        derivative_tolerance=1e-10, profile_refinement_tolerance=.002,
        full_finite_real_events_integrated=False, exterior_supplied=False)
    write(ROOT / 'soft-configuration.json', controls)
    original, features, models = setup(config)
    checks, records, output = [], [], {}
    moments = {}
    for join in config['joins']:
        for profile in controls['profiles']:
            for order in controls['orders']:
                scalar_moment, coordinates = profile_moments(features, join, order, profile)
                moments[join, profile, order] = scalar_moment, coordinates
                output[f'join{join}:profile{profile}:order{order}:moment'] = np.r_[scalar_moment, coordinates]
    maximum_derivative_error = 0.
    with mp.workdps(80):
        background_step, wave_step = mp.mpf(controls['background_step']), mp.mpf(controls['wave_step'])
        wave = np.r_[np.cos(np.arange(98) * .29 + .3), .3]
        for row in config['events']:
            parameters, weight = source.physics.parameters_and_weight(row['theta'], row['node'])
            event = geometry(parameters)
            rays = soft_rays(parameters)
            tests = models[0]['difference'].tests.evaluate(np.array(event['frequencies']))
            pole_zero = sum(ray['weight'] * ray['pole'] for ray in rays)
            for join in config['joins']:
                basis = features.evaluate(np.array(event['frequencies']), join)
                soft_features = features.evaluate(np.array(controls['soft_frequencies']), join)
                for state_index, state in enumerate(config['states']):
                    physical = [scalar(config['heat']) * mp.mpf(value) for value in state['coefficients']]
                    background = [state235.contraction(line, physical[:98]) for line in basis]
                    stats = statistics(event, background, physical[-1])
                    for degree in config['multipoles']:
                        harmonic = angular.angular_feature(np.array(event['directions']), degree)
                        mixed, unused, left, unused = projected(event, tests, basis, stats['mixed'], degree)
                        reference = projected(event, tests, basis, stats['equilibrium'], degree)[0]
                        pole_harmonic = sum(ray['weight'] * ray['pole'] * angular.angular_feature(ray['direction'], degree) for ray in rays)
                        prefix = f'{row["label"]}:join{join}:state{state_index}:l{degree}'
                        for profile in controls['profiles']:
                            changes = {}
                            wave_term = None
                            for order in controls['orders']:
                                scalar_moment, coordinate_moment = moments[join, profile, order]
                                background_moment = float(state235.contraction(coordinate_moment, physical[:98]))
                                wave_term = float(stats['linear_source']) * np.outer(left @ pole_harmonic, np.r_[coordinate_moment, 0.]) / (2 * degree + 1)
                                changes[order] = weight * (pole_zero * scalar_moment * mixed + pole_zero * background_moment * reference + wave_term)
                            residual = changes[4] - changes[6]
                            error = np.linalg.norm(residual) / max(np.linalg.norm(changes[6]), 1e-300)
                            check(checks, prefix + f':profile{profile}:separate-order subtraction/conversion cancellation', error, .002)
                            omitted_error = np.linalg.norm(weight * wave_term) / max(np.linalg.norm(changes[6]), 1e-300)
                            check(checks, prefix + f':profile{profile}:omitted wave-medium conversion rejected', int(omitted_error <= 1e-10), 0)
                            output[prefix + f':profile{profile}:real_subtraction_change'] = changes[4]
                            output[prefix + f':profile{profile}:profile_conversion_change'] = -changes[6]
                            if degree < 2:
                                check(checks, prefix + f':profile{profile}:independent gas force', np.linalg.norm(changes[6][0] + changes[6][-1]) / max(np.linalg.norm(changes[6][0]) + np.linalg.norm(changes[6][-1]), 1e-300))
                            records.append(dict(anchor=row['label'], join=join, model=state['model'], history=state['history'], degree=degree,
                                profile=profile, independent_quadrature_residual=float(error), omitted_wave_relative_error=float(omitted_error)))
                        photons = [state235.contraction(line, list(map(scalar, wave[:98]))) * scalar(harmonic[index, 0]) for index, line in enumerate(basis)]
                        gas = scalar(wave[-1]) if degree == 0 else mp.mpf(0)
                        velocity = [scalar(wave[-1]) * int(degree == 1 and axis == 0) for axis in range(3)]
                        wave_linear = prior.scalar_product(stats['equilibrium'], photons, gas, velocity, mp.mpf(0))
                        mixed_linear = prior.scalar_product(stats['mixed'], photons, gas, velocity, mp.mpf(0))
                        for ray_index in controls['ray_indices']:
                            ray = rays[ray_index]
                            soft_harmonic = scalar(angular.angular_feature(ray['direction'], degree)[0])
                            for soft_index, frequency in enumerate(controls['soft_frequencies']):
                                soft_background = state235.contraction(soft_features[soft_index], physical[:98])
                                soft_wave = soft_harmonic * state235.contraction(soft_features[soft_index], list(map(scalar, wave[:98])))
                                occupation = 1 / mp.expm1(scalar(frequency))
                                occupation_weight = occupation * (1 + occupation)
                                terms = [(1 + 2 * occupation) * mixed_linear,
                                    2 * occupation_weight * soft_background * wave_linear,
                                    2 * occupation_weight * soft_wave * stats['linear_source']]
                                expected = mp.fsum(terms)
                                samples = []
                                for background_sign, wave_sign in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                                    amplitude, disturbance = background_sign * background_step, wave_sign * wave_step
                                    photon_potential = [amplitude * value + disturbance * change for value, change in zip(background, photons)]
                                    occupation_actual = occupation + occupation_weight * (amplitude * soft_background + disturbance * soft_wave)
                                    flux = raw_flux(event, photon_potential, amplitude * physical[-1] + disturbance * gas, [disturbance * value for value in velocity])
                                    samples.append((1 + 2 * occupation_actual) * flux)
                                measured = (samples[0] - samples[1] - samples[2] + samples[3]) / (4 * background_step * wave_step)
                                error = float(abs(measured - expected) / max(mp.fsum(abs(value) for value in terms), mp.mpf('1e-300')))
                                maximum_derivative_error = max(maximum_derivative_error, error)
                                check(checks, prefix + f':ray{ray_index}:x{frequency}:nonlinear soft product', error)
            print(json.dumps(dict(anchor=row['label'], checks=len(checks), failed=sum(not entry['passed'] for entry in checks))), flush=True)
    save(ROOT / 'results/soft-profile-maps.npz', **output)
    failed = [entry for entry in checks if not entry['passed']]
    write(target, dict(state='complete', qualified=not failed, checks=checks, failed=failed, records=records,
        maximum_derivative_error=maximum_derivative_error, sha256=digest(ROOT / 'results/soft-profile-maps.npz'), finished_at=now(),
        scope='Full-basis common soft profile derivative and conversion, not the integrated finite real emission/absorption remainder',
        finite_floor=config['spectral_domain'][0], exterior_supplied=False))
    print(json.dumps(dict(checks=len(checks), failed=failed, maximum_derivative_error=maximum_derivative_error,
        maximum_profile_residual=max(row['independent_quadrature_residual'] for row in records))), flush=True)
    assert not failed, failed


if __name__ == '__main__':
    main()
