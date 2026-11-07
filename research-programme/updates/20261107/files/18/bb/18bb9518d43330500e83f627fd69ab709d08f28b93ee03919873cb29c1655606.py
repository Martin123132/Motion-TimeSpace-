import os

for variable in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
    os.environ[variable] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

import ast
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parent
DESTINATION = ROOT / 'saved-epoch-cell424'
if DESTINATION.exists():
    raise RuntimeError('Existing consumer preparation preserved; inspect before retrying')
if any((path / 'STOP-REQUESTED').exists() for path in (ROOT, ROOT.parent)):
    raise RuntimeError('Owner stop preserved')
setup_path = ROOT / 'check_correlated_readout.py'
statements = []
for statement in ast.parse(setup_path.read_text()).body:
    if isinstance(statement, ast.Assign) and any(isinstance(target, ast.Name) and target.id == 'probes' for target in statement.targets):
        break
    statements.append(statement)
namespace = dict(__file__=str(setup_path), __name__='saved_epoch_consumer_setup')
exec(compile(ast.Module(body=statements, type_ignores=[]), str(setup_path), 'exec'), namespace)
np, mp, parent = namespace['np'], namespace['mp'], namespace['retained']
register, process, BASE = namespace['register'], namespace['process'], namespace['BASE']
from restart_readout import load_verified_cell, digest
from saved_epoch_binding import bind


def write(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)


def check(name, passed, **values):
    checks.append(dict(name=name, passed=bool(passed), **values))


def rejected(name, action):
    try:
        action()
    except ValueError:
        check(name, True)
    else:
        check(name, False)


DESTINATION.mkdir()
identity = dict(pid=process.pid, created_time=process.create_time(), command=process.cmdline(), priority=process.nice(), affinity=process.cpu_affinity())
write(DESTINATION / 'prepare-start.json', dict(process=identity, started_at=datetime.now(timezone.utc).isoformat(), previous_goal_turn='progress: two direct source rays completed'))
print(json.dumps(dict(started=True, process=identity)), flush=True)
checks = []
restart = load_verified_cell(ROOT.parent, 424, ROOT.parent / 'supervisor-cells417-424.json')
namespace['sources'].update(restart['inputs'])
warm_config = json.loads(register(BASE / 'finite-real-mixed-source-20261026/configuration.json').read_text())
heats, ends, heat_paths = {}, {}, {}
for model in ('heavy', 'cold'):
    history_path = register(BASE / 'infrared-source-domain-20261008/backgrounds' / (model + '-nonlocal-refined-6400') / 'history.npz')
    tail_path = register(BASE / 'dynamical-infrared-tail-20261008/runs' / (model + '-production') / 'tail.npz')
    with np.load(history_path, allow_pickle=False) as saved:
        ends[model] = float(saved['expansion'][-1])
    with np.load(tail_path, allow_pickle=False) as saved:
        heats[model] = float(saved['heat'])
    heat_paths[model] = str(tail_path)
check('source expansion domains identical', ends['heavy'] == ends['cold'])
fraction = restart['coordinate'] / ends['heavy']
original, theta = parent.source.context(fraction)
check('source factory exactly reproduces restart coordinate', original.epochs[0].coordinate == restart['coordinate'])
contexts = {value['model']: value for value in parent.source.physics.epoch_context(original)[0]}
for path in original.inputs:
    register(path)
for model in ('heavy', 'cold'):
    background = parent.source.physics.thermal_wave.thermal.ThermalBackground(model)
    local = background.at(restart['coordinate'])
    predicted_theta = background.constants['k_B'] * background.temperature0 / (background.constants['m_e'] * background.constants['c']**2 * local['scale'])
    check(model + ':thermal source temperature', abs(predicted_theta / contexts[model]['theta'] - 1) <= 1e-10,
        relative=abs(predicted_theta / contexts[model]['theta'] - 1), limit=1e-10)
    check(model + ':source heat matches stored normalization', abs(heats[model] / contexts[model]['heat'] - 1) <= 1e-10,
        relative=abs(heats[model] / contexts[model]['heat'] - 1), limit=1e-10)
    check(model + ':source rate identity', abs(contexts[model]['rate'] / (local['coefficient'] / local['thermal_parameter']) - 1) <= 1e-10)
    for path in contexts[model]['inputs']:
        register(path)
binding = bind(parent.precise.Bundle, parent.precise.Features, original, contexts, restart, heats)
bundle, features = binding['bundle'], binding['features']
for index, record in enumerate(binding['records']):
    with mp.workdps(80):
        exact = binding['physical_columns'][2 * index]
        reconstructed = [mp.mpf(float(high)) + mp.mpf(float(low)) for high, low in zip(bundle.high[:, 2 * index], bundle.low[:, 2 * index])]
        scale = max(mp.sqrt(mp.fsum(value**2 for value in exact)), mp.mpf('1e-300'))
        error = mp.sqrt(mp.fsum((actual - expected)**2 for actual, expected in zip(reconstructed, exact))) / scale
        check(record['label'] + ':complete split state', error <= mp.mpf('1e-10'), relative=float(error), limit=1e-10)
        check(record['label'] + ':scale every coordinate exactly once', exact == [mp.mpf(float(record['heat'])) * value for value in binding['normalized'][index]])
