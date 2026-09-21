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
    destination = intake/'annular-exponential-transport-final-integrity.json'
    table = intake/'annular-exponential-transport-budgets.csv'
    samples_table = intake/'annular-exponential-transport-samples.csv'
    spatial_table = intake/'annular-spatial-Gram-four-way-split.csv'
    increments_table = intake/'annular-spatial-Gram-four-way-increments.csv'
    snapshot = intake/'annular-exponential-transport-resume-snapshot.md'
    executed = intake/'annular-exponential-transport-executed-sealer.py'
    if any(path.exists() for path in [destination, table, samples_table, spatial_table, increments_table, snapshot, executed]):
        raise FileExistsError('Immutable seal destination already exists.')
    report = dict(state='running', checks=[], inputs={}, outputs={}, github_action=False,
        subagents_used=False, full_GR_limit_proven=False, valid_for_physics_claim=False,
        full_live_P2_force_convergence_proven=False, no_new_trajectory_evolution=True,
        complete_nonlinear_adjoint_derived=False, certified_live_remainder_curvature_bound=False,
        nonnested_spatial_transfer_explicit=True, exact_coarse_to_fine_space_embedding_claimed=False,
        off_space_quadrature_not_a_continuous_integral_certificate=True,
        isolated_spatial_truncation_error_certified=False,
        protected_scan_scope='mtime since2026-09-19T11:24:59Z; not a pre-turn full hash baseline')
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

    def write_table(path, rows):
        with path.open('w', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        with path.open(encoding='utf-8', newline='') as stream:
            parsed = list(csv.DictReader(stream))
        check(path.name+'_sourced_nonclaim_rows_parse', len(parsed) == len(rows) and all(None not in row
            and row['valid_for_claim'] == 'False' and (root/row['source_path']).is_file() for row in parsed))
        check(path.name+'_numeric_values_finite', all(math.isfinite(value) for row in rows
            for value in row.values() if isinstance(value, (float, int))))
        own(path, 'outputs')

    save()
    try:
        previous = inherit(intake/'annular-live-Gram-transport-final-integrity.json')
        check('previous_checkpoint_and40failures_preserved', previous['state'] == 'complete'
            and all(row['passed'] for row in previous['checks']) and previous['total_failed_attempts_preserved'] == 40)
        names = ['annular-live-exponential-transport-MTS-attempt01',
            'annular-live-exponential-transport-reference-attempt01', 'annular-exponential-transport-algebra-attempt01',
            'annular-spatial-Gram-defect-split-attempt02']
        statuses = []
        for name in names:
            status = inherit(intake/name/'status.json')
            statuses.append(status)
            check(name+'_complete_nonclaim_private', status['state'] == 'complete'
                and all(row['passed'] for row in status['checks']) and not status['valid_for_physics_claim']
                and not status['full_GR_limit_proven'] and not status['full_live_P2_force_convergence_proven']
                and not status['github_action'] and not status['subagents_used'])
        failures = []
        for prefix in ['annular-live-exponential-transport-', 'annular-exponential-transport-algebra-',
                'annular-spatial-Gram-defect-split-']:
            for path in sorted(intake.glob(prefix+'*/status.json')):
                if path.parent.name not in names:
                    status = inherit(path)
                    check(path.parent.name+'_failed_attempt_preserved', status['state'] == 'failed')
                    failures.append(dict(folder=path.parent.name, error=status['error']))
        check('one_new_failed_nesting_assumption_preserved', len(failures) == 1
            and failures[0]['folder'] == 'annular-spatial-Gram-defect-split-attempt01', failures)
        count = sum(len(status['checks']) for status in statuses)
        check('302_successful_implementation_checks', count == 302, count)
        budgets, samples = [], []
        for name, status in zip(names[:2], statuses[:2]):
            expected_samples = 65 if status['branch'] == 'MTS' else 33
            expected_budgets = 16 if status['branch'] == 'MTS' else 12
            check(name+'_full_mode_and_live_feedback_scope', len(status['samples']) == expected_samples
                and len(status['cases']) == expected_budgets and status['no_new_evolution']
                and status['full_live_geometry_reconstructed'] and status['all_scalar_modes_retained']
                and status['frozen_linear_split_not_frozen_geometry_dynamics']
                and status['defect_not_an_integrator_error_certificate']
                and status['initial_and_terminal_geometry_terms_retained'])
            source_path = str((intake/name/'status.json').relative_to(root))
            for item in status['cases']:
                budgets.append(dict(branch=status['branch'], **item, source_path=source_path))
                check(name+'_'+item['observable']+'_'+str(item['sample_intervals'])+'_nonclaim', not item['valid_for_claim'])
            for item in status['samples']:
                samples.append(dict(branch=status['branch'], **item, source_path=source_path))
            for intervals in [8, 16, 32]+([64] if status['branch'] == 'MTS' else []):
                parts = {row['observable']:row for row in status['cases'] if row['sample_intervals'] == intervals}
                for quantity in ['endpoint_pairing', 'exponential_forcing', 'unresolved_trajectory_and_quadrature_defect']:
                    error = abs(parts['all_Gram_rows'][quantity]-parts['source_Gram_rows'][quantity]-parts['remaining_Gram_rows'][quantity])
                    check(name+'_'+str(intervals)+'_'+quantity+'_partitions_add', error < 3e-15, error)
        check('independent_high_frequency_and_curvature_controls', statuses[2]['independent_augmented_matrix_exponential_control']
            and statuses[2]['curvature_bound_requires_actual_remainder_derivative_control'] and len(statuses[2]['cases']) == 15)
        write_table(table, budgets)
        write_table(samples_table, samples)
        spatial = statuses[3]
        check('spatial_off_space_extension_scope_retained', len(spatial['cases']) == 4
            and spatial['no_new_evolution'] and spatial['all_Gram_rows_retained']
            and spatial['full_geometry_reconstructed_on_both_paths']
            and spatial['counterfactuals_not_evolved_states'] and spatial['spatial_hierarchy_not_continuum_error']
            and spatial['nonnested_mesh_transfer_retained']
            and spatial['off_space_extension_uses_unchanged_fine_quadrature']
            and spatial['off_space_quadrature_not_a_continuous_integral_certificate'])
        spatial_rows, increments = [], []
        source_path = str((intake/names[3]/'status.json').relative_to(root))
        components = ['field_state_difference', 'transfer_commutator', 'geometry_source_difference', 'operator_mesh_difference']
        for case in spatial['cases']:
            tag = case['branch']+'_'+str(case['time'])
            check(tag+'_actual_nonnesting_not_silenced', not case['source_mesh_is_nested']
                and len(case['unmatched_coarse_edges']) == 11 and case['maximum_coarse_edge_distance'] > 1e-3
                and not case['valid_for_claim'] and case['transfer_diagnostic']['retains_original_fine_mass_and_quadrature'])
            for part in case['partitions']:
                spatial_rows.append(dict(branch=case['branch'], time=case['time'], coarse_count=case['coarse_count'],
                    fine_count=case['fine_count'], **part, source_path=source_path))
                check(tag+'_'+part['partition']+'_four_components_reconstruct', not part['valid_for_claim']
                    and abs(part['direct_difference']-sum(part[key] for key in components)) < 3e-20
                    and abs(part['direct_difference']) <= part['absolute_four_term_bound']+3e-20)
            parts = {part['partition']:part for part in case['partitions']}
            check(tag+'_spatial_partitions_add', all(abs(parts['all_rows'][key]-parts['source_straddling'][key]
                -parts['remaining'][key]) < 3e-20 for key in components+['direct_difference']))
        for branch in ['reference', 'MTS']:
            first = {part['partition']:part for case in spatial['cases'] if case['branch'] == branch and case['time'] == 0.
                for part in case['partitions']}
            last = {part['partition']:part for case in spatial['cases'] if case['branch'] == branch and case['time'] > 0.
                for part in case['partitions']}
            for partition in ['all_rows', 'source_straddling', 'remaining']:
                changes = {key:last[partition][key]-first[partition][key] for key in components+['direct_difference']}
                check(branch+'_'+partition+'_time_increment_telescope', abs(changes['direct_difference']
                    -sum(changes[key] for key in components)) < 3e-20)
                increments.append(dict(branch=branch, partition=partition, time_start=0., time_end=4e-5,
                    **changes, initial_error_dynamical_influence_removed=False, valid_for_claim=False, source_path=source_path))
        write_table(spatial_table, spatial_rows)
        write_table(increments_table, increments)
        note = root/'DERIVATION-20260919-exponential-force-defect-transport.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json|csv))`', content)
        check('all_cited_local_paths_exist', bool(cited) and all((root/name).is_file() for name in cited), cited)
        check('scope_and_unresolved_defect_disclosed', 'Live results pending' not in content
            and 'does not establish the full GR limit' in content and 'NOT automatically the time integrator' in content
            and '13.58%' in content and '12.5718%' in content and 'any inference of exact nesting is withdrawn' in content
            and 'NOT an isolated spatial truncation error' in content and 'The numerical usefulness of this bound has NOT yet been tested' in content)
        own(note)
        for name in ['annular_exponential_transport_20260919.py', 'validate_annular_exponential_transport_20260919.py',
                'run_annular_live_exponential_transport_20260919.py', 'derive_annular_spatial_Gram_defect_split_20260919.py',
                'derive_annular_spatial_Gram_transfer_split_v2_20260919.py', 'seal_annular_exponential_transport_20260919.py']:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('sources_compile_without_bytecode', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026, 9, 19, 11, 24, 59, tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= start]
        check('protected_mtime_changed_count_zero', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        own(executed, 'outputs')
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(),
            implementation_checks=count, total_failed_attempts_preserved=40+len(failures),
            new_failed_executions=len(failures), new_failures=failures, distinct_files_rehashed=len(cache),
            full_interval_retested=False, budget_rows=len(budgets), sample_rows=len(samples),
            spatial_rows=len(spatial_rows), spatial_increment_rows=len(increments))
        save()
        print(json.dumps(dict(state='complete', implementation_checks=count, integrity_checks=len(report['checks']),
            files_rehashed=len(cache), failed_attempts_preserved=40+len(failures), budget_rows=len(budgets), sample_rows=len(samples),
            spatial_rows=len(spatial_rows), spatial_increment_rows=len(increments))), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
