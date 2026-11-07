from common235 import *
import state235


def extended(value):
    return np.longdouble(mp.nstr(value, 32)) if isinstance(value, mp.mpf) else np.longdouble(value)


def stable_coefficients(event, potential, gas):
    temperature = extended(event['temperature'])
    frequencies = np.array(event['frequencies'], dtype=np.longdouble)
    signs = np.array(event['signs'], dtype=np.longdouble)
    occupation = 1 / np.expm1(frequencies)
    forward = occupation + (signs < 0)
    reverse = occupation + (signs > 0)
    shift = np.array([extended(value) for value in potential])
    gas = extended(gas)
    mean_subtracted = extended(state235.mean_energy(mp.nstr(scalar(event['temperature']), 85)) - 1)
    initial_score = ((extended(event['electron_initial'][0]) - 1) - mean_subtracted) / temperature
    transfer = np.array(event['electron_transfer'], dtype=np.longdouble)
    score_difference = -transfer[0] / temperature
    final_score = initial_score - score_difference
    forward_photon = np.sum(forward * shift)
    signed_photon = np.sum(signs * shift)
    reverse_change = final_score * gas + np.sum(reverse * shift)
    source_change = score_difference * gas - signed_photon
    photon = forward * source_change - signs * reverse_change + signs * (forward + reverse) * shift
    gas_change = score_difference * (initial_score + final_score - 2) * gas + score_difference * forward_photon - final_score * signed_photon
    initial_momentum = np.array(event['electron_initial'][1:], dtype=np.longdouble)
    velocity = (initial_momentum * source_change - transfer[1:] * (reverse_change - gas)) / temperature
    return dict(photon=photon.tolist(), gas=gas_change, velocity=velocity.tolist(), density=source_change)


def main():
    modest()
    config = protocol()
    target = ROOT / 'results/real-vertex.json'
    assert not target.exists()
    write(ROOT / 'real-configuration.json', dict(frozen_at=now(), script_sha256=digest(Path(__file__)),
        soft_frequencies=[1.2e-6, 1e-5, 1e-4, 1e-3], ray_indices=[0, 11, 23], tolerance=1e-10,
        longdouble_bits=np.finfo(np.longdouble).bits, full_real_integral_complete=False))
    original, features, models = setup(config)
    checks, records = [], []
    with mp.workdps(80):
        parent_config = read(BRANCH / 'mixed-angular-vertex-20261026/configuration.json')
        for row in config['events']:
            parameters, unused = source.physics.parameters_and_weight(row['theta'], row['node'])
            events = list(prior.selected_events(parameters, parent_config))
            rays = list(angular.inherited.source.angular_nodes(4))
            for index in (0, 11, 23):
                direction, unused = rays[index]
                doppler = angular.inherited.source.dot(parameters['bath'], np.r_[1., direction])
                for frequency in (1.2e-6, 1e-5, 1e-4, 1e-3):
                    for sign in (-1, 1):
                        events.append((f'floor{frequency}:ray{index}:sign{sign}', geometry(parameters, sign * frequency * row['theta'] / doppler, direction)))
            for name, event in events:
                frequencies = np.array(event['frequencies'])
                for join in config['joins']:
                    basis = features.evaluate(frequencies, join)
                    for state in config['states']:
                        physical = [scalar(config['heat']) * mp.mpf(value) for value in state['coefficients']]
                        potential = [state235.contraction(line, physical[:98]) for line in basis]
                        actual = stable_coefficients(event, potential, physical[-1])
                        expected = statistics(event, potential, physical[-1])['mixed']
                        actual_vector = [mp.mpf(str(value)) for value in prior.vector(actual)]
                        expected_vector = prior.vector(expected)
                        error = prior.mp_relative(actual_vector, expected_vector)
                        check(checks, f'{row["label"]}:{name}:join{join}:{state["model"]}:{state["history"]}:rearranged real coefficients', error)
                        records.append(dict(anchor=row['label'], event=name, join=join, model=state['model'], history=state['history'], relative_error=error,
                            maximum_photon_occupation=float(max(1 / np.expm1(frequencies)))))
            print(json.dumps(dict(anchor=row['label'], events=len(events), checks=len(checks), failed=sum(not entry['passed'] for entry in checks))), flush=True)
    failed = [entry for entry in checks if not entry['passed']]
    write(target, dict(state='complete', qualified=not failed, checks=checks, failed=failed, records=records, finished_at=now(),
        scope='Exact rearranged statistical real/Born vertex, compared to80-digit original; not integrated matched remainder'))
    print(json.dumps(dict(checks=len(checks), failed=failed, maximum_error=max(row['relative_error'] for row in records))), flush=True)
    assert not failed, failed


if __name__ == '__main__':
    main()
