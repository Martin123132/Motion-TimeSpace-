from run233 import *


def dagger(matrix):
    return matrix.transpose_conj()


def anti(first, second):
    return (first * second + second * first) / 2


def pair(first, second, channels, forward, reverse):
    identity = mp.eye(2)
    gain = lambda matrix: sum((channel * matrix * dagger(channel) for channel in channels), mp.zeros(2))
    adjoint = lambda matrix: sum((dagger(channel) * matrix * channel for channel in channels), mp.zeros(2))
    initial = reverse * anti(identity + first, adjoint(second)) - forward * anti(first, adjoint(identity + second))
    final = forward * anti(identity + second, gain(first)) - reverse * anti(second, gain(identity + first))
    return initial, final


def combined_norm(values):
    return mp.sqrt(mp.fsum(abs(value)**2 for matrix in values for value in matrix))


def main():
    modest()
    config, frozen = run_protocol()
    target = ROOT / 'results/polarization.json'
    assert not target.exists()
    write(ROOT / 'polarization-configuration.json', dict(frozen_at=now(), script_sha256=digest(Path(__file__)), tolerance=1e-10,
        scope='Actual Born spin channels in their own transported frames; not a complete polarized matched hierarchy'))
    original, features, unused = setup(config)
    checks, records = [], []
    with mp.workdps(80):
        pauli = [mp.eye(2), mp.matrix([[1, 0], [0, -1]]), mp.matrix([[0, 1], [1, 0]]), mp.matrix([[0, -mp.j], [mp.j, 0]])]
        for row in config['events']:
            parameters, weight = source.physics.parameters_and_weight(row['theta'], row['node'])
            tensor, mueller, unused = angular.inherited.source.tree_map(parameters)
            mp.mp.dps = 80
            channels = [mp.matrix([[mp.mpc(complex(value)) for value in line] for line in matrix])
                for matrix in tensor.transpose(2, 3, 1, 0).reshape(4, 2, 2)]
            event = geometry(parameters)
            frequencies = np.array(event['frequencies'])
            reference = [1 / mp.expm1(scalar(value)) for value in frequencies]
            susceptibility = [value * (1 + value) for value in reference]
            for state in config['states']:
                coefficient = list(map(mp.mpf, state['coefficients']))
                for join in config['joins']:
                    values = features.evaluate(frequencies, join)
                    potential = [scalar(config['heat']) * mp.fsum(scalar(value) * coeff for value, coeff in zip(line, coefficient[:98])) for line in values]
                    gas = scalar(config['heat']) * coefficient[-1]
                    stats = statistics(event, potential, gas)
                    population = [value + thermal * shift for value, thermal, shift in zip(reference, susceptibility, potential)]
                    rate_forward = electron_ratio(scalar(event['electron_initial'][0]), scalar(row['theta']), 1 + gas)[0]
                    rate_reverse = electron_ratio(scalar(event['electron_initial'][0]) + scalar(event['electron_transfer'][0]), scalar(row['theta']), 1 + gas)[0]
                    forward = rate_forward / (reference[0] * (1 + reference[1]))
                    reverse = rate_reverse / (reference[1] * (1 + reference[0]))
                    left_coefficient = susceptibility[0] * (forward * (1 + population[1]) - reverse * population[1])
                    right_coefficient = susceptibility[1] * (reverse * (1 + population[0]) - forward * population[0])
                    prefix = f'{row["label"]}:{state["model"]}:{state["history"]}:join{join}'
                    check(checks, prefix + ':scalar incoming derivative', abs(left_coefficient - stats['exact']['photon'][0]))
                    check(checks, prefix + ':scalar outgoing derivative', abs(right_coefficient + stats['exact']['photon'][1]))
                    for polarization, incoming_wave in enumerate(pauli):
                        outgoing_wave = pauli[(polarization + 1) % 4] / 3
                        gain = lambda matrix: sum((channel * matrix * dagger(channel) for channel in channels), mp.zeros(2))
                        adjoint = lambda matrix: sum((dagger(channel) * matrix * channel for channel in channels), mp.zeros(2))
                        predicted = (right_coefficient * adjoint(outgoing_wave) - left_coefficient * anti(incoming_wave, adjoint(mp.eye(2))),
                            left_coefficient * gain(incoming_wave) - right_coefficient * anti(outgoing_wave, gain(mp.eye(2))))
                        step = mp.mpf('1e-20')
                        positive = pair(population[0] * mp.eye(2) + step * susceptibility[0] * incoming_wave,
                            population[1] * mp.eye(2) + step * susceptibility[1] * outgoing_wave, channels, forward, reverse)
                        negative = pair(population[0] * mp.eye(2) - step * susceptibility[0] * incoming_wave,
                            population[1] * mp.eye(2) - step * susceptibility[1] * outgoing_wave, channels, forward, reverse)
                        measured = tuple((after - before) / (2 * step) for after, before in zip(positive, negative))
                        difference = tuple(value - expected for value, expected in zip(measured, predicted))
                        check(checks, prefix + f':pol{polarization}:nonlinear matrix derivative', combined_norm(difference) / combined_norm(predicted))
                        trace = lambda matrix: matrix[0, 0] + matrix[1, 1]
                        check(checks, prefix + f':pol{polarization}:trace exchange', abs(trace(predicted[0]) + trace(predicted[1])) / combined_norm(predicted))
                        for side, matrix in enumerate(predicted):
                            check(checks, prefix + f':pol{polarization}:side{side}:Hermitian', mp.norm(matrix - dagger(matrix)) / combined_norm(predicted))
                    records.append(dict(anchor=row['label'], model=state['model'], history=state['history'], join=join,
                        intensity_from_Q=float(mueller[0, 1] / mueller[0, 0]), Q_from_intensity=float(mueller[1, 0] / mueller[0, 0]),
                        statistical_incoming_mixed=float(stats['mixed']['photon'][0]), statistical_outgoing_mixed=float(stats['mixed']['photon'][1])))
    failed = [row for row in checks if not row['passed']]
    write(target, dict(state='complete', checks=checks, failed=failed, qualified=not failed, records=records, finished_at=now(),
        reused_owner='moving-polarized-thermal-20261008/polarized_source.py:tree_map', new_virtual_integrals=0,
        scope='Polarized Born event derivative about actual saved scalar occupations; full polarized angular projection and matched NLO remain separate'))
    print(json.dumps(dict(polarization_checks=len(checks), failed=failed, maximum_I_Q=max(abs(row['intensity_from_Q']) for row in records))), flush=True)
    assert not failed, failed


if __name__ == '__main__':
    main()
