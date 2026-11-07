from common238 import *


def run():
    modest()
    config = protocol()
    basis = packet(ROOT / 'frozen/basis.npz')
    mass = np.triu(basis['mass']) + np.triu(basis['mass'], 1).T
    with mp.workdps(100):
        exact_energy = [mp.fsum(scalar(basis['temperature'][index]) * scalar(mass[index, column]) for index in (0, 1)) for column in range(96)]
        energy_high = np.array([float(value) for value in exact_energy])[:, None]
        energy_low = np.array([float(value - scalar(float(value))) for value in exact_energy])[:, None]
    temperature = basis['temperature'][:, None]
    records = []
    for event in config['events']:
        matrices = packet(PARENT / 'results' / (event['label'] + '-assessment.npz'))
        ports = packet(ROOT / 'results' / (event['label'] + '-ports.npz'))
        contexts = read(ROOT / 'results' / (event['label'] + '-contexts.json'))
        for state, context in zip(config['states'], contexts):
            opacity = context['opacity']
            for version in config['angular_versions']:
                for join in config['joins']:
                    for degree in config['multipoles']:
                        for component in config['components']:
                            key = f'angular{version}:join{join}:{state["model"]}:{state["history"]}:l{degree}:{component}'
                            weak = matrices[key]
                            source = ports[key + ':photon']
                            protected_weak = opacity * precise.stable_dot(weak[1:-1].T, temperature, np.zeros_like(temperature))[:, 0]
                            protected_solve = precise.stable_dot(source.T, energy_high, energy_low)[:, 0] / (2 * degree + 1)
                            expected = opacity * weak[0]
                            records.append(dict(anchor=event['label'], key=key,
                                raw=relative(ports[key + ':photon_moment'], expected),
                                weak_moment=relative(protected_weak, expected),
                                same_mass_readout=relative(protected_solve, expected),
                                same_mass_versus_weak=relative(protected_solve, protected_weak)))
    report = dict(records=records, maximums={name: max(row[name] for row in records)
        for name in ('raw', 'weak_moment', 'same_mass_readout', 'same_mass_versus_weak')},
        finished_at=now(), script_sha256=digest(__file__), inputs_changed=False)
    write(ROOT / 'results/precision-diagnosis.json', report)
    print(json.dumps(report['maximums']), flush=True)


if __name__ == '__main__':
    run()
