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
PARENT = BRANCH / 'lower-outer-frequency-temperature-test-20261020'
PARENT_SHA = 'c6fb74f90dfbec9832944124d7108fd91d158175ac0ddc6c8907c102f9d9de74'
sys.path.insert(0, str(PARENT))
import stage175_frequency_common as previous
source = previous.source
np, mp = previous.np, previous.mp
STARTED = '2026-10-20T16:31:40+00:00'
DEADLINE = '2026-10-20T20:00:00+00:00'
ELECTRONS, ANGLES, BRANCHES = previous.ELECTRONS, previous.ANGLES, previous.BRANCHES
digest, write_json = source.digest, source.write_json
combine, norm = source.precise_combine, source.photon_norm
read_pair, predictors = previous.read_pair, previous.predictors
angle_label, event_key = previous.angle_label, previous.event_key


def inputs():
    paths = {*ROOT.glob('*.py'), ROOT / 'ACCEPTANCE.md', ROOT / 'DERIVATION.md', PARENT / 'results/stage-integrity.json'}
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
    rows.append(dict(name=label, value=value, tolerance=tolerance, passed=bool(np.isfinite(value) and value < tolerance)))


def event_path(tag, key):
    angle, electron = key.split(':electron')
    return ROOT / 'events' / tag / angle / f'electron-{int(electron):02d}.npz'


def nodes(theta, frequency):
    selected = [node for node in source.physics.integration_nodes(theta, 7) if node['frequency'] == frequency]
    assert len(selected) == 36 and len({event_key(node) for node in selected}) == 36
    for angle in ANGLES:
        assert [node['electron_index'] for node in selected if angle_label(node['cosine']) == angle] == ELECTRONS
    return selected


def virtual(parameters):
    identity = source.physics.event_owner.inherited.virtual_identity(parameters)
    key = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()
    locations = [BRANCH / name / 'virtual-cache' / key[:2] / (key + '.json') for name in
                 ['lower-outer-frequency-temperature-test-20261020', 'upper-adjacent-frequency-temperature-test-20261020', 'adjacent-frequency-temperature-test-20261020', 'scattering-angle-temperature-sum-20261020', 'electron-direction-temperature-average-20261020',
                  'microscopic-temperature-tangent-20261019', 'predictor-anchor-order6-20261018',
                  'incoming-band13-order8-20261018', 'targeted-frequency-band-refinement-20261018', 'incoming-band820-order7-20261018']]
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


def reference_prediction():
    path = PARENT / 'results/frozen/predictions.npz'
    with np.load(path) as packet:
        index = list(packet['groups']).index('four_frequency_partial')
        predictions = [(packet['high'][index, order].copy(), packet['low'][index, order].copy()) for order in range(3)]
        derivatives = [(packet['derivative_high'][index, order].copy(), packet['derivative_low'][index, order].copy()) for order in range(4)]
    return predictions, derivatives, path


def reference_target():
    path = PARENT / 'results/assessment/actuals.npz'
    with np.load(path) as packet:
        index = list(packet['groups']).index('four_frequency_partial')
        pair = (packet['high'][index].copy(), packet['low'][index].copy())
    return pair, path
