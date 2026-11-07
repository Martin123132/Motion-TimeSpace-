import os

for variable in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
    os.environ[variable] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

import ast
import json
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

import psutil

ROOT = Path(__file__).resolve().parent
CONSUMER = ROOT / 'saved-epoch-cell424'
BANK = ROOT / 'final-epoch-kinematic-bank'
DESTINATION = ROOT / 'event-coupling-hessian-001'
process = psutil.Process()
process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
process.cpu_affinity([4])
sys.dont_write_bytecode = True
started = time.monotonic()


def now():
    return datetime.now(timezone.utc).isoformat()


def guard():
    if time.monotonic() - started >= 45 * 60:
        raise TimeoutError('Bounded coupling qualification reached45 minutes')
    if any((path / 'STOP-REQUESTED').exists() for path in (ROOT, ROOT.parent, CONSUMER, DESTINATION)):
        raise RuntimeError('Owner stop preserved; do not automatically retry')
    if (ROOT.parent / 'execution-v3/STOP-REQUEST.json').exists():
        raise RuntimeError('Execution stop preserved; do not automatically retry')


def write(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)


def read(path):
    return json.loads(Path(path).read_text())


guard()
if DESTINATION.exists():
    raise RuntimeError('Existing coupling attempt preserved; inspect before any new attempt')
DESTINATION.mkdir()
identity = dict(pid=process.pid, created_time=process.create_time(), command=process.cmdline(),
    priority=process.nice(), affinity=process.cpu_affinity())
write(DESTINATION / 'start.json', dict(started_at=now(), process=identity))
print(json.dumps(dict(started=True, process=identity)), flush=True)


