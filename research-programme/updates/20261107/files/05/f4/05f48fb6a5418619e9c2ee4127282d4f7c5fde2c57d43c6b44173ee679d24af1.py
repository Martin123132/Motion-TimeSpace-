import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
import sys
sys.dont_write_bytecode = True
from pathlib import Path
ROOT = Path(__file__).resolve().parent
BRANCH, POST = ROOT.parent, ROOT.parent.parent
PARENT = BRANCH / 'population-matched-source-20261008'
sys.path.insert(0, str(PARENT))
import population_common as inherited
from population_common import np, math, json, time, special, linalg, interpolate, weak, prior, thermal_wave, I3, Spectra
from datetime import datetime, timezone
from contextlib import contextmanager
modest, digest, write_json = inherited.modest, inherited.digest, inherited.write_json
STARTED = datetime(2026, 10, 8, 10, 2, 38, tzinfo=timezone.utc)


def finish(folder, report, script, extra=()):
    paths = {ROOT / 'rectangular_common.py', ROOT / 'ACCEPTANCE.md', Path(script).resolve(),
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


class TestFunctions:
    def __init__(self, basis, density=48001, exact=False):
        self.basis, self.exact = basis, exact
        self.frequency = np.geomspace(1e-6, 60., density)
        self.spline = interpolate.CubicSpline(np.log(self.frequency), basis.evaluate(self.frequency), axis=0, extrapolate=False)
        self.prime = self.spline.derivative()

    def evaluate(self, frequency):
        frequency = np.asarray(frequency)
        if np.any(frequency < 1e-6 * (1 - 1e-10)) or np.any(frequency > 60 * (1 + 1e-10)):
            raise ValueError('Test evaluation outside explicit spectral domain')
        values = self.basis.evaluate(frequency) if self.exact else self.spline(np.log(np.clip(frequency, 1e-6, 60.)))
        values[..., 0] = 1 / self.basis.norms[0]
        values[..., 1] = (frequency - self.basis.mean) / self.basis.norms[1]
        return np.concatenate([frequency[..., None], values], axis=-1)

    def derivative(self, frequency):
        frequency = np.asarray(frequency)
        values = self.basis.derivative(frequency) if self.exact else self.prime(np.log(frequency)) / frequency[..., None]
        values[..., 0] = 0.
        values[..., 1] = 1 / self.basis.norms[1]
        return np.concatenate([np.ones(frequency.shape + (1,)), values], axis=-1)
