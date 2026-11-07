from __future__ import annotations
import os
for variable in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[variable] = '1'
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import argparse
import hashlib
ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH / 'expanded-source-gravity-response-20261027'
SOURCE = BRANCH / 'hard-angle-source-expansion-20261027'
HISTORY = BRANCH / 'history-aware-operator-temperature-test-20261025'
sys.path[:0] = [str(PARENT), str(BRANCH / 'cold-source-temperature-connection-20261025')]
import common241 as prior
import connection208 as connection
from common241 import np, mp, read, write, save, packet, digest, register, check, modest, now, precise
SEAL = '409ddb91f6e6c6da76947d609e3a85924a3d144c0ba9496f48510617c45c0e2f'


def modules(inputs):
    for module in list(sys.modules.values()):
        filename = getattr(module, '__file__', None)
        if filename:
            path = Path(filename).resolve()
            if path.suffix == '.py' and path.is_relative_to(BRANCH) and not path.is_relative_to(ROOT):
                register(inputs, path)


def prepare():
    modest()
    assert not (ROOT / 'configuration.json').exists()
    inputs = {}
    seal = read(register(inputs, PARENT / 'results/stage-integrity.json', SEAL))
    assert seal['qualified']
    config = read(register(inputs, SOURCE / 'configuration.json'))
    history_config = read(register(inputs, HISTORY / 'configuration.json'))
    assert config['target_fraction'] == history_config['target_fraction']
    assert config['target_theta'] == history_config['theta']
    original, theta = connection.source.context(config['target_fraction'])
    assert theta == config['target_theta']
    for path in original.inputs:
        register(inputs, path)
    for model in ('heavy', 'cold'):
        for grid in ('half', 'quarter'):
            register(inputs, HISTORY / f'histories/{model}-{grid}.json')
    modules(inputs)
    write(ROOT / 'inputs.json', inputs)
    write(ROOT / 'configuration.json', dict(stage=242, started_at=now(), previous_goal_turn='progress',
        parent_seal=SEAL, states=config['states'], heat=config['heat'], target_theta=theta,
        target_fraction=config['target_fraction'], coordinate=original.coordinate,
        identity_tolerance=1e-10, history_mesh_tolerance=.01, refinement_tolerance=.002,
        working_digits=80, audit_digits=100, units='derivatives per u=ln(a/a_initial)',
        original_bank_changed=False, original_histories_changed=False, original_tolerances_changed=False,
        protocol_hashes={path.name: digest(path) for path in ROOT.iterdir() if path.suffix in ('.py', '.md')}))
    print(dict(prepared=True, inputs=len(inputs)), flush=True)


def protocol():
    config = read(ROOT / 'configuration.json')
    for name, expected in config['protocol_hashes'].items():
        assert digest(ROOT / name) == expected, name
    for path, expected in read(ROOT / 'inputs.json').items():
        assert digest(path) == expected, path
    return config


def norm(vector):
    return mp.sqrt(mp.fsum(value * value for value in vector))


def relative(first, second):
    return norm(first - second) / max(norm(second), mp.mpf('1e-300'))


def rhs(equation, state, coordinate, inverse):
    stiffness = equation.stiffness(coordinate)
    departure = state['profile'] - equation.template * state['gas']
    forcing = stiffness * departure
    profile = inverse * forcing
    work = 1 + equation.heat * state['gas']
    gas = -((equation.energy * profile)[0] + work) / equation.heat
    return dict(profile=profile, gas=gas, work=work), forcing


def flatten(state):
    return mp.matrix(list(state['profile']) + [mp.mpf(0), mp.mpf(0), state['gas']])


def predecessor(model, grid, target, inputs):
    owner = connection.evolution
    seed_path = connection.WARM / f'histories/{model}/{grid}/complete.json'
    register(inputs, seed_path)
    seed, previous_coordinate, unused = owner.schedule(model, grid)
    points = [dict(coordinate=previous_coordinate, state=seed['older']),
        dict(coordinate=seed['coordinate'], state=seed['current'])]
    chain = digest(seed_path)
    for path in sorted((connection.HISTORY / f'histories/{model}/{grid}/blocks').glob('*.json')):
        block = read(register(inputs, path))
        assert block['previous_chain'] == chain and all(row['passed'] for row in block['checks'])
        chain = hashlib.sha256((chain + digest(path)).encode()).hexdigest()
        points.extend(block['states'])
    complete = read(register(inputs, connection.HISTORY / f'histories/{model}/{grid}/complete.json'))
    assert complete['chain'] == chain
    earlier = [point for point in points if point['coordinate'] < target]
    return earlier[-2:], chain


