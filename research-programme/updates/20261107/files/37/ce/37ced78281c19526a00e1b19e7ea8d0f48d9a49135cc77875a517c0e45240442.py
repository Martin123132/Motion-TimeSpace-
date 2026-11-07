from derive_annular_source_gravity_20260914 import EvidenceRun
from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal, localcontext
import csv
import hashlib
import json
import math
import re
import sympy as sp


def radial_chain_checks():
    metric, area_r, relabel_r = sp.symbols('F A_r f_r', positive=True)
    area_t, shift, relabel_t = sp.symbols('A_t v f_t', real=True)
    transformed_metric = metric * relabel_r**2
    transformed_shift = relabel_r * shift - relabel_t
    transformed_area_r = area_r / relabel_r
    transformed_area_t = area_t - area_r * relabel_t / relabel_r
    assert sp.simplify(transformed_metric * transformed_area_r**2 - metric * area_r**2) == 0
    assert sp.simplify(transformed_shift * transformed_area_r - transformed_area_t - (shift * area_r - area_t)) == 0
    time, radius = sp.symbols('t r', real=True, positive=True)
    lapse = sp.Function('N', positive=True)(time, radius)
    radial_metric = sp.Function('F', positive=True)(time, radius)
    density = sp.Function('rho')(time, radius)
    radial_pressure = sp.Function('pr')(time, radius)
    transverse_pressure = sp.Function('pt')(time, radius)
    mixed = sp.Function('K')(time, radius)
    measure = lapse * radius**2 / sp.sqrt(radial_metric)
    lapse_covector = -radius**2 * density / sp.sqrt(radial_metric)
    metric_covector = -lapse * radius**2 * radial_pressure / (2 * radial_metric**sp.Rational(3, 2))
    area_covector = 2 * lapse * radius * transverse_pressure / sp.sqrt(radial_metric)
    combination = -sp.diff(lapse, radius) * lapse_covector - sp.diff(radial_metric, radius) * metric_covector
    combination += -sp.diff(2 * radial_metric * metric_covector, radius) + sp.diff(measure * mixed, time) - area_covector
    divergence = sp.diff(mixed, time) + (sp.diff(lapse, time) / lapse - sp.diff(radial_metric, time) / (2 * radial_metric)) * mixed
    divergence += sp.diff(radial_pressure, radius) + (density + radial_pressure) * sp.diff(lapse, radius) / lapse
    divergence += 2 * (radial_pressure - transverse_pressure) / radius
    assert sp.simplify(combination - measure * divergence) == 0
    return dict(time_dependent_radial_metric_invariance=True, time_dependent_radial_shift_invariance=True,
                metric_covector_to_radial_divergence_signs=True,
                scope='Algebraic coordinate/variational identities for the stated extension; no full-system on-shell residual is set to zero.')


def main():
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260914'
    hashes, runs = {}, []
    for name in ['annular-native-time-current-attempt01', 'annular-native-time-current-validation-attempt01']:
        path = intake / name / 'status.json'
        report = json.loads(path.read_text())
        assert report['state'] == 'complete' and all(check['passed'] for check in report['checks'])
        runs.append(dict(name=name, checks=len(report['checks']), seconds=report['seconds']))
        for category in ['inputs', 'outputs']:
            for relative, digest in report[category].items():
                assert relative not in hashes or hashes[relative] == digest, relative
                hashes[relative] = digest
        hashes[str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()
    documents = ['DERIVATION-20260928-native-time-current-and-areal-momentum.md', 'RESULTS-20260928-native-time-current-and-areal-momentum.md']
    cited = set()
    for name in documents:
        path = root / name
        hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
        for reference in re.findall(r'`([^`\n]+\.(?:md|py|json|csv))`', path.read_text()):
            assert (root / reference).is_file(), reference
            cited.add(reference)
    for name in ['CURRENT_LOCAL_RESUME.md', 'scripts/seal_annular_native_time_current_20260928.py']:
        hashes[name] = hashlib.sha256((root / name).read_bytes()).hexdigest()
    failures = [relative for relative, digest in hashes.items() if not (root / relative).is_file()
                or hashlib.sha256((root / relative).read_bytes()).hexdigest() != digest]
    assert not failures, failures
    tables = {
        'annular-native-time-current-attempt01/native-current-comparison.csv': 36,
        'annular-native-time-current-attempt01/native-time-variations.csv': 144,
        'annular-native-time-current-attempt01/wave-areal-momentum.csv': 72,
        'annular-native-time-current-validation-attempt01/independent-current-replay.csv': 36,
        'annular-native-time-current-validation-attempt01/wave-momentum-quadrature.csv': 36,
    }
    with localcontext() as context:
        context.prec = 90
        for relative, count in tables.items():
            with (intake / relative).open(newline='') as handle:
                rows = list(csv.DictReader(handle))
            assert len(rows) == count and all(None not in row and None not in row.values() for row in rows)
            for row in rows:
                for column, value in row.items():
                    if column not in ['branch', 'level', 'kind']:
                        assert math.isfinite(float(value)), (relative, column)
                if 'error' in row:
                    assert Decimal(row['error']) <= Decimal(row['tolerance'])
                if 'extrapolated' in row:
                    assert abs(Decimal(row['extrapolated']) - Decimal(row['predicted'])) <= Decimal(row['tolerance'])
                    assert abs(Decimal(row['raw']) - Decimal(row['current']) - Decimal(row['boundary_rate'])) < Decimal('1e-65')
    scripts = ['annular_native_time_current_20260928.py', 'derive_annular_native_time_current_20260928.py',
               'validate_annular_native_time_current_20260928.py', 'seal_annular_native_time_current_20260928.py']
    for name in scripts:
        path = root / 'scripts' / name
        compile(path.read_text(), str(path), 'exec')
    assert not (root / 'scripts/__pycache__').exists()
    cutoff = datetime.fromisoformat('2026-09-27T23:41:05+00:00').timestamp()
    protected = root.parent / 'formalization-workbench'
    changes = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= cutoff]
    assert not changes, changes
    algebra = radial_chain_checks()
    seal = dict(state='complete', sealed_at=datetime.now(timezone.utc).isoformat(), runs=runs,
                unique_files_rehashed=len(hashes), mismatches=failures, cited_paths_checked=len(cited), CSV_rows=tables,
                compiled_scripts=scripts, no_bytecode_cache=True, protected_workbench_mtime_changes=changes,
                protected_since='2026-09-27T23:41:05+00:00', algebra=algebra,
                owned_numerical_execs_finished=[31942, 22398], github_action=False, subagents_used=False,
                new_nonlinear_solves=0, full_radial_balance_recomputed=False,
                navigation_pointer_note='CURRENT_LOCAL_RESUME.md is hashed at this checkpoint but intentionally mutable in later turns.', hashes=hashes)
    path = intake / 'annular-native-time-current-final-integrity-20260928.json'
    with path.open('x', encoding='utf-8') as handle:
        json.dump(seal, handle, indent=2)
        handle.write('\n')
    print(json.dumps({key:seal[key] for key in ['state', 'unique_files_rehashed', 'mismatches', 'cited_paths_checked', 'protected_workbench_mtime_changes', 'algebra']}))


if __name__ == '__main__':
    main()
