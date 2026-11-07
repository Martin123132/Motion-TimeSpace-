import os

for variable in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
    os.environ[variable] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

import ast
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONSUMER = ROOT / 'saved-epoch-cell424'
DESTINATION = CONSUMER / 'precision-check-001'
if DESTINATION.exists():
    raise RuntimeError('Existing precision test preserved; inspect before retrying')
if any((path / 'STOP-REQUESTED').exists() for path in (ROOT, ROOT.parent, CONSUMER)):
    raise RuntimeError('Owner stop preserved')
from restart_readout import digest, load_verified_cell

manifest = json.loads((CONSUMER / 'manifest.json').read_text())
assert manifest['passed'] and digest(CONSUMER / 'columns.npz') == manifest['columns_sha256']
for path, checksum in manifest['inputs'].items():
    if digest(path) != checksum:
        raise RuntimeError('Frozen consumer input changed: ' + path)
setup_path = ROOT / 'check_full_tail_factors.py'
statements = []
for statement in ast.parse(setup_path.read_text()).body:
    if isinstance(statement, ast.Assign) and any(isinstance(target, ast.Name) and target.id == 'checks' for target in statement.targets):
        break
    statements.append(statement)
context = dict(__file__=str(setup_path), __name__='precise_epoch_source_setup')
exec(compile(ast.Module(body=statements, type_ignores=[]), str(setup_path), 'exec'), context)
namespace = context['namespace']
np, mp, parent = namespace['np'], namespace['mp'], namespace['retained']
process, BASE = namespace['process'], namespace['BASE']
import integrate236 as retained
from saved_epoch_binding import bind
from full_tail_factors import FullTailFactors
from full_tail_action import FullTailActionFactors, SplitColumns
from precise_epoch_response import PreciseEpochResponse, scalar, split_array


def write(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)


def compare(name, actual, expected, group, target=None):
    rows = checks if target is None else target
    first, second = list(np.asarray(actual, dtype=object).flat), list(np.asarray(expected, dtype=object).flat)
    if len(first) != len(second):
        raise ValueError('Reference dimensions differ')
    with mp.workdps(80):
        error = mp.sqrt(mp.fsum((scalar(value) - scalar(reference))**2 for value, reference in zip(first, second)))
        scale = max(mp.sqrt(mp.fsum(scalar(value)**2 for value in second)), mp.mpf('1e-300'))
        relative = error / scale
        rows.append(dict(name=name, group=group, relative=float(relative), absolute=float(error), scale=float(scale), limit=1e-10,
            passed=bool(mp.isfinite(relative) and relative <= mp.mpf('1e-10'))))


def difference(values, pair):
    baseline, candidate, delta = 3 * pair, 3 * pair + 1, 3 * pair + 2
    direct = [after[candidate] - before[baseline] for after, before in zip(values[candidate+1], values[baseline+1])]
    predicted = [mp.fsum([first[delta], second[baseline], second[delta]]) for first, second in zip(values[baseline+1], values[delta+1])]
    equilibrium = [row[candidate] - row[baseline] for row in values[0]]
    return direct, predicted, equilibrium, [row[delta] for row in values[0]]


DESTINATION.mkdir()
identity = dict(pid=process.pid, created_time=process.create_time(), command=process.cmdline(), priority=process.nice(), affinity=process.cpu_affinity())
write(DESTINATION / 'start.json', dict(process=identity, started_at=datetime.now(timezone.utc).isoformat()))
print(json.dumps(dict(started=True, process=identity)), flush=True)
restart = load_verified_cell(ROOT.parent, 424, ROOT.parent / 'supervisor-cells417-424.json')
original, theta = parent.source.context(manifest['fraction'])
contexts = {value['model']: value for value in parent.source.physics.epoch_context(original)[0]}
assert contexts == manifest['contexts'] and theta == manifest['theta']
binding = bind(parent.precise.Bundle, parent.precise.Features, original, contexts, restart, manifest['history_heats'])
bundle = binding['bundle']
with np.load(CONSUMER / 'columns.npz', allow_pickle=False) as saved:
    assert np.array_equal(bundle.high, saved['high']) and np.array_equal(bundle.low, saved['low'])
inputs = {**manifest['inputs'], **namespace['sources'], **restart['inputs']}
for module in list(sys.modules.values()):
    filename = getattr(module, '__file__', None)
    if filename and Path(filename).suffix == '.py' and Path(filename).resolve().is_relative_to(BASE):
        inputs[str(Path(filename).resolve())] = digest(filename)
