import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
PARENTS = {
    'final_epoch_real_source.py': '51be2f0631decc27bf4e0bff8e7fc8e31bf1e4327b567a0e97e7ae7d40a7aa94',
    'check_final_epoch_real_source.py': '2a195897175d7f11803109df8230c505fc4d1efd1024acf2b62120dddb256d10',
    'compare_final_epoch_real_orders.py': 'c00c67fcb4812f8134077b5db108d4978c4a6b95eff2d5440044038584f256db',
    'run_final_epoch_qualification.py': '3bce2ba5cf8f926f43ecd9bed7f68632a45b35ea5265ec773d007e6b243edebd',
    'check_precise_compensated_source.py': '5b3932e9ad077bcdf78535255fa88a40f0d4c0b8397111941575b857c4669a2f',
    'check_native_compensated_pairs.py': 'c42294cf440616e2b8becfacda9ece47d7d75bc5474dd757edddbac3072ff829',
    'exact_kinematic_cache.py': '82bb160a0514212101fc2e570971cbc52149b7f8f01504eb63acd71e5789d671',
}


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


def verify(inputs):
    for path, expected in inputs.items():
        if digest(path) != expected:
            raise RuntimeError('Frozen input changed: ' + str(path))


def replace(source, before, after, changes):
    count = source.count(before)
    if count != 1:
        raise RuntimeError(f'Expected exactly one adaptation boundary, got {count}: {before}')
    changes.append(dict(before=before, after=after, count=count))
    return source.replace(before, after)


def qualification_source(mode, ray):
    from run_final_epoch_qualification import source_text
    source = source_text(mode)
    changes = []
    target = f'compensated-epoch-source-final450-ray{ray:03d}'
    source = replace(source, 'compensated-epoch-source-final450-001', target, changes)
    if mode == 'precise':
        source = replace(source, 'list(retained.angular.inherited.source.angular_nodes(8))[0]',
                         f'list(retained.angular.inherited.source.angular_nodes(8))[{ray}]', changes)
        source = replace(source, 'owner = RationalDirection(retained.precise_context(parameters), direction)',
                         'owner = cached_owner(retained.precise_context(parameters), direction)', changes)
        source = replace(source, 'angular_ray=0,', f'angular_ray={ray},', changes)
        insertion = "    inputs.update(restart['inputs'])"
        addition = insertion + '\n' + ''.join(
            f"    inputs[str(ROOT / {name!r})] = digest(ROOT / {name!r})\n" for name in (
                'run_final_real_directions.py', 'final-epoch-kinematic-bank/protocol.json',
                f'final-epoch-kinematic-bank/ray-{ray:03d}.json', f'final-epoch-kinematic-bank/ray-{ray:03d}-kernel.json'))
        source = replace(source, insertion, addition.rstrip(), changes)
    else:
        source = replace(source, 'CONSUMER=CONSUMER, read=read, ast=ast, json=json, sys=sys, Path=Path)',
                         'CONSUMER=CONSUMER, read=read, ast=ast, json=json, sys=sys, Path=Path, cached_owner=cached_owner)', changes)
        source = replace(source, 'actual_history_cell=424,', f'actual_history_cell=450, angular_ray={ray},', changes)
    return source, changes


