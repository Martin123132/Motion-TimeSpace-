import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
import sys
sys.dont_write_bytecode = True
from pathlib import Path
from datetime import datetime, timezone
import hashlib
ROOT = Path(__file__).resolve().parent
BRANCH, POST = ROOT.parent, ROOT.parent.parent
PARENT = BRANCH / 'electron-azimuth-source-20261009'
OUTER = BRANCH / 'outer-population-source-20261008'
sys.path.insert(0, str(PARENT))
import azimuth_common as inherited
from azimuth_common import np, math, json, time, special, linalg, interpolate, weak, thermal_wave, I3, Spectra, TestFunctions, SplitReal, PanelRule, population_nodes, node_key, compact_rule
from fast_source import FastSplit
digest, write_json = inherited.digest, inherited.write_json


def modest():
    import psutil
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([int(os.environ.get('MTS_CPU', '2'))])

STARTED = datetime(2026, 10, 9, 15, 59, 13, tzinfo=timezone.utc)
PARENT_SEAL = '3d339bc2e6ad345ca3cb5145e63943f195bae54223faa7ac5ba85ec9833e5587'


def finish(folder, report, script, extra=()):
    paths = {ROOT / 'polar_common.py', ROOT / 'ACCEPTANCE.md', Path(script).resolve(), PARENT / 'results/stage-integrity.json'}
    paths.update(Path(path).resolve() for path in extra)
    for module in list(sys.modules.values()):
        filename = getattr(module, '__file__', None)
        if filename:
            path = Path(filename).resolve()
            if path.suffix == '.py' and path.is_relative_to(BRANCH):
                paths.add(path)
    report.update(state='complete', finished_utc=datetime.now(timezone.utc).isoformat(),
        script_sha256=digest(script), input_hashes={str(path):digest(path) for path in sorted(paths)})
    report['count'] = len(report['checks'])
    report['all_checks_passed'] = all(row['passed'] for row in report['checks'])
    write_json(folder / 'status.json', report)
    (folder / 'COMPLETE').write_text('complete\n', encoding='utf-8')


def virtual_identity(parameters):
    return dict(lab_energy=parameters['lab_energy'], cosine=parameters['lab_cosine'],
        velocity=parameters['velocity'].tolist(), temperature=parameters['temperature'], order=2,
        script_sha256=digest(weak.source.__file__),
        stage88_sha256=digest(BRANCH / 'matched-weak-redistribution-20261008/results/stage-integrity.json'))


def owned_loop(parameters):
    identity = virtual_identity(parameters)
    key = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()
    path = ROOT / 'virtual-cache' / key[:2] / (key + '.json')
    if path.exists():
        saved = json.loads(path.read_text())
        assert saved['identity'] == identity and saved['finite'] and np.isfinite(saved['scalar'])
    else:
        tensor, response = weak.source.virtual_map(parameters, 2)
        scalar = float(response[0, 0])
        assert np.isfinite(scalar)
        saved = dict(identity=identity, scalar=scalar, finite=True)
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix('.tmp')
        write_json(temporary, saved)
        temporary.replace(path)
    return saved['scalar'], path
