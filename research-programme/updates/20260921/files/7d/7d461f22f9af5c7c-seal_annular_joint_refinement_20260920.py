from derive_annular_source_gravity_20260914 import EvidenceRun
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
import csv
import hashlib
import json
import re
import traceback


def main():
    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    prefix = 'annular-joint-candidate-refinement'
    destination = intake/(prefix+'-final-integrity.json')
    executed = intake/(prefix+'-executed-sealer.py')
    snapshot = intake/(prefix+'-resume-snapshot.md')
    specifications = [('assembly', 0, 'cases', 6), ('meshes', 0, 'meshes', 4),
        ('matrix-checks', 0, 'matrix_checks', 32), ('response', 1, 'cases', 12),
        ('source-diagnostics', 1, 'forces', 24), ('arithmetic-refinement', 1, 'refinement', 6),
        ('reversal', 1, 'reversal', 6), ('spatial-changes', 1, 'spatial', 6),
        ('extension-sensitivity', 1, 'extension_sensitivity', 3), ('decision', 1, 'decision', 1)]
    tables = [intake/(prefix+'-'+label+'.csv') for label, unused, unused_key, unused_count in specifications]
    if any(path.exists() for path in [destination, executed, snapshot]+tables):
        raise FileExistsError('Immutable seal destination already exists.')
    report = dict(state='running', checks=[], inputs={}, outputs={}, github_action=False, subagents_used=False,
        original_live_action_unchanged=True, no_new_live_evolution=True, candidate_only=True,
        frozen_background_only=True, homogeneous_scalar_block_only=True, moving_source_evolved=False,
        source_force_diagnostic_only=True, physical_force_mismatch_fixed=False,
        self_consistent_candidate_metric_solved=False, full_GR_limit_proven=False, valid_for_physics_claim=False,
        full_live_P2_force_convergence_proven=False, spatial_convergence_proven=False,
        certified_continuous_time_bound=False, actual_time_integrated_force_test=False,
        nonuniform_parent_uniqueness_proven=False,
        protected_scan_scope='mtime since2026-09-20T18:05:58Z; not a pre-turn whole-tree hash baseline')
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
                    raise RuntimeError('Conflicting source: '+name)
                report['inputs'][key] = expected
        own(path)
        return data

    save()
    try:
        previous = inherit(intake/'annular-complete-frozen-candidate-final-integrity.json')
        check('preceding_seal_unchanged', previous['state'] == 'complete'
            and all(row['passed'] for row in previous['checks'])
            and previous['source_Schur_reaction_derived_and_controlled']
            and previous['frozen_scalar_response_arithmetic_qualified'] and not previous['physical_force_mismatch_fixed'])
        names = ['annular-joint-candidate-refinement-build-attempt01', 'annular-joint-candidate-refinement-response-attempt01']
        statuses = [inherit(intake/name/'status.json') for name in names]
        for name, status in zip(names, statuses):
            check(name+'_complete_nonclaim', status['state'] == 'complete'
                and all(row['passed'] for row in status['checks']) and status['candidate_only']
                and status['original_live_action_unchanged'] and status['frozen_background_only']
                and not status['physical_force_mismatch_fixed'] and not status['self_consistent_candidate_metric_solved']
                and not status['full_GR_limit_proven'] and not status['valid_for_physics_claim']
                and not status['full_live_P2_force_convergence_proven'] and not status['certified_continuous_time_bound']
                and not status['github_action'] and not status['subagents_used'])
        assembly, response = statuses
        check('joint_field_and_Gram_refinement_qualified', assembly['joint_refinement_assembly_qualified']
            and len(assembly['meshes']) == 4 and all(row['field_dofs'] == row['gram_knots'] == 1094*2**row['level']
                and row['cells'] == 547*2**row['level'] and row['all_cells_bisected'] for row in assembly['meshes']))
        check('all_bulk_forms_preserved_and_quadrature_checked', len(assembly['matrix_checks']) == 32
            and all(Decimal(row['quadrature_relative_change']) < Decimal('3e-10')
                and Decimal(row['parent_pullback_relative_change']) < Decimal('3e-10')
                and row['not_a_physical_force_gate'] for row in assembly['matrix_checks']))
        check('positive_mass_and_all_mode_bound', len(assembly['cases']) == 6
            and all(Decimal(row['minimum_mass_pivot']) > 0 and Decimal(row['mass_jacobi_ratio']) < 1
                and 0 < row['steps_at_4e_5'] <= 512 for row in assembly['cases']))
        check('homogeneous_pilot_not_full_coupled_force_test', response['refined_pilot_arithmetic_qualified']
            and response['homogeneous_scalar_block_only'] and response['source_force_diagnostic_only']
            and not response['moving_source_evolved'] and not response['actual_time_integrated_force_test']
            and not response['spatial_convergence_proven'])
        expected = {(branch, extension, level, 1094*2**level, digits, degree)
            for branch, extension in [('reference', 'reference'), ('MTS', 'primary'), ('MTS', 'alternative')]
            for level in [1, 2] for digits, degree in [(32, 48), (48, 64)]}
        check('all_branches_levels_modes_and_arithmetic_settings', len(response['cases']) == 12
            and {(row['branch'], row['extension'], row['level'], row['count'], row['digits'], row['degree'])
                for row in response['cases']} == expected)
        check('unchanged_energy_gates', all(Decimal(row['relative_energy_drift'])
            < Decimal('1e-20' if row['digits'] == 32 else '1e-34') for row in response['cases']))
        check('unchanged_arithmetic_refinement_gates', len(response['refinement']) == 6
            and all(Decimal(row['relative_phase_energy_error']) < Decimal('1e-20')
                and Decimal(row['relative_source_diagnostic_change']) < Decimal('1e-19')
                and row['not_a_physical_force_gate'] for row in response['refinement']))
        check('unchanged_full_reversal_gate', len(response['reversal']) == 6
            and all(Decimal(row['relative_phase_energy_error']) < Decimal('1e-32') for row in response['reversal']))
        check('positive_source_inertia_and_nonclaim_diagnostics', len(response['forces']) == 24
            and all(Decimal(row['field_inertia_complement']) >= 0 and Decimal(row['total_inertia']) > 0
                and row['diagnostic_not_coupled'] for row in response['forces']))
        sensitivity = response['extension_sensitivity']
        check('both_absolute_and_relative_spatial_trends_recorded', len(sensitivity) == 3
            and [row['level'] for row in sensitivity] == [0, 1, 2]
            and response['decision']['absolute_extension_difference_shrinks_on_both_refinements'] == all(
                abs(Decimal(last['reduced_source_diagnostic_difference'])) < abs(Decimal(first['reduced_source_diagnostic_difference']))
                for first, last in zip(sensitivity, sensitivity[1:]))
            and response['decision']['relative_extension_difference_shrinks_on_both_refinements'] == all(
                Decimal(last['relative_source_diagnostic_difference']) < Decimal(first['relative_source_diagnostic_difference'])
                for first, last in zip(sensitivity, sensitivity[1:])))
        check('spatial_measurements_not_convergence_certificate_or_selection', len(response['spatial']) == 6
            and all(row['not_a_continuum_error_bound'] for row in response['spatial'])
            and not response['decision']['physical_winner_selected'] and not response['decision']['continuum_limit_proven']
            and all(not row['a_selection_or_rejection_criterion'] for row in sensitivity))
        row_counts = []
        for path, (label, status_index, key, expected_count) in zip(tables, specifications):
            raw = statuses[status_index][key]
            raw = raw if isinstance(raw, list) else [raw]
            rows = [dict(**row, source_path=str((intake/names[status_index]/'status.json').relative_to(root))) for row in raw]
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
            row_counts.append(len(rows))
            own(path, 'outputs')
        note = root/'DERIVATION-20260920-joint-candidate-spatial-refinement.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json|csv))`', content)
        check('report_complete_and_cited_paths_exist', 'RESULTS_PENDING' not in content and bool(cited)
            and all((root/name).is_file() for name in cited), cited)
        for name in cited:
            own(root/name)
        own(note)
        for name in ['build_annular_joint_refinement_20260920.py', 'run_annular_joint_refinement_20260920.py',
                'seal_annular_joint_refinement_20260920.py']:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('new_sources_compile_without_bytecode', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026, 9, 20, 18, 5, 58, tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= start]
        check('protected_workbench_mtime_unchanged', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        own(executed, 'outputs')
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(),
            implementation_checks=sum(len(status['checks']) for status in statuses),
            implementation_check_breakdown={name:len(status['checks']) for name, status in zip(names, statuses)},
            total_failed_attempts_preserved=previous['total_failed_attempts_preserved'], new_failures=[],
            distinct_files_rehashed=len(cache), table_rows=row_counts,
            joint_refinement_assembly_qualified=True, refined_pilot_arithmetic_qualified=True,
            measured_spatial_decision=response['decision'], next_target='Derive and independently validate the candidate radial metric constraint and Jacobian from the same bulk/nodal action variation plus original gravity/source/boundary terms, with exact reference reduction. Then solve a candidate-owned initial metric, retaining both extensions and the unresolved spatial diagnostic budget. No blind extra mesh doubling or long coupled evolution; spatial convergence, physical force repair and GR claims remain open.')
        save()
        print(json.dumps(dict(state='complete', checks=report['implementation_checks'], integrity_checks=len(report['checks']),
            files_rehashed=len(cache), table_rows=row_counts, failures_preserved=report['total_failed_attempts_preserved'])), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
