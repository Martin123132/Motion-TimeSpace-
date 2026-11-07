import os

for variable in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
    os.environ[variable] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

import argparse
import ast
import json
import math
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DESTINATION = ROOT / 'final-epoch-kinematic-bank'
parser = argparse.ArgumentParser()
parser.add_argument('mode', choices=('freeze', 'run'))
parser.add_argument('--count', type=int, default=8)
parser.add_argument('--minutes', type=float, default=30)
arguments = parser.parse_args()
if not 1 <= arguments.count <= 8 or not 0 < arguments.minutes <= 60:
    parser.error('One bounded worker:1..8 rays and at most60minutes')


def stopped():
    return any((path / 'STOP-REQUESTED').exists() for path in (ROOT, ROOT.parent, DESTINATION))


if stopped():
    raise RuntimeError('Owner stop preserved')
setup_path = ROOT / 'check_correlated_readout.py'
statements = []
for statement in ast.parse(setup_path.read_text()).body:
    if isinstance(statement, ast.Assign) and any(isinstance(target, ast.Name) and target.id == 'probes' for target in statement.targets):
        break
    statements.append(statement)
namespace = dict(__file__=str(setup_path), __name__='final_kinematic_source_setup')
exec(compile(ast.Module(body=statements, type_ignores=[]), str(setup_path), 'exec'), namespace)
np, mp, parent, process, BASE = (namespace[name] for name in ('np', 'mp', 'retained', 'process', 'BASE'))
register = namespace['register']
sys.path.insert(0, str(BASE / 'exact-dirac-density-20261027'))
import rational239 as rational
import integrate236 as integration
from density236 import Direction
from exact_kinematic_cache import CachedDirection, pack, FIELDS
from restart_readout import digest


def read(path):
    return json.loads(Path(path).read_text())


def write(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)


def now():
    return datetime.now(timezone.utc).isoformat()


def identity():
    return dict(pid=process.pid, created_time=process.create_time(), command=process.cmdline(), priority=process.nice(), affinity=process.cpu_affinity())


def verify(inputs):
    for path, checksum in inputs.items():
        if digest(path) != checksum:
            raise RuntimeError('Frozen input changed: ' + path)


def compare(rows, name, actual, expected):
    error = abs(actual - expected) / max(abs(expected), mp.mpf('1e-300'))
    rows.append(dict(name=name, relative=float(error), limit=1e-10, passed=bool(mp.isfinite(error) and error <= mp.mpf('1e-10'))))


science_path = register(ROOT.parent / 'execution-v3/science-config.json')
science = read(science_path)
assert digest(science_path) == '508063733ce6897fc455c4e2f0419614b557abb46f84d1b88a8b45540a2537e1'
grids_path = register(science['execution_grids'])
assert digest(grids_path) == science['execution_grids_sha256']
with np.load(grids_path, allow_pickle=False) as grids:
    final_coordinate = float(grids['coarse'][451])
original, theta = namespace['original'], namespace['theta']
assert original.epochs[0].coordinate == final_coordinate
source_config = read(register(BASE / 'finite-real-mixed-source-20261026/configuration.json'))
assert theta == source_config['target_theta'] and namespace['config']['target_fraction'] == source_config['target_fraction']
event_nodes = [node for node in parent.source.physics.integration_nodes(theta, 7) if node['frequency'] == 14.]
assert len(event_nodes) == 36
node = event_nodes[0]
parameters, event_weight = parent.source.physics.parameters_and_weight(theta, node)
angular_nodes = [(direction, float(weight)) for direction, weight in integration.angular.inherited.source.angular_nodes(8)]
assert len(angular_nodes) == 128 and abs(math.fsum(weight for direction, weight in angular_nodes) - 4 * math.pi) < 1e-13
for module in list(sys.modules.values()):
    filename = getattr(module, '__file__', None)
    if filename and Path(filename).suffix == '.py' and Path(filename).resolve().is_relative_to(BASE):
        register(filename)
for name in ('final_kinematic_bank.py', 'exact_kinematic_cache.py', 'check_correlated_readout.py'):
    register(ROOT / name)
