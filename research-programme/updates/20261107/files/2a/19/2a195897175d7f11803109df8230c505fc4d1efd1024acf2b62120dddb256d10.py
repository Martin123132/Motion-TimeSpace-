import os
for variable in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
    os.environ[variable] = '1'
import argparse
import hashlib
import json
import math
import sys
from contextlib import ExitStack
from datetime import datetime, timezone
from pathlib import Path
import psutil
import numpy as np

sys.dont_write_bytecode = True
process = psutil.Process()
process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
process.cpu_affinity([4])
ROOT = Path(__file__).resolve().parent
DESTINATION = ROOT / 'final-epoch-real-source-ray000'
parser = argparse.ArgumentParser()
parser.add_argument('--order', type=int, choices=(18, 26), required=True)
arguments = parser.parse_args()
job = DESTINATION / f'order-{arguments.order}'
output = job / 'independent.json'
if output.exists():
    raise RuntimeError('Existing independent evidence preserved')


def read(path):
    return json.loads(Path(path).read_text())


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def guard():
    if (ROOT.parent / 'execution-v3/STOP-REQUEST.json').exists() or any(
            (directory / 'STOP-REQUESTED').exists() for directory in (ROOT, ROOT.parent, DESTINATION)):
        raise RuntimeError('Owner stop preserved')


def independent_sum(arrays):
    if not arrays or any(value.shape != arrays[0].shape for value in arrays):
        raise ValueError('Matching nonempty source arrays required')
    return np.array([math.fsum(map(float, values)) for values in zip(*(value.flat for value in arrays))]).reshape(arrays[0].shape)


checks = []


def compare(name, actual, expected):
    if actual.shape != expected.shape or not np.isfinite(actual).all() or not np.isfinite(expected).all():
        raise ValueError('Invalid source comparison: ' + name)
    if actual.ndim == 3:
        error = np.linalg.norm(actual - expected, axis=1)
        scale = np.linalg.norm(expected, axis=1)
    elif actual.ndim == 1:
        error, scale = np.linalg.norm(actual - expected), np.linalg.norm(expected)
    else:
        raise ValueError('Unexpected retained action shape')
    relative = np.asarray(error / np.maximum(scale, 1e-300))
    checks.append(dict(name=name, entries=int(relative.size), maximum=float(np.max(relative)),
                       failed_entries=int(np.sum(relative > 1e-10)), limit=1e-10,
                       passed=bool(np.all(relative <= 1e-10))))


guard()
protocol_path = DESTINATION / 'protocol.json'
protocol = read(protocol_path)
report = read(job / 'complete.json')
if not report['passed'] or report['protocol_sha256'] != digest(protocol_path):
    raise RuntimeError('Completed source protocol not qualified')
if report['packet_sha256'] != digest(job / 'complete.npz'):
    raise RuntimeError('Completed packet changed')
for path, expected in protocol['inputs'].items():
    if digest(path) != expected:
        raise RuntimeError('Frozen source changed: ' + path)
previous = digest(protocol_path)
expected_panels = protocol['panels'][str(arguments.order)]
metadata_paths = sorted(job.glob('panel-*.json'))
if len(metadata_paths) != len(expected_panels) or len(metadata_paths) != report['panels']:
    raise RuntimeError('Missing or extra radial panels')
for index, path in enumerate(metadata_paths):
    row = read(path)
    if not row['passed'] or row['panel'] != index or row['order'] != arguments.order or row['previous_sha256'] != previous:
        raise RuntimeError('Panel chain changed')
    if row['packet_sha256'] != digest(path.with_suffix('.npz')) or not all(value['passed'] for value in row['checks']):
        raise RuntimeError('Panel packet/check failure')
    previous = digest(path)
if previous != report['last_panel_sha256']:
    raise RuntimeError('Final panel link changed')
