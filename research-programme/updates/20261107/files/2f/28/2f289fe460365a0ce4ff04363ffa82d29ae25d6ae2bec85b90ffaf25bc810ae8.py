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


def main():
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260914'
    states = {
        'annular-native-shape-stress-attempt01': 'complete',
        'annular-native-shape-stress-validation-attempt01': 'failed',
        'annular-native-shape-stress-validation-attempt02': 'complete',
        'annular-native-areal-lift-attempt01': 'complete',
    }
    hashes, run_rows = {}, []
    for name, expected in states.items():
        path = intake / name / 'status.json'
        report = json.loads(path.read_text())
        assert report['state'] == expected, name
        if expected == 'complete':
            assert all(check['passed'] for check in report['checks']), name
        else:
            assert report['checks'][-1]['name'] == 'actual_hinge_omission_changes_energy'
            assert not report['checks'][-1]['passed']
            assert all(check['passed'] for check in report['checks'][:-1])
        run_rows.append(dict(name=name, state=expected, checks=len(report['checks']), seconds=report.get('seconds')))
        for category in ['inputs', 'outputs']:
            for relative, digest in report[category].items():
                assert relative not in hashes or hashes[relative] == digest, relative
                hashes[relative] = digest
        hashes[str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()
    documents = ['RESULTS-20260928-native-kernel-shape-stress.md',
                 'DERIVATION-20260928-native-kernel-shape-stress.md',
                 'DERIVATION-20260928-native-areal-metric-lift.md',
                 'DERIVATION-20260928-native-hinge-control-correction.md']
    cited = set()
    for name in documents:
        path = root / name
        for reference in re.findall(r'`([^`\n]+\.(?:md|py|json|csv))`', path.read_text()):
            assert (root / reference).is_file(), reference
            cited.add(reference)
        hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    for name in ['CURRENT_LOCAL_RESUME.md', 'scripts/audit_annular_native_shape_final_20260928.py']:
        hashes[name] = hashlib.sha256((root / name).read_bytes()).hexdigest()
    mismatches = [relative for relative, digest in hashes.items()
                  if not (root / relative).is_file() or hashlib.sha256((root / relative).read_bytes()).hexdigest() != digest]
    assert not mismatches, mismatches
    tables = {
        'annular-native-shape-stress-attempt01/native-shape-and-current.csv': 12,
        'annular-native-shape-stress-validation-attempt02/real-native-variations.csv': 84,
        'annular-native-shape-stress-validation-attempt02/current-primitive-replay.csv': 36,
        'annular-native-areal-lift-attempt01/areal-metric-responses.csv': 108,
        'annular-native-areal-lift-attempt01/native-spatial-Ward.csv': 36,
        'annular-native-areal-lift-attempt01/source-affine-power.csv': 12,
    }
    maximum_error_ratio = 0.
    table_rows = {}
    with localcontext() as context:
        context.prec = 80
        for name, count in tables.items():
            with (intake / name).open(newline='') as handle:
                rows = list(csv.DictReader(handle))
            assert len(rows) == count and all(None not in row and None not in row.values() for row in rows), name
            for row in rows:
                for column, value in row.items():
                    if column not in ['branch', 'level', 'direction', 'sector']:
                        assert math.isfinite(float(value)), (name, column)
                if 'extrapolated' in row:
                    error = abs(Decimal(row['extrapolated']) - Decimal(row['predicted']))
                    assert error <= Decimal(row['tolerance'])
                    assert abs(error - Decimal(row['error'])) < Decimal('1e-70')
                    maximum_error_ratio = max(maximum_error_ratio, float(error / Decimal(row['tolerance'])))
                if 'angular_difference' in row:
                    difference = Decimal(row['new_spatial']) - Decimal(row['old_spatial'])
                    assert abs(difference - Decimal(row['angular_difference'])) < Decimal('1e-70')
            table_rows[name] = rows
    reader = (root / documents[0]).read_text()
    source_rows = table_rows['annular-native-shape-stress-attempt01/native-shape-and-current.csv']
    for level in ['Fine', 'Third']:
        line = next(line for line in reader.splitlines() if line.startswith('| ' + level + ' |'))
        values = [float(value.strip()) for value in line.split('|')[2:-1]]
        row = next(row for row in source_rows if row['branch'] == 'MTS-primary' and row['level'] == level.lower() and row['test'] == '1')
        for value, channel in zip(values, ['field_transport', 'kernel_shape', 'metric_coefficient', 'total_shape']):
            assert abs(value - float(row[channel])) < 6e-23, (level, channel)
    scripts = ['annular_physical_native_kernel_20260928.py', 'derive_annular_native_shape_stress_20260928.py',
               'validate_annular_native_shape_stress_20260928.py', 'validate_annular_native_shape_stress_v2_20260928.py',
               'derive_annular_native_areal_lift_20260928.py', 'audit_annular_native_shape_final_20260928.py']
    for name in scripts:
        path = root / 'scripts' / name
        compile(path.read_text(), str(path), 'exec')
    assert not (root / 'scripts/__pycache__').exists()
    cutoff = datetime.fromisoformat('2026-09-27T23:03:41+00:00').timestamp()
    protected = root.parent / 'formalization-workbench'
    changes = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= cutoff]
    assert not changes, changes
    lapse, metric, area_r = sp.symbols('N F A_r', positive=True)
    area_t, shift, time_form, area_form = sp.symbols('A_t v dt dA', real=True)
    original = -lapse**2 * time_form**2 + ((area_form - area_t * time_form) / area_r + shift * time_form)**2 / metric
    transformed = -lapse**2 * time_form**2 + (area_form + (shift * area_r - area_t) * time_form)**2 / (metric * area_r**2)
    assert sp.simplify(original - transformed) == 0
    result = dict(state='complete', audit_time=datetime.now(timezone.utc).isoformat(), runs=run_rows,
                  unique_files_rehashed=len(hashes), hash_mismatches=mismatches, cited_paths_checked=len(cited),
                  CSV_rows=tables, reader_numeric_table_checked=True, maximum_derivative_error_over_gate=maximum_error_ratio,
                  compiled_scripts=scripts, bytecode_cache=False, protected_workbench_mtime_changes=changes,
                  protected_since='2026-09-27T23:03:41+00:00',
                  time_dependent_areal_coordinate_identity_verified=True,
                  all_owned_numerical_execs_finished=[59260, 5006, 89886, 28774, 70078],
                  github_action=False, subagents_used=False, new_nonlinear_solves=0, hashes=hashes)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