if arguments.mode == 'freeze':
    if DESTINATION.exists():
        raise RuntimeError('Existing final-source protocol preserved')
    DESTINATION.mkdir()
    protocol = dict(frozen_at=now(), previous_goal_turn='progress: actual-history source binding and stable coupling verified',
        process=identity(), final_cell=450, final_coarse_node=451, coordinate=final_coordinate,
        theta=theta, fraction=source_config['target_fraction'], node=node, event_weight=event_weight,
        angular_order=8, radial_validation_order=26, angular_nodes=[dict(ray=ray, direction=list(map(float, direction)), weight=weight)
            for ray, (direction, weight) in enumerate(angular_nodes)],
        source_config=source_config, inputs=namespace['sources'], precision=80, serialized_digits=100, gate=1e-10,
        independent_dirac_selection='First, middle and last allowed frozen radial26 node for each sign, in every direction',
        every_radial_node_replay='Exact cached vs constructed density and kinematic event equality at80digits',
        no_history_inputs_supplied_to_density=True, endpoint_history_complete=False, propagation_head=424,
        photon_gas_source_integrated=False, original_bank_changed=False, grids_changed=False, tolerances_changed=False,
        scope='Temperature/event-dependent rational density coefficients only; one x14,event0 geometry,128 original angular directions',
        operations='One BelowNormal CPU4 numerical thread; honor stop and music intervention; no automatic retry')
    verify(protocol['inputs'])
    write(DESTINATION / 'protocol.json', protocol)
    print(json.dumps(dict(frozen=True, coordinate=final_coordinate, theta=theta, target_rays=128, inputs=len(protocol['inputs']), process=identity())), flush=True)
    raise SystemExit(0)
protocol = read(DESTINATION / 'protocol.json')
verify(protocol['inputs'])
assert protocol['coordinate'] == final_coordinate and protocol['theta'] == theta and protocol['node'] == node
import msvcrt
lease = (DESTINATION / 'worker.lock').open('a+b')
if lease.seek(0, 2) == 0:
    lease.write(b'0')
    lease.flush()
lease.seek(0)
msvcrt.locking(lease.fileno(), msvcrt.LK_NBLCK, 1)
reports = []
for ray in range(128):
    kernel_path = DESTINATION / f'ray-{ray:03d}-kernel.json'
    report_path = DESTINATION / f'ray-{ray:03d}.json'
    if not report_path.exists():
        if kernel_path.exists() or any(DESTINATION.glob(f'ray-{ray+1:03d}*')):
            raise RuntimeError('Orphan or skipped angular node requires inspection')
        break
    report = read(report_path)
    assert report['passed'] and report['ray'] == ray and report['protocol_sha256'] == digest(DESTINATION / 'protocol.json')
    assert digest(kernel_path) == report['kernel_sha256']
    reports.append(report)
expected_reports = {f'ray-{ray:03d}.json' for ray in range(len(reports))}
expected_kernels = {f'ray-{ray:03d}-kernel.json' for ray in range(len(reports))}
actual_files = {path.name for path in DESTINATION.glob('ray-*.json')}
if actual_files != expected_reports | expected_kernels:
    raise RuntimeError('Noncontiguous or orphan source packets require inspection')
for path in DESTINATION.glob('attempt-*-start.json'):
    end = path.with_name(path.name.replace('-start', '-end'))
    if not end.exists() or read(end)['state'] != 'batch_complete':
        raise RuntimeError('Prior interruption/failure requires review; no automatic retry')
if len(reports) == 128:
    raise RuntimeError('Completed angular kinematic bank preserved')
