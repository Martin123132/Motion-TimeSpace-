from common240 import *
import argparse
sys.path.insert(0, str(BRANCH / 'angular-source-gravity-bridge-20261027'))
from common238 import physical_states
COMPONENTS = ['leading_control', 'real_correction', 'virtual', 'state', 'MTS_correction', 'combined']


def freeze():
    config = protocol()
    assert not (ROOT / 'assessment-configuration.json').exists()
    write(ROOT / 'assessment-configuration.json', dict(frozen_at=now(), script_sha256=digest(__file__),
        configuration_sha256=digest(ROOT / 'configuration.json'), components=COMPONENTS,
        angular_comparison='4-to6 at radial26', radial_comparison='18-to26 at angular6 for the six new rows',
        event0_radial_owner='Existing Stage23618-to26 at angular4, independently retained',
        invariant_tolerance=config['identity_tolerance'], refinement_tolerance=config['refinement_tolerance'],
        sum='Already weighted event0+event1+event2, one electron node and one incident frequency only'))


def force_error(matrix):
    return float(np.linalg.norm(matrix[0] + matrix[-1]) / max(np.linalg.norm(matrix[0]) + np.linalg.norm(matrix[-1]), 1e-300))


def sum_real(row, order, radial, inputs, checks):
    values, compensation = {}, {}
    count = len(list(angular.inherited.source.angular_nodes(order)))
    for index in range(count):
        path = ((ROOT / 'real' / event_key(row) / f'angular{order}' / f'ray-{index:03d}.npz') if radial == 26 else
            ROOT / 'radial18' / event_key(row) / f'ray-{index:03d}.npz')
        metadata = read(register(inputs, path.with_suffix('.json')))
        assert metadata['angular_order'] == order and metadata['radial_order'] == radial and metadata['ray'] == index
        frozen = ROOT / ('configuration.json' if radial == 26 else 'radial-configuration.json')
        assert metadata['configuration_sha256'] == digest(frozen)
        register(inputs, path, metadata['sha256'])
        check(checks, f'{event_key(row)}:a{order}:r{radial}:ray{index}:event four-force', metadata['maximum_independent_four_force_residual'])
        for name, value in packet(path).items():
            if name not in values:
                values[name], compensation[name] = np.zeros_like(value), np.zeros_like(value)
            change = value - compensation[name]
            updated = values[name] + change
            compensation[name] = (updated - values[name]) - change
            values[name] = updated
    return values


def assess_difference(label, before, after, degree, checks, records, config):
    matrix_error = relative(before, after)
    gas_error = relative(before[-1], after[-1]) if degree < 2 else 0.
    photon_error = relative(before[1:-1], after[1:-1])
    for category, error in [('matrix', matrix_error), ('gas', gas_error), ('photon_shape', photon_error)]:
        check(checks, label + ':' + category, error, config['refinement_tolerance'])
    records.append(dict(name=label, degree=degree, matrix=matrix_error, gas=gas_error, photon_shape=photon_error,
        absolute_difference=float(np.linalg.norm(before - after)), reference_norm=float(np.linalg.norm(after))))


def new_event(config, row, inputs, checks, records):
    real = {(4, 26): sum_real(row, 4, 26, inputs, checks), (6, 26): sum_real(row, 6, 26, inputs, checks),
        (6, 18): sum_real(row, 6, 18, inputs, checks)}
    state_path = ROOT / 'state' / event_key(row) / 'state.npz'
    state_record = read(register(inputs, state_path.with_suffix('.json')))
    assert state_record['qualified']
    displaced = packet(register(inputs, state_path, state_record['sha256']))
    medium = {}
    for order in (4, 6):
        for join in config['joins']:
            path = ROOT / 'virtual' / event_key(row) / f'angular{order}-join{join}.npz'
            metadata = read(register(inputs, path.with_suffix('.json')))
            assert metadata['qualified']
            medium[order, join] = packet(register(inputs, path, metadata['sha256']))
    output = {}
    for join in config['joins']:
        for degree in config['multipoles']:
            for state_index in range(7):
                state = dict(model='equilibrium', history='equilibrium') if not state_index else config['states'][state_index - 1]
                variants = {}
                for order, radial in ((4, 26), (6, 26), (6, 18)):
                    leading = real[order, radial][f'control:join{join}:l{degree}:total'][state_index]
                    correction = real[order, radial][f'difference:join{join}:l{degree}:total'][state_index]
                    values = dict(leading_control=leading, real_correction=correction)
                    if state_index:
                        virtual = medium[order, join][f'state{state_index - 1}:l{degree}:total']
                        shifted = displaced[f'join{join}:state{state_index - 1}:l{degree}:step0.0005:total']
                        matched = correction + virtual + shifted
                        values.update(virtual=virtual, state=shifted, MTS_correction=matched, combined=leading + matched)
                    variants[order, radial] = values
                    if radial == 26:
                        for component, matrix in values.items():
                            key = f'angular{order}:join{join}:{state["model"]}:{state["history"]}:l{degree}:{component}'
                            output[key] = matrix
                            if degree < 2:
                                check(checks, event_key(row) + ':' + key + ':integrated four-force', force_error(matrix))
                for component in variants[6, 26]:
                    label = f'{event_key(row)}:join{join}:{state["model"]}:{state["history"]}:l{degree}:{component}'
                    assess_difference(label + ':angular4-to6', variants[4, 26][component], variants[6, 26][component], degree, checks, records, config)
                    assess_difference(label + ':radial18-to26', variants[6, 18][component], variants[6, 26][component], degree, checks, records, config)
                if state_index:
                    for part in ('statistical', 'background', 'wave'):
                        key = f'state{state_index - 1}:l{degree}:{part}'
                        label = f'{event_key(row)}:join{join}:{state["model"]}:{state["history"]}:l{degree}:virtual_{part}:angular4-to6'
                        assess_difference(label, medium[4, join][key], medium[6, join][key], degree, checks, records, config)
    return output