check('all18 physical/difference columns and both joins', bundle.high.shape == bundle.low.shape == (578, 36))
check('nonzero precision residuals retained', bool(np.any(bundle.low != 0)))
probes = np.array([1e-6, 7.952885162185943e-5, 1.5e-4, 2e-4, .01, 14., 60.])
for join in (0, 1):
    for derivative in (False, True):
        actual = features.evaluate(probes, join, derivative)
        reference = features.retained_features.evaluate(probes, join, derivative)[:, :96]
        check(f'profile spline preserved:join{join}:derivative{derivative}', np.array_equal(actual[:, :96], reference))
    for column in range(18):
        direct = parent.precise.stable_dot(np.c_[features.evaluate(probes, join), np.zeros(len(probes))], bundle.high[:, 2*column:2*column+1], bundle.low[:, 2*column:2*column+1])[:, 0]
        check(f'physical bundle readout:join{join}:column{column}', np.array_equal(bundle.functions(probes)[:, 1+2*column+join], direct))
wrong_epoch = SimpleNamespace(epochs=[SimpleNamespace(coordinate=restart['coordinate'] + .001)])
rejected('wrong epoch rejected', lambda: bind(parent.precise.Bundle, parent.precise.Features, wrong_epoch, contexts, restart, heats))
missing = dict(restart, states={key: value for key, value in restart['states'].items() if key != 'cold-bank-s4'})
rejected('missing baseline rejected', lambda: bind(parent.precise.Bundle, parent.precise.Features, original, contexts, missing, heats))
wrong_contexts = {**contexts, 'cold': {**contexts['cold'], 'theta': contexts['cold']['theta'] * 1.001}}
rejected('mismatched model temperature rejected', lambda: bind(parent.precise.Bundle, parent.precise.Features, original, wrong_contexts, restart, heats))
rejected('wrong physical heat rejected', lambda: bind(parent.precise.Bundle, parent.precise.Features, original, contexts, restart, {**heats, 'heavy': heats['heavy'] * 2}))
warm = next(row for row in warm_config['events'] if row['label'] == 'warm')
warm_nodes = [node for node in parent.source.physics.integration_nodes(warm['theta'], 7) if node['frequency'] == 14.]
check('original warm event regenerated exactly', len(warm_nodes) == 36 and warm_nodes[0] == warm['node'])
nodes = [node for node in parent.source.physics.integration_nodes(theta, 7) if node['frequency'] == 14.]
check('all36 scattering geometries available at matching temperature', len(nodes) == 36)
node = nodes[0]
parameters, event_weight = parent.source.physics.parameters_and_weight(theta, node)
check('matching event differs from warm calibration', theta != warm['theta'] and node != warm['node'])
check('event lab energy follows actual theta', parameters['lab_energy'] == theta * 14.)
for module in list(sys.modules.values()):
    filename = getattr(module, '__file__', None)
    if filename and Path(filename).suffix == '.py' and Path(filename).resolve().is_relative_to(BASE):
        register(filename)
for name in ('prepare_saved_epoch.py', 'saved_epoch_binding.py', 'restart_readout.py', 'nodal_readout.py', 'adjoint_readout.py', 'correlated_readout.py', 'profile_preserving_features.py', 'check_correlated_readout.py'):
    register(ROOT / name)
check('all recorded source hashes unchanged', all(digest(path) == checksum for path, checksum in namespace['sources'].items()))
passed = all(row['passed'] for row in checks)
with (DESTINATION / 'columns.npz').open('xb') as stream:
    np.savez_compressed(stream, high=bundle.high, low=bundle.low, labels=np.array(binding['labels']),
        tail_frequency=restart['frequency'], master_frequency=features.frequency)
manifest = dict(passed=passed, created_at=datetime.now(timezone.utc).isoformat(), process=identity,
    cell=424, coordinate=restart['coordinate'], fraction=fraction, theta=theta, contexts=contexts,
    history_heats=heats, history_heat_paths=heat_paths, labels=binding['labels'], records=binding['records'],
    columns_sha256=digest(DESTINATION / 'columns.npz'), dimensions=dict(profile=96, tail=481, gas=1, physical_cases=12, differences=6, joins=2),
    event=dict(theta=theta, node=node, weight=event_weight), checks=checks, inputs=namespace['sources'],
    gate=1e-10, source_integrated=False, history_propagated=False, original_bank_changed=False,
    original_grids_changed=False, original_tolerances_changed=False,
    next='Test the actual source factors on these frozen histories at this temperature; keep all bilinear difference terms')
write(DESTINATION / 'manifest.json', manifest)
print(json.dumps(dict(passed=passed, checks=len(checks), failed=[row for row in checks if not row['passed']],
    coordinate=restart['coordinate'], theta=theta, shape=list(bundle.high.shape), inputs=len(namespace['sources']), process=identity)), flush=True)
raise SystemExit(0 if passed else 1)
