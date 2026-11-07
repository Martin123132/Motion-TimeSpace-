import argparse
import csv
import hashlib
import itertools
import json
import math
import os
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import psutil

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def read(path):
    return json.loads(Path(path).read_text())


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def ownership(pid, created):
    try:
        current = psutil.Process(pid)
        require(created is not None, 'Live PID with missing creation time requires review')
        return abs(current.create_time() - datetime.fromisoformat(created).timestamp()) < .01
    except psutil.NoSuchProcess:
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--first-ray', type=int, required=True, choices=range(1, 127))
    parser.add_argument('--check-only', action='store_true')
    arguments = parser.parse_args()
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([4])
    rays = [arguments.first_ray, arguments.first_ray + 1]
    campaign = ROOT / f'final-real-batch-rays{rays[0]:03d}-{rays[1]:03d}'
    output = campaign / 'integrity.json'
    require(arguments.check_only or not output.exists(), 'Existing integrity receipt preserved')
    protocol, ending = read(campaign / 'protocol.json'), read(campaign / 'end.json')
    require(ending['state'] == 'complete' and ending['completed_rays'] == protocol['rays'] == rays, 'Passing completed pair required')
    require(protocol['maximum_active_workers'] == 1 and protocol['panels_per_batch'] == 8 and protocol['radial_orders'] == [18, 26], 'Frozen batch policy changed')
    require(protocol['adapter_sha256'].lower() == read(ROOT / 'final-real-batch-rays001-002/protocol.json')['adapter_sha256'].lower(), 'Numerical worker differs from qualified previous batch')
    inputs = {}

    def register(path, expected):
        key = os.path.normcase(str(Path(path).resolve()))
        expected = expected.lower()
        require(key not in inputs or inputs[key] == expected, 'Conflicting source hashes: ' + key)
        inputs[key] = expected

    def guard():
        require(not any((directory / 'STOP-REQUESTED').exists() for directory in (ROOT, ROOT.parent, campaign))
                and not (ROOT.parent / 'execution-v3/STOP-REQUEST.json').exists()
                and not 3 <= datetime.now(timezone.utc).astimezone(ZoneInfo('Europe/London')).hour < 14,
                'Owner/music hold preserved')

    guard()
    for name in ('adapter', 'supervisor'):
        register(protocol[name], protocol[name + '_sha256'])
    register(protocol['execution_router']['retained_supervisor'], protocol['execution_router']['retained_sha256'])
    preserved = protocol['preserved_inputs']
    require(len(preserved) == 9 * rays[0], 'Earlier completion evidence coverage differs')
    for path, expected in preserved.items():
        register(path, expected)
    for previous in range(rays[0]):
        prior = ROOT / f'final-epoch-real-source-ray{previous:03d}'
        for path, expected in read(prior / 'protocol.json')['inputs'].items():
            register(path, expected)
    manifest = read(ROOT / 'saved-epoch-cell450/manifest.json')
    components = ('bank', 'candidate', 'bilinear_delta', 'equilibrium_delta')
    expected_rows = set(itertools.product(('control', 'difference', 'combined'), (0, 1), (0, 1, 2),
                                          ('heavy', 'cold'), (1, 2, 4), components))
    summaries = []
    for ray in rays:
        guard()
        directory = ROOT / f'final-epoch-real-source-ray{ray:03d}'
        qualified = ROOT / f'compensated-epoch-source-final450-ray{ray:03d}'
        local = read(directory / 'protocol.json')
        require(local['history_cell'] == 450 and local['angular_ray'] == ray and local['angular_order'] == 8,
                'Actual final direction identity differs')
        require(all(local[name] == manifest[name] for name in ('theta', 'event', 'labels'))
                and local['gate'] == 1e-10 and local['source_refinement_budget'] == .002, 'Frozen histories or gates differ')
        cache = read(ROOT / f'final-epoch-kinematic-bank/ray-{ray:03d}.json')
        require(cache['passed'] and cache['ray'] == ray and cache['angular_weight'] == local['angular_weight'], 'Wrong cache or angular weight')
        register(ROOT / f'final-epoch-kinematic-bank/ray-{ray:03d}-kernel.json', cache['kernel_sha256'])
        for path, expected in local['inputs'].items():
            register(path, expected)
        require(read(qualified / 'prediction.json')['angular_ray'] == ray, 'Precision qualification belongs to another direction')
        qualification = []
        for name in ('validation.json', 'native-paired-check/validation.json'):
            record = read(qualified / name)
            require(record['actual_history_cell'] == 450 and record['passed'] and all(row['passed'] for row in record['checks']), 'Unqualified ray-specific source')
            for path, expected in record['inputs'].items():
                register(path, expected)
            for packet in record['packets']:
                register(packet['path'], packet['sha256'])
            qualification.append(dict(name=name, checks=len(record['checks']), maximum=max(row.get('relative', 0) for row in record['checks'])))
        orders = []
        for order in (18, 26):
            job = directory / f'order-{order}'
            complete, independent = read(job / 'complete.json'), read(job / 'independent.json')
            require(complete['passed'] and independent['passed'] and all(row['passed'] for row in independent['checks']), 'Radial source or reconstruction gate failed')
            previous = digest(directory / 'protocol.json')
            require(complete['protocol_sha256'] == independent['protocol_sha256'] == previous, 'Radial protocol mismatch')
            records = sorted(job.glob('panel-*.json'))
            require(len(records) == complete['panels'] == len(local['panels'][str(order)]), 'Panel coverage mismatch')
            for index, path in enumerate(records):
                record = read(path)
                require(record['passed'] and record['panel'] == index and record['order'] == order and record['previous_sha256'] == previous,
                        'Radial restart chain mismatch: ' + str(path))
                register(path.with_suffix('.npz'), record['packet_sha256'])
                previous = digest(path)
                register(path, previous)
            require(complete['last_panel_sha256'] == previous, 'Final panel link mismatch')
            register(job / 'complete.json', independent['complete_sha256'])
            require(complete['packet_sha256'] == independent['complete_packet_sha256'], 'Completed packet mismatch')
            register(job / 'complete.npz', complete['packet_sha256'])
            orders.append(dict(order=order, panels=len(records), independent_vectors=independent['checked_vectors'], maximum_identity=independent['maximum_relative']))
        comparison = read(directory / 'order18-vs26.json')
        require(comparison['all_component_rows_within_budget'] and comparison['budget'] == .002, 'Original refinement gate failed')
        for path, expected in comparison['inputs'].items():
            register(path, expected)
        marker = read(campaign / f'ray{ray:03d}-complete.json')
        require(marker['passed'] and marker['ray'] == ray and Path(marker['comparison']).resolve() == (directory / 'order18-vs26.json').resolve(), 'Completion marker mismatch')
        register(marker['comparison'], marker['sha256'])
        rows = comparison['rows']
        fields = ('mode', 'join', 'degree', 'model', 'subdivision', 'component')
        require(len(rows) == len(expected_rows) and {tuple(row[name] for name in fields) for row in rows} == expected_rows,
                'Missing or duplicate baseline/MTS refinement combination')
        with (directory / 'order18-vs26.csv').open(newline='', encoding='utf-8') as stream:
            csv_rows = list(csv.DictReader(stream))
        require(len(csv_rows) == len(rows), 'CSV row count mismatch')
        for row, csv_row in zip(rows, csv_rows):
            require(row['within_component_budget'] and row['budget'] == .002 and math.isfinite(row['relative']) and 0 <= row['relative'] <= .002,
                    'Invalid refinement result')
            require(None not in csv_row and all(str(row[name]) == csv_row[name] for name in fields)
                    and all(float(csv_row[name]) == row[name] for name in ('absolute', 'scale', 'relative', 'budget'))
                    and csv_row['within_component_budget'] == 'True', 'CSV diagnostics differ from JSON')
        summaries.append(dict(ray=ray, comparison=str(directory / 'order18-vs26.json'), comparison_sha256=marker['sha256'],
                              rows=len(rows), orders=orders, qualification=qualification,
                              maximum_relative=max(row['relative'] for row in rows),
                              component_maxima={name:max(row['relative'] for row in rows if row['component'] == name) for name in components}))
    for index, (path, expected) in enumerate(inputs.items()):
        if index % 32 == 0:
            guard()
        require(digest(path) == expected, 'Frozen file changed: ' + path)
    for run in ending['runs']:
        require(run['actual_exit_code'] == 0 and run['process_exited'] and not ownership(run['pid'], run['creation_time']),
                'Task worker did not exit cleanly: ' + run['label'])
    require(not ownership(protocol['process']['pid'], protocol['process']['creation_time']), 'Supervisor still active')
    result = dict(passed=True, checked_at=datetime.now(timezone.utc).isoformat(), started=protocol['started_utc'], finished=ending['finished_utc'],
                  campaign=str(campaign), protocol_sha256=digest(campaign/'protocol.json'), end_sha256=digest(campaign/'end.json'),
                  completed_new_rays=rays, completed_total_rays=list(range(rays[-1]+1)), remaining_count=127-rays[-1],
                  rays=summaries, new_radial_panels=sum(order['panels'] for summary in summaries for order in summary['orders']),
                  new_comparison_rows=sum(summary['rows'] for summary in summaries), maximum_new_relative=max(summary['maximum_relative'] for summary in summaries),
                  verified_unique_files=len(inputs), preserved_prior_files=len(preserved), inputs_sha256=hashlib.sha256(json.dumps(inputs,sort_keys=True).encode()).hexdigest(),
                  input_mismatches=[], csv_and_cartesian_coverage=True, successful_child_exits=len(ending['runs']),
                  supervisor_exited=True, task_workers_still_running=0, killed_processes=[], github_actions=False,
                  script_sha256=digest(__file__), audit_process=dict(pid=process.pid, created_time=process.create_time(), command=process.cmdline()),
                  scope='Finite real/pole source plus separator at final x14/event0; per-direction order18/26 diagnostic, not full angular or final-spectrum error')
    if not arguments.check_only:
        with output.open('x', encoding='utf-8') as stream:
            json.dump(result,stream,indent=2,allow_nan=False)
    print(json.dumps(result,allow_nan=False))


if __name__ == '__main__':
    main()
