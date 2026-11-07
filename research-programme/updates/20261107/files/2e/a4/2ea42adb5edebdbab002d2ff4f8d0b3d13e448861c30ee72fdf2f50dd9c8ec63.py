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
PARENT = ROOT / 'event-coupling-hessian-001'
DESTINATION = PARENT / 'bounded-cache-check'
process = psutil.Process()
process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
process.cpu_affinity([4])
sys.dont_write_bytecode = True
started = time.monotonic()


def guard():
    if time.monotonic() - started > 20 * 60:
        raise TimeoutError('Bounded cache qualification reached20 minutes')
    if any((path / 'STOP-REQUESTED').exists() for path in (ROOT, ROOT.parent, CONSUMER, PARENT, DESTINATION)):
        raise RuntimeError('Owner stop preserved')
    if (ROOT.parent / 'execution-v3/STOP-REQUEST.json').exists():
        raise RuntimeError('Execution stop preserved')


def write(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)


guard()
if DESTINATION.exists():
    raise RuntimeError('Existing bounded-cache qualification preserved')
DESTINATION.mkdir()
identity = dict(pid=process.pid, created_time=process.create_time(), command=process.cmdline(),
    priority=process.nice(), affinity=process.cpu_affinity())
write(DESTINATION / 'start.json', dict(started_at=datetime.now(timezone.utc).isoformat(), process=identity))
print(json.dumps(dict(started=True, process=identity)), flush=True)


