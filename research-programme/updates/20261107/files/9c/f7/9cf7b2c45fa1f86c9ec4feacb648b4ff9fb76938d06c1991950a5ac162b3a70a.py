from history242 import *
import time
import types
from datetime import datetime, timezone
sys.path.insert(0, str(SOURCE))
import common240 as retained
import virtual240 as virtual_owner
import assess240 as assessment
import state235
from common240 import angular, scalar, source
TARGET = ROOT / 'target'


def clone(function, **bindings):
    namespace = dict(function.__globals__)
    namespace.update(bindings)
    return types.FunctionType(function.__code__, namespace, function.__name__, function.__defaults__, function.__closure__)


def prepare_target():
    modest()
    base = protocol()
    assert not (TARGET / 'configuration.json').exists()
    inherited = read(SOURCE / 'configuration.json')
    inputs = dict(read(ROOT / 'inputs.json'))
    old = read(register(inputs, HISTORY / 'configuration.json'))
    events = []
    for original in old['target'][:3]:
        row = dict(original, label='target')
        assert row['node']['frequency'] == 14 and row['node']['electron_index'] == 0
        stem = HISTORY / 'target' / f'event-{row["event"]:02d}'
        report = read(register(inputs, stem.with_suffix('.json')))
        assert not report['failed_checks']
        row['source_path'] = str(register(inputs, stem.with_suffix('.npz'), report['sha256']))
        row['source_sha256'] = report['sha256']
        row['loop_path'] = str(register(inputs, report['loop_path'], report['loop_sha256']))
        row['loop_sha256'] = report['loop_sha256']
        parameters, weight = source.physics.parameters_and_weight(row['theta'], row['node'])
        assert weight == row['weight'] and row['theta'] == base['target_theta']
        assert read(row['loop_path'])['identity'] == source.physics.event_owner.inherited.virtual_identity(parameters)
        events.append(row)
    for join in (0, 1):
        register(inputs, virtual_owner.retained_virtual.VIRTUAL / 'radial' / f'join{join}-order6.npz')
    modules(inputs)
    config = {key: inherited[key] for key in ('states', 'heat', 'target_fraction', 'target_theta',
        'spectral_domain', 'maximum_log_width', 'angular_orders', 'radial_order', 'virtual_radial_order',
        'digits', 'virtual_digits', 'joins', 'multipoles', 'canonical_steps', 'identity_tolerance',
        'refinement_tolerance', 'same_discretization_replay_tolerance')}
    config.update(stage=242, frozen_at=now(), events=events,
        deadline_timestamp=datetime(2026, 10, 27, 13, 20, tzinfo=timezone.utc).timestamp(),
        script_sha256=digest(__file__), target_history_theta_owned=True, input_manifest=inputs,
        source_scope='x14, first electron, all three saved hard angles; target temperature, same saved six states',
        tail_tangent_included=False, explicit_operator_derivative_included=False,
        original_bank_changed=False, original_tolerances_changed=False)
    write(TARGET / 'configuration.json', config)
    print(dict(target_frozen=True, events=3, full_real_rays=528), flush=True)


def target_protocol():
    config = read(TARGET / 'configuration.json')
    assert digest(__file__) == config['script_sha256']
    for path, expected in config['input_manifest'].items():
        assert digest(path) == expected, path
    return config


def jobs(config):
    for row in config['events']:
        for order, radial in ((4, 26), (6, 26), (6, 18)):
            count = len(list(angular.inherited.source.angular_nodes(order)))
            for ray in range(count):
                stem = ((TARGET / 'real' / retained.event_key(row) / f'angular{order}' / f'ray-{ray:03d}') if radial == 26
                    else TARGET / 'radial18' / retained.event_key(row) / f'ray-{ray:03d}')
                yield row, order, radial, ray, stem


