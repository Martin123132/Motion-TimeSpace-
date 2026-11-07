import os
for variable in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
    os.environ[variable] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

import argparse
import ast
import json
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo
import psutil

ROOT = Path(__file__).resolve().parent
CONSUMER = ROOT / 'saved-epoch-cell450'
QUALIFIED = ROOT / 'compensated-epoch-source-final450-001'
DESTINATION = ROOT / 'final-epoch-real-source-ray000'
process = psutil.Process()
process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
process.cpu_affinity([4])
sys.dont_write_bytecode = True
sys.setrecursionlimit(3000)
parser = argparse.ArgumentParser()
parser.add_argument('mode', choices=('freeze', 'run'))
parser.add_argument('--order', type=int, choices=(18, 26), default=26)
parser.add_argument('--panels', type=int, default=41)
parser.add_argument('--minutes', type=float, default=55)
parser.add_argument('--stop-utc')
arguments = parser.parse_args()
if not 1 <= arguments.panels <= 41 or not 0 < arguments.minutes <= 60:
    parser.error('One bounded worker,1..41 panels,at most60minutes')
if arguments.mode == 'run' and not arguments.stop_utc:
    parser.error('A separately supplied current-turn UTC stop time is required')
stop_time = datetime.fromisoformat(arguments.stop_utc.replace('Z', '+00:00')) if arguments.stop_utc else None
if stop_time and stop_time.utcoffset().total_seconds() != 0:
    parser.error('Stop time must be explicit UTC')
started = time.monotonic()


def now():
    return datetime.now(timezone.utc).isoformat()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.flush()
        os.fsync(stream.fileno())


def identity():
    return dict(pid=process.pid, created_time=process.create_time(), command=process.cmdline(),
                priority=process.nice(), affinity=process.cpu_affinity())


def stopping():
    directories = (ROOT, ROOT.parent, CONSUMER, QUALIFIED, DESTINATION)
    return (any((directory / 'STOP-REQUESTED').exists() for directory in directories)
            or (ROOT.parent / 'execution-v3/STOP-REQUEST.json').exists()
            or 3 <= datetime.now(timezone.utc).astimezone(ZoneInfo('Europe/London')).hour < 14
            or bool(stop_time and datetime.now(timezone.utc) >= stop_time))


def guard():
    if stopping():
        raise RuntimeError('Owner/time stop preserved; no automatic retry')


guard()
from restart_readout import digest
from run_final_epoch_qualification import source_text
import numpy as np
import mpmath as mp
from coupled_source_difference import assemble


def verify(inputs):
    for path, expected in inputs.items():
        if digest(path) != expected:
            raise RuntimeError('Frozen input changed: ' + path)


def save(path, arrays):
    with Path(path).open('xb') as stream:
        np.savez_compressed(stream, **arrays)
        stream.flush()
        os.fsync(stream.fileno())


def cached_owner(parameters, direction):
    from exact_kinematic_cache import CachedDirection
    report_path = ROOT / 'final-epoch-kinematic-bank/ray-000.json'
    report = read(report_path)
    if not report['passed'] or report['ray'] != 0:
        raise RuntimeError('Qualified final direction required')
    return CachedDirection(parameters, direction, ROOT / 'final-epoch-kinematic-bank/ray-000-kernel.json',
                           report['kernel_sha256'])


def setup():
    source = source_text('precise')
    previous = 'owner = RationalDirection(retained.precise_context(parameters), direction)'
    if source.count(previous) != 1:
        raise RuntimeError('Qualified owner construction boundary changed')
    source = source.replace(previous, 'owner = cached_owner(retained.precise_context(parameters), direction)')
    main_function = next(statement for statement in ast.parse(source).body
                         if isinstance(statement, ast.FunctionDef) and statement.name == 'main')
    statements = []
    for statement in main_function.body:
        if isinstance(statement, ast.Assign) and any(isinstance(target, ast.Name) and target.id == 'protocol' for target in statement.targets):
            break
        statements.append(statement)
    else:
        raise RuntimeError('Read-only setup boundary changed')
    context = dict(__file__=str(ROOT / 'check_precise_compensated_source.py'), __name__='final_real_source_setup',
                   ROOT=ROOT, CONSUMER=CONSUMER, read=read, ast=ast, json=json, sys=sys, Path=Path,
                   cached_owner=cached_owner, endpoint_guard=guard)
    exec(compile(ast.Module(body=statements, type_ignores=[]), 'final_real_source_setup', 'exec'), context)
    return context


