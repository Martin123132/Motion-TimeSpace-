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
    prefix = 'annular-candidate-canonical-response'
    destination = intake/(prefix+'-final-integrity.json')
    snapshot = intake/(prefix+'-resume-snapshot.md')
    executed = intake/(prefix+'-executed-sealer.py')
    specifications = [('cases', 'cases', 6), ('derivatives', 'derivative_checks', 24),
        ('probe-inertia', 'inertia_entries', 96), ('quadrature-refinement', 'refinement', 3)]
    tables = [intake/(prefix+'-'+label+'.csv') for label, unused, unused_count in specifications]
    if any(path.exists() for path in [destination, snapshot, executed]+tables):
        raise FileExistsError('Immutable output already exists.')
    report = dict(state='running', checks=[], inputs={}, outputs={}, candidate_only=True,
        polar_zero_shift_only=True, github_action=False, subagents_used=False,
        original_live_action_unchanged=True, no_new_evolution=True,
        full_GR_limit_proven=False, valid_for_physics_claim=False, physical_force_mismatch_fixed=False,
        spatial_convergence_proven=False, full_live_P2_force_convergence_proven=False,
        full_canonical_inverse_qualified=False, all_mode_reduced_inertia_positive_proven=False,
        exact_finite_label_Galerkin_evolution_qualified=False,
        general_nonzero_shift_or_temporal_current_derived=False,
        protected_scan_scope='mtime since2026-09-20T21:42:14Z; not a pre-turn whole-tree hash baseline')
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
        previous = inherit(intake/'annular-candidate-radial-metric-final-integrity.json')
        check('previous_radial_metric_evidence_unchanged', previous['state'] == 'complete'
            and all(row['passed'] for row in previous['checks']) and previous['candidate_initial_metric_qualified']
            and not previous['full_GR_limit_proven'])
        source = intake/'annular-candidate-live-momenta-attempt01/status.json'
        status = inherit(source)
        check('new_run_complete_all_checks_pass', status['state'] == 'complete'
            and all(row['passed'] for row in status['checks']))
        check('scope_and_nonclaim_flags_retained', status['candidate_only'] and status['polar_zero_shift_only']
            and status['original_live_action_unchanged'] and status['no_new_evolution']
            and not status['new_coupled_evolution'] and not status['github_action'] and not status['subagents_used']
            and not status['valid_for_physics_claim'] and not status['full_GR_limit_proven']
            and not status['physical_force_mismatch_fixed'] and not status['spatial_convergence_proven']
            and not status['full_live_P2_force_convergence_proven']
            and not status['general_nonzero_shift_or_temporal_current_derived'])
        check('action_owned_momenta_and_directional_response_computed', status['candidate_momenta_computed']
            and status['continuous_material_action_momenta_computed']
            and status['directional_live_velocity_response_qualified']
            and status['stationary_action_envelope_numerically_checked'])
        check('initial_slice_velocity_ownership_preserved', status['initial_physical_time'] == 0.
            and status['self_consistent_candidate_metric_solved'] and status['fixed_physical_fields_and_velocities']
            and not status['old_canonical_momenta_preserved'])
        check('no_full_inverse_all_mode_or_evolution_claim', status['directional_response_only']
            and not status['full_canonical_inverse_qualified'] and not status['all_mode_reduced_inertia_positive_proven']
            and not status['exact_finite_label_Galerkin_evolution_qualified'])
        expected = {(branch, extension, degree, order)
            for branch, extension in [('reference', 'reference'), ('MTS', 'primary'), ('MTS', 'alternative')]
            for degree, order in [(18, 20), (22, 28)]}
        check('reference_and_both_candidates_equal_settings', len(status['cases']) == 6 and {
            (row['branch'], row['extension'], row['radial_degree'], row['label_order'])
            for row in status['cases']} == expected)
        check('full_momentum_size_and_coherent_metric', all(row['field_dofs'] == 1094
            and row['material_labels'] == 15 and row['momentum_components'] == 16425
            and row['metric_change_from_preceding'] < 2e-9 and row['integral_residual'] < 2e-12
            and row['old_momenta_not_preserved'] for row in status['cases']))
        check('directional_inertia_and_derivative_gates', all(row['directional_reciprocity_error'] < 2e-7
            and row['full_momentum_directional_relative_error'] < 2e-8
            and row['minimum_fixed_probe_eigenvalue'] > 0
            and row['four_probe_not_all_mode_certificate'] for row in status['cases']))
        check('live_probe_positivity_reported_not_promoted', all(
            row['live_probe_positive'] == (row['minimum_live_probe_eigenvalue'] > 0)
            for row in status['cases']) and not status['all_mode_reduced_inertia_positive_proven'])
        check('independent_reference_pointwise_recovery', all(row['center_pullback_change_from_old'] < 2e-9
            for row in status['cases'] if row['branch'] == 'reference'))
        check('independent_response_and_envelope_gates', len(status['derivative_checks']) == 24
            and all(row['forcing_error'] < 2e-11 and row['metric_relative_error'] < 2e-8
                and row['linear_residual'] < 2e-11 and row['fixed_action_relative_error'] < 2e-8
                and row['envelope_relative_error'] < 2e-6 for row in status['derivative_checks']))
        check('probe_matrix_entries_complete_and_nonclaim', len(status['inertia_entries']) == 96
            and all(row['four_probe_not_all_mode_certificate'] for row in status['inertia_entries']))
        check('joint_quadrature_refinement_not_evolution_convergence', len(status['refinement']) == 3
            and all(max(row['momentum_relative_change'], row['live_inertia_relative_change']) < 2e-6
                and row['not_field_spatial_or_evolution_convergence'] for row in status['refinement']))
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
            check(label+'_sourced_nonclaim_rows_parse', len(parsed) == len(rows) == expected_count
                and all(None not in row and None not in row.values() and row['valid_for_claim'] == 'False'
                    and (root/row['source_path']).is_file() for row in parsed))
            own(path, 'outputs')
            row_counts.append(len(parsed))
        note = root/'DERIVATION-20260920-candidate-canonical-momenta-and-live-response.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json|csv|npz))`', content)
        check('report_complete_all_cited_sources_exist', 'RESULTS_PENDING' not in content and bool(cited)
            and all((root/name).is_file() for name in cited), cited)
        for name in cited:
            own(root/name)
        own(note)
        for name in ['annular_candidate_canonical_response_20260920.py',
                'derive_annular_candidate_canonical_response_20260920.py',
                'seal_annular_candidate_canonical_response_20260920.py']:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('new_scripts_compile_without_bytecode', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026, 9, 20, 21, 42, 14, tzinfo=timezone.utc).timestamp()
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
            continuous_material_action_momenta_computed=True, directional_live_velocity_response_qualified=True,
            stationary_action_envelope_numerically_checked=True, candidate_momenta_computed=True,
            next_target='Build and qualify the full weighted canonical inverse with simultaneous candidate radial gravity, recovering the known initial velocities from perturbed guesses. Matrix-free response and appropriate preconditioning, no silent mode deletion or reuse of unweighted collocation momenta. Test reference and both MTS extensions before any short coupled evolution. Four-probe positivity is not all-mode reduced-inertia positivity; temporal/current, spatial force and full GR obligations remain open.')
        save()
        print(json.dumps(dict(state='complete', checks=report['implementation_checks'], integrity_checks=len(report['checks']),
            files_rehashed=len(cache), table_rows=row_counts, failures_preserved=report['total_failed_attempts_preserved'])), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()

