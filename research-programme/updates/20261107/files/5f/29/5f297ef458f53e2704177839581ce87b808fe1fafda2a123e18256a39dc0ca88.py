from common235 import *
import state235


def main():
    modest()
    config, frozen = state235.state_protocol()
    assert not (ROOT / 'results/state-replay.json').exists()
    write(ROOT / 'replay-configuration.json', dict(frozen_at=now(), script_sha256=digest(Path(__file__)),
        tolerance=1e-7, tolerance_owner=str(BRANCH / 'matched-angular-source-20261026/configuration.json'),
        scope='Original equilibrium displaced-state matrix limit on its retained97 columns; added mixed terms are tested separately'))
    original, features, models = setup(config)
    checks, records = [], []
    for row in config['events']:
        parameters, weight = source.physics.parameters_and_weight(row['theta'], row['node'])
        path = ROOT / 'runs' / row['label'] / 'state.npz'
        current = packet(path)
        retained = list(range(96)) + [98]
        with mp.workdps(80):
            for step in config['canonical_steps']:
                independent = models[0]['difference'].state_correction(parameters, step=step)['total']
                for join in config['joins']:
                    source_block = weight * independent[:, join::2][:, :-1]
                    predicted = current[f'join{join}:state0:l0:step{step}:equilibrium'][:, retained]
                    error = relative(predicted, -source_block)
                    check(checks, f'{row["label"]}:join{join}:step{step}:original positive-weak convention replay', error, 1e-7)
                    records.append(dict(anchor=row['label'], join=join, step=step, relative_error=error))
    failed = [entry for entry in checks if not entry['passed']]
    write(ROOT / 'results/state-replay.json', dict(state='complete', qualified=not failed, checks=checks, failed=failed, records=records, finished_at=now()))
    print(json.dumps(dict(checks=len(checks), failed=failed, maximum_relative_error=max(row['relative_error'] for row in records))), flush=True)
    assert not failed, failed


if __name__ == '__main__':
    main()