def main():
    from restart_readout import digest, load_verified_cell

    manifest = read(CONSUMER / 'manifest.json')
    bank = read(BANK / 'protocol.json')
    bank_validation = read(BANK / 'validation.json')
    saved_validation = read(CONSUMER / 'precision-check-001/validation.json')
    if not all(value['passed'] for value in (manifest, bank_validation, saved_validation)):
        raise RuntimeError('Passing retained controls required')
    inputs = {**manifest['inputs'], **bank_validation['inputs'], **saved_validation['inputs']}
    for path, checksum in inputs.items():
        if digest(path) != checksum:
            raise RuntimeError('Retained frozen input changed: ' + path)
    if digest(CONSUMER / 'columns.npz') != manifest['columns_sha256']:
        raise RuntimeError('Saved physical history columns changed')
    packet_path = CONSUMER / 'precision-check-001/responses-split.npz'
    if digest(packet_path) != saved_validation['packet_sha256']:
        raise RuntimeError('Saved precision oracle changed')
    setup_path = ROOT / 'check_full_tail_factors.py'
    statements = []
    for statement in ast.parse(setup_path.read_text()).body:
        if isinstance(statement, ast.Assign) and any(isinstance(target, ast.Name) and target.id == 'checks' for target in statement.targets):
            break
        statements.append(statement)
    context = dict(__file__=str(setup_path), __name__='event_coupling_source_setup')
    exec(compile(ast.Module(body=statements, type_ignores=[]), str(setup_path), 'exec'), context)
    namespace = context['namespace']
    np, mp, parent, base = (namespace[name] for name in ('np', 'mp', 'retained', 'BASE'))
    import integrate236 as integration
    import factors236 as retained
    from saved_epoch_binding import bind
    from full_tail_factors import FullTailFactors
    from full_tail_action import FullTailActionFactors, SplitColumns
    from precise_epoch_response import PreciseEpochResponse, scalar, split_array
    from event_coupling import EventCoupling
    from factored_epoch_response import FactoredEpochResponse
    sys.path.insert(0, str(base / 'exact-dirac-density-20261027'))
    from exact_kinematic_cache import CachedDirection

    restart = load_verified_cell(ROOT.parent, 424, ROOT.parent / 'supervisor-cells417-424.json')
    original, theta = parent.source.context(manifest['fraction'])
    contexts = {value['model']: value for value in parent.source.physics.epoch_context(original)[0]}
    if contexts != manifest['contexts'] or theta != manifest['theta']:
        raise RuntimeError('Source epoch/thermal context changed')
    binding = bind(parent.precise.Bundle, parent.precise.Features, original, contexts, restart, manifest['history_heats'])
    bundle = binding['bundle']
    with np.load(CONSUMER / 'columns.npz', allow_pickle=False) as saved:
        if not np.array_equal(bundle.high, saved['high']) or not np.array_equal(bundle.low, saved['low']):
            raise RuntimeError('Full physical history binding changed')
    inputs.update(namespace['sources'])
    inputs.update(restart['inputs'])
    for module in list(sys.modules.values()):
        filename = getattr(module, '__file__', None)
        if filename and Path(filename).suffix == '.py' and Path(filename).resolve().is_relative_to(base):
            inputs[str(Path(filename).resolve())] = digest(filename)
    for name in ('event_coupling.py', 'factored_epoch_response.py', 'check_event_coupling.py', 'EVENT-COUPLING-DERIVATION.md'):
        path = ROOT / name
        if path.suffix == '.py':
            compile(path.read_text(), str(path), 'exec')
        inputs[str(path)] = digest(path)
    for path in (CONSUMER / 'manifest.json', CONSUMER / 'columns.npz', CONSUMER / 'precision-check-001/validation.json', packet_path,
            BANK / 'protocol.json', BANK / 'validation.json'):
        inputs[str(path)] = digest(path)
    for ray in range(128):
        report_path = BANK / f'ray-{ray:03d}.json'
        kernel_path = BANK / f'ray-{ray:03d}-kernel.json'
        report = read(report_path)
        if not report['passed'] or digest(kernel_path) != report['kernel_sha256']:
            raise RuntimeError('Final-temperature kinematic packet changed')
        inputs[str(report_path)] = digest(report_path)
        inputs[str(kernel_path)] = report['kernel_sha256']
    protocol = dict(frozen_at=now(), previous_goal_turn='progress: final-temperature128-direction kinematic bank completed and verified',
        inputs=inputs, gate=1e-10, precision=80, nonlinear_precision=100, nonlinear_step='1e-12',
        saved_source='cell424,all18 physical/difference columns,both joins,l0/1/2,four signed soft probes',
        final_source='x14,event0,all128 angular directions,two positive frequency probes and both signs; no fabricated final history',
        nonlinear_source='Born and four signed real cell424 events, every photon/gas/velocity/density mixed entry',
        predictions=['matrix reproduces coefficient_state', 'photon/gas Hessian symmetric with zero photon diagonal',
            'independent raw_flux mixed derivatives reproduce the matrix', 'all saved source blocks and stable paired differences agree',
            'soft reference plus remainder equals the complete source', 'radiation/gas exchange rows unchanged'],
        background_step='1e-12', wave_step='1e-12', physical_background_coordinates=578, photon_coordinates=577,
        planned_precision_rejection=True, source_integrated=False, main_propagation_head=424,
        original_bank_changed=False, original_grids_changed=False, original_tolerances_changed=False)
    write(DESTINATION / 'prediction.json', protocol)
    checks, packets, nonlinear_events, timings = [], {}, [], {}

    def compare(name, actual, expected, group):
        actual_values = list(np.asarray(actual, dtype=object).flat)
        expected_values = list(np.asarray(expected, dtype=object).flat)
        if len(actual_values) != len(expected_values):
            raise ValueError('Different comparison shapes')
        error = mp.sqrt(mp.fsum((scalar(value) - scalar(reference))**2 for value, reference in zip(actual_values, expected_values)))
        scale = max(mp.sqrt(mp.fsum(scalar(value)**2 for value in expected_values)), mp.mpf('1e-300'))
        relative = error / scale
        checks.append(dict(name=name, group=group, relative=float(relative), absolute=float(error), limit=1e-10,
            passed=bool(mp.isfinite(relative) and relative <= mp.mpf('1e-10'))))

    def exact(name, passed, group):
        checks.append(dict(name=name, group=group, passed=bool(passed)))

    def vector(coefficients):
        return [*coefficients['photon'], coefficients['gas'], *coefficients['velocity'], coefficients['density']]

    def coefficient_check(event, name):
        operator = EventCoupling(event)
        compare(name + ':equilibrium', vector(operator.equilibrium()), vector(retained.equilibrium(event)), 'equilibrium')
        exact(name + ':symmetric', all(operator.matrix[first, second] == operator.matrix[second, first]
            for first in range(operator.count + 1) for second in range(operator.count + 1)), 'hessian-structure')
        exact(name + ':zero-photon-diagonal', all(operator.matrix[photon, photon] == 0 for photon in range(operator.count)), 'hessian-structure')
        for column in range(operator.count + 1):
            potential = [mp.mpf(int(column == photon)) for photon in range(operator.count)]
            gas = mp.mpf(int(column == operator.count))
            compare(name + f':column{column}', vector(operator.coefficients(potential, gas)),
                vector(retained.coefficient_state(event, potential, gas)), 'coefficient-identity')
        return operator

    parameters, unused = parent.source.physics.parameters_and_weight(theta, manifest['event']['node'])
    direction = list(integration.angular.inherited.source.angular_nodes(8))[0][0]
    with mp.workdps(80):
        retained.state235.mean_energy.cache_clear()
        owner = integration.Direction(integration.precise_context(parameters), direction)
        factors = FullTailFactors(owner, bundle, context['tests'])
        projections = {join: SplitColumns(bundle.high[:, join::2], bundle.low[:, join::2]) for join in (0, 1)}
        native = FullTailActionFactors(owner, bundle, context['tests'], projections)
        soft = [scalar(value) * owner.temperature / owner.doppler for value in (1e-4, .01)]
        events = {sign: [owner.event(sign * value) for value in soft] for sign in (-1, 1)}
        native_data = {sign: native.evaluate(soft, events[sign], sign) for sign in (-1, 1)}
        oracle = PreciseEpochResponse(factors, bundle.high[:, ::2], bundle.low[:, ::2])
        factored = FactoredEpochResponse(factors, bundle.high[:, ::2], bundle.low[:, ::2])
        nonlinear_events.append(('born', factors.event))
        coefficient_check(factors.event, 'cell424:born')
        results = {}
        for join in (0, 1):
            for degree in (0, 1, 2):
                guard()
                label = f'born:join{join}:l{degree}'
                compare(label, factored.born(join, degree), oracle.born(join, degree), 'born-right')
                results[label] = factored.response(factors.left[degree], factored.born(join, degree), degree)
                for sign in (-1, 1):
                    for node in range(2):
                        began = time.perf_counter()
                        actual = factored.current(join, degree, soft[node], events[sign][node], sign)
                        timings['factored_current_seconds'] = timings.get('factored_current_seconds', 0) + time.perf_counter() - began
                        began = time.perf_counter()
                        expected = oracle.current(join, degree, soft[node], events[sign][node], sign)
                        timings['oracle_current_seconds'] = timings.get('oracle_current_seconds', 0) + time.perf_counter() - began
                        label = f'sign{sign}:node{node}:join{join}:l{degree}'
                        for field in ('complete', 'reference', 'right_delta'):
                            for state in range(19):
                                compare(label + f':{field}:state{state}', actual[field][state], expected[field][state], 'right-' + field)
                        for state in range(19):
                            compare(label + f':coefficients:state{state}', vector(actual['coefficients'][state]),
                                vector(expected['coefficients'][state]), 'actual-history-coefficients')
                        left = factors.left[degree] + native_data[sign][degree, 'left_delta'][node]
                        results[label] = factored.response(left, actual['complete'], degree)
                        for state in range(19):
                            assembled = [[reference + remainder for reference, remainder in zip(first, second)]
                                for first, second in zip(actual['reference'][state], actual['right_delta'][state])]
                            compare(label + f':soft-sum:state{state}', assembled, actual['complete'][state], 'soft-reference-remainder')
                        if join == 0 and degree == 0:
                            nonlinear_events.append((label, actual['current_event']))
                            coefficient_check(actual['current_event'], 'cell424:' + label)
                print(json.dumps(dict(phase='saved-source', join=join, degree=degree, blocks=len(results))), flush=True)
        with np.load(packet_path, allow_pickle=False) as saved:
            for label, values in results.items():
                expected = np.array([scalar(upper) + scalar(lower) for upper, lower in zip(saved[label + ':high'].flat,
                    saved[label + ':low'].flat)], dtype=object).reshape(saved[label + ':high'].shape)
                for state in range(19):
                    for column in range(18):
                        compare(label + f':state{state}:column{column}', [row[column] for row in values[state]], expected[state, :, column], 'saved-response')
                        if not label.endswith('l2'):
                            photon, gas = values[state][0][column], values[state][-1][column]
                            relative = abs(photon + gas) / max(abs(photon) + abs(gas), mp.mpf('1e-300'))
                            checks.append(dict(name=label + f':state{state}:column{column}', group='exchange', relative=float(relative),
                                limit=1e-10, passed=bool(relative <= mp.mpf('1e-10'))))
                differences = []
                for pair in range(6):
                    baseline, candidate, change = 3 * pair, 3 * pair + 1, 3 * pair + 2
                    direct = [after[candidate] - before[baseline] for after, before in zip(values[candidate + 1], values[baseline + 1])]
                    stable = [mp.fsum([first[change], second[baseline], second[change]])
                        for first, second in zip(values[baseline + 1], values[change + 1])]
                    reference = [scalar(upper) + scalar(lower) for upper, lower in zip(saved[label + ':difference-high'][pair], saved[label + ':difference-low'][pair])]
                    compare(label + f':pair{pair}', stable, direct, 'three-term-identity')
                    compare(label + f':pair{pair}', stable, reference, 'saved-paired-difference')
                    differences.append(stable)
                packets[label + ':high'], packets[label + ':low'] = split_array(values)
                packets[label + ':difference-high'], packets[label + ':difference-low'] = split_array(differences)
        exact('operator-built-once-per-kinematic-event', len(factored.current_operators) == 4, 'reuse')
        exact('full-readouts-cached-per-event-and-join', len(factored.current_readouts) == 8, 'reuse')
        with mp.workdps(60):
            try:
                factored.born(0, 0)
            except ValueError:
                rejected = True
            else:
                rejected = False
        exact('different-precision-rejected', rejected, 'negative-controls')
    print(json.dumps(dict(phase='saved-source-complete', checks=len(checks), timings=timings)), flush=True)
    with mp.workdps(100):
        retained.state235.mean_energy.cache_clear()
        parent.thermodynamics.cache_clear()
        step = mp.mpf('1e-12')
        for label, event in nonlinear_events:
            guard()
            operator = EventCoupling(event)
            measured = mp.matrix(operator.count + 5, operator.count + 1)
            for row in range(operator.count + 5):
                for column in range(operator.count + 1):
                    numerator = mp.mpf(0)
                    for background_sign in (-1, 1):
                        for wave_sign in (-1, 1):
                            potential = [step * (background_sign * int(column == photon) + wave_sign * int(row == photon))
                                for photon in range(operator.count)]
                            gas = step * (background_sign * int(column == operator.count) + wave_sign * int(row == operator.count))
                            velocity = [step * wave_sign * int(row == operator.count + 1 + axis) for axis in range(3)]
                            density = step * wave_sign * int(row == operator.count + 4)
                            numerator += background_sign * wave_sign * parent.raw_flux(event, potential, gas, velocity, density)
                    measured[row, column] = numerator / (4 * step**2)
            for column in range(operator.count + 1):
                compare(label + f':column{column}', list(measured[:, column]), list(operator.matrix[:, column]), 'nonlinear-flux-derivative')
            print(json.dumps(dict(phase='independent-nonlinear-derivative', event=label)), flush=True)
    with mp.workdps(80):
        retained.state235.mean_energy.cache_clear()
        final_parameters, unused = parent.source.physics.parameters_and_weight(bank['theta'], bank['node'])
        final_parameters = integration.precise_context(final_parameters)
        for ray, angular in enumerate(bank['angular_nodes']):
            guard()
            kernel = BANK / f'ray-{ray:03d}-kernel.json'
            final_owner = CachedDirection(final_parameters, angular['direction'], kernel, inputs[str(kernel)])
            incoming = final_owner.transform * final_owner.spin.photon(final_owner.energy, final_owner.directions[0])
            outgoing = final_owner.transform * final_owner.spin.photon(final_owner.hard0, final_owner.directions[1])
            initial = list(final_owner.transform * final_owner.initial)
            for sign in (-1, 1):
                for frequency in (1e-4, .01):
                    soft = scalar(frequency) * final_owner.temperature / final_owner.doppler
                    event = final_owner.event(sign * soft)
                    transfer = list(final_owner.transform * mp.matrix([event['kinetic'], *event['recoil']]))
                    shift = float(event['hard_shift'] * final_owner.hard_doppler / final_owner.temperature)
                    current = dict(temperature=final_owner.temperature, frequencies=[incoming[0] / final_owner.temperature,
                        outgoing[0] / final_owner.temperature + scalar(shift), scalar(frequency)],
                        electron_initial=initial, electron_transfer=transfer, signs=[-1, 1, sign])
                    coefficient_check(current, f'final:ray{ray}:sign{sign}:frequency{frequency}')
            if (ray + 1) % 16 == 0:
                print(json.dumps(dict(phase='final-temperature', rays=ray + 1)), flush=True)
    guard()
    for path, checksum in inputs.items():
        if digest(path) != checksum:
            raise RuntimeError('Frozen input changed during qualification: ' + path)
    with (DESTINATION / 'responses-split.npz').open('xb') as stream:
        np.savez_compressed(stream, **packets)
    groups = {group: dict(checks=sum(row['group'] == group for row in checks),
        failed=sum(row['group'] == group and not row['passed'] for row in checks),
        maximum_relative=max(row.get('relative', 0) for row in checks if row['group'] == group))
        for group in sorted({row['group'] for row in checks})}
    report = dict(passed=all(row['passed'] for row in checks), checks=checks, groups=groups, inputs=inputs,
        prediction_sha256=digest(DESTINATION / 'prediction.json'), packet_sha256=digest(DESTINATION / 'responses-split.npz'),
        timings=timings, process=identity, finished_at=now(), elapsed_seconds=time.monotonic() - started,
        response_blocks=len(results), full_history_coordinates=578, physical_and_difference_columns=18,
        nonlinear_events=len(nonlinear_events), final_temperature_directions=128, history_propagated=False,
        source_integrated=False, source_budget_assessed=False, original_bank_changed=False,
        original_grids_changed=False, original_tolerances_changed=False, previous_failed_protocol_preserved=True)
    write(DESTINATION / 'validation.json', report)
    print(json.dumps(dict(passed=report['passed'], checks=len(checks), groups=groups, timings=timings,
        failed=[row for row in checks if not row['passed']][:10], seconds=report['elapsed_seconds'])), flush=True)
    return 0 if report['passed'] else 1


try:
    exit_code = main()
except BaseException as error:
    write(DESTINATION / 'end.json', dict(state='exception', process=identity, finished_at=now(),
        exception=repr(error), traceback=traceback.format_exc(), automatic_retry_allowed=False))
    raise
else:
    write(DESTINATION / 'end.json', dict(state='passed' if exit_code == 0 else 'failed', process=identity,
        finished_at=now(), exit_code=exit_code, automatic_retry_allowed=False))
    raise SystemExit(exit_code)