def describe(panels):
    return [dict(panel=index, frequencies=list(map(float, frequency)), measures=list(map(float, measure)),
                 emission=bool(emission), absorption=bool(absorption))
            for index, (frequency, measure, emission, absorption) in enumerate(panels)]


def flatten(actions, labels):
    result = {}
    for key, values in actions.items():
        name = f'{key[0]}:join{key[1]}:l{key[2]}'
        result[name + ':actions'] = values
        for case, components in assemble(values, labels).items():
            for component, vector in components.items():
                result[name + ':' + case + ':' + component] = vector
    return result


def checks_for(arrays):
    checks = []
    for name, values in arrays.items():
        if not np.isfinite(values).all():
            raise FloatingPointError('Nonfinite source: ' + name)
        if not name.endswith(':actions') or ':l2:' in name:
            continue
        photon, gas = values[:, 0, :], values[:, -1, :]
        residual = np.abs(photon + gas) / np.maximum(np.abs(photon) + np.abs(gas), 1e-300)
        checks.append(dict(name=name + ':exchange', entries=int(residual.size),
                           failed_entries=int(np.sum(residual > 1e-10)), maximum=float(np.max(residual)),
                           limit=1e-10, passed=bool(np.all(residual <= 1e-10))))
    return checks


def accumulate(totals, corrections, values):
    for name, value in values.items():
        if name not in totals:
            totals[name] = np.zeros_like(value)
            corrections[name] = np.zeros_like(value)
        updated = totals[name] + value
        corrections[name] += np.where(np.abs(totals[name]) >= np.abs(value),
                                      (totals[name] - updated) + value,
                                      (value - updated) + totals[name])
        totals[name] = updated


def resolved(totals, corrections):
    high, low = {}, {}
    for name, total in totals.items():
        high[name] = total + corrections[name]
        virtual = high[name] - total
        low[name] = (total - (high[name] - virtual)) + (corrections[name] - virtual)
    return high, low


context = setup()
retained, owner, native, manifest = (context[name] for name in ('retained', 'owner', 'native', 'manifest'))
event_weight, angular_weight = context['event_weight'], context['angular_weight']
panel_action, logarithm_action = context['panel_action'], context['logarithm_action']
keys = [(mode, join, degree) for mode in ('control', 'difference') for join in (0, 1) for degree in (0, 1, 2)]
with mp.workdps(80):
    panels_by_order = {order: list(retained.panels(owner, order, context['source_config'])) for order in (18, 26)}
inputs = dict(context['inputs'])
for relative in ('saved-epoch-cell450/manifest.json', 'saved-epoch-cell450/columns.npz',
                 'compensated-epoch-source-final450-001/validation.json',
                 'compensated-epoch-source-final450-001/native-paired-check/validation.json',
                 'final-epoch-kinematic-bank/protocol.json', 'final-epoch-kinematic-bank/ray-000.json',
                 'final-epoch-kinematic-bank/ray-000-kernel.json', 'final_epoch_real_source.py',
                 'run_final_epoch_qualification.py', 'coupled_source_difference.py', 'exact_kinematic_cache.py',
                 'check_final_source_accumulation.py', 'final-source-sum-controls.json'):
    path = ROOT / relative
    inputs[str(path)] = digest(path)
for path in (QUALIFIED / 'validation.json', QUALIFIED / 'native-paired-check/validation.json'):
    report = read(path)
    if not report['passed'] or not all(row['passed'] for row in report['checks']):
        raise RuntimeError('Actual endpoint source qualification failed')
    inputs.update(report['inputs'])
    for packet in report.get('packets', report.get('outputs', [])):
        inputs[packet['path']] = packet['sha256']
