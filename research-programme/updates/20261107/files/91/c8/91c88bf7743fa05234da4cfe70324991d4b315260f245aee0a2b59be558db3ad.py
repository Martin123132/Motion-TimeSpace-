from run233 import *


def main():
    modest()
    config, frozen = run_protocol()
    path = ROOT / 'results/controls.json'
    assert not path.exists()
    write(ROOT / 'controls-configuration.json', dict(frozen_at=now(), script_sha256=digest(Path(__file__)), identity_tolerance=1e-10))
    original, features, models = setup(config)
    checks, records = [], []
    with mp.workdps(80):
        for row in config['events']:
            parameters, weight = source.physics.parameters_and_weight(row['theta'], row['node'])
            event = geometry(parameters)
            frequencies = np.array(event['frequencies'])
            tests = models[0]['difference'].tests.evaluate(frequencies)
            for state in config['states']:
                for join in config['joins']:
                    coefficients = list(map(mp.mpf, state['coefficients']))
                    values = features.evaluate(frequencies, join)
                    potential = [scalar(config['heat']) * mp.fsum(scalar(value) * coefficient for value, coefficient in zip(line, coefficients[:98])) for line in values]
                    gas = scalar(config['heat']) * coefficients[-1]
                    stats = statistics(event, potential, gas)
                    prefix = f'{row["label"]}:{state["model"]}:{state["history"]}:join{join}'
                    matrix, unused, unused, unused = projected(event, tests, values, stats['mixed'], 1)
                    wrong_pairing = np.linalg.norm(matrix[0]) / max(np.linalg.norm(matrix[0]) + np.linalg.norm(matrix[-1]), 1e-300)
                    check(checks, prefix + ':missing gas rejected', int(wrong_pairing <= 1e-10), 0)
                    wrong_sign = mp_relative([-value for value in vector(stats['mixed'])], vector(stats['mixed']))
                    check(checks, prefix + ':wrong derivative sign rejected', int(wrong_sign <= 1e-10), 0)
                    stripped = [mp.mpf(0)] * len(potential)
                    gas_only = statistics(event, stripped, gas)
                    omitted_bose = mp_relative(gas_only['mixed']['photon'], stats['mixed']['photon'])
                    check(checks, prefix + ':omitted photon occupation derivative rejected', int(omitted_bose <= 1e-10), 0)
                    half = statistics(event, [value / 2 for value in potential], gas / 2)
                    full_remainder = mp.sqrt(mp.fsum(value**2 for value in vector(stats['remainder'])))
                    half_remainder = mp.sqrt(mp.fsum(value**2 for value in vector(half['remainder'])))
                    check(checks, prefix + ':mixed linearity', mp_relative(vector(half['mixed']), [value / 2 for value in vector(stats['mixed'])]))
                    records.append(dict(anchor=row['label'], model=state['model'], history=state['history'], join=join,
                        omitted_bose_relative_error=omitted_bose, missing_gas_error=wrong_pairing,
                        remainder_half_over_full=float(half_remainder / full_remainder)))
        for join in config['joins']:
            for frequency in (1e-8, 80.):
                try:
                    features.evaluate(frequency, join)
                except AssertionError:
                    rejected = True
                else:
                    rejected = False
                check(checks, f'outside explicit domain:{join}:{frequency}', int(not rejected), 0)
        for row in config['events']:
            parameters, weight = source.physics.parameters_and_weight(row['theta'], row['node'])
            event = geometry(parameters)
            actual_basis = features.evaluate(np.array(event['frequencies']), 0)
            check(checks, row['label'] + ':all98 photon coordinates retained', actual_basis.shape[-1] - 98, 0)
    failed = [row for row in checks if not row['passed']]
    write(path, dict(state='complete', checks=checks, failed=failed, qualified=not failed, records=records, finished_at=now()))
    print(json.dumps(dict(control_checks=len(checks), failed=failed, minimum_omitted_Bose_error=min(row['omitted_bose_relative_error'] for row in records))), flush=True)
    assert not failed, failed


if __name__ == '__main__':
    main()
