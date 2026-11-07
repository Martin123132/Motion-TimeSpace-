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
    target = directory / 'annular-all-native-jump-integrity-20261003.json'
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
    parent_path = directory / 'annular-septic-coupled-response-integrity-20261003.json'
    parent = json.loads(parent_path.read_text())
    if parent['state'] != 'complete' or parent['mismatches']:
        raise RuntimeError('Incomplete parent')
    verify(parent_path.relative_to(root))
    for relative, expected in parent['hashes'].items():
        verify(relative, expected)
    failures = {'annular-all-native-jump-construction-attempt01': 'outer_neighbour_initial_force_zero',
        'annular-balanced-force-primary-attempt01': 'weak_and_integrated_force_consistency',
        'annular-balanced-force-reference-attempt01': 'weak_and_integrated_force_consistency',
        'annular-product-basis-live-primary-attempt01': 'TypeError',
        'annular-product-basis-live-reference-attempt01': 'TypeError'}
    names = ['annular-all-native-jump-construction-attempt01', 'annular-all-native-jump-construction-attempt02',
        'annular-all-native-jump-live-primary-attempt01', 'annular-all-native-jump-live-reference-attempt01',
        'annular-all-native-jump-analysis-attempt01', 'annular-all-native-jump-time-response-attempt01',
        'annular-balanced-force-primary-attempt01', 'annular-balanced-force-reference-attempt01',
        'annular-force-basis-diagnostic-primary-attempt01', 'annular-force-basis-diagnostic-reference-attempt01',
        'annular-product-basis-live-primary-attempt01', 'annular-product-basis-live-reference-attempt01',
        'annular-product-basis-live-primary-attempt02', 'annular-product-basis-live-reference-attempt02',
        'annular-product-basis-product-time-response-attempt01', 'annular-product-basis-balanced-time-response-attempt01',
        'annular-product-source-feedback-attempt01',
        'annular-product-source-corrected-live-primary-attempt01', 'annular-product-source-corrected-live-reference-attempt01',
        'annular-product-source-corrected-product-time-response-attempt01', 'annular-product-source-corrected-balanced-time-response-attempt01',
        'annular-jump-projection-decomposition-attempt01']
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
    scripts = ['construct_annular_all_native_jump_20261003.py', 'construct_annular_all_native_jump_v2_20261003.py',
        'solve_annular_all_native_jump_20261003.py', 'probe_annular_all_native_jump_20261003.py',
        'analyze_annular_all_native_jump_20261003.py', 'seal_annular_all_native_jump_20261003.py',
        'annular_balanced_native_force_20261003.py', 'check_annular_balanced_force_20261003.py',
        'annular_product_basis_20261003.py', 'diagnose_annular_force_basis_20261003.py',
        'annular_product_live_20261003.py', 'solve_annular_product_basis_20261003.py', 'solve_annular_product_basis_v2_20261003.py', 'probe_annular_product_basis_20261003.py',
        'correct_annular_product_source_feedback_20261003.py', 'solve_annular_product_source_corrected_20261003.py',
        'probe_annular_product_source_corrected_20261003.py', 'analyze_annular_jump_projection_20261003.py']
    for name in scripts:
        path = root / 'scripts' / name
        compile(path.read_text(), str(path), 'exec')
        verify(path.relative_to(root))
    citations = []
    for name in ['DERIVATION-20261003-all-native-jump-response.md', 'RESULTS-20261003-all-native-jump-response.md',
            'DERIVATION-20261003-balanced-native-force-test.md', 'DERIVATION-20261003-product-basis-force-repair.md']:
        verify(name)
        for relative in re.findall(r'\x60([^\x60]+\.(?:md|py|json|npz|csv))\x60', (root / name).read_text()):
            verify(relative)
            citations.append(relative)
    csv_count = 0
    for path in (directory / 'annular-all-native-jump-analysis-attempt01').glob('*.csv'):
        with path.open(encoding='utf-8', newline='') as stream:
            rows = list(csv.DictReader(stream))
        if any(None in row or any(value is None for value in row.values()) or row['valid_for_claim'] != 'False' for row in rows):
            raise RuntimeError('Malformed CSV ' + str(path))
        csv_count += len(rows)
    if csv_count != 4:
        raise RuntimeError('Unexpected CSV row count')
    jet = reports['annular-all-native-jump-time-response-attempt01']
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
    repaired_probes = {}
    for key, report_name in [(prefix + mode, 'annular-' + prefix + mode + '-time-response-attempt01')
            for prefix in ['product-basis-', 'product-source-corrected-'] for mode in ['product', 'balanced']]:
        probe = reports[report_name]
        arrays = []
        for row in probe['probes']:
            with np.load(root / row['path'], allow_pickle=False) as archive:
                arrays.append({name: archive[name] for name in probe['witnesses']})
        for name, witness in probe['witnesses'].items():
            estimates = [(row[name]-arrays[0][name])/amount for row, amount in zip(arrays[1:], probe['amounts'])]
            coarse, fine = (4*estimates[1]-estimates[0])/3, (4*estimates[2]-estimates[1])/3
            if float(np.max(abs(fine))) != witness['maximum'] or float(np.max(abs(fine-coarse))) != witness['Richardson_difference']:
                raise RuntimeError('Product-basis time replay failed ' + key + ':' + name)
        repaired_probes[key] = dict(witnesses=probe['witnesses'], versus_previous=probe['versus_previous'],
            slope_response_strong_weak_gap=probe['slope_response_strong_weak_gap'],
            value_response_strong_weak_gap=probe['value_response_strong_weak_gap'])
    for branch in ['primary', 'reference']:
        diagnostic = reports['annular-force-basis-diagnostic-' + branch + '-attempt01']
        for row in diagnostic['results']:
            if not row['original_equivalence_gate_passed'] or any(item['product_relative'] >= 5e-13 for item in row['flat_rows']):
                raise RuntimeError('Product-basis oracle failed ' + branch)
            with np.load(root / row['path'], allow_pickle=False) as archive:
                for first, second in [('old', 'balanced'), ('product', 'balanced'), ('old', 'product')]:
                    actual = float(np.max(abs(archive[first]-archive[second])))
                    if actual != row[first+'_'+second]['absolute']:
                        raise RuntimeError('Force diagnostic replay failed ' + branch)
        live = reports['annular-product-basis-live-' + branch + '-attempt02']
        if any(row['force_form_relative_difference'] >= 2e-10 for row in live['balanced_results']):
            raise RuntimeError('Full force equivalence failed ' + branch)
        corrected = reports['annular-product-source-corrected-live-' + branch + '-attempt01']
        if any(row['force_form_relative_difference'] >= 2e-10 for row in corrected['balanced_results']):
            raise RuntimeError('Corrected full force equivalence failed ' + branch)
        if branch == 'primary' and not all(row['initial_candidate'] for row in corrected['results'] + corrected['balanced_results']):
            raise RuntimeError('Corrected initial gates failed')
    feedback = reports['annular-product-source-feedback-attempt01']
    with np.load(root / feedback['initial_path'], allow_pickle=False) as archive:
        residual = archive['response_matrix'] @ archive['correction'] + archive['target']
        if float(np.max(abs(residual))) != feedback['source_residual_predicted']:
            raise RuntimeError('Coupled source response replay failed')
    decomposition = reports['annular-jump-projection-decomposition-attempt01']
    for row in decomposition['results']:
        with np.load(root / row['path'], allow_pickle=False) as archive:
            error = np.max(abs(archive['measured']-archive['weak_strong_transfer']-archive['inferred_strong']))
            if float(np.max(abs(archive['measured']))) != row['maximum_jump'] or error > 5e-15*row['maximum_jump']:
                raise RuntimeError('Weak/strong jump split failed')
    start = datetime(2026, 10, 3, 1, 8, 39, tzinfo=timezone.utc).timestamp()
    protected = root.parent / 'formalization-workbench'
    changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= start]
    bytecode = list((root / 'scripts').rglob('__pycache__'))
    if mismatches or changed or bytecode:
        raise RuntimeError(dict(mismatches=mismatches, protected_changes=changed, bytecode=list(map(str, bytecode))))
    analysis = reports['annular-all-native-jump-analysis-attempt01']
    result = dict(state='complete', sealed_at=datetime.now(timezone.utc).isoformat(), hashes=hashes, mismatches=mismatches,
        unique_files_rehashed=len(hashes), authorities=authorities, scripts_compiled=scripts, csv_rows_parsed=csv_count,
        cited_local_paths_validated=sorted(set(citations)), live_results=analysis['summary'],
        live_initial_candidate=analysis['live_initial_candidate'], time_jet_witnesses=jet['witnesses'],
        versus_previous=jet['versus_previous'], source_hinge_and_time_jet_algebra_replayed=True,
        repaired_product_basis_probes=repaired_probes, force_oracles_replayed=True,
        product_basis_live={branch:reports['annular-product-basis-live-' + branch + '-attempt02']['results'] for branch in ['primary', 'reference']},
        balanced_force_live={branch:reports['annular-product-basis-live-' + branch + '-attempt02']['balanced_results'] for branch in ['primary', 'reference']},
        corrected_product_live={branch:reports['annular-product-source-corrected-live-' + branch + '-attempt01']['results'] for branch in ['primary', 'reference']},
        corrected_balanced_live={branch:reports['annular-product-source-corrected-live-' + branch + '-attempt01']['balanced_results'] for branch in ['primary', 'reference']},
        full_coupled_source_feedback_replayed=True,
        weak_strong_jump_decomposition=decomposition['results'], weak_strong_jump_decomposition_replayed=True,
        all_native_jump_update_constructed=True, exact_inactive_zero_load_not_assumed=True,
        retained_failures=failures, spatial_refinement_of_new_state=False, physical_trajectory_computed=False,
        continuous_material_bound_proven=False, valid_for_physics_claim=False,
        protected_workbench_changed_since_turn_start=0, bytecode_cache_present=False, pending={},
        current_resume_excluded=True, github_action=False, subagents_used=False)
    with target.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(state='complete', files=len(hashes), mismatches=len(mismatches), scripts=len(scripts),
        csv_rows=csv_count, passed_checks=sum(row['passed_checks'] for row in authorities.values()), protected_changes=0)), flush=True)


if __name__ == '__main__':
    main()
