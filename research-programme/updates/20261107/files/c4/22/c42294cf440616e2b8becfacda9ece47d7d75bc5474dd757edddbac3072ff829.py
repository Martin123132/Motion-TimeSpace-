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
PARENT = ROOT / 'compensated-epoch-source-001'
DESTINATION = PARENT / 'native-paired-check'
process = psutil.Process()
process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
process.cpu_affinity([4])
sys.dont_write_bytecode = True
started = time.monotonic()


def now():
    return datetime.now(timezone.utc).isoformat()


def read(path):
    return json.loads(Path(path).read_text())


def write(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)


def guard():
    if time.monotonic() - started > 20 * 60:
        raise TimeoutError('Bounded native paired-source check reached20 minutes')
    if any((path / 'STOP-REQUESTED').exists() for path in (ROOT, ROOT.parent, CONSUMER, PARENT, DESTINATION)):
        raise RuntimeError('Owner stop preserved')
    if (ROOT.parent / 'execution-v3/STOP-REQUEST.json').exists():
        raise RuntimeError('Execution stop preserved')


guard()
if DESTINATION.exists():
    raise RuntimeError('Existing native paired check preserved')
DESTINATION.mkdir()
identity = dict(pid=process.pid, created_time=process.create_time(), command=process.cmdline(),
    priority=process.nice(), affinity=process.cpu_affinity())
write(DESTINATION / 'start.json', dict(started_at=now(), process=identity))
print(json.dumps(dict(started=True, process=identity)), flush=True)


