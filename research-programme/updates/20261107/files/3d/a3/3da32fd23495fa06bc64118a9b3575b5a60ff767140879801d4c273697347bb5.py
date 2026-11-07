from common238 import *
import itertools


def run():
    modest()
    config = protocol()
    target = ROOT / 'results/hessian.json'
    assert not target.exists()
    exact, high, low = physical_states(config)
    checks, records, output = [], [], {}
    for event in config['events']:
        anchor = event['label']
        saved = packet(PARENT / 'results' / (anchor + '-assessment.npz'))
        for version in config['angular_versions']:
            for join in config['joins']:
                for component in config['components']:
                    applied = []
                    for state_index, state in enumerate(config['states']):
                        key = f'angular{version}:join{join}:{state["model"]}:{state["history"]}:l0:{component}'
                        matrix = saved[key]
                        result = precise.stable_dot(matrix, high, low)
                        applied.append(result)
                        output[key.replace(':l0:', ':quadratic_background:')] = .5 * result[:, state_index]
                    for first, second in itertools.combinations(range(len(config['states'])), 2):
                        left, right = applied[first][:, second], applied[second][:, first]
                        denominator = max(np.linalg.norm(left) + np.linalg.norm(right), 1e-300)
                        error = float(2 * np.linalg.norm(left - right) / denominator)
                        prefix = f'{anchor}:angular{version}:join{join}:{component}:B{first}:B{second}'
                        check(checks, prefix + ':mixed derivative exchange', error, config['identity_tolerance'])
                        gas_scale = max(abs(left[-1]) + abs(right[-1]), 1e-300)
                        gas_error = float(2 * abs(left[-1] - right[-1]) / gas_scale)
                        check(checks, prefix + ':gas mixed derivative exchange', gas_error, config['identity_tolerance'])
                        records.append(dict(anchor=anchor, angular_version=version, join=join, component=component,
                            first=first, second=second, vector_error=error, gas_error=gas_error))
        print(json.dumps(dict(anchor=anchor, checks=len(checks), failures=sum(not row['passed'] for row in checks))), flush=True)
        save(ROOT / 'results' / (anchor + '-quadratic-background.npz'), **output)
        output = {}
    failures = [row for row in checks if not row['passed']]
    report = dict(stage=238, state='complete', qualified=not failures, checks=checks, failed=failures,
        records=records, maximum_vector_error=max(row['vector_error'] for row in records),
        maximum_gas_error=max(row['gas_error'] for row in records), script_sha256=digest(__file__),
        scope='Crossed monopole Hessian on all six saved histories; algebraic homogeneity of the retained Taylor order remains explicit', finished_at=now())
    write(target, report)
    print(json.dumps(dict(checks=len(checks), failures=len(failures), maximum_vector_error=report['maximum_vector_error'],
        maximum_gas_error=report['maximum_gas_error'], first_failures=failures[:8])), flush=True)


if __name__ == '__main__':
    run()
