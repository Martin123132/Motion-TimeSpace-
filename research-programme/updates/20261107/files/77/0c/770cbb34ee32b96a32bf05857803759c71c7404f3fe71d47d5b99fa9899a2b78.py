import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
import sys
sys.dont_write_bytecode = True
from pathlib import Path
ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH / 'infrared-source-domain-20261008'
POST = BRANCH.parent
sys.path.insert(0, str(PARENT))
import nonlocal_common as inherited
from nonlocal_common import np, math, json, time, special, linalg, interpolate, thermal_wave, integrated_dc, I3, I4
from nonlocal_dc import current_basis, soft_slope_row
from sourced_emission import GauntTable, SourcedEmission
from soft_compton_moments import incoming_transform, source
from scipy import sparse
from scipy.sparse import linalg as sparse_linalg
from datetime import datetime, timezone
modest, digest, write_json = inherited.modest, inherited.digest, inherited.write_json
STARTED = datetime(2026, 10, 8, 5, 35, 16, tzinfo=timezone.utc)


def finish(folder, report, script, extra=()):
    paths = {ROOT / 'tail_common.py', ROOT / 'ACCEPTANCE.md', Path(script).resolve(),
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


class FreeFree:
    br_rates = SourcedEmission.br_rates

    def __init__(self, background, frequency):
        self.background, self.frequency = background, frequency
        self.inputs = [inherited.BACKGROUND / 'sources' / ('gauntff_merged_Z0' + str(charge) + '.dat') for charge in [1, 2]]
        self.tables = [GauntTable(path, charge) for path, charge in zip(self.inputs, [1, 2])]


def jump_events(theta, order):
    ratios, conductance = [], []
    for velocity, gas_weight in inherited.inherited.gas_rule(theta, order, order):
        transform, bath, incoming_doppler = incoming_transform(velocity)
        for direction, angular_weight in source.angular_nodes(order):
            ratio = incoming_doppler * source.dot(bath, np.r_[1., direction])
            coefficient = gas_weight * (1 - velocity[2]) * 3 / (16 * np.pi)
            coefficient *= angular_weight * (1 + direction[2]**2)
            ratios.append(ratio)
            conductance.append(coefficient)
    return np.array(ratios), np.array(conductance)


def stencil(theta, order, spacing, offsets):
    ratios, rates = jump_events(theta, order)
    shifts = np.log(ratios) / spacing
    lower = np.floor(shifts).astype(int)
    fraction = shifts - lower
    assert lower.min() >= offsets[0] and (lower + 1).max() <= offsets[-1]
    result = np.zeros(len(offsets))
    np.add.at(result, lower - offsets[0], rates * (1 - fraction))
    np.add.at(result, lower + 1 - offsets[0], rates * fraction)
    eigenvalue = float(rates @ (-np.expm1(-np.log(ratios))))
    assert result.min() >= 0
    result[-offsets[0]] -= rates.sum()
    return result, eigenvalue


def split_matrix(coefficients, offsets, size):
    margin = max(-int(offsets[0]), int(offsets[-1]))
    rows, columns, values = [], [], []
    for offset, coefficient in zip(offsets, coefficients):
        if coefficient:
            rows.extend(range(size))
            columns.extend(np.arange(size) + margin + offset)
            values.extend([coefficient] * size)
    extended = sparse.csr_matrix((values, (rows, columns)), shape=(size, size + 2 * margin))
    return extended[:, margin:margin + size].tocsc(), extended[:, :margin], extended[:, margin + size:]


def plasma_ratio(background, theta):
    constants = background.constants
    wavelength = 6.62607015e-34 / (2 * np.pi * constants['m_e'] * constants['c'])
    density = background.electron0 / (background.theta0 / theta)**3
    return math.sqrt(4 * np.pi * integrated_dc.ALPHA * density * wavelength**3) / theta
