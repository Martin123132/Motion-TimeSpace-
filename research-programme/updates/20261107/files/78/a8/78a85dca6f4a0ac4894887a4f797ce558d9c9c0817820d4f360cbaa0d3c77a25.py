import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import json
import hashlib
from datetime import datetime, timezone
import time
ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH / 'microscopic-temperature-tangent-20261019'
PARENT_SHA = '7db6e7dd1af7379166622b2b76262f6f6f2ff84b7e1cdeecf9522bc66ab6353f'
sys.path.insert(0, str(PARENT))
import source_tangent as source
import numpy as np
import mpmath as mp
STARTED = '2026-10-19T23:15:19+00:00'
DEADLINE = '2026-10-20T02:50:00+00:00'
ELECTRONS = [0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14]
REUSED = {0: 8, 5: 9, 8: 10, 13: 11}
BRANCHES = ['moving_history', 'fixed_incident']
digest = source.digest
write_json = source.write_json
combine = source.precise_combine
norm = source.photon_norm


def read_pair(path):
    with np.load(path) as data:
        return data['high'].copy(), data['low'].copy()


def inputs():
    paths = {*ROOT.glob('*.py'), ROOT / 'ACCEPTANCE.md', ROOT / 'DERIVATION.md',
             PARENT / 'results/stage-integrity.json'}
    for module in list(sys.modules.values()):
        filename = getattr(module, '__file__', None)
        if filename and Path(filename).suffix == '.py' and Path(filename).resolve().is_relative_to(BRANCH):
            paths.add(Path(filename).resolve())
    return paths


def finish(folder, checks, paths=(), **fields):
    folder.mkdir(parents=True, exist_ok=True)
    packet = dict(state='complete', finished_utc=datetime.now(timezone.utc).isoformat(), checks=checks,
                  count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                  input_hashes={str(path): digest(path) for path in sorted(inputs() | set(map(Path, paths)))}, **fields)
    write_json(folder / 'status.json', packet)
    (folder / 'COMPLETE').write_text('complete\n', encoding='utf-8')
    return packet


def verify(folder):
    packet = json.loads((folder / 'status.json').read_text())
    assert packet['state'] == 'complete' and (folder / 'COMPLETE').exists()
    for filename, checksum in packet['input_hashes'].items():
        assert digest(filename) == checksum, filename
    return packet


def check(rows, label, value, tolerance):
    value = float(value)
    rows.append(dict(name=label, value=value, tolerance=tolerance,
                     passed=bool(np.isfinite(value) and value < tolerance)))


def event_path(tag, electron):
    if electron in REUSED:
        location = 'events/target' if tag == 'target' else 'results/state-overlays/' + tag
        return PARENT / location / f'event-{REUSED[electron]:03d}.npz'
    return ROOT / 'events' / tag / f'electron-{electron:02d}.npz'


def nodes(theta):
    selected = [node for node in source.physics.integration_nodes(theta, 7)
                if node['frequency'] == 14. and node['cosine'] == 0.]
    assert [node['electron_index'] for node in selected] == ELECTRONS
    return selected


def virtual(parameters):
    identity = source.physics.event_owner.inherited.virtual_identity(parameters)
    key = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()
    locations = [BRANCH / name / 'virtual-cache' / key[:2] / (key + '.json') for name in
                 ['microscopic-temperature-tangent-20261019', 'predictor-anchor-order6-20261018',
                  'incoming-band13-order8-20261018', 'targeted-frequency-band-refinement-20261018',
                  'incoming-band820-order7-20261018']]
    path = next((path for path in locations if path.exists()), ROOT / 'virtual-cache' / key[:2] / (key + '.json'))
    reused = path.exists()
    if reused:
        packet = json.loads(path.read_text())
        assert packet['identity'] == identity and packet['finite']
    else:
        unused, response = source.physics.weak.source.virtual_map(parameters, 2)
        packet = dict(identity=identity, scalar=float(response[0, 0]), finite=bool(np.isfinite(response[0, 0])))
        assert packet['finite']
        write_json(path, packet)
    mp.mp.dps = 60
    return packet['scalar'], path, reused


def predictors(pairs, delta):
    tangents, curvatures = [], []
    for step, plus, minus in [(.01, 'plus', 'minus'), (.005, 'plus_half', 'minus_half')]:
        tangents.append(combine([pairs[plus], pairs[minus]], [1/(2*step), -1/(2*step)]))
        curvatures.append(combine([pairs[plus], pairs['anchor'], pairs[minus]], [1/step**2, -2/step**2, 1/step**2]))
    linear = combine([pairs['anchor'], tangents[1]], [1, delta])
    quadratic = combine([linear, curvatures[1]], [1, delta**2/2])
    coarse = combine([pairs['anchor'], tangents[0], curvatures[0]], [1, delta, delta**2/2])
    return [linear, quadratic, coarse], [*tangents, *curvatures]


def selected_pair(pair, index):
    return pair[0][index], pair[1][index]