def render(stage, ray):
    changes = []
    if stage in ('precise', 'native'):
        source, changes = qualification_source(stage, ray)
        parent = 'check_precise_compensated_source.py' if stage == 'precise' else 'check_native_compensated_pairs.py'
    else:
        parent = ('check_final_epoch_real_source.py' if stage == 'check' else
                  'compare_final_epoch_real_orders.py' if stage == 'compare' else 'final_epoch_real_source.py')
        source = (ROOT / parent).read_text().replace('\r\n', '\n')
        source = replace(source, 'final-epoch-real-source-ray000', f'final-epoch-real-source-ray{ray:03d}', changes)
        if stage in ('freeze', 'run'):
            source = replace(source, 'from run_final_epoch_qualification import source_text', 'source_text = endpoint_source_text', changes)
            first = source.index('def cached_owner(parameters, direction):')
            last = source.index('\n\ndef setup():', first)
            source = replace(source, source[first:last],
                             'def cached_owner(parameters, direction):\n    return qualified_cached_owner(parameters, direction)', changes)
            before = "    previous = 'owner = RationalDirection(retained.precise_context(parameters), direction)'\n    if source.count(previous) != 1:\n        raise RuntimeError('Qualified owner construction boundary changed')\n    source = source.replace(previous, 'owner = cached_owner(retained.precise_context(parameters), direction)')\n"
            source = replace(source, before, '', changes)
            count = source.count('compensated-epoch-source-final450-001')
            if count != 3:
                raise RuntimeError('Expected three retained qualification path boundaries')
            source = source.replace('compensated-epoch-source-final450-001', f'compensated-epoch-source-final450-ray{ray:03d}')
            changes.append(dict(before='compensated-epoch-source-final450-001', after=f'compensated-epoch-source-final450-ray{ray:03d}', count=count))
            source = replace(source, 'def stopping():\n', 'def stopping():\n    if adapter_stopping():\n        return True\n', changes)
            for before, after in (('final-epoch-kinematic-bank/ray-000.json', f'final-epoch-kinematic-bank/ray-{ray:03d}.json'),
                                  ('final-epoch-kinematic-bank/ray-000-kernel.json', f'final-epoch-kinematic-bank/ray-{ray:03d}-kernel.json'),
                                  ('angular_ray=0,', f'angular_ray={ray},')):
                source = replace(source, before, after, changes)
        elif stage == 'check':
            source = replace(source, 'compensated-epoch-source-final450-001/native-paired-check/separator-logarithm.npz',
                             f'compensated-epoch-source-final450-ray{ray:03d}/native-paired-check/separator-logarithm.npz', changes)
        if 'event0/ray0' in source:
            source = replace(source, 'event0/ray0', f'event0/ray{ray}', changes)
    if 'def guard():\n' in source:
        source = replace(source, 'def guard():\n', 'def guard():\n    adapter_guard()\n', changes)
    if 'def write(path, value):\n' in source:
        source = replace(source, 'def write(path, value):\n',
                         "def write(path, value):\n    if Path(path).name in ('protocol.json', 'prediction.json'):\n        value = dict(value, execution_adapter=ADAPTATION)\n", changes)
    metadata = dict(parent=str(ROOT / parent), parent_sha256=PARENTS[parent], replacements=changes,
                    transformed_sha256=hashlib.sha256(source.encode()).hexdigest())
    return source, metadata


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('stage', choices=('precise', 'native', 'freeze', 'run', 'check', 'compare'))
    parser.add_argument('--ray', type=int, required=True)
    parser.add_argument('--stop-utc', required=True)
    parser.add_argument('--compile-only', action='store_true')
    arguments, remaining = parser.parse_known_args()
    if not 1 <= arguments.ray <= 127:
        parser.error('Remaining actual directions1..127 only; ray0 is preserved')
    stop = datetime.fromisoformat(arguments.stop_utc.replace('Z', '+00:00'))
    if stop.utcoffset() is None or stop.utcoffset().total_seconds() != 0:
        parser.error('Explicit UTC stop required')
    verify({ROOT / name: expected for name, expected in PARENTS.items()})
    ray = arguments.ray
    destination = ROOT / f'final-epoch-real-source-ray{ray:03d}'
    qualified = ROOT / f'compensated-epoch-source-final450-ray{ray:03d}'

    def adapter_stopping():
        return (datetime.now(timezone.utc) >= stop
                or 3 <= datetime.now(timezone.utc).astimezone(ZoneInfo('Europe/London')).hour < 14
                or any((directory / 'STOP-REQUESTED').exists() for directory in
                       (ROOT, ROOT.parent, destination, qualified, ROOT / 'final-real-batch-rays001-002',
                        ROOT / 'saved-epoch-cell450', ROOT / 'final-epoch-kinematic-bank'))
                or (ROOT.parent / 'execution-v3/STOP-REQUEST.json').exists()
                or shutil.disk_usage(ROOT).free < 6 * 1024**3)

    def adapter_guard():
        if adapter_stopping():
            raise RuntimeError('Owner/music/time hold preserved; no automatic retry')

    def cached_owner(parameters, direction):
        from exact_kinematic_cache import CachedDirection
        report_path = ROOT / f'final-epoch-kinematic-bank/ray-{ray:03d}.json'
        protocol_path = ROOT / 'final-epoch-kinematic-bank/protocol.json'
        report, protocol = read(report_path), read(protocol_path)
        if (not report['passed'] or not all(row['passed'] for row in report['checks']) or report['ray'] != ray
                or report['protocol_sha256'] != digest(protocol_path) or protocol['final_cell'] != 450
                or protocol['angular_order'] != 8 or protocol['gate'] != 1e-10):
            raise RuntimeError('Qualified actual endpoint cache required for this direction')
        verify(protocol['inputs'])
        return CachedDirection(parameters, direction, ROOT / f'final-epoch-kinematic-bank/ray-{ray:03d}-kernel.json', report['kernel_sha256'])

    source, metadata = render(arguments.stage, ray)
    precise_source, precise_changes = qualification_source('precise', ray)
    compile(precise_source, str(ROOT / 'check_precise_compensated_source.py'), 'exec')
    program = compile(source, str(ROOT / metadata['parent']), 'exec')
    adaptation = dict(adapter=str(Path(__file__)), adapter_sha256=digest(Path(__file__)), ray=ray,
                      history_cell=450, parents=PARENTS, program=metadata,
                      precise_setup=dict(transformed_sha256=hashlib.sha256(precise_source.encode()).hexdigest(), replacements=precise_changes),
                      scope='Retained final source formulas at a different original angular8 direction; ray-specific precision/separator qualification; no reflected reuse')
    if arguments.compile_only:
        print(json.dumps(dict(compiled=True, stage=arguments.stage, ray=ray, program_sha256=metadata['transformed_sha256'])))
        raise SystemExit(0)
    adapter_guard()
    sys.argv = [str(Path(__file__)), *([arguments.stage] if arguments.stage in ('freeze', 'run') else []), *remaining]
    if arguments.stage in ('freeze', 'run'):
        sys.argv.extend(['--stop-utc', arguments.stop_utc])
    context = dict(__file__=str(Path(__file__)), __name__='retained_final_real_direction', ADAPTATION=adaptation,
                   adapter_guard=adapter_guard, adapter_stopping=adapter_stopping, endpoint_guard=adapter_guard, cached_owner=cached_owner,
                   qualified_cached_owner=cached_owner,
                   endpoint_source_text=(lambda *unused: precise_source))
    exec(program, context)
