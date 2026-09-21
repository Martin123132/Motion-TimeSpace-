from derive_annular_source_gravity_20260914 import EvidenceRun
from datetime import datetime, timezone
from pathlib import Path
import csv
import hashlib
import json
import math
import re
import traceback


def main():
    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    prefix = 'annular-candidate-full-canonical-inverse'
    destination = intake/(prefix+'-final-integrity.json')
    snapshot = intake/(prefix+'-resume-snapshot.md')
    executed = intake/(prefix+'-executed-sealer.py')
    specifications = [('cases', 'cases', 15), ('preconditioners', 'preconditioners', 6),
        ('controls', 'controls', 6), ('quadrature-roundtrips', 'refinement', 3),
        ('iterations', 'iterations', None)]
    tables = [intake/(prefix+'-'+label+'.csv') for label, unused, unused_count in specifications]
    if any(path.exists() for path in [destination, snapshot, executed]+tables):
        raise FileExistsError('Immutable seal destination already exists.')
    report = dict(state='running', inputs={}, outputs={}, checks=[], github_action=False,
        subagents_used=False, candidate_only=True, polar_zero_shift_only=True,
        fixed_coordinates_only=True, original_live_action_unchanged=True, no_new_evolution=True,
        new_coupled_evolution=False, full_GR_limit_proven=False, valid_for_physics_claim=False,
        global_canonical_inverse_proven=False, all_mode_reduced_inertia_positive_proven=False,
        modes_deleted=False, general_nonzero_shift_or_temporal_current_derived=False,
        physical_force_mismatch_fixed=False, spatial_convergence_proven=False,
        full_live_P2_force_convergence_proven=False,
        protected_scan_scope='mtime since2026-09-20T22:03:46Z; not a pre-turn whole-tree hash baseline')
    cache = {}

    def digest(path):
        path = path.resolve()
        if path not in cache:
            hasher = hashlib.sha256()
            with path.open('rb') as stream:
                while chunk := stream.read(1024*1024):
                    hasher.update(chunk)
            cache[path] = hasher.hexdigest()
        return cache[path]

    def own(path, category='inputs'):
        report[category][str(path.resolve().relative_to(root))] = digest(path)

    def save():
        destination.write_text(json.dumps(report, indent=2, allow_nan=False)+'\n', encoding='utf-8')

    def check(name, passed, detail=None):
        report['checks'].append(dict(name=name, passed=bool(passed), detail=detail))
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    def inherit(path):
        data = json.loads(path.read_text())
        for category in ['inputs', 'outputs']:
            for name, expected in data[category].items():
                source = (root/name).resolve()
                key = str(source.relative_to(root))
                if not source.is_file() or digest(source) != expected:
                    raise RuntimeError('Changed sealed input: '+name)
                if key in report['inputs'] and report['inputs'][key] != expected:
                    raise RuntimeError('Conflicting sealed input: '+name)
                report['inputs'][key] = expected
        own(path)
        return data

    save()
    try:
        previous = inherit(intake/'annular-candidate-canonical-response-final-integrity.json')
        check('preceding_momentum_evidence_unchanged', previous['state'] == 'complete'
            and all(row['passed'] for row in previous['checks']) and previous['candidate_momenta_computed'])
        source = intake/'annular-candidate-full-canonical-inverse-attempt01/status.json'
        status = inherit(source)
        check('full_inverse_run_complete_all_checks_pass', status['state'] == 'complete'
            and all(row['passed'] for row in status['checks']))
        check('private_fixed_coordinate_nonclaim_scope', status['fixed_coordinates_only']
            and status['candidate_only'] and status['polar_zero_shift_only'] and status['no_new_evolution']
            and status['original_live_action_unchanged'] and not status['new_coupled_evolution']
            and not status['github_action'] and not status['subagents_used']
            and not status['full_GR_limit_proven'] and not status['valid_for_physics_claim']
            and not status['physical_force_mismatch_fixed'] and not status['spatial_convergence_proven']
            and not status['full_live_P2_force_convergence_proven']
            and not status['general_nonzero_shift_or_temporal_current_derived'])
        check('numerical_full_inverse_not_global_theorem', status['full_canonical_inverse_qualified']
            and status['full_component_inverse_numerically_qualified'] and status['perturbed_momentum_targets_solved']
            and not status['global_canonical_inverse_proven']
            and not status['all_mode_reduced_inertia_positive_proven'] and not status['modes_deleted'])
        check('targets_owned_by_weighted_action', status['target_momenta_action_owned']
            and not status['original_unweighted_momenta_reused'] and status['initial_physical_time'] == 0.)
        expected = {(branch, extension, degree, seed)
            for branch, extension in [('reference', 'reference'), ('MTS', 'primary'), ('MTS', 'alternative')]
            for degree in [18, 22]
            for seed in (['roundtrip_1', 'roundtrip_2']+(['shifted_target'] if degree == 22 else []))}
        check('all_branches_both_roundtrips_and_shifted_targets', len(status['cases']) == 15
            and {(row['branch'], row['extension'], row['radial_degree'], row['seed'])
                for row in status['cases']} == expected)
        check('all_component_momentum_radial_and_chart_gates', all(row['full_components'] == 16425
            and row['all_components_solved'] and row['relative_momentum_residual'] < 2e-11
            and row['maximum_correction'] < 2e-10 and row['radial_residual'] < 2e-12
            and row['minimum_F'] > 0 and row['maximum_speed_ratio'] < 1
            for row in status['cases']))
        check('all_roundtrip_velocities_recovered', sum(row['roundtrip'] for row in status['cases']) == 12
            and all(row['maximum_velocity_difference_from_known'] < 2e-9
                for row in status['cases'] if row['roundtrip']))
        check('new_targets_give_nontrivial_new_velocities', all(row['maximum_velocity_difference_from_known'] > 1e-6
            for row in status['cases'] if not row['roundtrip']))
        check('complete_preconditioner_and_no_deleted_directions', len(status['preconditioners']) == 6
            and all(row['full_components'] == 16425 and row['field_components'] == 16410
                and row['source_components'] == 15 and row['field_half_bandwidth'] == 44
                and row['minimum_diagonal'] > 0 and row['minimum_scaled_field_cholesky_pivot'] > 0
                and row['minimum_scaled_source_schur_eigenvalue'] > 0 and row['symmetry_error'] < 2e-12
                and row['constructed_from_perturbed_not_known_solution']
                and row['cache_bytes'] <= status['cache_budget_bytes'] for row in status['preconditioners']))
        check('condition_estimates_explicitly_not_certified_bounds', all(row['condition_estimates_not_upper_bounds']
            and math.isfinite(row['raw_one_norm_condition_estimate'])
            and math.isfinite(row['scaled_one_norm_condition_estimate'])
            and row['raw_one_norm_condition_estimate'] >= 1 and row['scaled_one_norm_condition_estimate'] >= 1
            for row in status['preconditioners']))
        check('independent_full_linear_controls', len(status['controls']) == 6
            and all(row['preconditioner_recovery_relative_error'] < 2e-9
                and row['preconditioner_residual_relative_error'] < 2e-11
                and row['fixed_momentum_Jacobian_relative_error'] < 2e-10 for row in status['controls']))
        check('roundtrip_quadrature_consistency_not_physical_convergence', len(status['refinement']) == 3
            and all(row['maximum_roundtrip_velocity_difference'] < 2e-9
                and row['targets_use_their_own_quadrature'] and row['not_physical_spatial_or_evolution_convergence']
                for row in status['refinement']))
        histories = {}
        for row in status['iterations']:
            histories.setdefault(row['case'], []).append(row)
        check('all_nonlinear_histories_saved_and_descending', len(histories) == 15
            and all(rows[0]['maximum_preconditioned_correction'] > 1e-4
                and all(after['momentum_relative_residual'] < before['momentum_relative_residual']
                    for before, after in zip(rows, rows[1:])) for rows in histories.values()))
        row_counts = []
        for path, (label, key, expected_count) in zip(tables, specifications):
            rows = [dict(**row, source_path=str(source.relative_to(root))) for row in status[key]]
            fields = list(dict.fromkeys(field for row in rows for field in row))
            with path.open('w', encoding='utf-8', newline='') as stream:
                writer = csv.DictWriter(stream, fieldnames=fields)
                writer.writeheader()
                writer.writerows(rows)
            with path.open(encoding='utf-8', newline='') as stream:
                parsed = list(csv.DictReader(stream))
            check(label+'_sourced_nonclaim_rows_parse', len(parsed) == len(rows)
                and (expected_count is None or len(parsed) == expected_count)
                and all(None not in row and None not in row.values() and row['valid_for_claim'] == 'False'
                    and (root/row['source_path']).is_file() for row in parsed))
            own(path, 'outputs')
            row_counts.append(len(parsed))
        note = root/'DERIVATION-20260920-full-weighted-canonical-inverse.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json|csv|npz))`', content)
        check('report_complete_and_cited_sources_exist', 'RESULTS_PENDING' not in content and bool(cited)
            and all((root/name).is_file() for name in cited), cited)
        for name in cited:
            own(root/name)
        own(note)
        for name in ['annular_candidate_full_inverse_20260920.py',
                'derive_annular_candidate_full_inverse_20260920.py',
                'seal_annular_candidate_full_inverse_20260920.py']:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('new_scripts_compile_without_bytecode', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026, 9, 20, 22, 3, 46, tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*')
            if path.is_file() and path.stat().st_mtime >= start]
        check('protected_workbench_mtime_unchanged', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        own(executed, 'outputs')
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(),
            implementation_checks=len(status['checks']), total_failed_attempts_preserved=previous['total_failed_attempts_preserved'],
            new_failures=[], distinct_files_rehashed=len(cache), table_rows=row_counts,
            full_canonical_inverse_qualified=True, full_component_inverse_numerically_qualified=True,
            canonical_inverse_scope=status['canonical_inverse_scope'], perturbed_momentum_targets_solved=True,
            rejected_trial_count=len(status['rejected_trials']),
            next_target='Derive and independently qualify matching continuous-material coordinate covectors from the same candidate action, including transport, Gram/source terms and sampled metric gradients. Combine with the full weighted inverse for a very short canonical trajectory only after force qualification. Equal reference/MTS step controls; no general-shift/current, force-convergence or full-GR claim from fixed-coordinate inverse success.')
        save()
        print(json.dumps(dict(state='complete', checks=report['implementation_checks'], integrity_checks=len(report['checks']),
            files_rehashed=len(cache), table_rows=row_counts, failures_preserved=report['total_failed_attempts_preserved'])), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()