sum_controls = read(ROOT / 'final-source-sum-controls.json')
if not sum_controls['passed']:
    raise RuntimeError('Source accumulation controls failed')
verify(sum_controls['inputs'])
verify(inputs)
guard()

if arguments.mode == 'freeze':
    if DESTINATION.exists():
        raise RuntimeError('Existing frozen source campaign preserved')
    DESTINATION.mkdir()
    write(DESTINATION / 'protocol.json', dict(frozen_at=now(), process=identity(), inputs=inputs,
        history_cell=450, coordinate=manifest['coordinate'], theta=manifest['theta'], event=manifest['event'],
        angular_ray=0, angular_order=8, angular_weight=float(angular_weight), event_weight=event_weight,
        panels={str(order): describe(panels) for order, panels in panels_by_order.items()},
        labels=manifest['labels'], gate=1e-10, source_refinement_budget=0.002,
        predictions=['Physical photon/gas exchange remains balanced in every retained source block',
                     'Stable paired contrasts retain all three bilinear terms through radial integration'],
        scope='One actual endpoint x14/event0/ray0 finite real/pole radial integral plus mandatory separator logarithm',
        full_angular_sum=False, matched_virtual_state_conversion_included=False, source_budget_assessed=False,
        normalization='Original event/angular/radial weights included once; no renormalization',
        summation='Neumaier full actions and separately accumulated stable paired components; two-sum high/low final packets',
        original_bank_changed=False, grids_changed=False, tolerances_changed=False))
    print(json.dumps(dict(frozen=True, inputs=len(inputs), panels={order: len(value) for order, value in panels_by_order.items()})), flush=True)
    raise SystemExit(0)

protocol = read(DESTINATION / 'protocol.json')
verify(protocol['inputs'])
if inputs != protocol['inputs'] or describe(panels_by_order[arguments.order]) != protocol['panels'][str(arguments.order)]:
    raise RuntimeError('Source inputs or original nodes/weights changed')
job = DESTINATION / f'order-{arguments.order}'
job.mkdir(exist_ok=True)
if (job / 'complete.json').exists():
    raise RuntimeError('Completed quadrature preserved')
for previous in job.glob('attempt-*-start.json'):
    ending = previous.with_name(previous.name.replace('-start', '-end'))
    if not ending.exists() or read(ending)['state'] != 'batch_complete':
        raise RuntimeError('Prior interruption/failure requires review')
attempt = 'attempt-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
write(job / (attempt + '-start.json'), dict(started_at=now(), process=identity(), order=arguments.order,
      maximum_panels=arguments.panels, maximum_minutes=arguments.minutes, stop_utc=arguments.stop_utc))
previous_hash, records = digest(DESTINATION / 'protocol.json'), []
totals, corrections = {}, {}
panels = panels_by_order[arguments.order]
for index in range(len(panels)):
    path = job / f'panel-{index:03d}.json'
    if not path.exists():
        if path.with_suffix('.npz').exists():
            raise RuntimeError('Unsealed panel packet preserved')
        break
    record = read(path)
    if not record['passed'] or record['panel'] != index or record['previous_sha256'] != previous_hash or digest(path.with_suffix('.npz')) != record['packet_sha256']:
        raise RuntimeError('Panel chain changed')
    records.append(record)
    previous_hash = digest(path)
if records:
    with np.load(job / f'panel-{len(records)-1:03d}.npz', allow_pickle=False) as saved:
        totals = {name[4:]: saved[name].copy() for name in saved.files if name.startswith('sum:')}
        corrections = {name[5:]: saved[name].copy() for name in saved.files if name.startswith('corr:')}
