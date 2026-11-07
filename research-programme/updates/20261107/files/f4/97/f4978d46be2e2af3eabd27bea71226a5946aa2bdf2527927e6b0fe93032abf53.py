import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
import sys
sys.dont_write_bytecode = True
from pathlib import Path
from datetime import datetime, timezone
ROOT = Path(__file__).resolve().parent
BRANCH, POST = ROOT.parent, ROOT.parent.parent
PARENT = BRANCH / 'complete-corrected-history-20261015'
sys.path.insert(0, str(PARENT))
import complete_history_common as inherited
from complete_history_common import np, math, json, linalg, digest, write_json, modest, infrared_ladder, read_npz, compact_defect, norm, load_histories
from shape_common import ShapeReadout, BETA
PARENT_SEAL = '597aa4d9c82a9eaaf01e8fa274cce6a7343ee29bfe0b3906fefb71afde51669f'
STARTED = datetime(2026, 10, 15, 19, 43, 19, tzinfo=timezone.utc)
NAMES = ['baseline', 'MTS_window_join1', 'MTS_window_join2']
DISPLAY_NAMES = NAMES + ['baseline_plus_window_join1', 'baseline_plus_window_join2']
EPS = np.finfo(float).eps
BINS = np.array([1e-5, 1e-4, 1e-3, .01, .1, 1., 10., 60.])


def ancestors():
    chain = inherited.ancestors()
    path = PARENT / 'results/stage-integrity.json'
    assert digest(path) == PARENT_SEAL
    return {path: json.loads(path.read_text()), **chain}


def finish(folder, report, script, extra=()):
    paths = {ROOT / 'spectrum_decomposition_common.py', ROOT / 'ACCEPTANCE.md',
             ROOT / 'DERIVATION.md', Path(script).resolve(), PARENT / 'results/stage-integrity.json'}
    paths.update(Path(path).resolve() for path in extra)
    for module in list(sys.modules.values()):
        filename = getattr(module, '__file__', None)
        if filename:
            path = Path(filename).resolve()
            if path.suffix == '.py' and path.is_relative_to(BRANCH):
                paths.add(path)
    report.update(state='complete', finished_utc=datetime.now(timezone.utc).isoformat(),
                  script_sha256=digest(script),
                  input_hashes={str(path): digest(path) for path in sorted(paths)})
    report['count'] = len(report['checks'])
    report['all_checks_passed'] = all(bool(row['passed']) for row in report['checks'])
    write_json(folder / 'status.json', report)
    (folder / 'COMPLETE').write_text('complete\n', encoding='utf-8')


def test(checks, name, value, limit=1e-10):
    value = float(value)
    checks.append(dict(name=name, value=value, limit=limit,
                       passed=bool(np.isfinite(value) and value < limit)))


def expanded(value):
    return np.concatenate([value, value[..., :1] + value[..., 1:3]], axis=-1)


def metrics(reader, split, heat):
    residual_power = (reader.measure[:, None] * split['residual'] ** 2).sum(axis=0)
    fractions = []
    for lower, upper in zip(BINS[:-1], BINS[1:]):
        chosen = (reader.frequency >= lower) & (reader.frequency < upper)
        local = (reader.measure[chosen, None] * split['residual'][chosen] ** 2).sum(axis=0)
        fractions.append(np.divide(local, residual_power, out=np.zeros_like(local), where=residual_power > 0).tolist())
    return dict(mu=(heat * split['amplitudes'][0]).tolist(),
                y=(heat * split['amplitudes'][1]).tolist(),
                temperature_energy_fraction=(heat * split['eta']).tolist(),
                temperature_standard_fraction=(heat * split['eta_standard']).tolist(),
                photon_energy_fraction=(heat * split['energy']).tolist(),
                spectral_energy_defect=split['energy_defect'].tolist(),
                distortion_norm=split['distortion_norm'].tolist(),
                residual_norm=split['residual_norm'].tolist(),
                residual_norm_fraction=split['residual_fraction'].tolist(),
                joint_captured_squared_fraction=split['captured_squared_fraction'].tolist(),
                residual_squared_fraction_by_frequency_bin=fractions)


def invariants(checks, reader, split, label):
    scale = np.maximum(norm(split['potential'], reader.measure), 1e-300)
    dscale = np.maximum(split['distortion_norm'], 1e-300)
    reconstructed = split['temperature'] + split['joint'] + split['residual']
    test(checks, 'Reconstruction:' + label, np.max(norm(reconstructed - split['potential'], reader.measure) / scale))
    standard = reader.frequency[:, None] * split['eta_standard'] + reader.standard @ split['amplitudes'] + split['residual']
    test(checks, 'Standard convention:' + label, np.max(norm(standard - split['potential'], reader.measure) / scale))
    cross = (reader.templates.T * reader.measure) @ split['residual']
    test(checks, 'Mu y orthogonality:' + label, np.max(abs(cross) / (reader.template_norms[:, None] * dscale)))
    test(checks, 'Squared norm partition:' + label,
         np.max(abs(split['distortion_norm'] ** 2 - split['joint_norm'] ** 2 - split['residual_norm'] ** 2) / dscale ** 2))
    alternative = linalg.lstsq(reader.design, np.sqrt(reader.measure)[:, None] * split['distortion'], lapack_driver='gelsd')[0] / reader.template_norms[:, None]
    test(checks, 'Independent SVD:' + label, np.max(norm(reader.templates @ (alternative - split['amplitudes']), reader.measure) / dscale))
    allowance = 256 * EPS * np.maximum((reader.measure * reader.frequency) @
        (abs(split['potential']) + abs(split['temperature']) + abs(split['joint']) + abs(split['residual'])), 1e-300)
    residual_energy = (reader.measure * reader.frequency) @ split['residual']
    test(checks, 'Retained energy discrepancy:' + label, np.max(abs(residual_energy - split['energy_defect']) / allowance), 1.)