def real(worker):
    modest()
    config = target_protocol()
    original, features, models = retained.setup(config)
    integrator = retained.candidate_integrator()
    folder = TARGET / 'workers' / f'real{worker}'
    status = dict(pid=os.getpid(), state='running', worker=worker, started_at=now(), completed_this_run=0)
    write(folder / 'status.json', status)
    for index, (row, order, radial, ray, stem) in enumerate(jobs(config)):
        if index % 2 != worker:
            continue
        if stem.with_suffix('.json').exists():
            report = read(stem.with_suffix('.json'))
            assert report['configuration_sha256'] == digest(TARGET / 'configuration.json')
            assert report['sha256'] == digest(stem.with_suffix('.npz'))
            continue
        assert not stem.with_suffix('.npz').exists(), 'Recover unsealed packet before resuming'
        if time.time() >= config['deadline_timestamp'] or (ROOT / 'STOP-REQUESTED').exists():
            status.update(state='safe_stop', next_index=index, saved_at=now())
            write(folder / 'status.json', status)
            return
        with mp.workdps(config['digits']):
            arrays, metadata = integrator(dict(config, angular_order=order), row, radial, ray, original, features, models)
        assert metadata['maximum_independent_four_force_residual'] <= config['identity_tolerance']
        assert all(np.all(np.isfinite(value)) for value in arrays.values())
        save(stem.with_suffix('.npz'), **arrays)
        report = dict(event_key=retained.event_key(row), angular_order=order, radial_order=radial, ray=ray,
            **metadata, sha256=digest(stem.with_suffix('.npz')), configuration_sha256=digest(TARGET / 'configuration.json'),
            finished_at=now(), worker=worker)
        write(stem.with_suffix('.json'), report)
        status.update(completed_this_run=status['completed_this_run'] + 1, last_index=index, last_packet=str(stem), saved_at=now())
        write(folder / 'status.json', status)
        if status['completed_this_run'] % 8 == 0:
            print(dict(worker=worker, saved=status['completed_this_run'], event=row['event'], angular=order, radial=radial, seconds=metadata['seconds']), flush=True)
    status.update(state='complete', finished_at=now())
    write(folder / 'status.json', status)


def secondary():
    modest()
    config = target_protocol()
    original, features, models = retained.setup(config)
    tensor_function = clone(virtual_owner.tensors, ROOT=TARGET)
    for row in config['events']:
        for order in config['angular_orders']:
            checks = []
            tensors = tensor_function(row, order, checks)
            for join in config['joins']:
                output = TARGET / 'virtual' / retained.event_key(row) / f'angular{order}-join{join}.npz'
                if output.exists():
                    report = read(output.with_suffix('.json'))
                    assert report['qualified'] and digest(output) == report['sha256']
                    continue
                mapped = virtual_owner.scalar_maps(config, row, tensors, features, join, checks)
                values = virtual_owner.blocks(config, row, join, mapped, features, models, checks)
                save(output, **mapped, **values)
                failures = [entry for entry in checks if not entry['passed']]
                write(output.with_suffix('.json'), dict(qualified=not failures, checks=checks, failed=failures,
                    sha256=digest(output), finished_at=now(), script_sha256=digest(__file__)))
                assert not failures, failures
                print(dict(virtual=row['event'], angular=order, join=join), flush=True)
        state_target = TARGET / 'state' / retained.event_key(row) / 'state.npz'
        if state_target.exists():
            report = read(state_target.with_suffix('.json'))
            assert report['qualified'] and digest(state_target) == report['sha256']
            continue
        checks, output = [], {}
        parameters, weight = source.physics.parameters_and_weight(row['theta'], row['node'])
        with mp.workdps(80):
            planck = state235.phase_geometry(parameters)['planck_mass_squared']
            alpha = mp.mpf(str(angular.inherited.source.ALPHA))
            analytic = 2 * mp.pi * alpha * scalar(row['theta'])**2 / 3
            check(checks, 'target Planck mass functional', abs(planck / analytic - 1))
            for join in config['joins']:
                radial = packet(virtual_owner.retained_virtual.VIRTUAL / 'radial' / f'join{join}-order6.npz')
                coefficient = 4 * alpha * scalar(row['theta'])**2 / mp.pi
                mass_coefficients = np.array([float(coefficient * scalar(value)) for value in radial['constant'][:98]])
                mass_vector = np.r_[mass_coefficients, 0.]
                for state_index, state in enumerate(config['states']):
                    physical = [scalar(config['heat']) * mp.mpf(value) for value in state['coefficients']]
                    mass_background = state235.contraction(mass_coefficients, physical[:98])
                    for degree in config['multipoles']:
                        values = {}
                        for step in config['canonical_steps']:
                            unit = state235.unit_state(parameters, features, models[0]['difference'].tests, join, physical, degree, step)
                            first = float(planck) * unit['mixed']['total']
                            second = float(mass_background) * unit['equilibrium']['total']
                            equilibrium = unit['equilibrium']['total'] @ np.array(list(map(float, physical))) if degree == 0 else np.zeros(98)
                            third = np.outer(equilibrium, mass_vector) if degree == 0 else np.zeros_like(first)
                            values[step] = weight * (first + second + third)
                            prefix = f'join{join}:state{state_index}:l{degree}:step{step}'
                            for name, matrix in [('statistical', weight * first), ('background_mass', weight * second),
                                    ('wave_mass', weight * third), ('total', values[step])]:
                                output[prefix + ':' + name] = matrix
                                if degree < 2 and np.linalg.norm(matrix) > 0:
                                    check(checks, prefix + ':' + name + ':independent gas', assessment.force_error(matrix))
                            output[prefix + ':equilibrium'] = weight * float(planck) * unit['equilibrium']['total']
                        check(checks, prefix + ':canonical refinement', retained.relative(values[.001], values[.0005]), config['refinement_tolerance'])
        save(state_target, **output)
        failures = [entry for entry in checks if not entry['passed']]
        write(state_target.with_suffix('.json'), dict(qualified=not failures, checks=checks, failed=failures,
            sha256=digest(state_target), finished_at=now(), script_sha256=digest(__file__)))
        assert not failures, failures
        print(dict(state=row['event'], checks=len(checks)), flush=True)