state = 'batch_complete'
deadline = time.monotonic() + arguments.minutes * 60
try:
    with mp.workdps(80):
        retained.state235.mean_energy.cache_clear()
        for index in range(len(records), min(len(panels), len(records) + arguments.panels)):
            if stopping():
                state = 'operational_pause'
                break
            if time.monotonic() >= deadline:
                break
            began = time.monotonic()
            frequency, measure, emission, absorption = panels[index]
            soft = [retained.scalar(value) * owner.temperature / owner.doppler for value in frequency]
            densities, events = {}, {}
            for sign, allowed in ((1, emission), (-1, absorption)):
                if allowed:
                    evaluated = [owner.densities(sign * value) for value in soft]
                    densities[sign] = [value[0] for value in evaluated]
                    events[sign] = [value[1] for value in evaluated]
            factor_data = {sign: native.evaluate(soft, values, sign) for sign, values in events.items()}
            actions = {key: panel_action(native, frequency, measure, densities, factor_data, *key,
                       event_weight, angular_weight, emission, absorption) for key in keys}
            values = flatten(actions, manifest['labels'])
            checks = checks_for(values)
            accumulate(totals, corrections, values)
            packet = job / f'panel-{index:03d}.npz'
            save(packet, {**{'point:' + name: value for name, value in values.items()},
                          **{'sum:' + name: value for name, value in totals.items()},
                          **{'corr:' + name: value for name, value in corrections.items()}})
            record = dict(panel=index, order=arguments.order, passed=all(row['passed'] for row in checks),
                          previous_sha256=previous_hash, packet_sha256=digest(packet), checks=checks,
                          process=identity(), seconds=time.monotonic() - began, finished_at=now())
            write(packet.with_suffix('.json'), record)
            print(json.dumps(dict(panel=index, order=arguments.order, passed=record['passed'], seconds=record['seconds'])), flush=True)
            if not record['passed']:
                state = 'failed_gate'
                break
            records.append(record)
            previous_hash = digest(packet.with_suffix('.json'))
        if len(records) == len(panels) and state == 'batch_complete':
            log_actions = {key: logarithm_action(native, *key, event_weight, angular_weight) for key in keys}
            logarithms = flatten(log_actions, manifest['labels'])
            finite, finite_low = resolved(totals, corrections)
            accumulate(totals, corrections, logarithms)
            final, final_low = resolved(totals, corrections)
            checks = checks_for(logarithms) + checks_for(final)
            packet = job / 'complete.npz'
            save(packet, {**{'finite:' + name: value for name, value in finite.items()},
                          **{'finite_low:' + name: value for name, value in finite_low.items()},
                          **{'logarithm:' + name: value for name, value in logarithms.items()},
                          **{'total:' + name: value for name, value in final.items()},
                          **{'total_low:' + name: value for name, value in final_low.items()},
                          **{'rawsum:' + name: value for name, value in totals.items()},
                          **{'corr:' + name: value for name, value in corrections.items()}})
            verify(protocol['inputs'])
            passed = all(row['passed'] for row in checks)
            write(job / 'complete.json', dict(passed=passed, panels=len(records), order=arguments.order,
                last_panel_sha256=previous_hash, protocol_sha256=digest(DESTINATION / 'protocol.json'),
                packet_sha256=digest(packet), checks=checks, process=identity(), finished_at=now(),
                final_high_low_reconstruction='total plus total_low; rawsum/corr are audit state, not extra source terms',
                whole_source_complete=False, source_refinement_budget_assessed=False))
            state = 'complete' if passed else 'failed_gate'
except BaseException as error:
    write(job / (attempt + '-end.json'), dict(state='exception', process=identity(), finished_at=now(),
          error=repr(error), traceback=traceback.format_exc(), completed_panels=len(records), no_automatic_retry=True))
    raise
else:
    write(job / (attempt + '-end.json'), dict(state=state, process=identity(), finished_at=now(),
          completed_panels=len(records), no_automatic_retry=True))
    print(json.dumps(dict(state=state, order=arguments.order, completed_panels=len(records))), flush=True)
    raise SystemExit(0 if state in ('complete', 'batch_complete') else 2 if state == 'operational_pause' else 1)