def main():
    from restart_readout import digest, load_verified_cell

    parent_report = json.loads((PARENT / 'validation.json').read_text())
    if not parent_report['passed']:
        raise RuntimeError('Passing full coupling qualification required')
    inputs = dict(parent_report['inputs'])
    inputs[str(PARENT / 'validation.json')] = digest(PARENT / 'validation.json')
    for name in ('bounded_factored_epoch_response.py', 'check_bounded_event_coupling.py'):
        path = ROOT / name
        compile(path.read_text(), str(path), 'exec')
        inputs[str(path)] = digest(path)
    for path, checksum in inputs.items():
        if digest(path) != checksum:
            raise RuntimeError('Frozen input changed: ' + path)
    write(DESTINATION / 'prediction.json', dict(inputs=inputs, frozen_at=datetime.now(timezone.utc).isoformat(), gate=1e-10,
        cache_capacities=[1, 2, 4], evaluation_order='same four saved signed probes, two complete passes, both joins and l0/1/2',
        predictions=['all retained right responses preserved after eviction/reconstruction',
            'steady cache contains at most capacity events and twice capacity readouts', 'orphan readouts absent',
            'capacities1/2 evict and rebuild without changing results', 'invalid capacities rejected'],
        original_bank_changed=False, original_grids_changed=False, original_tolerances_changed=False))
    setup_path = ROOT / 'check_full_tail_factors.py'
    statements = []
    for statement in ast.parse(setup_path.read_text()).body:
        if isinstance(statement, ast.Assign) and any(isinstance(target, ast.Name) and target.id == 'checks' for target in statement.targets):
            break
        statements.append(statement)
    context = dict(__file__=str(setup_path), __name__='bounded_coupling_setup')
    exec(compile(ast.Module(body=statements, type_ignores=[]), str(setup_path), 'exec'), context)
    namespace = context['namespace']
    np, mp, parent = (namespace[name] for name in ('np', 'mp', 'retained'))
    import integrate236 as integration
    from saved_epoch_binding import bind
    from full_tail_factors import FullTailFactors
    from precise_epoch_response import scalar
    from factored_epoch_response import FactoredEpochResponse
    from bounded_factored_epoch_response import BoundedFactoredEpochResponse

    manifest = json.loads((CONSUMER / 'manifest.json').read_text())
    restart = load_verified_cell(ROOT.parent, 424, ROOT.parent / 'supervisor-cells417-424.json')
    original, theta = parent.source.context(manifest['fraction'])
    contexts = {value['model']: value for value in parent.source.physics.epoch_context(original)[0]}
    if contexts != manifest['contexts'] or theta != manifest['theta']:
        raise RuntimeError('Source context changed')
    bundle = bind(parent.precise.Bundle, parent.precise.Features, original, contexts, restart, manifest['history_heats'])['bundle']
    with np.load(CONSUMER / 'columns.npz', allow_pickle=False) as saved:
        if not np.array_equal(bundle.high, saved['high']) or not np.array_equal(bundle.low, saved['low']):
            raise RuntimeError('Carried physical columns changed')
    checks, capacities = [], []

    def exact(name, passed):
        checks.append(dict(name=name, passed=bool(passed)))

    def compare(name, actual, expected):
        first, second = list(np.asarray(actual, dtype=object).flat), list(np.asarray(expected, dtype=object).flat)
        if len(first) != len(second):
            raise ValueError('Reference dimensions differ')
        error = mp.sqrt(mp.fsum((scalar(value) - scalar(reference))**2 for value, reference in zip(first, second)))
        scale = max(mp.sqrt(mp.fsum(scalar(value)**2 for value in second)), mp.mpf('1e-300'))
        relative = error / scale
        checks.append(dict(name=name, relative=float(relative), limit=1e-10, passed=bool(relative <= mp.mpf('1e-10'))))

    with mp.workdps(80):
        integration.state235.mean_energy.cache_clear()
        parameters, unused = parent.source.physics.parameters_and_weight(theta, manifest['event']['node'])
        direction = list(integration.angular.inherited.source.angular_nodes(8))[0][0]
        owner = integration.Direction(integration.precise_context(parameters), direction)
        factors = FullTailFactors(owner, bundle, context['tests'])
        high, low = bundle.high[:, ::2], bundle.low[:, ::2]
        reference = FactoredEpochResponse(factors, high, low)
        soft = [scalar(value) * owner.temperature / owner.doppler for value in (1e-4, .01)]
        events = {sign: [owner.event(sign * value) for value in soft] for sign in (-1, 1)}
        expected = {(sign, node, join, degree): reference.current(join, degree, soft[node], events[sign][node], sign)
            for sign in (-1, 1) for node in range(2) for join in (0, 1) for degree in (0, 1, 2)}
        for capacity in (1, 2, 4):
            bounded = BoundedFactoredEpochResponse(factors, high, low, capacity)
            maximum_events, maximum_readouts = 0, 0
            for repeat in range(2):
                for sign in (-1, 1):
                    for node in range(2):
                        for join in (0, 1):
                            for degree in (0, 1, 2):
                                guard()
                                actual = bounded.current(join, degree, soft[node], events[sign][node], sign)
                                prefix = f'capacity{capacity}:repeat{repeat}:sign{sign}:node{node}:join{join}:l{degree}'
                                for field in ('complete', 'reference', 'right_delta'):
                                    compare(prefix + ':' + field, actual[field], expected[sign, node, join, degree][field])
                                maximum_events = max(maximum_events, len(bounded.current_operators))
                                maximum_readouts = max(maximum_readouts, len(bounded.current_readouts))
                                exact(prefix + ':capacity', len(bounded.current_operators) <= capacity and len(bounded.current_readouts) <= 2 * capacity)
                                exact(prefix + ':no-orphans', all(key[0] in bounded.current_operators for key in bounded.current_readouts))
            exact(f'capacity{capacity}:expected-evictions', bounded.evictions == (8 - capacity if capacity < 4 else 0))
            capacities.append(dict(capacity=capacity, maximum_events=maximum_events, maximum_readouts=maximum_readouts, evictions=bounded.evictions))
            print(json.dumps(dict(capacity_complete=capacity, evictions=bounded.evictions)), flush=True)
        for capacity in (0, -1, 9, 1.5, True):
            try:
                BoundedFactoredEpochResponse(factors, high, low, capacity)
            except ValueError:
                rejected = True
            else:
                rejected = False
            exact('reject-capacity:' + repr(capacity), rejected)
    for path, checksum in inputs.items():
        if digest(path) != checksum:
            raise RuntimeError('Frozen input changed during cache check: ' + path)
    report = dict(passed=all(row['passed'] for row in checks), checks=checks, capacities=capacities, inputs=inputs,
        maximum_relative=max(row.get('relative', 0) for row in checks), process=identity,
        prediction_sha256=digest(DESTINATION / 'prediction.json'), finished_at=datetime.now(timezone.utc).isoformat(),
        seconds=time.monotonic() - started, all_physical_columns_retained=True, original_bank_changed=False,
        original_grids_changed=False, original_tolerances_changed=False, main_propagation_head=424)
    write(DESTINATION / 'validation.json', report)
    print(json.dumps(dict(passed=report['passed'], checks=len(checks), maximum_relative=report['maximum_relative'],
        capacities=capacities, failed=[row for row in checks if not row['passed']][:8], seconds=report['seconds'])), flush=True)
    return 0 if report['passed'] else 1


try:
    exit_code = main()
except BaseException as error:
    write(DESTINATION / 'end.json', dict(state='exception', process=identity, finished_at=datetime.now(timezone.utc).isoformat(),
        exception=repr(error), traceback=traceback.format_exc(), automatic_retry_allowed=False))
    raise
else:
    write(DESTINATION / 'end.json', dict(state='passed' if exit_code == 0 else 'failed', process=identity,
        finished_at=datetime.now(timezone.utc).isoformat(), exit_code=exit_code, automatic_retry_allowed=False))
    raise SystemExit(exit_code)