def serial(state):
    return dict(profile=[mp.nstr(value, 85) for value in state['profile']],
        gas=mp.nstr(state['gas'], 85), work=mp.nstr(state['work'], 85))


def bracket(data, target):
    index = int(np.searchsorted(data['expansion'], target))
    assert 0 < index < len(data['expansion'])
    assert data['expansion'][index - 1] < target < data['expansion'][index]
    return index - 1, index


def saved_slope(data, key, target):
    left, right = bracket(data, target)
    width = mp.mpf(float(data['expansion'][right])) - mp.mpf(float(data['expansion'][left]))
    before = np.atleast_1d(data[key][left])
    after = np.atleast_1d(data[key][right])
    return mp.matrix([(mp.mpf(float(last)) - mp.mpf(float(first))) / width for first, last in zip(before, after)])


def run():
    modest()
    config = protocol()
    assert not (ROOT / 'results/history.json').exists()
    inputs, checks, records, arrays = dict(read(ROOT / 'inputs.json')), [], [], {}
    original, theta = connection.source.context(config['target_fraction'])
    states = config['states']
    owner = connection.evolution
    with mp.workdps(config['working_digits']):
        coordinate = mp.mpf(config['coordinate'])
        for model_index, model in enumerate(('heavy', 'cold')):
            candidate = owner.Equation(model)
            bank = owner.history.previous.ProbeEquation(model, 'bank')
            inverse = candidate.mass ** -1
            check(checks, model + ':same bank/candidate mass', norm(candidate.mass - bank.mass))
            check(checks, model + ':same saved heat scale', candidate.heat / mp.mpf(config['heat']) - 1)
            audit_results = {}
            with mp.workdps(config['audit_digits']):
                audit_candidate = owner.Equation(model)
                audit_bank = owner.history.previous.ProbeEquation(model, 'bank')
                audit_inverse = audit_candidate.mass ** -1
                for state in [row for row in states if row['model'] == model]:
                    vector = list(map(mp.mpf, state['coefficients']))
                    physical = dict(profile=mp.matrix(vector[:96]), gas=vector[-1], work=mp.mpf(0))
                    equation = audit_bank if state['history'] == 'original' else audit_candidate
                    audit_results[state['history']] = rhs(equation, physical, coordinate, audit_inverse)[0]
            for state in [row for row in states if row['model'] == model]:
                history = state['history']
                vector = list(map(mp.mpf, state['coefficients']))
                physical = dict(profile=mp.matrix(vector[:96]), gas=vector[-1], work=mp.mpf(0))
                equation = bank if history == 'original' else candidate
                result, forcing = rhs(equation, physical, coordinate, inverse)
                prefix = model + ':' + history
                check(checks, prefix + ':kinetic RHS residual', relative(equation.mass * result['profile'], forcing))
                energy = (equation.energy * result['profile'])[0] + equation.heat * result['gas'] + result['work']
                scale = abs((equation.energy * result['profile'])[0]) + abs(equation.heat * result['gas']) + abs(result['work'])
                check(checks, prefix + ':photon gas work identity', abs(energy) / scale)
                audit = audit_results[history]
                check(checks, prefix + ':80/100 profile', relative(result['profile'], audit['profile']))
                check(checks, prefix + ':80/100 gas', abs(result['gas'] / audit['gas'] - 1))
                if history != 'original':
                    record = read(register(inputs, HISTORY / f'histories/{model}-{history}.json'))
                    assert not record['failed_checks'] and record['coordinate'] == config['coordinate']
                    owned = owner.history.parse_state(record['current'])
                    check(checks, prefix + ':exact saved profile ownership', relative(physical['profile'], owned['profile']), 0)
                    check(checks, prefix + ':exact saved gas ownership', physical['gas'] - owned['gas'], 0)
                    points, chain = predecessor(model, history, config['coordinate'], inputs)
                    assert chain == record['source_chain'] and points[-1]['coordinate'] == record['previous_coordinate']
                    older, current = [owner.history.parse_state(point['state']) for point in points]
                    step = coordinate - mp.mpf(points[-1]['coordinate'])
                    previous_step = mp.mpf(points[-1]['coordinate']) - mp.mpf(points[-2]['coordinate'])
                    ratio = step / previous_step
                    coefficient = (1 + 2 * ratio) / (1 + ratio)
                    older_weight = ratio ** 2 / (1 + ratio)
                    bdf = {key: (coefficient * (owned[key] - current[key]) - older_weight * (current[key] - older[key])) / step
                        for key in ('profile', 'gas', 'work')}
                    check(checks, prefix + ':BDF2 profile derivative', relative(bdf['profile'], result['profile']))
                    check(checks, prefix + ':BDF2 gas derivative', abs(bdf['gas'] / result['gas'] - 1))
                    check(checks, prefix + ':BDF2 work derivative', abs(bdf['work'] / result['work'] - 1))
                else:
                    expected = original.epochs[0].original[model]
                    check(checks, prefix + ':original coefficient ownership',
                        norm(physical['profile'] - mp.matrix([mp.mpf(float(value)) for value in expected])), 0)
                    check(checks, prefix + ':original gas ownership', physical['gas'] - mp.mpf(original.gas[model_index]), 0)
                    path = Path(original.inputs[4 * model_index])
                    data = packet(register(inputs, path))
                    slope = dict(profile=saved_slope(data, 'profiles', config['coordinate']),
                        gas=saved_slope(data, 'temperature_scaled', config['coordinate'])[0], work=mp.mpf(0))
                    smooth_result, unused = rhs(candidate, physical, coordinate, inverse)
                    records.append(dict(model=model, history=history, interpolant_derivative=serial(slope),
                        smooth_operator_on_same_state=serial(smooth_result),
                        interpolant_profile_residual=float(relative(slope['profile'], result['profile'])),
                        interpolant_gas_residual=float(abs(slope['gas'] / result['gas'] - 1)),
                        smooth_vs_bank_profile=float(relative(smooth_result['profile'], result['profile'])),
                        smooth_vs_bank_gas=float(abs(smooth_result['gas'] / result['gas'] - 1))))
                exact = flatten(result)
                high = np.array([float(value) for value in exact])
                low = np.array([float(value - mp.mpf(float(part))) for value, part in zip(exact, high)])
                arrays[prefix + ':high'], arrays[prefix + ':low'] = high, low
                records.append(dict(model=model, history=history, rhs=serial(result), coefficient_tangent=[mp.nstr(value, 85) for value in exact]))
                print(dict(history_tangent=prefix, checks=len(checks), failed=sum(not row['passed'] for row in checks)), flush=True)
            left = next(row for row in records if row['model'] == model and row['history'] == 'half' and 'rhs' in row)
            right = next(row for row in records if row['model'] == model and row['history'] == 'quarter' and 'rhs' in row)
            half = owner.history.parse_state(left['rhs'])
            quarter = owner.history.parse_state(right['rhs'])
            check(checks, model + ':history tangent mesh photon', relative(half['profile'], quarter['profile']), config['history_mesh_tolerance'])
            check(checks, model + ':history tangent mesh gas', abs(half['gas'] / quarter['gas'] - 1), config['history_mesh_tolerance'])
            tail_path = Path(original.inputs[4 * model_index + 2])
            data = packet(register(inputs, tail_path))
            tail = saved_slope(data, 'slope', config['coordinate'])
            current = mp.matrix([mp.mpf(float(value)) for value in original.epochs[0].tails[model][1]])
            projection = mp.fsum(first * second for first, second in zip(tail, current)) / mp.fsum(value * value for value in current)
            remainder = tail - projection * current
            arrays[model + ':tail_frequency'] = data['frequency']
            arrays[model + ':tail_slope_derivative'] = np.array(list(map(float, tail)))
            records.append(dict(model=model, kind='external_saved_tail_tangent', source_path=str(tail_path),
                relative_size=float(norm(tail) / norm(current)), proportional_coefficient=mp.nstr(projection, 85),
                nonproportional_fraction=float(norm(remainder) / norm(tail)),
                note='Diagnostic projection only, never a replacement for the full shape tangent.',
                derivative=[mp.nstr(value, 85) for value in tail]))
    modules(inputs)
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    output = ROOT / 'results/history-tangents.npz'
    save(output, **arrays)
    failures = [row for row in checks if not row['passed']]
    write(ROOT / 'results/history.json', dict(stage=242, qualified=not failures, checks=checks, failed=failures,
        records=records, consumed_inputs=inputs, output_sha256=digest(output), finished_at=now(),
        source_contraction_complete=False, full_source_derivative_complete=False))
    print(dict(history_complete=True, checks=len(checks), failed=failures), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['prepare', 'run'])
    arguments = parser.parse_args()
    prepare() if arguments.phase == 'prepare' else run()
