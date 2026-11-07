from common243 import *
import argparse
import hashlib
import time


def freeze():
    config = protocol()
    assert not (ROOT / 'replay-configuration.json').exists()
    write(ROOT / 'replay-configuration.json', dict(frozen_at=now(), script_sha256=digest(__file__),
        configuration_sha256=digest(ROOT / 'configuration.json'),
        method='Exact original Stage199 variable-step replay,80-digit state and100-digit final-step audit',
        identity_tolerance=config['identity_tolerance'], models=['heavy', 'cold'], grids=['half', 'quarter'],
        block_size=8, prior_bank_modified=False))


def replay_protocol():
    config = protocol()
    frozen = read(ROOT / 'replay-configuration.json')
    assert frozen['script_sha256'] == digest(__file__)
    assert frozen['configuration_sha256'] == digest(ROOT / 'configuration.json')
    return config


def run(model):
    modest()
    config = replay_protocol()
    status_path = DATA / 'workers' / f'replay-{model}.json'
    write(status_path, dict(state='running', pid=os.getpid(), model=model, started_at=now()))
    for case in [row for row in config['cases'] if row['model'] == model]:
        grid = case['grid']
        folder = DATA / 'replayed199' / model / grid
        if (folder / 'complete.json').exists():
            result = read(folder / 'complete.json')
            assert result['qualified'] and result['runner_sha256'] == digest(__file__)
            continue
        inputs = dict(read(ROOT / 'inputs.json'))
        expected = read(register(inputs, continued.ROOT / f'histories/{model}/{grid}/complete.json'))
        old, unused, old_chain = history.read_history(model, 'candidate', grid)
        assert old_chain == expected['source_chain_sha256'] == case['stage189_chain']
        start, step, target = case['stage189_stop'], case['step'], case['stage199_stop']
        coordinates, index = [], 1
        while start + index * step < target - 1e-14:
            coordinates.append(start + index * step)
            index += 1
        coordinates.append(target)
        assert len(coordinates) == case['missing_steps']
        restart_path = folder / 'restart.json'
        restart = read(restart_path) if restart_path.exists() else dict(done=0, current=old[-1], older=old[-2], chain=None)
        chain = None
        for path in sorted((folder / 'blocks').glob('*.json')):
            block = read(path)
            assert block['previous_hash'] == chain and block['stop'] <= restart['done']
            assert block['runner_sha256'] == digest(__file__) and all(row['passed'] for row in block['checks'])
            chain = digest(path)
        assert chain == restart['chain']
        with mp.workdps(80):
            equation = continued.ContinuedEquation(model, 'candidate')
            current, older = history.parse_state(restart['current']), history.parse_state(restart['older'])
            rows, diagnostics, states = [], [], []
            block_start = restart['done']
            for ordinal in range(restart['done'], len(coordinates)):
                before = start if ordinal == 0 else coordinates[ordinal - 1]
                before_previous = start - step if ordinal == 0 else start if ordinal == 1 else coordinates[ordinal - 2]
                delta = mp.mpf(coordinates[ordinal]) - mp.mpf(before)
                previous_delta = mp.mpf(before) - mp.mpf(before_previous)
                updated, diagnostic = equation.advance(current, older, mp.mpf(coordinates[ordinal]), delta, previous_delta)
                rows.extend(history.identity_rows([dict(diagnostic, ordinal=ordinal)]))
                if ordinal == len(coordinates) - 1:
                    with mp.workdps(100):
                        independent = continued.ContinuedEquation(model, 'candidate')
                        audited, unused = independent.advance(current, older, mp.mpf(coordinates[ordinal]), delta, previous_delta)
                        check(rows, '80/100 final profile', prior.relative(updated['profile'], audited['profile']))
                        check(rows, '80/100 final gas', abs(updated['gas'] / audited['gas'] - 1))
                    for label, actual, expected_state in [('current', updated, expected['current']), ('older', current, expected['older'])]:
                        saved_state = history.parse_state(expected_state)
                        check(rows, label + ':saved profile replay', prior.relative(actual['profile'], saved_state['profile']))
                        check(rows, label + ':saved gas replay', actual['gas'] - saved_state['gas'])
                        check(rows, label + ':saved work replay', actual['work'] - saved_state['work'])
                assert all(row['passed'] for row in rows), [row for row in rows if not row['passed']]
                older, current = current, updated
                states.append(dict(coordinate=coordinates[ordinal], state=history.previous.serial_state(current)))
                diagnostics.append(diagnostic)
                final = ordinal == len(coordinates) - 1
                if len(states) == 8 or final:
                    path = folder / 'blocks' / f'{block_start:04d}-{ordinal + 1:04d}.json'
                    assert not path.exists()
                    write(path, dict(start=block_start, stop=ordinal + 1, previous_hash=chain, runner_sha256=digest(__file__),
                        states=states, diagnostics=diagnostics, checks=rows))
                    chain = digest(path)
                    restart = dict(done=ordinal + 1, current=history.previous.serial_state(current),
                        older=history.previous.serial_state(older), chain=chain, coordinate=coordinates[ordinal],
                        runner_sha256=digest(__file__))
                    write(restart_path, restart)
                    print(dict(model=model, grid=grid, recovered=ordinal + 1, total=len(coordinates)), flush=True)
                    states, rows, diagnostics, block_start = [], [], [], ordinal + 1
            modules(inputs)
            for path, checksum in inputs.items():
                assert digest(path) == checksum, path
            write(folder / 'complete.json', dict(restart, qualified=True, model=model, grid=grid,
                expected_endpoint_sha256=digest(continued.ROOT / f'histories/{model}/{grid}/complete.json'),
                input_chain=old_chain, consumed_inputs=inputs, finished_at=now()))
    write(status_path, dict(state='complete', pid=os.getpid(), model=model, finished_at=now()))


