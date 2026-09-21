from derive_annular_source_gravity_20260914 import EvidenceRun
from datetime import datetime, timezone
from pathlib import Path
import csv
import hashlib
import json
import re
import traceback


def main():
    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    prefix = 'annular-candidate-radial-metric'
    destination = intake/(prefix+'-final-integrity.json')
    executed = intake/(prefix+'-executed-sealer.py')
    snapshot = intake/(prefix+'-resume-snapshot.md')
    specifications = [('local-jacobians', 0, 'jacobians', 3),
        ('manufactured-pushforwards', 0, 'pushforwards', 12),
        ('initial-metrics', 1, 'cases', 6), ('radial-label-refinement', 1, 'refinement', 3),
        ('factor-controls', 1, 'factor_checks', 2), ('extension-differences', 1, 'extension_differences', 2),
        ('new-failures', 2, 'failures', 3)]
    tables = [intake/(prefix+'-'+label+'.csv') for label, unused, unused_key, unused_count in specifications]
    if any(path.exists() for path in [destination, executed, snapshot]+tables):
        raise FileExistsError('Immutable seal destination already exists.')
    report = dict(state='running', checks=[], inputs={}, outputs={},
        github_action=False, subagents_used=False, candidate_only=True, polar_zero_shift_only=True,
        original_live_action_unchanged=True, no_new_evolution=True,
        self_consistent_candidate_metric_solved=False, candidate_initial_metric_qualified=False,
        fixed_physical_fields_and_velocities=True, old_canonical_momenta_preserved=False,
        new_candidate_canonical_momenta_computed=False, metric_eliminated_inertia_computed=False,
        physical_force_mismatch_fixed=False, full_live_P2_force_convergence_proven=False,
        spatial_convergence_proven=False, full_GR_limit_proven=False, valid_for_physics_claim=False,
        certified_continuous_time_bound=False, general_nonzero_shift_or_temporal_current_derived=False,
        nonuniform_parent_uniqueness_proven=False,
        protected_scan_scope='mtime since2026-09-20T21:09:43Z; not a pre-turn whole-tree hash baseline')
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
                    raise RuntimeError('Changed sealed source: '+name)
                if key in report['inputs'] and report['inputs'][key] != expected:
                    raise RuntimeError('Conflicting sealed source: '+name)
                report['inputs'][key] = expected
        own(path)
        return data

    save()
    try:
        previous = inherit(intake/'annular-joint-candidate-refinement-final-integrity.json')
        check('preceding_seal_unchanged', previous['state'] == 'complete'
            and all(row['passed'] for row in previous['checks'])
            and previous['joint_refinement_assembly_qualified'] and previous['refined_pilot_arithmetic_qualified']
            and not previous['physical_force_mismatch_fixed'] and not previous['spatial_convergence_proven'])
        names = ['annular-candidate-radial-derivation-attempt03', 'annular-candidate-initial-metric-attempt02']
        statuses = [inherit(intake/name/'status.json') for name in names]
        for name, status in zip(names, statuses):
            check(name+'_complete_and_scope_retained', status['state'] == 'complete'
                and all(row['passed'] for row in status['checks']) and status['candidate_only']
                and status['polar_zero_shift_only'] and status['original_live_action_unchanged']
                and status['no_new_evolution'] and not status['full_GR_limit_proven']
                and not status['valid_for_physics_claim'] and not status['physical_force_mismatch_fixed']
                and not status['full_live_P2_force_convergence_proven'] and not status['certified_continuous_time_bound']
                and not status['general_nonzero_shift_or_temporal_current_derived']
                and not status['github_action'] and not status['subagents_used'])
        derivation, metric = statuses
        check('radial_action_boundary_and_pushforward_derived', derivation['radial_constraint_derived']
            and derivation['radial_jacobian_qualified'] and derivation['boundary_action_retained']
            and derivation['collar_pushforward_qualified'])
        check('local_Jacobian_and_original_rhs_controls', len(derivation['jacobians']) == 3
            and all(row['symbolic_max_error'] < 3e-12 and row['original_rhs_max_error'] < 3e-14
                for row in derivation['jacobians']))
        check('manufactured_pushforward_controls_not_parent_data', len(derivation['pushforwards']) == 12
            and all(row['relative_error'] < 1e-10 and row['manufactured_control_not_parent_data']
                for row in derivation['pushforwards']))
        check('coherent_initial_slice_not_previous_frozen_source', metric['initial_physical_time'] == 0.
            and metric['previous_frozen_metric_physical_time'] == 4e-5
            and not metric['same_source_state_as_previous_frozen_pilot'])
        check('candidate_initial_metric_solved_velocity_owned_only', metric['self_consistent_candidate_metric_solved']
            and metric['candidate_initial_metric_qualified'] and metric['fixed_physical_fields_and_velocities']
            and not metric['old_canonical_momenta_preserved'] and not metric['new_candidate_canonical_momenta_computed']
            and metric['no_new_canonical_evolution'] and not metric['spatial_convergence_proven'])
        expected = {(branch, extension, degree, order)
            for branch, extension in [('reference', 'reference'), ('MTS', 'primary'), ('MTS', 'alternative')]
            for degree, order in [(18, 20), (22, 28)]}
        check('all_branches_and_settings_present', len(metric['cases']) == 6
            and {(row['branch'], row['extension'], row['radial_degree'], row['label_order'])
                for row in metric['cases']} == expected)
        check('all_radial_and_global_Jacobian_gates_retained', all(row['field_dofs'] == 1094
            and row['radial_segments'] == 2182 and row['radial_nodes'] == 2182*(row['radial_degree']+1)
            and row['integral_residual'] < 2e-12 and row['global_Jacobian_error'] < 3e-11
            and max(row['off_grid_mass_residual'], row['off_grid_log_lapse_residual']) < 1e-8
            and row['boundary_error'] < 2e-12 and row['minimum_F'] > 0
            and row['maximum_source_speed_ratio'] < 1 and row['velocity_owned_not_old_canonical_state']
            for row in metric['cases']))
        check('reference_original_metric_recovered', all(max(row['maximum_mass_change_from_old'],
            row['maximum_log_lapse_change_from_old']) < 2e-9 for row in metric['cases'] if row['branch'] == 'reference'))
        check('joint_radial_label_not_field_force_convergence', len(metric['refinement']) == 3
            and all(max(row['maximum_mass_change'], row['maximum_log_lapse_change']) < row['numerical_gate']
                and row['not_a_spatial_force_convergence_gate'] for row in metric['refinement']))
        check('factor_preparation_and_label_controls', len(metric['factor_checks']) == 2
            and all(row['center_factor_error'] == 0 and row['label_factor_relative_error'] < 1e-11
                and row['high_precision_atom_preparation_digits'] == 64 for row in metric['factor_checks']))
        check('extension_comparison_not_uniqueness_claim', len(metric['extension_differences']) == 2
            and all(row['not_a_uniqueness_certificate'] for row in metric['extension_differences']))
        failures = [
            ('annular-candidate-radial-derivation-attempt01', 'symbolic_zero_normalization',
             'Unchanged expression proved zero by rational combination/factorization in v2/v3.'),
            ('annular-candidate-radial-derivation-attempt02', 'substitution_API_syntax',
             'Corrected dictionary substitution in v3; no equation change.'),
            ('annular-candidate-initial-metric-attempt01', 'incoherent_time_slice_input',
             'Later whole state mismatched initial scalar profile; v2 uses whole t=0 state and independent trajectory checks.')]
        failed_rows = []
        for name, classification, resolution in failures:
            source = intake/name/'status.json'
            failed = inherit(source)
            check(name+'_failed_evidence_retained', failed['state'] == 'failed' and bool(failed.get('error'))
                and not failed['valid_for_physics_claim'])
            failed_rows.append(dict(attempt=name, classification=classification, error=failed['error'],
                resolution=resolution, promoted=False, source_path=str(source.relative_to(root)), valid_for_claim=False))
        sources = statuses+[dict(failures=failed_rows)]
        row_counts = []
        for path, (label, status_index, key, expected_count) in zip(tables, specifications):
            rows = []
            for raw in sources[status_index][key]:
                row = dict(raw)
                if status_index < 2:
                    row['source_path'] = str((intake/names[status_index]/'status.json').relative_to(root))
                rows.append(row)
            fields = list(dict.fromkeys(field for row in rows for field in row))
            with path.open('w', encoding='utf-8', newline='') as stream:
                writer = csv.DictWriter(stream, fieldnames=fields)
                writer.writeheader()
                writer.writerows(rows)
            with path.open(encoding='utf-8', newline='') as stream:
                parsed = list(csv.DictReader(stream))
            check(label+'_sourced_nonclaim_rows_parse', len(parsed) == len(rows) == expected_count
                and all(None not in row and None not in row.values() and row['valid_for_claim'] == 'False'
                    and (root/row['source_path']).is_file() for row in parsed))
            row_counts.append(len(parsed))
            own(path, 'outputs')
        note = root/'DERIVATION-20260920-candidate-radial-constraint-and-initial-metric.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json|csv|npz))`', content)
        check('report_complete_and_cited_sources_exist', 'RESULTS_PENDING' not in content
            and len(cited) >= 15 and all((root/name).is_file() for name in cited), cited)
        for name in cited:
            own(root/name)
        own(note)
        for name in ['annular_candidate_radial_constraint_20260920.py',
                'derive_annular_candidate_radial_constraint_20260920.py',
                'derive_annular_candidate_radial_constraint_v2_20260920.py',
                'derive_annular_candidate_radial_constraint_v3_20260920.py',
                'solve_annular_candidate_initial_metric_20260920.py',
                'solve_annular_candidate_initial_metric_v2_20260920.py',
                'seal_annular_candidate_radial_metric_20260920.py']:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('all_new_scripts_compile_without_bytecode', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026, 9, 20, 21, 9, 43, tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*')
            if path.is_file() and path.stat().st_mtime >= start]
        check('protected_workbench_mtime_unchanged', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        own(executed, 'outputs')
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(),
            implementation_checks=sum(len(status['checks']) for status in statuses),
            implementation_check_breakdown={name:len(status['checks']) for name, status in zip(names, statuses)},
            total_failed_attempts_preserved=previous['total_failed_attempts_preserved']+len(failed_rows),
            new_failures=failed_rows, distinct_files_rehashed=len(cache), table_rows=row_counts,
            radial_constraint_derived=True, radial_jacobian_qualified=True,
            boundary_action_retained=True, collar_pushforward_qualified=True,
            self_consistent_candidate_metric_solved=True, candidate_initial_metric_qualified=True,
            initial_physical_time=0., previous_frozen_metric_physical_time=4e-5,
            same_source_state_as_previous_frozen_pilot=False,
            next_target='Compute candidate momenta on the coherent solved t=0 metric; derive and independently qualify metric-eliminated velocity response including outer clock and material weights. Test canonical inversion and reference reduction before any short coupled step. Fixed-background Schur positivity is not a live-gravity inertia theorem; general-shift/current, spatial force convergence, physical discrepancies and full GR claims remain open.')
        save()
        print(json.dumps(dict(state='complete', checks=report['implementation_checks'], integrity_checks=len(report['checks']),
            files_rehashed=len(cache), table_rows=row_counts, failures_preserved=report['total_failed_attempts_preserved'])), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()