def assess():
    modest()
    config = target_protocol()
    checks, records, inputs = [], [], {}
    sum_real = clone(assessment.sum_real, ROOT=TARGET)
    new_event = clone(assessment.new_event, ROOT=TARGET, sum_real=sum_real)
    radial_config = TARGET / 'radial-configuration.json'
    if not radial_config.exists():
        write(radial_config, read(TARGET / 'configuration.json'))
    assert digest(radial_config) == digest(TARGET / 'configuration.json')
    summed = {}
    for row in config['events']:
        output = new_event(config, row, inputs, checks, records)
        save(TARGET / 'results' / f'event{row["event"]}-components.npz', **output)
        for name, value in output.items():
            summed[name] = summed.get(name, np.zeros_like(value)) + value
    for name, value in summed.items():
        degree = int(name.split(':')[-2][1:])
        if name.startswith('angular4:'):
            assessment.assess_difference('target-three-angle:' + name, value,
                summed[name.replace('angular4:', 'angular6:', 1)], degree, checks, records, config)
        if degree < 2:
            check(checks, name + ':combined force', assessment.force_error(value))
    quadratic = assessment.hessians(config, summed, checks)
    destination = TARGET / 'results/three-hard-angle-sum.npz'
    save(destination, **summed, **quadratic)
    failures = [entry for entry in checks if not entry['passed']]
    write(TARGET / 'results/assessment.json', dict(qualified=not failures, checks=checks, failed=failures,
        records=records, consumed_inputs=inputs, output_sha256=digest(destination), finished_at=now(),
        target_history_theta_owned=True, tail_derivative_included=False, operator_temperature_derivative_included=False))
    print(dict(target_assessed=True, checks=len(checks), failed=len(failures), first_failures=failures[:5]), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['prepare', 'real', 'secondary', 'assess'])
    parser.add_argument('--worker', type=int, choices=[0, 1], default=0)
    arguments = parser.parse_args()
    if arguments.phase == 'prepare':
        prepare_target()
    elif arguments.phase == 'real':
        real(arguments.worker)
    elif arguments.phase == 'secondary':
        secondary()
    else:
        assess()
