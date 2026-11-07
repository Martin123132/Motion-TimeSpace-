from __future__ import annotations
import os
for variable in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[variable] = '1'
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import json
import hashlib
import time
from datetime import datetime, timezone
ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH / 'matched-angular-source-20261026'
PRODUCTION = BRANCH / 'complete-panel-operator-final-20261026'
HISTORY = BRANCH / 'history-aware-operator-temperature-test-20261025'
sys.path[:0] = [str(BRANCH / 'complete-panel-operator-batch1-20261025'), str(PARENT)]
import batch218 as production
import angular232 as angular
np, mp, linear = production.np, production.mp, production.linear
source, cached, precise, api = production.source, production.prior.lift.cached, production.prior.lift.precise, production.api
SEAL = '64e89d8d61b511318964b9ce86af4eb73c961906721dd623696350712a7f7f61'
START = '2026-10-26T19:47:59+00:00'


def now():
    return datetime.now(timezone.utc).isoformat()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def digest(path):
    hasher = hashlib.sha256()
    with Path(path).open('rb') as handle:
        for block in iter(lambda: handle.read(1048576), b''):
            hasher.update(block)
    return hasher.hexdigest()


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.partial')
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    os.replace(temporary, path)


def save(path, **values):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.partial')
    with temporary.open('wb') as handle:
        np.savez_compressed(handle, **values)
    os.replace(temporary, path)


def packet(path):
    with np.load(path, allow_pickle=False) as archive:
        return {name: archive[name].copy() for name in archive.files}


def register(inputs, path, expected=None):
    path = str(Path(path).resolve())
    value = digest(path)
    assert expected is None or expected == value, path
    assert path not in inputs or inputs[path] == value, path
    inputs[path] = value
    return Path(path)


def modules(inputs):
    for module in list(sys.modules.values()):
        filename = getattr(module, '__file__', None)
        if filename:
            path = Path(filename).resolve()
            if path.suffix == '.py' and path.is_relative_to(BRANCH) and not path.is_relative_to(ROOT):
                register(inputs, path)


def check(checks, name, value, limit=1e-10):
    value = abs(float(value))
    checks.append(dict(name=name, value=value, limit=limit, passed=bool(np.isfinite(value) and value <= limit)))


def relative(first, second):
    return float(np.linalg.norm(np.asarray(first) - np.asarray(second)) / max(np.linalg.norm(second), 1e-300))


def modest():
    import psutil
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([int(os.environ.get('MTS_CPU', '2'))])


def protocol():
    config = read(ROOT / 'configuration.json')
    for name, value in config['protocol_hashes'].items():
        assert digest(ROOT / name) == value, name
    return config


def prepare():
    assert not (ROOT / 'configuration.json').exists()
    assert digest(PARENT / 'results/stage-integrity.json') == SEAL
    parent = read(PARENT / 'results/stage-integrity.json')
    inputs = {}
    register(inputs, PARENT / 'results/stage-integrity.json', SEAL)
    for name, value in parent['file_hashes'].items():
        register(inputs, PARENT / name, value)
    config = read(register(inputs, PRODUCTION / 'configuration.json'))
    events = [row for row in config['events'] if row['frequency_index'] == 3 and row['event'] == 0]
    assert len(events) == 3 and {row['label'] for row in events} == {'warm', 'middle', 'cold'}
    for row in events:
        register(inputs, row['source_path'], row['source_sha256'])
        register(inputs, row['loop_path'], row['loop_sha256'])
        directory = BRANCH / 'complete-panel-operator-batch2-20261026/events/frequency-3' / row['label']
        record = read(register(inputs, directory / 'event-00.json'))
        row['operator_path'] = str(register(inputs, directory / 'event-00.npz', record['sha256']))
        row['operator_sha256'] = record['sha256']
        assert not record['failed_checks']
    original, theta = source.context(config['target_fraction'])
    assert theta == config['theta']
    for path in original.inputs:
        register(inputs, path)
    heat = original.epochs[0].heat
    states = []
    with mp.workdps(80):
        for model_index, model in enumerate(('heavy', 'cold')):
            original_vector = [mp.mpf(float(value)) for value in original.epochs[0].original[model]]
            original_gas = mp.mpf(float(original.gas[model_index]))
            for history in ('original', 'half', 'quarter'):
                if history == 'original':
                    vector, gas = original_vector, original_gas
                else:
                    path = register(inputs, HISTORY / f'histories/{model}-{history}.json')
                    record = read(path)
                    assert not record['failed_checks']
                    vector = list(map(mp.mpf, record['current']['profile']))
                    gas = mp.mpf(record['current']['gas'])
                coefficients = vector + [mp.mpf(int(model_index == 0)), mp.mpf(int(model_index == 1)), gas]
                states.append(dict(model=model, history=history, coefficients=[mp.nstr(value, 80) for value in coefficients]))
    coefficient_path = register(inputs, PRODUCTION / 'frozen/history-coefficients.npz')
    modules(inputs)
    bookmarks = {str(path): digest(path) for path in (BRANCH / 'RESUME-CURRENT.md', BRANCH.parent / 'CURRENT_LOCAL_RESUME.md')}
    write(ROOT / 'inputs.json', inputs)
    write(ROOT / 'configuration.json', dict(stage=233, turn_start=START, previous_turn='no progress: verified completed artifacts; this stage implements the next physical derivative',
        frozen_at=now(), events=events, states=states, target_fraction=config['target_fraction'], target_theta=theta,
        heat=heat, coefficient_path=str(coefficient_path), coefficient_sha256=digest(coefficient_path),
        history_policy='same saved target history held fixed while varying the operator temperature, as in Stage209',
        real_direction_indices=[0, 11, 23], real_upper_fractions=[.02, .2, .8], angular_rule=4,
        multipoles=[0, 1, 2], joins=[0, 1], arithmetic_digits=80, identity_tolerance=1e-10,
        original_bank_changed=False, original_tolerances_changed=False, new_virtual_integrals=0,
        maximum_workers=2, numerical_threads=1, bookmarks=bookmarks,
        protocol_hashes={path.name: digest(path) for path in ROOT.iterdir() if path.suffix in ('.py', '.md')}))
    print(json.dumps(dict(prepared=True, events=len(events), states=len(states), heat=heat, inputs=len(inputs))), flush=True)


if __name__ == '__main__':
    modest()
    prepare()