for path in (Path(__file__), ROOT / 'precise_epoch_response.py', ROOT / 'full_tail_factors.py', ROOT / 'full_tail_action.py',
    ROOT / 'retained_column_differences.py', CONSUMER / 'manifest.json', CONSUMER / 'columns.npz',
    CONSUMER / 'factor-check-001/validation.json', CONSUMER / 'factor-check-001/responses.npz'):
    inputs[str(path)] = digest(path)
prediction = dict(frozen_at=datetime.now(timezone.utc).isoformat(), inputs=inputs, coordinate=restart['coordinate'], theta=theta,
    gate=1e-10, precisions=[60, 80], nonlinear_check_digits=100, background_step='1e-12', wave_step='1e-20',
    retained_scope='All18 saved physical/difference columns, both joins, l0/1/2, original event0 and two signed soft probes',
    predictions=['60/80-digit contractions agree', 'full-coordinate expanded equilibrium delta agrees with projected contraction',
        'paired source differences preserve all three bilinear terms before rounding', 'nonlinear collision flux has the predicted mixed derivative'],
    preserved_failed_protocol=str(CONSUMER / 'factor-check-001'), original_gate_changed=False,
    source_integrated=False, history_propagated=False)
write(DESTINATION / 'prediction.json', prediction)
parameters, unused_weight = parent.source.physics.parameters_and_weight(theta, manifest['event']['node'])
direction, unused_angular_weight = list(retained.angular.inherited.source.angular_nodes(8))[0]
checks, old_diagnostics, packets = [], [], {}
with mp.workdps(80):
    owner = retained.Direction(retained.precise_context(parameters), direction)
    factors = FullTailFactors(owner, bundle, context['tests'])
    projections = {join: SplitColumns(bundle.high[:, join::2], bundle.low[:, join::2]) for join in (0, 1)}
    old_native = FullTailActionFactors(owner, bundle, context['tests'], projections)
    soft = [scalar(value) * owner.temperature / owner.doppler for value in (1e-4, .01)]
    events = {sign: [owner.event(sign * value) for value in soft] for sign in (-1, 1)}
    old_events = {sign: old_native.evaluate(soft, events[sign], sign) for sign in (-1, 1)}
    full_events = {sign: factors.evaluate(soft, events[sign], sign) for sign in (-1, 1)}
results, oracles, details = {}, {}, {}
for digits in (60, 80):
    retained.state235.mean_energy.cache_clear()
    with mp.workdps(digits):
        oracle = PreciseEpochResponse(factors, bundle.high[:, ::2], bundle.low[:, ::2])
        oracles[digits] = oracle
        current_results = {}
        for join in (0, 1):
            for degree in (0, 1, 2):
                current_results[f'born:join{join}:l{degree}'] = oracle.response(factors.left[degree], oracle.born(join, degree), degree)
                for sign in (-1, 1):
                    for node in range(2):
                        event_data = oracle.current(join, degree, soft[node], events[sign][node], sign)
                        left = factors.left[degree] + old_events[sign][degree, 'left_delta'][node]
                        label = f'sign{sign}:node{node}:join{join}:l{degree}'
                        current_results[label] = oracle.response(left, event_data['complete'], degree)
                        if digits == 80:
                            details[join, degree, sign, node] = event_data
                if any((path / 'STOP-REQUESTED').exists() for path in (ROOT, ROOT.parent, CONSUMER)):
                    raise RuntimeError('Owner stop preserved')
        results[digits] = current_results
    print(json.dumps(dict(precision_complete=digits, response_blocks=len(current_results))), flush=True)