def assemble():
    modest()
    config = replay_protocol()
    inputs, checks, cases = dict(read(ROOT / 'inputs.json')), [], []
    for case in config['cases']:
        model, grid = case['model'], case['grid']
        folder = DATA / 'replayed199' / model / grid
        report = read(register(inputs, folder / 'complete.json'))
        assert report['qualified'] and report['runner_sha256'] == digest(__file__)
        original_states, unused, chain = history.read_history(model, 'candidate', grid)
        assert chain == report['input_chain']
        reference = packet(register(inputs, history.directory(model, 'candidate', grid) / 'reference.npz'))
        coordinates = list(map(float, reference['expansion']))
        points = [dict(coordinate=coordinate, state=state, owner=189) for coordinate, state in zip(coordinates, original_states)]
        chain = None
        for path in sorted((folder / 'blocks').glob('*.json')):
            block = read(register(inputs, path))
            assert block['previous_hash'] == chain
            chain = digest(path)
            points.extend(dict(row, owner=199) for row in block['states'])
            checks.extend(dict(row, name=f'{model}:{grid}:' + row['name']) for row in block['checks'])
        assert chain == report['chain']
        seed_path = continued.ROOT / f'histories/{model}/{grid}/complete.json'
        chain = digest(register(inputs, seed_path))
        for path in sorted((connection.HISTORY / f'histories/{model}/{grid}/blocks').glob('*.json')):
            block = read(register(inputs, path))
            assert block['previous_chain'] == chain and all(row['passed'] for row in block['checks'])
            chain = hashlib.sha256((chain + digest(path)).encode()).hexdigest()
            points.extend(dict(row, owner=200) for row in block['states'] if row['coordinate'] < config['target_coordinate'])
        complete = read(register(inputs, connection.HISTORY / f'histories/{model}/{grid}/complete.json'))
        assert complete['chain'] == chain
        target_path = prior.HISTORY / f'histories/{model}-{grid}.json'
        target = read(register(inputs, target_path))
        assert target['source_chain'] == chain and not target['failed_checks']
        assert points[-1]['coordinate'] == target['previous_coordinate']
        points.append(dict(coordinate=target['coordinate'], state=target['current'], owner=209))
        assert points[0]['coordinate'] == case['start'] and points[-1]['coordinate'] == config['target_coordinate']
        assert all(last['coordinate'] > first['coordinate'] for first, last in zip(points[:-1], points[1:]))
        metadata = read(register(inputs, history.directory(model, 'candidate', grid) / 'reference.json'))
        destination = DATA / 'drives' / f'{model}-{grid}.json'
        write(destination, dict(model=model, grid=grid, points=points, previous=metadata['previous'],
            previous_step=case['step'] * dict(half=2, quarter=4)[grid], source_chain_189=case['stage189_chain'],
            source_chain_200=chain, target_sha256=digest(target_path), qualified=True,
            reconstruction='Saved discrete physical states; continuous drive reconstruction must be declared separately'))
        cases.append(dict(model=model, grid=grid, points=len(points), start=points[0]['coordinate'],
            stop=points[-1]['coordinate'], path=str(destination), sha256=digest(destination)))
    modules(inputs)
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    write(DATA / 'drives/validation.json', dict(qualified=all(row['passed'] for row in checks), checks=checks,
        failed=[row for row in checks if not row['passed']], cases=cases, consumed_inputs=inputs, finished_at=now()))
    print(dict(assembled=True, cases=cases, checks=len(checks)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['freeze', 'heavy', 'cold', 'assemble'])
    arguments = parser.parse_args()
    if arguments.phase == 'freeze':
        freeze()
    elif arguments.phase == 'assemble':
        assemble()
    else:
        run(arguments.phase)
