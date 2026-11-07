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
DESTINATION = ROOT / 'compensated-epoch-source-001'
process = psutil.Process()
process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
process.cpu_affinity([4])
sys.dont_write_bytecode = True
started = time.monotonic()


def now():
    return datetime.now(timezone.utc).isoformat()


def guard():
    if time.monotonic() - started > 55 * 60:
        raise TimeoutError('Pointwise source qualification reached55 minutes')
    if any((path / 'STOP-REQUESTED').exists() for path in (ROOT, ROOT.parent, CONSUMER, DESTINATION)):
        raise RuntimeError('Owner stop preserved; no automatic retry')
    if (ROOT.parent / 'execution-v3/STOP-REQUEST.json').exists():
        raise RuntimeError('Execution stop preserved; no automatic retry')


def read(path):
    return json.loads(Path(path).read_text())


def write(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)


guard()
if DESTINATION.exists():
    raise RuntimeError('Existing compensated source attempt preserved')
DESTINATION.mkdir()
identity = dict(pid=process.pid, created_time=process.create_time(), command=process.cmdline(),
    priority=process.nice(), affinity=process.cpu_affinity())
write(DESTINATION / 'start.json', dict(started_at=now(), process=identity))
print(json.dumps(dict(started=True, process=identity)), flush=True)