with mp.workdps(80):
    for label, values in results[80].items():
        for state in range(19):
            for column in range(18):
                compare(f'{label}:state{state}:column{column}', [row[column] for row in results[60][label][state]],
                    [row[column] for row in values[state]], '60-vs80')
        differences = []
        for pair in range(6):
            direct, predicted, actual_equilibrium, predicted_equilibrium = difference(values, pair)
            compare(f'{label}:pair{pair}', direct, predicted, 'bilinear-difference')
            compare(f'{label}:pair{pair}', actual_equilibrium, predicted_equilibrium, 'equilibrium-difference')
            lower_direct = difference(results[60][label], pair)[0]
            compare(f'{label}:pair{pair}', lower_direct, direct, 'difference60-vs80')
            differences.append(direct)
        high, low = split_array(values)
        packets[label + ':high'], packets[label + ':low'] = high, low
        delta_high, delta_low = split_array(differences)
        packets[label + ':difference-high'], packets[label + ':difference-low'] = delta_high, delta_low
        if not label.endswith('l2'):
            for state in range(19):
                for column in range(18):
                    photon, gas = values[state][0][column], values[state][-1][column]
                    relative = abs(photon + gas) / max(abs(photon) + abs(gas), mp.mpf('1e-300'))
                    checks.append(dict(name=f'{label}:state{state}:column{column}', group='exchange', relative=float(relative), limit=1e-10, passed=relative <= mp.mpf('1e-10')))
    oracle = oracles[80]
    selected = details[1, 1, 1, 0]
    independent = oracle.expanded_equilibrium_delta(selected, 1, 1, factors.harmonics[1])
    old_full = projections[1].right(full_events[1][1, 1, 'right_delta'])[0, 0]
    old_projected = old_events[1][1, 1, 'right_delta'][0, 0]
    for column in range(18):
        compare(f'full578:column{column}', independent[column], selected['right_delta'][0][column], 'independent-expanded-reference')
        compare(f'old-native:column{column}', old_projected[column], independent[column], 'old-native', old_diagnostics)
        compare(f'old-full-factor:column{column}', old_full[column], independent[column], 'old-full-factor', old_diagnostics)
    with np.load(CONSUMER / 'factor-check-001/responses.npz', allow_pickle=False) as saved:
        for label, values in results[80].items():
            for pair in range(6):
                rounded_direct = difference(saved[label].tolist(), pair)[0]
                compare(f'{label}:pair{pair}', rounded_direct, difference(values, pair)[0], 'old-rounded-source-difference', old_diagnostics)
with mp.workdps(100):
    background_step, wave_step = mp.mpf('1e-12'), mp.mpf('1e-20')
    parent.thermodynamics.cache_clear()
    for pair in range(6):
        baseline, change = 3 * pair, 3 * pair + 2
        for background_column, wave_column, name in ((baseline, change, 'background-fixed'), (change, baseline, 'background-change')):
            background_values = [row[background_column] for row in oracle.base[0]]
            wave_values = [row[wave_column] * scalar(factors.harmonics[0][index, 0]) for index, row in enumerate(oracle.base[0])]
            numerator = mp.mpf(0)
            for background_sign in (-1, 1):
                for wave_sign in (-1, 1):
                    potential = [background_sign * background_step * before + wave_sign * wave_step * after for before, after in zip(background_values, wave_values)]
                    gas = background_sign * background_step * oracle.gas[background_column] + wave_sign * wave_step * oracle.gas[wave_column]
                    numerator += background_sign * wave_sign * parent.raw_flux(factors.event, potential, gas)
            actual = numerator / (4 * background_step * wave_step)
            expected = oracle.born(0, 0)[background_column + 1][wave_column][0]
            compare(f'pair{pair}:{name}', [actual], [expected], 'nonlinear-flux-mixed-derivative')
for path, checksum in inputs.items():
    if digest(path) != checksum:
        raise RuntimeError('Frozen source changed: ' + path)
with (DESTINATION / 'responses-split.npz').open('xb') as stream:
    np.savez_compressed(stream, **packets)
groups = {group: dict(checks=sum(row['group'] == group for row in checks), failed=sum(row['group'] == group and not row['passed'] for row in checks),
    maximum=max(row['relative'] for row in checks if row['group'] == group)) for group in sorted({row['group'] for row in checks})}
old_groups = {group: dict(checks=sum(row['group'] == group for row in old_diagnostics), failed=sum(row['group'] == group and not row['passed'] for row in old_diagnostics),
    maximum=max(row['relative'] for row in old_diagnostics if row['group'] == group)) for group in sorted({row['group'] for row in old_diagnostics})}
report = dict(passed=all(row['passed'] for row in checks), checks=checks, groups=groups,
    old_diagnostics=old_diagnostics, old_groups=old_groups, old_protocol_still_failed=True,
    prediction_sha256=digest(DESTINATION / 'prediction.json'), packet_sha256=digest(DESTINATION / 'responses-split.npz'),
    inputs=inputs, process=identity, finished_at=datetime.now(timezone.utc).isoformat(),
    scope='Unrounded physical contractions on the exact cell424 source epoch, same basis/kinematics; fixed-grid arithmetic refinement and independent nonlinear derivative',
    source_integrated=False, source_budget_assessed=False, history_propagated=False, tolerances_changed=False)
write(DESTINATION / 'validation.json', report)
print(json.dumps(dict(passed=report['passed'], checks=len(checks), groups=groups, old_diagnostics=old_groups,
    failed=[row for row in checks if not row['passed']][:12], process=identity)), flush=True)
raise SystemExit(0 if report['passed'] else 1)
