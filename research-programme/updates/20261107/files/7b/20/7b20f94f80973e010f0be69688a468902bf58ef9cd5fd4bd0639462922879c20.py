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
    kernel.SetPriorityClass.argtypes = [ctypes.c_void_p, ctypes.c_uint]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 1 << 4) or not kernel.SetPriorityClass(kernel.GetCurrentProcess(), 0x4000):
        raise OSError('Resource cap failed')
    root = Path(__file__).resolve().parents[1]
    directory = root / 'source-intake/navier-stokes/20260914'
    target = directory / 'annular-septic-coupled-response-integrity-20261003.json'
    if target.exists():
        raise FileExistsError(target)
    hashes, mismatches, authorities, reports = {}, [], {}, {}
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
    parent_path = directory / 'annular-high-order-source-separation-integrity-20261003.json'
    parent = json.loads(parent_path.read_text())
    if parent['state'] != 'complete' or parent['mismatches']:
        raise RuntimeError('Incomplete parent')
    verify(parent_path.relative_to(root))
    for relative, expected in parent['hashes'].items():
        verify(relative, expected)
    failures = {'annular-septic-source-feedback-attempt01': 'decimal.InvalidOperation',
        'annular-septic-feedback-validation-attempt01': 'independent_source_cross_and_inertia_factors'}
    names = ['annular-septic-response-construction-attempt01', 'annular-septic-live-primary-attempt01',
        'annular-septic-live-reference-attempt01', 'annular-septic-live-analysis-attempt01', 'annular-septic-time-response-attempt01',
        'annular-septic-source-feedback-attempt01', 'annular-septic-source-feedback-attempt02',
        'annular-septic-feedback-validation-attempt01', 'annular-septic-feedback-validation-attempt02',
        'annular-septic-source-corrected-live-primary-attempt01', 'annular-septic-source-corrected-live-reference-attempt01',
        'annular-septic-source-corrected-analysis-attempt01', 'annular-septic-source-corrected-time-response-attempt01',
        'annular-zero-load-third-jet-law-attempt01']
    for name in names:
        path = directory / name / 'status.json'
        report = json.loads(path.read_text())
        if name in failures:
            if report['state'] != 'failed' or failures[name] not in report.get('traceback', ''):
                raise RuntimeError('Changed retained failure ' + name)
        elif report['state'] != 'complete' or not report['checks'] or not all(row['passed'] for row in report['checks']):
            raise RuntimeError('Incomplete authority ' + name)
        reports[name] = report
        verify(path.relative_to(root))
        for category in ['inputs', 'outputs']:
            for relative, expected in report[category].items():
                verify(relative, expected)
        for member in path.parent.iterdir():
            if member.is_file():
                verify(member.relative_to(root))
        authorities[name] = dict(state=report['state'], checks=len(report['checks']), passed_checks=sum(row['passed'] for row in report['checks']))
    scripts = ['construct_annular_septic_response_20261003.py', 'solve_annular_septic_response_20261003.py',
        'probe_annular_septic_time_response_20261003.py', 'analyze_annular_septic_response_20261003.py',
        'seal_annular_septic_response_20261003.py', 'correct_annular_septic_source_feedback_20261003.py',
        'correct_annular_septic_source_feedback_v2_20261003.py', 'validate_annular_septic_feedback_20261003.py',
        'validate_annular_septic_feedback_v2_20261003.py', 'solve_annular_septic_source_corrected_20261003.py',
        'probe_annular_septic_source_corrected_20261003.py', 'analyze_annular_septic_source_corrected_20261003.py',
        'derive_annular_zero_load_third_jet_20261003.py']
    for name in scripts:
        path = root / 'scripts' / name
        compile(path.read_text(), str(path), 'exec')
        verify(path.relative_to(root))
    citations = []
    for name in ['DERIVATION-20261003-septic-coupled-response.md', 'DERIVATION-20261003-source-Hessian-feedback-correction.md',
            'RESULTS-20261003-septic-coupled-response.md']:
        verify(name)
        for relative in re.findall(r'\x60([^\x60]+\.(?:md|py|json|npz|csv))\x60', (root / name).read_text()):
            verify(relative)
            citations.append(relative)
    csv_count = 0
    csv_paths = list((directory / 'annular-septic-live-analysis-attempt01').glob('*.csv')) + list((directory / 'annular-septic-source-corrected-analysis-attempt01').glob('*.csv'))
    for path in csv_paths:
        with path.open(encoding='utf-8', newline='') as stream:
            rows = list(csv.DictReader(stream))
        if any(None in row or any(value is None for value in row.values()) or row['valid_for_claim'] != 'False' for row in rows):
            raise RuntimeError('Malformed CSV ' + str(path))
        csv_count += len(rows)
    if csv_count != 8:
        raise RuntimeError('Unexpected CSV row count')
    for label in ['annular-septic-time-response-attempt01', 'annular-septic-source-corrected-time-response-attempt01']:
        jet = reports[label]
        arrays = []
        for row in jet['probes']:
            with np.load(root / row['path'], allow_pickle=False) as archive:
                arrays.append({name: archive[name] for name in jet['witnesses']})
        for name, witness in jet['witnesses'].items():
            derivatives = [(row[name] - arrays[0][name]) / amount for row, amount in zip(arrays[1:], jet['amounts'])]
            coarse, fine = (4 * derivatives[1] - derivatives[0]) / 3, (4 * derivatives[2] - derivatives[1]) / 3
            if float(np.max(abs(fine))) != witness['maximum'] or float(np.max(abs(fine - coarse))) != witness['Richardson_difference']:
                raise RuntimeError('Time-response replay failed ' + name)
        for index, row in enumerate(arrays):
            error = np.max(abs(row['shape'] - row['ordinary_shape'] - row['hinge_shape']))
            if error > 2e-12 * max(np.max(abs(row['shape'])), 1e-50):
                raise RuntimeError('Separated shape replay failed ' + str(index))
    start = datetime(2026, 10, 3, 0, 7, 25, tzinfo=timezone.utc).timestamp()
    protected = root.parent / 'formalization-workbench'
    changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= start]
    bytecode = list((root / 'scripts').rglob('__pycache__'))
    if mismatches or changed or bytecode:
        raise RuntimeError(dict(mismatches=mismatches, protected_changes=changed, bytecode=list(map(str, bytecode))))
    analysis = reports['annular-septic-source-corrected-analysis-attempt01']
    validation = reports['annular-septic-feedback-validation-attempt02']
    result = dict(state='complete', sealed_at=datetime.now(timezone.utc).isoformat(), hashes=hashes, mismatches=mismatches,
        unique_files_rehashed=len(hashes), authorities=authorities, scripts_compiled=scripts, csv_rows_parsed=csv_count,
        cited_local_paths_validated=sorted(set(citations)), live_results=analysis['summary'],
        live_initial_candidate=analysis['live_initial_candidate'], time_jet_witnesses=jet['witnesses'],
        P7_over_P6=jet['P7_over_P6'], all_three_improved=jet['all_three_improved'],
        first_P7_response=reports['annular-septic-time-response-attempt01']['witnesses'],
        source_correction_condition=reports['annular-septic-source-feedback-attempt02']['response_condition'],
        full_force_Hessian_tangent_error=validation['force_Hessian_tangent_error'],
        original_strict_source_relative_validation_passed=validation['original_source_relative_gate_passed'],
        source_tangent_absolute_error=validation['source_absolute_error'],
        uncancelled_source_roundoff_diagnostic=validation['source_roundoff_budget'],
        numerical_roundoff_diagnostic_is_not_interval_proof=True, retained_failures=failures,
        zero_load_third_jump_law_derived=True, zero_load_core_repair_constructed=False,
        source_hinge_and_time_jet_algebra_replayed=True, third_jet_update_constructed_and_solved=True,
        spatial_refinement_of_new_state=False, physical_trajectory_computed=False,
        continuous_material_bound_proven=False, valid_for_physics_claim=False,
        protected_workbench_changed_since_turn_start=0, bytecode_cache_present=False, pending={},
        current_resume_excluded=True, github_action=False, subagents_used=False)
    with target.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(state='complete', files=len(hashes), mismatches=len(mismatches), scripts=len(scripts),
        csv_rows=csv_count, passed_checks=sum(row['passed_checks'] for row in authorities.values()), protected_changes=0)), flush=True)


if __name__ == '__main__':
    main()
