import csv
import itertools
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import psutil
from verify_remaining_real_pair import digest, read, require


ROOT = Path(__file__).resolve().parent
CAMPAIGN = ROOT / 'final-stable-real-batch-rays003-004'
ORIGINAL = ROOT / 'final-real-batch-rays003-004'


def validate():
    def respect_hold():
        require(not any((folder / 'STOP-REQUESTED').exists() for folder in (CAMPAIGN, ROOT, ROOT.parent))
                and not (ROOT.parent / 'execution-v3/STOP-REQUEST.json').exists()
                and not 3 <= datetime.now(ZoneInfo('Europe/London')).hour < 14, 'Owner/music hold')

    respect_hold()
    protocol = read(CAMPAIGN / 'protocol.json')
    end = read(CAMPAIGN / 'end.json')
    require(end['state'] == 'complete' and end['failure'] is None and end['completed_rays'] == protocol['rays'] == [3, 4], 'Incomplete pair')
    require(protocol['order'] == [18, 26] and protocol['panels_per_job'] == 8 and protocol['max_active_numerical_workers'] == 1, 'Batch policy')
    require(protocol['identity_gate'] == 1e-10 and protocol['refinement_gate'] == .002, 'Original gates')
    hashes = {}

    def track(path, expected):
        path = Path(path).resolve()
        require(path not in hashes or hashes[path] == expected.lower(), 'Conflicting fingerprints: ' + str(path))
        hashes[path] = expected.lower()

    def checks(record):
        require(record['passed'] and record['checks'] and all(row['passed'] for row in record['checks']), 'Missing or failed checks')

    def gone(record):
        try:
            process = psutil.Process(record['pid'])
            require(abs(process.create_time() - record['created_time']) >= .01, 'Owned process still present: ' + str(record['pid']))
        except psutil.NoSuchProcess:
            pass

    previous = read(ORIGINAL / 'protocol.json')['preserved_inputs']
    require(len(previous) == 27 and all(protocol['protected'][path] == value for path, value in previous.items()), 'Rays 0–2 not protected')
    for ledger in (protocol['protected'], protocol['inputs']):
        for path, value in ledger.items():
            track(path, value)
    old = ROOT / 'final-epoch-real-source-ray003'
    required_raw = {old / 'protocol.json'} | {
        old / 'order-18' / f'panel-{index:03d}.{suffix}' for index in range(37) for suffix in ('json','npz')}
    require(required_raw | {Path(path) for path in previous} == {Path(path) for path in protocol['protected']}, 'Preserved raw evidence set')
    for ray in range(3):
        for path, value in read(ROOT / f'final-epoch-real-source-ray{ray:03d}/protocol.json')['inputs'].items():
            track(path, value)
    failed = read(old / 'order-18/panel-036.json')
    require(not failed['passed'] and read(ORIGINAL / 'end.json')['state'] == 'failed', 'Original failed evidence lost')
    replay = read(CAMPAIGN / 'verified-panel036.json')
    checks(replay)
    require(replay['gate'] == 1e-10 and len(replay['checks']) == 6 and all(row.get('maximum', 0) <= replay['gate'] for row in replay['checks']), 'Production oracle')
    for receipt in end['runs']:
        start = read(CAMPAIGN / (receipt['label'] + '.start.json'))
        require(read(CAMPAIGN / (receipt['label'] + '.end.json')) == receipt and all(receipt[key] == val for key, val in start.items())
                and receipt['actual_exit_code'] == 0, 'Child receipt: ' + receipt['label'])
        gone(receipt)
    require(len(end['runs']) == len(list(CAMPAIGN.glob('*.start.json'))) == len(list(CAMPAIGN.glob('*.end.json'))), 'Unaccounted job')
    gone(protocol['process'])
    manifest = read(ROOT / 'saved-epoch-cell450/manifest.json')
    fields = ('mode', 'join', 'degree', 'model', 'subdivision', 'component')
    components = ('bank', 'candidate', 'bilinear_delta', 'equilibrium_delta')
    expected = set(itertools.product(('control','difference','combined'), (0,1), (0,1,2), ('heavy','cold'), (1,2,4), components))
    results = []
    for ray in (3, 4):
        directory = ROOT / f'final-epoch-real-v2-ray{ray:03d}'
        source = ROOT / f'compensated-epoch-source-final450-ray{ray:03d}'
        native = ROOT / f'final-absorption-native-v2-ray{ray:03d}'
        local = read(directory / 'protocol.json')
        if ray == 3:
            prefix = read(directory / 'prefix-reuse.json')
            require(prefix['panels'] == 35 and prefix['order'] == 18 and not prefix['failed_panel_copied']
                    and prefix['source_protocol'] == digest(old / 'protocol.json') and prefix['target_protocol'] == digest(directory / 'protocol.json')
                    and local['panels'] == read(old / 'protocol.json')['panels'], 'Original grid/prefix provenance')
        require((local['angular_ray'], local['angular_order'], local['history_cell'], local['gate'], local['source_refinement_budget']) == (ray,8,450,1e-10,.002)
                and all(local[key] == manifest[key] for key in ('theta','event','labels'))
                and not any(local[key] for key in ('original_bank_changed','grids_changed','tolerances_changed')), 'Ray setup')
        cache = read(ROOT / f'final-epoch-kinematic-bank/ray-{ray:03d}.json')
        checks(cache)
        require((cache['ray'], cache['angular_weight'], cache['panel_count']) == (ray,local['angular_weight'],41), 'Ray bank')
        track(ROOT / f'final-epoch-kinematic-bank/ray-{ray:03d}-kernel.json', cache['kernel_sha256'])
        for path, value in local['inputs'].items():
            track(path, value)
        require(read(source / 'prediction.json')['angular_ray'] == ray, 'Wrong source')
        qualifications = []
        for location in (source, native):
            record = read(location / 'validation.json')
            checks(record)
            require(record['actual_history_cell'] == 450 and record.get('angular_ray',ray) == ray, 'Wrong histories')
            for path, value in record['inputs'].items():
                track(path, value)
            for packet in record['packets']:
                track(packet['path'], packet['sha256'])
            qualifications.append(len(record['checks']))
        orders = []
        for order in (18, 26):
            job = directory / f'order-{order}'
            complete, independent = read(job / 'complete.json'), read(job / 'independent.json')
            checks(complete)
            checks(independent)
            current = digest(directory / 'protocol.json')
            require(complete['protocol_sha256'] == independent['protocol_sha256'] == current and complete['order'] == independent['order'] == order, 'Protocol link')
            panels = local['panels'][str(order)]
            require(len(list(job.glob('panel-*.json'))) == complete['panels'] == independent['panels'] == len(panels) == 41, 'Coverage')
            for index, panel in enumerate(panels):
                require(panel['panel'] == index and len(panel['frequencies']) == len(panel['measures']) == order
                        and all(math.isfinite(value) and value > 0 for value in panel['frequencies'] + panel['measures']), 'Radial grid')
                record_path = job / f'panel-{index:03d}.json'
                record = read(record_path)
                checks(record)
                require(record['previous_sha256'] == current and (record['panel'],record['order']) == (index,order), 'Panel chain')
                current = digest(record_path)
                track(record_path.with_suffix('.npz'), record['packet_sha256'])
                if ray == 3 and order == 18 and index < 35:
                    original = old / job.name / record_path.name
                    require(Path(record['reused_from']) == original and not (panel['absorption'] and not panel['emission']), 'Unsafe prefix')
                    track(original, record['original_metadata_sha256'])
                    track(original.with_suffix('.npz'), record['packet_sha256'])
                else:
                    require('reused_from' not in record, 'Unexpected copied panel')
            require(complete['last_panel_sha256'] == current and complete['packet_sha256'] == independent['complete_packet_sha256'], 'Terminal chain')
            track(job / 'complete.json', independent['complete_sha256'])
            track(job / 'complete.npz', complete['packet_sha256'])
            orders.append(dict(order=order, panels=len(panels), checked_vectors=independent['checked_vectors'], maximum_identity=independent['maximum_relative']))
        comparison_path = directory / 'order18-vs26.json'
        comparison = read(comparison_path)
        marker = read(CAMPAIGN / f'ray{ray:03d}-complete.json')
        require(marker['ray'] == ray and Path(marker['comparison']) == comparison_path, 'Wrong completion marker')
        track(comparison_path, marker['sha256'])
        require(comparison['all_component_rows_within_budget'] and comparison['budget'] == .002 and comparison['compared_rules'] == [18,26], 'Refinement')
        for path, value in comparison['inputs'].items():
            track(path, value)
        rows = comparison['rows']
        require(len(rows) == len(expected) and {tuple(row[name] for name in fields) for row in rows} == expected, 'Cartesian coverage')
        with (directory / 'order18-vs26.csv').open(newline='', encoding='utf-8') as stream:
            csv_rows = list(csv.DictReader(stream))
        for row, table in zip(rows, csv_rows, strict=True):
            require(row['within_component_budget'] and row['budget'] == .002 and 0 <= row['relative'] <= .002
                    and all(str(row[key]) == table[key] for key in fields) and table['within_component_budget'] == 'True'
                    and all(float(table[key]) == row[key] for key in ('absolute','scale','relative','budget')), 'Refinement row')
        results.append(dict(ray=ray, theta=local['theta'], rows=len(rows), qualifications=qualifications, orders=orders,
                            model_maxima={name:max(row['relative'] for row in rows if row['model'] == name) for name in ('heavy','cold')},
                            component_maxima={name:max(row['relative'] for row in rows if row['component'] == name) for name in components}))
    for index, (path, value) in enumerate(hashes.items()):
        if index % 32 == 0:
            respect_hold()
        require(digest(path) == value, 'Hash mismatch: ' + str(path))
    return dict(passed=True, finished=datetime.now(timezone.utc).isoformat(), actual_child_exits=len(end['runs']),
                protected_files=len(protocol['protected']), verified_files=len(hashes), campaign_end_sha256=digest(CAMPAIGN / 'end.json'),
                coverage={ray:str(ROOT / (f'final-epoch-real-source-ray{ray:03d}' if ray < 3 else f'final-epoch-real-v2-ray{ray:03d}')) for ray in range(5)},
                rays=results, prefix_reused=35, recalculated_panels=129, verified_oracle=replay, task_workers_remaining=0,
                scope='Individual finite real/pole directions only; rays 0–2 retained under original arithmetic pending common-representation comparison.')


if __name__ == '__main__':
    worker = psutil.Process()
    worker.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    worker.cpu_affinity([4])
    result = validate()
    with (CAMPAIGN / 'integrity.json').open('x', encoding='utf-8') as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
    print(json.dumps({key:result[key] for key in ('passed','actual_child_exits','verified_files','rays')},allow_nan=False))
