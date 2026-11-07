from common235 import *
import state235 as implementation
import copy


def main():
    modest()
    config = protocol()
    assert not (ROOT / 'results/state-tangent-controls.json').exists()
    write(ROOT / 'tangent-controls-configuration.json', dict(frozen_at=now(), script_sha256=digest(Path(__file__)),
        implementation_sha256=digest(ROOT / 'state235.py'), eta_step='1e-18', tolerance=1e-10))
    original, features, models = setup(config)
    checks, records = [], []
    with mp.workdps(80):
        step = mp.mpf('1e-18')
        for row in config['events']:
            parameters, unused = source.physics.parameters_and_weight(row['theta'], row['node'])
            tangent = implementation.phase_geometry(parameters)
            event = tangent['event']
            temperature = scalar(row['theta'])
            text = mp.nstr(temperature, 85)
            independent_mean = mp.diff(lambda eta: implementation.mean_energy(text, mp.nstr(eta, 85)), mp.mpf(0))
            check(checks, row['label'] + ':mean-energy mass derivative', abs(implementation.mean_tangent(text) / independent_mean - 1))
            frequencies = np.array(event['frequencies'])
            for join in config['joins']:
                basis = features.evaluate(frequencies, join)
                slopes = features.evaluate(frequencies, join, True)
                for state in config['states']:
                    physical = [scalar(config['heat']) * mp.mpf(value) for value in state['coefficients']]
                    potential = [implementation.contraction(line, physical[:98]) for line in basis]
                    potential_prime = [implementation.contraction(line, physical[:98]) * shift for line, shift in zip(slopes, tangent['frequency_shift'])]
                    original_stats = statistics(event, potential, physical[-1])
                    reference = implementation.coefficients_at(event, potential, physical[-1])
                    derivative = implementation.tangent_coefficients(event, tangent, potential, potential_prime, physical[-1])
                    omitted = implementation.tangent_coefficients(event, tangent, potential, potential_prime, physical[-1], omit_mean=True)
                    samples = []
                    for eta in (step, -step):
                        shifted = copy.deepcopy(event)
                        for name, shifts in [('frequencies', tangent['frequency_shift']), ('electron_initial', tangent['initial_shift']), ('electron_transfer', tangent['transfer_shift'])]:
                            shifted[name] = [scalar(value) + eta * change for value, change in zip(event[name], shifts)]
                        sample = implementation.coefficients_at(shifted, [value + eta * change for value, change in zip(potential, potential_prime)], physical[-1], eta)
                        samples.append(sample)
                    prefix = f'{row["label"]}:join{join}:{state["model"]}:{state["history"]}'
                    for part in ('equilibrium', 'mixed'):
                        expected = prior.vector(derivative[part])
                        measured = [(upper - lower) / (2 * step) for upper, lower in zip(prior.vector(samples[0][part]), prior.vector(samples[1][part]))]
                        check(checks, prefix + ':' + part + ':original coefficients', prior.mp_relative(prior.vector(reference[part]), prior.vector(original_stats[part])))
                        error = prior.mp_relative(measured, expected)
                        check(checks, prefix + ':' + part + ':independent mass derivative', error)
                        if part == 'mixed':
                            wrong = prior.mp_relative(prior.vector(omitted[part]), expected)
                            check(checks, prefix + ':omitted mean-energy derivative rejected', int(wrong <= 1e-10), 0)
                            records.append(dict(anchor=row['label'], join=join, model=state['model'], history=state['history'], derivative_error=error, omitted_mean_error=wrong))
    failed = [entry for entry in checks if not entry['passed']]
    report = dict(state='complete', qualified=not failed, checks=checks, failed=failed, records=records, finished_at=now())
    write(ROOT / 'results/state-tangent-controls.json', report)
    print(json.dumps(dict(checks=len(checks), failed=failed, maximum_derivative_error=max(row['derivative_error'] for row in records), minimum_omitted_mean_error=min(row['omitted_mean_error'] for row in records))), flush=True)
    assert not failed, failed


if __name__ == '__main__':
    main()
