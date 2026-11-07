from common240 import *


def run():
    modest()
    config = protocol()
    assert not (ROOT / 'results/preflight.json').exists()
    checks, records = [], []
    nodes = list(angular.inherited.source.angular_nodes(4))
    with mp.workdps(80):
        for row in config['events']:
            parameters, weight = source.physics.parameters_and_weight(row['theta'], row['node'])
            for ray in (0, 11, 23):
                owner = RationalDirection(precise_context(parameters), nodes[ray][0])
                check(checks, event_key(row) + f':ray{ray}:soft residue', abs(owner.soft_residue() / owner.pole['full'] - 1))
                for frequency in (1.2e-6, 1.37123456789, 3.):
                    for sign in (1, -1):
                        signed = sign * scalar(frequency) * owner.temperature / owner.doppler
                        candidate, event = owner.densities(signed)
                        reference, unused = Direction.densities(owner, signed)
                        for component in ('full', 'control', 'difference'):
                            for subtract in (False, True):
                                pole = owner.pole[component] / abs(signed) if subtract else 0
                                error = abs(candidate[component] - reference[component]) / max(abs(reference[component] - pole), mp.mpf('1e-300'))
                                check(checks, f'{event_key(row)}:ray{ray}:x{frequency}:sign{sign}:{component}:subtract{subtract}', error)
                        records.append(dict(event=event_key(row), ray=ray, frequency=frequency, sign=sign, weight=weight))
    failures = [row for row in checks if not row['passed']]
    result = dict(stage=240, qualified=not failures, checks=checks, failed=failures, records=records,
        maximum_error=max(row['value'] for row in checks), script_sha256=digest(__file__), finished_at=now())
    write(ROOT / 'results/preflight.json', result)
    print(json.dumps(dict(checks=len(checks), failures=failures[:5], maximum_error=result['maximum_error'])), flush=True)


if __name__ == '__main__':
    run()