def main():
    from restart_readout import digest, load_verified_cell

    qualification_paths = [ROOT / 'event-coupling-hessian-001/validation.json',
        ROOT / 'event-coupling-hessian-001/bounded-cache-check/validation.json']
    inputs = {}
    for path in qualification_paths:
        report = read(path)
        if not report['passed']:
            raise RuntimeError('Passing derived coupling/cache controls required')
        inputs.update(report['inputs'])
        inputs[str(path)] = digest(path)
    for name in ('precise_compensated_source.py', 'check_precise_compensated_source.py', 'COMPENSATED-EPOCH-SOURCE.md'):
        path = ROOT / name
        if path.suffix == '.py':
            compile(path.read_text(), str(path), 'exec')
        inputs[str(path)] = digest(path)
    for path, checksum in inputs.items():
        if digest(path) != checksum:
            raise RuntimeError('Frozen source changed: ' + path)
    setup_path = ROOT / 'check_full_tail_factors.py'
    statements = []
    for statement in ast.parse(setup_path.read_text()).body:
        if isinstance(statement, ast.Assign) and any(isinstance(target, ast.Name) and target.id == 'checks' for target in statement.targets):
            break
        statements.append(statement)
    context = dict(__file__=str(setup_path), __name__='precise_compensated_source_setup')
    exec(compile(ast.Module(body=statements, type_ignores=[]), str(setup_path), 'exec'), context)
    namespace = context['namespace']
    np, mp, parent, base = (namespace[name] for name in ('np', 'mp', 'retained', 'BASE'))
    import integrate236 as retained
    from saved_epoch_binding import bind
    from full_tail_factors import FullTailFactors
    from full_tail_action import FullTailActionFactors, SplitColumns, panel_action, logarithm_action
    from precise_epoch_response import PreciseEpochResponse, scalar, split_array
    from bounded_factored_epoch_response import BoundedFactoredEpochResponse
    from precise_compensated_source import point, logarithm, array
    sys.path.insert(0, str(base / 'exact-dirac-density-20261027'))
    from rational239 import RationalDirection

    manifest = read(CONSUMER / 'manifest.json')
    restart = load_verified_cell(ROOT.parent, 424, ROOT.parent / 'supervisor-cells417-424.json')
    original, theta = parent.source.context(manifest['fraction'])
    contexts = {value['model']: value for value in parent.source.physics.epoch_context(original)[0]}
    if contexts != manifest['contexts'] or theta != manifest['theta']:
        raise RuntimeError('Source-owned context changed')
    bundle = bind(parent.precise.Bundle, parent.precise.Features, original, contexts, restart, manifest['history_heats'])['bundle']
    with np.load(CONSUMER / 'columns.npz', allow_pickle=False) as saved:
        if not np.array_equal(bundle.high, saved['high']) or not np.array_equal(bundle.low, saved['low']):
            raise RuntimeError('Actual carried history changed')
    source_config = read(base / 'finite-real-mixed-source-20261026/configuration.json')
    parameters, event_weight = parent.source.physics.parameters_and_weight(theta, manifest['event']['node'])
    direction, angular_weight = list(retained.angular.inherited.source.angular_nodes(8))[0]
    with mp.workdps(80):
        retained.state235.mean_energy.cache_clear()
        owner = RationalDirection(retained.precise_context(parameters), direction)
        factors = FullTailFactors(owner, bundle, context['tests'])
        projections = {join: SplitColumns(bundle.high[:, join::2], bundle.low[:, join::2]) for join in (0, 1)}
        native = FullTailActionFactors(owner, bundle, context['tests'], projections)
        candidate = BoundedFactoredEpochResponse(factors, bundle.high[:, ::2], bundle.low[:, ::2])
        panels = list(retained.panels(owner, 26, source_config))
        upper = retained.upper_limits(owner)
    with mp.workdps(100):
        retained.state235.mean_energy.cache_clear()
        oracle = PreciseEpochResponse(factors, bundle.high[:, ::2], bundle.low[:, ::2])
    regions = {name: [index for index, panel in enumerate(panels) if (panel[2], panel[3]) == flags]
        for name, flags in (('both', (True, True)), ('absorption', (False, True)), ('reference', (False, False)))}
    if any(not indices for indices in regions.values()):
        raise RuntimeError('All three original physical domains required')
    if len(panels) <= 9 or not panels[9][2]:
        raise RuntimeError('Original sensitive panel9 must lie in the both-real domain')
    selected = [(regions['both'][0], 0), (9, 0), (regions['both'][-1], 25),
        (regions['absorption'][0], 0), (regions['absorption'][-1], 25),
        (regions['reference'][0], 0), (regions['reference'][-1], 25)]
    selected = list(dict.fromkeys(selected))
    descriptions = [dict(panel=panel_index, node=node, frequency=float(panels[panel_index][0][node]),
        measure=float(panels[panel_index][1][node]), emission=bool(panels[panel_index][2]), absorption=bool(panels[panel_index][3]))
        for panel_index, node in selected]
    inputs.update(namespace['sources'])
    inputs.update(restart['inputs'])
    for module in list(sys.modules.values()):
        filename = getattr(module, '__file__', None)
        if filename and Path(filename).suffix == '.py' and (Path(filename).resolve().is_relative_to(base)
                or Path(filename).resolve().parent == ROOT):
            inputs[str(Path(filename).resolve())] = digest(filename)
    protocol = dict(frozen_at=now(), previous_goal_turn='progress: event coupling derived, saved source verified, bounded cache qualified',
        inputs=inputs, coordinate=restart['coordinate'], theta=theta, points=descriptions, radial_order=26, angular_order=8,
        angular_ray=0, event_node=manifest['event']['node'], event_weight=event_weight, angular_weight=float(angular_weight),
        upper_limits=[float(value) for value in upper], precision=80, reference_precision=100, gate=1e-10,
        source_modes=['control', 'difference'], joins=[0, 1], degrees=[0, 1, 2], coordinates=578, columns=18,
        predictions=['stable source agrees with un-rearranged100-digit source in all three domains',
            'paired baseline/MTS difference preserves all three bilinear terms', 'radiation/gas exchange unchanged',
            'separator logarithm agrees', 'missing/invalid source arguments rejected'],
        native_float_comparison='Diagnostic only; same1e-10 gate, retain every failure without relabelling',
        source_integrated=False, partial_points_not_propagated=True, actual_history_cell=424, endpoint_history_not_substituted=True,
        original_bank_changed=False, original_grids_changed=False, original_tolerances_changed=False)
    write(DESTINATION / 'prediction.json', protocol)
    print(json.dumps(dict(frozen_points=descriptions, inputs=len(inputs))), flush=True)
    checks, diagnostics, packets = [], [], []

    def compare(name, actual, expected, group, target=None):
        target = checks if target is None else target
        actual, expected = list(np.asarray(actual, dtype=object).flat), list(np.asarray(expected, dtype=object).flat)
        if len(actual) != len(expected):
            raise ValueError('Different comparison dimensions')
        error = mp.sqrt(mp.fsum((scalar(value) - scalar(reference))**2 for value, reference in zip(actual, expected)))
        scale = max(mp.sqrt(mp.fsum(scalar(value)**2 for value in expected)), mp.mpf('1e-300'))
        relative = error / scale
        target.append(dict(name=name, group=group, relative=float(relative), absolute=float(error), scale=float(scale), limit=1e-10,
            passed=bool(mp.isfinite(relative) and relative <= mp.mpf('1e-10'))))

    def independent_reference(frequency, join, degree):
        population = 1 / mp.expm1(scalar(frequency))
        coupling = 2 * population * (1 + population) / (1 + 2 * population)
        soft = oracle.contract(factors.features.evaluate(np.array([frequency]), join))[0]
        born = oracle.born(join, degree)
        harmonic = factors.harmonics[degree][2]
        values = []
        for state in range(19):
            background = mp.mpf(0) if state == 0 else soft[state - 1]
            density = mp.mpf(0) if state == 0 else oracle.born_coefficients[join][state]['density']
            values.append([[born[state][column][axis] + coupling * (background * born[0][column][axis]
                + density * soft[column] * scalar(harmonic[axis])) for axis in range(len(harmonic))] for column in range(18)])
        return born, values, population

    def brute_point(description, densities, currents, left_delta, mode, join, degree):
        born, reference, population = independent_reference(description['frequency'], join, degree)
        local_temperature = owner.temperature / owner.doppler
        energy = scalar(description['frequency']) * local_temperature
        base_left = array(factors.left[degree])
        pieces = [-owner.pole[mode] * (1 + 2 * population) / energy * array(oracle.response(base_left, reference, degree))]
        if not description['emission']:
            pieces.append(owner.pole[mode] / energy * array(oracle.response(base_left, born, degree)))
        for sign, allowed in ((1, description['emission']), (-1, description['absorption'])):
            if allowed:
                statistical = 1 + population if sign == 1 else population
                complete = array(oracle.response(base_left + array(left_delta[sign]), currents[sign]['complete'], degree))
                pieces.append(statistical * densities[sign][mode] * complete)
        total = np.array([mp.fsum(values) for values in zip(*(piece.flat for piece in pieces))], dtype=object).reshape(pieces[0].shape)
        scale = scalar(description['measure']) * local_temperature * scalar(event_weight) * scalar(angular_weight) / 2
        return scale * total

    def check_block(label, actual, reference, native_values, storage):
        for state in range(19):
            for column in range(18):
                compare(label + f':state{state}:column{column}', actual[state, :, column], reference[state, :, column], 'precise-source')
                compare(label + f':state{state}:column{column}', native_values[state, :, column], reference[state, :, column], 'native-float-source', diagnostics)
                if not label.endswith('l2'):
                    photon, gas = actual[state, 0, column], actual[state, -1, column]
                    residual = abs(photon + gas) / max(abs(photon) + abs(gas), mp.mpf('1e-300'))
                    checks.append(dict(name=label + f':state{state}:column{column}', group='exchange', relative=float(residual),
                        limit=1e-10, passed=bool(residual <= mp.mpf('1e-10'))))
        deltas = []
        for pair in range(6):
            baseline, candidate_index, delta = 3 * pair, 3 * pair + 1, 3 * pair + 2
            stable = [mp.fsum(values) for values in zip(actual[baseline + 1, :, delta], actual[delta + 1, :, baseline], actual[delta + 1, :, delta])]
            direct = actual[candidate_index + 1, :, candidate_index] - actual[baseline + 1, :, baseline]
            reference_delta = reference[candidate_index + 1, :, candidate_index] - reference[baseline + 1, :, baseline]
            compare(label + f':pair{pair}', stable, direct, 'three-term-identity')
            compare(label + f':pair{pair}', stable, reference_delta, 'paired-precision')
            compare(label + f':pair{pair}', actual[0, :, delta], reference[0, :, candidate_index] - reference[0, :, baseline], 'equilibrium-paired-precision')
            deltas.append(stable)
        storage[label + ':high'], storage[label + ':low'] = split_array(actual)
        storage[label + ':difference-high'], storage[label + ':difference-low'] = split_array(deltas)

    for point_index, description in enumerate(descriptions):
        guard()
        began = time.monotonic()
        frequency, measure = description['frequency'], description['measure']
        allowed_signs = [sign for sign, allowed in ((1, description['emission']), (-1, description['absorption'])) if allowed]
        with mp.workdps(80):
            retained.state235.mean_energy.cache_clear()
            soft = scalar(frequency) * owner.temperature / owner.doppler
            densities, events, native_data = {}, {}, {}
            for sign in allowed_signs:
                densities[sign], events[sign] = owner.densities(sign * soft)
                native_data[sign] = native.evaluate([soft], [events[sign]], sign)
            candidates, old_values, lefts = {}, {}, {}
            for join in (0, 1):
                for degree in (0, 1, 2):
                    guard()
                    current = {sign: candidate.current(join, degree, soft, events[sign], sign) for sign in allowed_signs}
                    left_delta = {sign: native_data[sign][degree, 'left_delta'][0] for sign in allowed_signs}
                    lefts[join, degree] = left_delta
                    for mode in ('control', 'difference'):
                        key = mode, join, degree
                        candidates[key] = point(candidate, frequency, measure, densities, current, left_delta, mode, join, degree,
                            event_weight, angular_weight, description['emission'], description['absorption'])
                        old_values[key] = panel_action(native, np.array([frequency]), np.array([measure]),
                            {sign: [value] for sign, value in densities.items()}, native_data, mode, join, degree,
                            event_weight, angular_weight, description['emission'], description['absorption'])
            if point_index == 0:
                defaults = dict(response=candidate, frequency=frequency, measure=measure, densities=densities,
                    current=current, left_delta=left_delta, mode='control', join=1, degree=2, event_weight=event_weight,
                    angular_weight=angular_weight, emission_allowed=True, absorption_allowed=True)
                for name, updates in (('missing-density', dict(densities={})), ('negative-frequency', dict(frequency=-1)),
                    ('invalid-mode', dict(mode='unknown')), ('missing-absorption-domain', dict(absorption_allowed=False)),
                    ('zero-weight', dict(event_weight=0))):
                    try:
                        point(**dict(defaults, **updates))
                    except ValueError:
                        rejected = True
                    else:
                        rejected = False
                    checks.append(dict(name=name, group='negative-controls', passed=rejected))
                with mp.workdps(40):
                    try:
                        point(**defaults)
                    except ValueError:
                        rejected = True
                    else:
                        rejected = False
                checks.append(dict(name='low-precision-rejected', group='negative-controls', passed=rejected))
        storage = {}
        with mp.workdps(100):
            retained.state235.mean_energy.cache_clear()
            reference_densities = {sign: owner.densities(sign * soft)[0] for sign in allowed_signs}
            for join in (0, 1):
                for degree in (0, 1, 2):
                    guard()
                    currents = {sign: oracle.current(join, degree, soft, events[sign], sign) for sign in allowed_signs}
                    for mode in ('control', 'difference'):
                        key = mode, join, degree
                        reference = brute_point(description, reference_densities, currents, lefts[join, degree], mode, join, degree)
                        label = f'point{point_index}:{mode}:join{join}:l{degree}'
                        check_block(label, candidates[key], reference, old_values[key], storage)
        path = DESTINATION / f'point-{point_index:03d}.npz'
        with path.open('xb') as stream:
            np.savez_compressed(stream, **storage)
        packets.append(dict(path=str(path), sha256=digest(path), point=description))
        write(DESTINATION / f'point-{point_index:03d}.json', dict(packet=packets[-1], seconds=time.monotonic() - began,
            cumulative_checks=len(checks), cumulative_failures=sum(not row['passed'] for row in checks)))
        print(json.dumps(dict(point_complete=point_index, frequency=frequency, emission=description['emission'], absorption=description['absorption'],
            checks=len(checks), failures=sum(not row['passed'] for row in checks), seconds=time.monotonic() - began)), flush=True)
    guard()
    log_storage = {}
    with mp.workdps(80):
        retained.state235.mean_energy.cache_clear()
        log_candidate = {(mode, join, degree): logarithm(candidate, mode, join, degree, event_weight, angular_weight)
            for mode in ('control', 'difference') for join in (0, 1) for degree in (0, 1, 2)}
        log_native = {(mode, join, degree): logarithm_action(native, mode, join, degree, event_weight, angular_weight)
            for mode in ('control', 'difference') for join in (0, 1) for degree in (0, 1, 2)}
    with mp.workdps(100):
        retained.state235.mean_energy.cache_clear()
        for key, actual in log_candidate.items():
            mode, join, degree = key
            scale = scalar(event_weight) * scalar(angular_weight) * owner.pole[mode] * mp.log(2 * retained.upper_limits(owner)[0]) / 2
            reference = scale * array(oracle.response(factors.left[degree], oracle.born(join, degree), degree))
            check_block(f'logarithm:{mode}:join{join}:l{degree}', actual, reference, log_native[key], log_storage)
    log_path = DESTINATION / 'separator-logarithm.npz'
    with log_path.open('xb') as stream:
        np.savez_compressed(stream, **log_storage)
    packets.append(dict(path=str(log_path), sha256=digest(log_path)))
    for path, checksum in inputs.items():
        if digest(path) != checksum:
            raise RuntimeError('Frozen input changed during source check: ' + path)
    def summary(rows):
        return {group: dict(checks=sum(row['group'] == group for row in rows), failed=sum(row['group'] == group and not row['passed'] for row in rows),
            maximum_relative=max(row.get('relative', 0) for row in rows if row['group'] == group)) for group in sorted({row['group'] for row in rows})}
    groups, native_groups = summary(checks), summary(diagnostics)
    report = dict(passed=all(row['passed'] for row in checks), checks=checks, groups=groups, native_diagnostics=diagnostics,
        native_groups=native_groups, inputs=inputs, packets=packets, process=identity, finished_at=now(), seconds=time.monotonic() - started,
        prediction_sha256=digest(DESTINATION / 'prediction.json'), selected_points=len(descriptions), source_integrated=False,
        partial_points_propagated=False, actual_history_cell=424, endpoint_history_substituted=False,
        original_bank_changed=False, original_grids_changed=False, original_tolerances_changed=False,
        scope='All physical/difference source actions at seven preselected original radial26 nodes and the separator logarithm; no full quadrature')
    write(DESTINATION / 'validation.json', report)
    print(json.dumps(dict(passed=report['passed'], checks=len(checks), groups=groups, native_groups=native_groups,
        failed=[row for row in checks if not row['passed']][:10], seconds=report['seconds'])), flush=True)
    return 0 if report['passed'] else 1


try:
    exit_code = main()
except BaseException as error:
    write(DESTINATION / 'end.json', dict(state='exception', process=identity, finished_at=now(), exception=repr(error),
        traceback=traceback.format_exc(), automatic_retry_allowed=False))
    raise
else:
    write(DESTINATION / 'end.json', dict(state='passed' if exit_code == 0 else 'failed', process=identity, finished_at=now(),
        exit_code=exit_code, automatic_retry_allowed=False))
    raise SystemExit(exit_code)