qualified = ROOT / 'compensated-epoch-source-final450-001/native-paired-check/separator-logarithm.npz'
finite_reference, total_reference = {}, {}
with ExitStack() as stack:
    packets = [stack.enter_context(np.load(path.with_suffix('.npz'), allow_pickle=False)) for path in metadata_paths]
    complete = stack.enter_context(np.load(job / 'complete.npz', allow_pickle=False))
    logarithm_control = stack.enter_context(np.load(qualified, allow_pickle=False))
    names = sorted(name[6:] for name in packets[0].files if name.startswith('point:'))
    for packet in packets:
        if sorted(name[6:] for name in packet.files if name.startswith('point:')) != names:
            raise RuntimeError('Source component coverage changed')
    for name in names:
        guard()
        points = [packet['point:' + name] for packet in packets]
        finite = independent_sum(points)
        logarithm = complete['logarithm:' + name]
        total = independent_sum([*points, logarithm])
        finite_reference[name], total_reference[name] = finite, total
        compare('finite:' + name, complete['finite:' + name] + complete['finite_low:' + name], finite)
        compare('total:' + name, complete['total:' + name] + complete['total_low:' + name], total)
        control_name = 'logarithm:' + (name[:-len('actions')] + 'all-native-actions' if name.endswith(':actions') else name)
        compare('qualified-logarithm:' + name, logarithm, logarithm_control[control_name])
    labels = {name: index for index, name in enumerate(protocol['labels'])}
    for source_name in [name for name in names if name.endswith(':actions')]:
        guard()
        prefix = source_name[:-len('actions')]
        arrays = [packet['point:' + source_name] for packet in packets] + [complete['logarithm:' + source_name]]
        for model in ('heavy', 'cold'):
            for subdivision in (1, 2, 4):
                baseline = labels[f'{model}-bank-s{subdivision}']
                candidate = labels[f'{model}-candidate-s{subdivision}']
                difference = labels[f'{model}-difference-s{subdivision}']
                extracted = {
                    'bank': [value[baseline + 1, :, baseline] for value in arrays],
                    'candidate': [value[candidate + 1, :, candidate] for value in arrays],
                    'equilibrium_delta': [value[0, :, difference] for value in arrays],
                    'bilinear_delta': [term for value in arrays for term in (
                        value[baseline + 1, :, difference], value[difference + 1, :, baseline],
                        value[difference + 1, :, difference])],
                }
                for component, values in extracted.items():
                    name = prefix + f'{model}-s{subdivision}:' + component
                    compare('independent-paired:' + name,
                            complete['total:' + name] + complete['total_low:' + name],
                            independent_sum(values))
    exchange = []
    for name, values in total_reference.items():
        if name.endswith(':actions') and ':l2:' not in name:
            residual = np.abs(values[:, 0, :] + values[:, -1, :]) / np.maximum(
                np.abs(values[:, 0, :]) + np.abs(values[:, -1, :]), 1e-300)
            exchange.append(dict(name=name, entries=int(residual.size), maximum=float(np.max(residual)),
                                 limit=1e-10, passed=bool(np.all(residual <= 1e-10))))
    checks.extend(exchange)
result = dict(passed=all(row['passed'] for row in checks), checks=checks,
              checked_vectors=sum(row.get('entries', 1) for row in checks), panels=len(metadata_paths),
              order=arguments.order, finished_at=datetime.now(timezone.utc).isoformat(),
              process=dict(pid=process.pid, created_time=process.create_time(), command=process.cmdline()),
              protocol_sha256=digest(protocol_path), complete_sha256=digest(job / 'complete.json'),
              complete_packet_sha256=digest(job / 'complete.npz'), script_sha256=digest(__file__),
              maximum_relative=max(row.get('maximum', 0) for row in checks),
              scope='Independent math.fsum of every saved panel, original qualified separator, independently indexed three-term contrasts and photon/gas exchange; not a second collision solver',
              source_refinement_budget_assessed=False, whole_source_complete=False)
with output.open('x', encoding='utf-8') as stream:
    json.dump(result, stream, indent=2, allow_nan=False)
print(json.dumps(dict(passed=result['passed'], order=arguments.order, panels=result['panels'],
                     checked_vectors=result['checked_vectors'], maximum_relative=result['maximum_relative'],
                     failed=[row for row in checks if not row['passed']][:10])))
raise SystemExit(0 if result['passed'] else 1)
