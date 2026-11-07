import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
import sys
sys.dont_write_bytecode = True
from pathlib import Path
ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
POST = BRANCH.parent
PARENT = BRANCH / 'dynamical-infrared-tail-20261008'
MATCHED = BRANCH / 'matched-weak-redistribution-20261008'
SOURCE = BRANCH / 'infrared-source-domain-20261008'
sys.path.insert(0, str(PARENT))
import tail_common as prior
from tail_common import np, math, json, time, special, linalg, interpolate, thermal_wave, I3
sys.path.insert(0, str(MATCHED))
import matched_weak as weak
from datetime import datetime, timezone
modest, digest, write_json = prior.modest, prior.digest, prior.write_json
STARTED = datetime(2026, 10, 8, 6, 2, 37, tzinfo=timezone.utc)


def finish(folder, report, script, extra=()):
    paths = {ROOT / 'population_common.py', ROOT / 'ACCEPTANCE.md', Path(script).resolve(),
             PARENT / 'results/stage-integrity.json'}
    paths.update(Path(path).resolve() for path in extra)
    for module in list(sys.modules.values()):
        filename = getattr(module, '__file__', None)
        if filename:
            path = Path(filename).resolve()
            if path.suffix == '.py' and path.is_relative_to(BRANCH):
                paths.add(path)
    report.update(state='complete', finished_utc=datetime.now(timezone.utc).isoformat(),
                  script_sha256=digest(script), input_hashes={str(path): digest(path) for path in sorted(paths)})
    report['count'] = len(report['checks'])
    report['all_checks_passed'] = all(item['passed'] for item in report['checks'])
    write_json(folder / 'status.json', report)
    (folder / 'COMPLETE').write_text('complete\n', encoding='utf-8')


class Spectra:
    def __init__(self, fraction, density=24001):
        self.basis, self.specification = prior.current_basis()
        self.frequency = np.geomspace(1e-6, 60., density)
        self.fraction, self.inputs = fraction, []
        self.values, self.gas = [], []
        self.original, self.tails = {}, {}
        self.heat = None
        for model in ['heavy', 'cold']:
            history = SOURCE / 'backgrounds' / (model + '-nonlocal-refined-6400') / 'history.npz'
            tail = PARENT / 'runs' / (model + '-production') / 'tail.npz'
            saved, low = dict(np.load(history)), dict(np.load(tail))
            coordinate = float(fraction * saved['expansion'][-1])
            self.coordinate = coordinate
            profile = interpolate.interp1d(saved['expansion'], saved['profiles'], axis=0)(coordinate)
            gas = float(np.interp(coordinate, saved['expansion'], saved['temperature_scaled']))
            slope = interpolate.interp1d(low['expansion'], low['slope'], axis=0)(coordinate)
            self.original[model], self.tails[model] = profile, (low['frequency'], slope)
            self.gas.append(gas)
            self.heat = float(low['heat'])
            for lower, upper in [(1e-4, 2e-4), (5e-5, 1e-4)]:
                phi = np.zeros(len(self.frequency))
                low_mask = self.frequency < upper
                low_phi = np.interp(np.log(self.frequency[low_mask]), np.log(low['frequency']), slope) * self.frequency[low_mask]
                high_mask = self.frequency > lower
                phi[high_mask] = self.basis.evaluate(self.frequency[high_mask]) @ profile
                phase = np.clip((self.frequency[low_mask] - lower) / (upper - lower), 0, 1)
                blend = phase**3 * (10 - 15 * phase + 6 * phase**2)
                phi[low_mask] = (1 - blend) * low_phi + blend * phi[low_mask]
                self.values.append(phi)
            self.inputs.extend([history, history.parent / 'status.json', tail, tail.parent / 'status.json'])
        self.values = np.column_stack(self.values)
        self.spline = interpolate.CubicSpline(np.log(self.frequency), self.values, axis=0, extrapolate=False)
        self.derivative_spline = self.spline.derivative()

    def functions(self, frequency, chemical=False):
        if chemical:
            raise ValueError('This projection reads energy and actual departures, not an unresolved chemical diagonal')
        frequency = np.asarray(frequency)
        tolerance = 1e-10
        if np.any(frequency < self.frequency[0] * (1 - tolerance)) or np.any(frequency > self.frequency[-1] * (1 + tolerance)):
            raise ValueError('Joined spectrum evaluated outside declared physical interval')
        coordinate = np.log(np.clip(frequency, self.frequency[0], self.frequency[-1]))
        return np.concatenate([frequency[..., None], self.spline(coordinate)], axis=-1)

    def derivatives(self, frequency, chemical=False):
        frequency = np.asarray(frequency)
        return np.r_[1., self.derivative_spline(math.log(float(frequency))) / frequency]

    def coefficients(self):
        result = np.zeros((6, 4))
        result[1:5, :] = np.eye(4)
        result[-1] = np.repeat(self.gas, 2)
        return result


def source_cache(parameters, order):
    import hashlib
    identity = dict(lab_energy=parameters['lab_energy'], cosine=parameters['lab_cosine'],
                    velocity=parameters['velocity'].tolist(), temperature=parameters['temperature'], order=order,
                    script_sha256=digest(weak.source.__file__), stage88_sha256=digest(MATCHED / 'results/stage-integrity.json'))
    key = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()
    folder = ROOT / 'virtual-cache'
    folder.mkdir(exist_ok=True)
    path = folder / (key + '.json')
    if path.exists():
        saved = json.loads(path.read_text())
        assert saved['identity'] == identity
        return saved['scalar'], path, False
    tensor, response = weak.source.virtual_map(parameters, order)
    scalar = float(response[0, 0])
    write_json(path, dict(identity=identity, scalar=scalar, finite=bool(np.isfinite(scalar))))
    return scalar, path, True