def main():
    from restart_readout import digest
    from coupled_source_difference import assemble

    report = read(PARENT / 'validation.json')
    protocol = read(PARENT / 'prediction.json')
    if not report['passed'] or report['selected_points'] != 7:
        raise RuntimeError('All seven compensated source points must be qualified')
    inputs = dict(report['inputs'])
    for path in (Path(__file__), ROOT / 'coupled_source_difference.py', PARENT / 'validation.json', PARENT / 'prediction.json'):
        inputs[str(path)] = digest(path)
    for packet in report['packets']:
        inputs[packet['path']] = packet['sha256']
    for path, checksum in inputs.items():
        if digest(path) != checksum:
            raise RuntimeError('Frozen input changed: ' + path)
    compile(Path(__file__).read_text(), str(Path(__file__)), 'exec')
    source = ROOT / 'check_precise_compensated_source.py'
    main_function = next(statement for statement in ast.parse(source.read_text()).body
        if isinstance(statement, ast.FunctionDef) and statement.name == 'main')
    statements = []
    for statement in main_function.body:
        if isinstance(statement, ast.Assign) and any(isinstance(target, ast.Name) and target.id == 'protocol' for target in statement.targets):
            break
        statements.append(statement)
    else:
        raise RuntimeError('Read-only setup boundary changed')
    context = dict(__file__=str(source), __name__='reused_compensated_source_setup', ROOT=ROOT,
        CONSUMER=CONSUMER, read=read, ast=ast, json=json, sys=sys, Path=Path)
    exec(compile(ast.Module(body=statements, type_ignores=[]), str(source), 'exec'), context)
    np, mp, retained, scalar, owner, native, manifest, event_weight, angular_weight = (
        context[name] for name in ('np', 'mp', 'retained', 'scalar', 'owner', 'native', 'manifest', 'event_weight', 'angular_weight'))
    panel_action, logarithm_action = context['panel_action'], context['logarithm_action']
    if context['descriptions'] != protocol['points'] or event_weight != protocol['event_weight'] or float(angular_weight) != protocol['angular_weight']:
        raise RuntimeError('Original point identities or weights changed')
    write(DESTINATION / 'prediction.json', dict(frozen_at=now(), inputs=inputs, gate=1e-10,
        reference='Saved compensated80-digit point/log packets, already compared with independent100-digit source',
        prediction='Fast native three-term coupled and equilibrium differences pass for both models/all refinements',
        direct_rounded_subtraction='Diagnostic only; preserve any failure at the same gate',
        original_bank_changed=False, original_grids_changed=False, original_tolerances_changed=False,
        no_high_precision_response_recomputation=True, selected_points=7, includes_separator_logarithm=True))
    checks, diagnostics, outputs = [], [], []

    def compare(name, actual, expected, group, target=None):
        target = checks if target is None else target
        error = mp.sqrt(mp.fsum((scalar(value) - reference)**2 for value, reference in zip(actual, expected)))
        scale = max(mp.sqrt(mp.fsum(value**2 for value in expected)), mp.mpf('1e-300'))
        relative = error / scale
        target.append(dict(name=name, group=group, relative=float(relative), absolute=float(error), limit=1e-10,
            passed=bool(mp.isfinite(relative) and relative <= mp.mpf('1e-10'))))

    def restored(high, low):
        return [scalar(upper) + scalar(lower) for upper, lower in zip(high, low)]

    def qualify(label, actions, saved, storage):
        high, low = saved[label + ':high'], saved[label + ':low']
        delta_high, delta_low = saved[label + ':difference-high'], saved[label + ':difference-low']
        assembly = assemble(actions, manifest['labels'])
        for pair, (case, result) in enumerate(assembly.items()):
            baseline, candidate, change = 3 * pair, 3 * pair + 1, 3 * pair + 2
            delta = restored(delta_high[pair], delta_low[pair])
            equilibrium_delta = restored(high[0, :, change], low[0, :, change])
            compare(label + ':' + case, result['bilinear_delta'], delta, 'native-stable-paired')
            compare(label + ':' + case, result['equilibrium_delta'], equilibrium_delta, 'native-stable-equilibrium')
            compare(label + ':' + case, result['bank'], restored(high[baseline + 1, :, baseline], low[baseline + 1, :, baseline]), 'native-baseline')
            compare(label + ':' + case, result['candidate'], restored(high[candidate + 1, :, candidate], low[candidate + 1, :, candidate]), 'native-MTS')
            compare(label + ':' + case, result['candidate'] - result['bank'], delta, 'rounded-paired-subtraction', diagnostics)
            compare(label + ':' + case, actions[0, :, candidate] - actions[0, :, baseline], equilibrium_delta, 'rounded-equilibrium-subtraction', diagnostics)
            for name, values in result.items():
                storage[label + ':' + case + ':' + name] = values
        storage[label + ':all-native-actions'] = actions

    with mp.workdps(80):
        retained.state235.mean_energy.cache_clear()
        for point_index, description in enumerate(protocol['points']):
            guard()
            frequency, measure = description['frequency'], description['measure']
            soft = scalar(frequency) * owner.temperature / owner.doppler
            densities, native_data = {}, {}
            for sign, allowed in ((1, description['emission']), (-1, description['absorption'])):
                if allowed:
                    density, event = owner.densities(sign * soft)
                    densities[sign] = [density]
                    native_data[sign] = native.evaluate([soft], [event], sign)
            storage = {}
            with np.load(PARENT / f'point-{point_index:03d}.npz', allow_pickle=False) as saved:
                for mode in ('control', 'difference'):
                    for join in (0, 1):
                        for degree in (0, 1, 2):
                            actions = panel_action(native, np.array([frequency]), np.array([measure]), densities, native_data,
                                mode, join, degree, event_weight, angular_weight, description['emission'], description['absorption'])
                            qualify(f'point{point_index}:{mode}:join{join}:l{degree}', actions, saved, storage)
            path = DESTINATION / f'point-{point_index:03d}.npz'
            with path.open('xb') as stream:
                np.savez_compressed(stream, **storage)
            outputs.append(dict(path=str(path), sha256=digest(path)))
            print(json.dumps(dict(point_complete=point_index, checks=len(checks), failures=sum(not row['passed'] for row in checks))), flush=True)
        storage = {}
        with np.load(PARENT / 'separator-logarithm.npz', allow_pickle=False) as saved:
            for mode in ('control', 'difference'):
                for join in (0, 1):
                    for degree in (0, 1, 2):
                        actions = logarithm_action(native, mode, join, degree, event_weight, angular_weight)
                        qualify(f'logarithm:{mode}:join{join}:l{degree}', actions, saved, storage)
        path = DESTINATION / 'separator-logarithm.npz'
        with path.open('xb') as stream:
            np.savez_compressed(stream, **storage)
        outputs.append(dict(path=str(path), sha256=digest(path)))
    for path, checksum in inputs.items():
        if digest(path) != checksum:
            raise RuntimeError('Frozen source changed during paired check: ' + path)
    def summary(rows):
        return {group: dict(checks=sum(row['group'] == group for row in rows), failed=sum(row['group'] == group and not row['passed'] for row in rows),
            maximum_relative=max(row['relative'] for row in rows if row['group'] == group)) for group in sorted({row['group'] for row in rows})}
    result = dict(passed=all(row['passed'] for row in checks), checks=checks, groups=summary(checks),
        diagnostics=diagnostics, diagnostic_groups=summary(diagnostics), inputs=inputs, packets=outputs, process=identity,
        prediction_sha256=digest(DESTINATION / 'prediction.json'), finished_at=now(), seconds=time.monotonic() - started,
        source_integrated=False, no_high_precision_response_recomputation=True, actual_history_cell=424,
        original_bank_changed=False, original_grids_changed=False, original_tolerances_changed=False)
    write(DESTINATION / 'validation.json', result)
    print(json.dumps(dict(passed=result['passed'], checks=len(checks), groups=result['groups'], diagnostics=result['diagnostic_groups'],
        failed=[row for row in checks if not row['passed']][:10], seconds=result['seconds'])), flush=True)
    return 0 if result['passed'] else 1


try:
    exit_code = main()
except BaseException as error:
    write(DESTINATION / 'end.json', dict(state='exception', process=identity, finished_at=now(), exception=repr(error),
        traceback=traceback.format_exc(), automatic_retry_allowed=False))
    raise
else:
    write(DESTINATION / 'end.json', dict(state='passed' if exit_code == 0 else 'failed', process=identity,
        finished_at=now(), exit_code=exit_code, automatic_retry_allowed=False))
    raise SystemExit(exit_code)