attempt = DESTINATION / ('attempt-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
write(attempt.with_name(attempt.name + '-start.json'), dict(process=identity(), started_at=now(), first_ray=len(reports), maximum_count=arguments.count, maximum_minutes=arguments.minutes))
print(json.dumps(dict(started=True, first_ray=len(reports), process=identity())), flush=True)
deadline = time.monotonic() + arguments.minutes * 60
completed, state = [], 'batch_complete'
with mp.workdps(80):
    precise_parameters = integration.precise_context(parameters)
    for ray in range(len(reports), min(128, len(reports) + arguments.count)):
        if stopped() or time.monotonic() >= deadline:
            state = 'planned_stop'
            break
        began = time.monotonic()
        direction, weight = angular_nodes[ray]
        build_started = time.monotonic()
        owner = rational.RationalDirection(precise_parameters, direction)
        construction_seconds = time.monotonic() - build_started
        kernel_path = DESTINATION / f'ray-{ray:03d}-kernel.json'
        write(kernel_path, pack(owner))
        kernel_sha256 = digest(kernel_path)
        reload_started = time.monotonic()
        cached = CachedDirection(precise_parameters, direction, kernel_path, kernel_sha256)
        reload_seconds = time.monotonic() - reload_started
        assert all(getattr(owner, field) == getattr(cached, field) for field in FIELDS)
        panels = list(integration.panels(owner, 26, source_config))
        cached_panels = list(integration.panels(cached, 26, source_config))
        assert len(panels) == len(cached_panels)
        nodes = {sign: [] for sign in (-1, 1)}
        exact_checks = 0
        for original_panel, loaded_panel in zip(panels, cached_panels):
            assert all(np.array_equal(first, second) for first, second in zip(original_panel, loaded_panel))
            frequency, measure, emission, absorption = original_panel
            for sign, allowed in ((1, emission), (-1, absorption)):
                if not allowed:
                    continue
                for value in frequency:
                    signed = sign * integration.scalar(value) * owner.temperature / owner.doppler
                    expected, expected_event = owner.densities(signed)
                    actual, actual_event = cached.densities(signed)
                    assert all(mp.isfinite(value) for value in actual.values())
                    assert actual['full'] >= 0 and actual['control'] >= 0
                    assert actual == expected and set(actual_event) == set(expected_event)
                    assert all(actual_event[name] == expected_event[name] for name in actual_event)
                    exact_checks += len(actual) + len(actual_event)
                    nodes[sign].append(signed)
        checks = []
        for sign, values in nodes.items():
            for index in sorted({0, len(values)//2, len(values)-1}):
                reference, unused_event = Direction.densities(cached, values[index])
                actual, unused_event = cached.densities(values[index])
                for component in ('full', 'control', 'difference'):
                    compare(checks, f'sign{sign}:node{index}:{component}:independent-Dirac', actual[component], reference[component])
        compare(checks, 'soft residue', cached.soft_residue(), cached.pole['full'])
        checks.append(dict(name='real intensity polynomial', relative=float(owner.imaginary_residual), limit=1e-10, passed=owner.imaginary_residual <= mp.mpf('1e-10')))
        report = dict(passed=all(row['passed'] for row in checks), ray=ray, checks=checks,
            exact_replay_checks=exact_checks, evaluated_events=sum(map(len, nodes.values())), panel_count=len(panels),
            source_coordinate=final_coordinate, source_theta=theta, angular_weight=weight,
            protocol_sha256=digest(DESTINATION / 'protocol.json'), kernel_sha256=kernel_sha256,
            construction_seconds=construction_seconds, reload_seconds=reload_seconds, seconds=time.monotonic()-began,
            kernel_bytes=kernel_path.stat().st_size, history_or_wave_used=False,
            process=identity(), finished_at=now())
        write(DESTINATION / f'ray-{ray:03d}.json', report)
        print(json.dumps(dict(ray=ray, passed=report['passed'], events=report['evaluated_events'], checks=len(checks),
            maximum=max(row['relative'] for row in checks), seconds=report['seconds'], construct=construction_seconds,
            reload=reload_seconds, bytes=report['kernel_bytes'])), flush=True)
        if not report['passed']:
            state = 'failed'
            break
        completed.append(ray)
verify(protocol['inputs'])
write(attempt.with_name(attempt.name + '-end.json'), dict(state=state, completed=completed, finished_at=now(), process=identity()))
print(json.dumps(dict(state=state, completed=completed, process=identity())), flush=True)
raise SystemExit(0 if state == 'batch_complete' else 2)
