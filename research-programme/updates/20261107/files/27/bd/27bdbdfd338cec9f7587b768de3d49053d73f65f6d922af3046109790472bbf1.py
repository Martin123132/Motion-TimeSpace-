from pathlib import Path
from datetime import datetime, timezone
import csv
import ctypes
import hashlib
import json
import os
import re


def main():
    for variable in ['OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS']:
        os.environ[variable] = '1'
    import numpy as np
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 1 << 2):
        raise OSError('Affinity failed')
    kernel.SetPriorityClass.argtypes = [ctypes.c_void_p, ctypes.c_uint]
    if not kernel.SetPriorityClass(kernel.GetCurrentProcess(), 0x4000):
        raise OSError('BelowNormal priority failed')
    root = Path(__file__).resolve().parents[1]
    directory = root / 'source-intake/navier-stokes/20260914'
    target = directory / 'annular-high-order-source-separation-integrity-20261003.json'
    if target.exists():
        raise FileExistsError(target)
    hashes, mismatches, authorities = {}, [], {}
    def verify(relative, expected=None):
        path = (root / relative).resolve()
        if path == root / 'CURRENT_LOCAL_RESUME.md':
            return
        if not path.is_relative_to(root) or not path.is_file():
            raise RuntimeError('Invalid integrity path ' + str(relative))
        key = str(path.relative_to(root))
        if key not in hashes:
            hashes[key] = hashlib.sha256(path.read_bytes()).hexdigest()
        if expected is not None and hashes[key] != expected:
            mismatches.append(key)
    parent_path = directory / 'annular-high-order-live-repair-integrity-20261003.json'
    parent = json.loads(parent_path.read_text())
    if parent['state'] != 'complete' or parent['mismatches']:
        raise RuntimeError('Incomplete parent')
    verify(parent_path.relative_to(root))
    for relative, expected in parent['hashes'].items():
        verify(relative, expected)
    failures = {
        'annular-high-order-adapter-validation-attempt01': 'P2_wave_source_force_replay',
        'annular-high-order-live-primary-attempt01': "bad operand type for abs(): 'list'",
        'annular-high-order-live-reference-attempt01': "bad operand type for abs(): 'list'",
    }
    names = list(failures) + ['annular-high-order-adapter-validation-attempt02',
        'annular-high-order-repair-preparation-attempt01', 'annular-high-order-live-primary-attempt02',
        'annular-high-order-live-reference-attempt02', 'annular-high-order-live-analysis-attempt01',
        'annular-high-order-time-jet-attempt01', 'annular-source-split-septic-algebra-attempt01',
        'annular-high-order-source-hinge-separation-attempt01']
    reports = {}
    for name in names:
        path = directory / name / 'status.json'
        report = json.loads(path.read_text())
        reports[name] = report
        failed = [row['name'] for row in report['checks'] if not row['passed']]
        if name in failures:
            if report['state'] != 'failed' or failures[name] not in report['error']:
                raise RuntimeError('Unexpected retained failure ' + name)
            expected = ['P2_wave_source_force_replay'] if 'validation' in name else []
            if failed != expected:
                raise RuntimeError('Changed failed original ' + name)
        elif report['state'] != 'complete' or not report['checks'] or failed:
            raise RuntimeError('Incomplete authority ' + name)
        verify(path.relative_to(root))
        for category in ['inputs', 'outputs']:
            for relative, expected in report[category].items():
                verify(relative, expected)
        for member in path.parent.iterdir():
            if member.is_file():
                verify(member.relative_to(root))
        authorities[name] = dict(state=report['state'], checks=len(report['checks']),
            passed_checks=sum(row['passed'] for row in report['checks']))
    scripts = ['annular_high_order_native_20261003.py', 'annular_high_order_native_v2_20261003.py',
        'validate_annular_high_order_20261003.py', 'validate_annular_high_order_v2_20261003.py',
        'prepare_annular_high_order_repair_20261003.py', 'annular_high_order_coupled_20261003.py',
        'annular_high_order_coupled_v2_20261003.py', 'solve_annular_high_order_repair_20261003.py',
        'solve_annular_high_order_repair_v2_20261003.py', 'analyze_annular_high_order_repair_20261003.py',
        'probe_annular_high_order_time_jet_20261003.py', 'derive_annular_source_split_septic_20261003.py',
        'seal_annular_high_order_repair_20261003.py', 'separate_annular_high_order_source_hinge_20261003.py',
        'seal_annular_high_order_repair_v2_20261003.py']
    for name in scripts:
        path = root / 'scripts' / name
        compile(path.read_text(), str(path), 'exec')
        verify(path.relative_to(root))
    citations = []
    for name in ['DERIVATION-20261003-live-higher-order-curvature-repair.md',
        'DERIVATION-20261003-explicit-third-jet-preservation-update.md',
        'DERIVATION-20261003-source-split-septic-construction.md',
        'RESULTS-20261003-live-higher-order-curvature-repair.md',
        'RESULTS-20261003-source-hinge-separation-addendum.md']:
        verify(name)
        for relative in re.findall(r'\x60([^\x60]+\.(?:md|py|json|npz|csv))\x60', (root / name).read_text()):
            verify(relative)
            citations.append(relative)
    csv_count = 0
    for path in (directory / 'annular-high-order-live-analysis-attempt01').glob('*.csv'):
        with path.open(encoding='utf-8', newline='') as stream:
            rows = list(csv.DictReader(stream))
        if any(None in row or any(value is None for value in row.values()) or row['valid_for_claim'] != 'False' for row in rows):
            raise RuntimeError('Malformed CSV ' + str(path))
        csv_count += len(rows)
    if csv_count != 4:
        raise RuntimeError('Unexpected CSV row count')
    jet = reports['annular-high-order-time-jet-attempt01']
    from fractions import Fraction
    live = reports['annular-high-order-live-primary-attempt02']
    mesh = json.loads((root / live['mesh_path']).read_text())
    support = list(map(Fraction, mesh['gram_support']))
    anchor = Fraction(mesh['anchor'])
    source_interval = sum(point < anchor for point in support) - 1
    source_adjacent_columns = [source_interval - 1, source_interval]
    witness_adjacent = {name: witness['column'] in source_adjacent_columns
        for name, witness in jet['witnesses'].items() if name in ['jump', 'point']}
    data = []
    for row in jet['probes']:
        with np.load(root / row['path'], allow_pickle=False) as archive:
            arrays = {name: archive[name] for name in archive.files}
        if not np.all(np.isfinite(arrays['shape'])) or not np.all(np.isfinite(arrays['moving_jump'])):
            raise RuntimeError('Nonfinite jet')
        data.append(arrays)
    for row in data[1:]:
        amount = float(row['amount'])
        expected = (row['shape'] - data[0]['shape']) / amount - amount * row['acceleration_form']
        if not np.array_equal(expected, row['corrected']):
            raise RuntimeError('Time-jet correction not reproduced')
        expected = (row['moving_jump'] - data[0]['moving_jump']) / amount
        if not np.array_equal(expected, row['moving_jump_second']):
            raise RuntimeError('Moving-jump second jet not reproduced')
    for name, field in [('shape', 'corrected'), ('jump', 'moving_jump_second'), ('point', 'point_second')]:
        coarse = (4 * data[2][field] - data[1][field]) / 3
        fine = (4 * data[3][field] - data[2][field]) / 3
        witness = jet['witnesses'][name]
        if float(np.max(abs(fine))) != witness['maximum'] or float(np.max(abs(fine - coarse))) != witness['Richardson_difference']:
            raise RuntimeError('Richardson witness changed')
    separation = reports['annular-high-order-source-hinge-separation-attempt01']
    separated = []
    for number in range(4):
        path = directory / 'annular-high-order-source-hinge-separation-attempt01' / ('jet' + str(number) + '-separated.npz')
        with np.load(path, allow_pickle=False) as archive:
            arrays = {name: archive[name] for name in archive.files}
        scale = max(np.max(abs(arrays['full'])), np.max(abs(arrays['ordinary'])), np.max(abs(arrays['hinge'])), 1e-50)
        if np.max(abs(arrays['full'] - arrays['ordinary'] - arrays['hinge'])) / scale >= 2e-12:
            raise RuntimeError('Source-hinge chain rule replay failed')
        separated.append(arrays)
    for name, witness in separation['witnesses'].items():
        estimates = [(row[name] - separated[0][name]) / float(row['amount']) for row in separated[1:]]
        coarse = (4 * estimates[1] - estimates[0]) / 3
        fine = (4 * estimates[2] - estimates[1]) / 3
        if float(np.max(abs(fine))) != witness['maximum'] or float(np.max(abs(fine - coarse))) != witness['Richardson_difference']:
            raise RuntimeError('Separated witness replay failed')
    source_estimates = [(row['source_covector'] - separated[0]['source_covector']) / float(row['amount']) for row in separated[1:]]
    source_coarse = (4 * source_estimates[1] - source_estimates[0]) / 3
    source_fine = (4 * source_estimates[2] - source_estimates[1]) / 3
    source_index = int(np.argmax(abs(source_fine)))
    source_witness = dict(initial_maximum=float(np.max(abs(separated[0]['source_covector']))),
        second_maximum=float(np.max(abs(source_fine))), label=jet['labels'][source_index],
        signed=float(source_fine[source_index]), Richardson_difference=float(np.max(abs(source_fine - source_coarse))))
    start = datetime(2026, 10, 2, 23, 3, 47, tzinfo=timezone.utc).timestamp()
    protected = root.parent / 'formalization-workbench'
    changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= start]
    bytecode = list((root / 'scripts').rglob('__pycache__'))
    if mismatches or changed or bytecode:
        raise RuntimeError(dict(mismatches=mismatches, protected_changes=changed, bytecode=list(map(str, bytecode))))
    analysis = reports['annular-high-order-live-analysis-attempt01']
    result = dict(state='complete', sealed_at=datetime.now(timezone.utc).isoformat(), hashes=hashes, mismatches=mismatches,
        unique_files_rehashed=len(hashes), authorities=authorities, scripts_compiled=scripts, csv_rows_parsed=csv_count,
        cited_local_paths_validated=sorted(set(citations)), live_results=analysis['summary'],
        live_initial_candidate=analysis['live_initial_candidate'], time_jet_witnesses=jet['witnesses'],
        source_adjacent_native_interior_columns=source_adjacent_columns,
        moving_witness_adjacent_to_source=witness_adjacent,
        time_jet_algebra_independently_replayed=True, explicit_third_jet_update_derived=True,
        source_hinge_chain_rule_independently_replayed=True, source_hinge_separated_witnesses=separation['witnesses'],
        source_slope_covector_second_jet=source_witness,
        exact_source_split_septic_endpoint_map_derived=True,
        third_jet_lift_constructed_in_live_state=False, spatial_refinement_of_new_state=False,
        physical_trajectory_computed=False, continuous_material_bound_proven=False, valid_for_physics_claim=False,
        retained_failure_reason='Adapter used rounded cell widths and polynomial gradients; daughter retains exact rational widths/Decimal derivatives. First live runners saved the low-order arrays before a list/abs reporting error; daughter reruns the same equations. Original failures are retained, not promoted.',
        protected_workbench_changed_since_turn_start=0, bytecode_cache_present=False, pending={},
        current_resume_excluded=True, github_action=False, subagents_used=False)
    with target.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(state='complete', files=len(hashes), mismatches=len(mismatches), scripts=len(scripts),
        csv_rows=csv_count, passed_checks=sum(row['passed_checks'] for row in authorities.values()), protected_changes=0)), flush=True)


if __name__ == '__main__':
    main()