def hessians(config, summed, checks):
    exact, high, low = physical_states(config)
    output = {}
    for order in (4, 6):
        for join in config['joins']:
            for component in COMPONENTS:
                contracted = []
                for state in config['states']:
                    key = f'angular{order}:join{join}:{state["model"]}:{state["history"]}:l0:{component}'
                    contracted.append(precise.stable_dot(summed[key], high, low))
                for first in range(6):
                    key = f'angular{order}:join{join}:{config["states"][first]["model"]}:{config["states"][first]["history"]}:C2:{component}'
                    output[key] = contracted[first][:, first] / 2
                    for second in range(first + 1, 6):
                        forward, reverse = contracted[first][:, second], contracted[second][:, first]
                        scale = max(np.linalg.norm(forward), np.linalg.norm(reverse), 1e-300)
                        check(checks, key + f':crossed{first}-{second}', np.linalg.norm(forward - reverse) / scale)
                        gas_scale = max(abs(forward[-1]), abs(reverse[-1]), 1e-300)
                        check(checks, key + f':crossed gas{first}-{second}', abs(forward[-1] - reverse[-1]) / gas_scale)
    return output


def run(anchor):
    modest()
    config = protocol()
    frozen = read(ROOT / 'assessment-configuration.json')
    assert frozen['script_sha256'] == digest(__file__)
    assert frozen['configuration_sha256'] == digest(ROOT / 'configuration.json')
    assert not (ROOT / 'results' / (anchor + '-assessment.json')).exists()
    inputs, checks, records = {}, [], []
    old_path = REFERENCE / 'results' / (anchor + '-assessment.npz')
    old_report = read(REFERENCE / 'results' / (anchor + '-assessment.json'))
    old = packet(register(inputs, old_path, old_report['output_sha256']))
    summed = {name: value.copy() for name, value in old.items() if name.startswith(('angular4:', 'angular6:'))}
    per_event = {}
    for row in config['events']:
        if row['label'] != anchor:
            continue
        values = new_event(config, row, inputs, checks, records)
        assert set(values) == set(summed)
        for name in summed:
            summed[name] += values[name]
        per_event[event_key(row)] = values
        save(ROOT / 'results' / (event_key(row) + '-components.npz'), **values)
    for name in summed:
        if name.startswith('angular4:'):
            degree = int(name.split(':')[-2][1:])
            assess_difference(anchor + ':three-hard-angle-sum:' + name, summed[name], summed[name.replace('angular4:', 'angular6:', 1)],
                degree, checks, records, config)
        degree = int(name.split(':')[-2][1:])
        if degree < 2:
            check(checks, anchor + ':three-hard-angle-sum:' + name + ':independent four-force', force_error(summed[name]))
    density = hessians(config, summed, checks)
    target = ROOT / 'results' / (anchor + '-three-hard-angle-sum.npz')
    save(target, **summed, **density)
    failures = [entry for entry in checks if not entry['passed']]
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    report = dict(stage=240, anchor=anchor, state='complete', qualified=not failures, checks=checks, failed=failures,
        records=records, output_sha256=digest(target), consumed_inputs=inputs, script_sha256=digest(__file__),
        maximum_refinement=max(max(row['matrix'], row['gas'], row['photon_shape']) for row in records),
        scope='Three hard-angle quadrature at x14 and first electron node; two new angles individually refined; event0 reused',
        finished_at=now())
    write(ROOT / 'results' / (anchor + '-assessment.json'), report)
    print(json.dumps(dict(anchor=anchor, checks=len(checks), failures=len(failures), first_failures=failures[:8],
        maximum_refinement=report['maximum_refinement'])), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['freeze', 'warm', 'middle', 'cold'])
    arguments = parser.parse_args()
    freeze() if arguments.mode == 'freeze' else run(arguments.mode)
