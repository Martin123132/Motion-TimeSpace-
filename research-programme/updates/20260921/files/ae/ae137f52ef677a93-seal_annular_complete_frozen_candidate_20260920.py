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
    prefix = 'annular-complete-frozen-candidate'
    destination = intake/(prefix+'-final-integrity.json')
    executed = intake/(prefix+'-executed-sealer.py')
    snapshot = intake/(prefix+'-resume-snapshot.md')
    specifications = [
        ('assembly', 0, 'cases', 3), ('coefficient-derivatives', 0, 'derivatives', 12),
        ('matrix-refinement', 0, 'refinement', 16), ('source-controls', 1, 'source_controls', 3),
        ('atom-pairings', 1, 'pairings', 4), ('response', 2, 'cases', 6),
        ('source-diagnostics', 2, 'forces', 12), ('response-refinement', 2, 'refinement', 3),
        ('reversal', 2, 'reversal', 3), ('extension-sensitivity', 2, 'extension_sensitivity', 1)]
    tables = [intake/(prefix+'-'+label+'.csv') for label, unused, unused_key, unused_count in specifications]
    if any(path.exists() for path in [destination, executed, snapshot]+tables):
        raise FileExistsError('Immutable seal destination already exists.')
    report = dict(state='running', checks=[], inputs={}, outputs={}, github_action=False, subagents_used=False,
        no_new_live_evolution=True, original_live_action_unchanged=True, candidate_only=True,
        frozen_background_only=True, homogeneous_scalar_block_only=True, moving_source_evolved=False,
        source_force_diagnostic_only=True, full_GR_limit_proven=False, valid_for_physics_claim=False,
        full_live_P2_force_convergence_proven=False, certified_continuous_time_bound=False,
        self_consistent_candidate_metric_solved=False, physical_force_mismatch_fixed=False,
        actual_time_integrated_force_test=False, nonuniform_parent_uniqueness_proven=False,
        protected_scan_scope='mtime since2026-09-20T16:32:37Z; not a pre-turn whole-tree hash baseline')
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
        previous = inherit(intake/'annular-nonuniform-Gram-final-integrity.json')
        check('preceding_seal_unchanged', previous['state'] == 'complete'
            and all(item['passed'] for item in previous['checks'])
            and previous['primary_variational_candidate_qualified'] and previous['stable_fixed_profile_kernel_qualified']
            and not previous['physical_force_mismatch_fixed'])
        names = ['annular-complete-frozen-candidate-attempt01',
            'annular-complete-candidate-controls-attempt01', 'annular-common-candidate-response-attempt01']
        statuses = [inherit(intake/name/'status.json') for name in names]
        for name, status in zip(names, statuses):
            check(name+'_complete_nonclaim', status['state'] == 'complete'
                and all(item['passed'] for item in status['checks'])
                and status['original_live_action_unchanged'] and status['candidate_only']
                and not status['valid_for_physics_claim'] and not status['full_GR_limit_proven']
                and not status['physical_force_mismatch_fixed'] and not status['full_live_P2_force_convergence_proven']
                and not status['certified_continuous_time_bound'] and not status['self_consistent_candidate_metric_solved']
                and not status['github_action'] and not status['subagents_used'])
        assembly, controls, response = statuses
        check('full_prescribed_background_field_action_assembled', assembly['full_candidate_assembly_qualified']
            and assembly['no_new_evolution'] and len(assembly['cases']) == 3
            and all(row['count'] == 1094 and Decimal(row['minimum_mass_pivot']) > 0
                and Decimal(row['mass_jacobi_ratio']) < 1 for row in assembly['cases']))
        check('independent_source_Euler_and_propagator_controls', controls['full_source_Euler_controls_qualified']
            and controls['frozen_scalar_propagator_qualified'] and controls['no_new_evolution']
            and len(controls['source_controls']) == 3 and all(row['error'] < 3e-12 for row in controls['source_controls']))
        check('previous_atom_values_recovered', len(controls['pairings']) == 4
            and all(Decimal(row['error']) < Decimal('1e-24') for row in controls['pairings']))
        check('pilot_is_restricted_not_a_coupled_force_test', response['frozen_scalar_response_arithmetic_qualified']
            and response['no_new_live_evolution'] and not response['no_new_evolution']
            and response['homogeneous_scalar_block_only'] and not response['moving_source_evolved']
            and response['source_force_diagnostic_only'] and not response['actual_time_integrated_force_test']
            and response['original_physical_mismatch_percentages_unchanged'])
        check('all_modes_and_equal_refinement_for_all_branches', len(response['cases']) == 6
            and all(row['count'] == 1094 for row in response['cases'])
            and {(row['branch'], row['extension'], row['digits'], row['degree']) for row in response['cases']}
            == {(branch, extension, digits, degree) for branch, extension in
                [('reference', 'reference'), ('MTS', 'primary'), ('MTS', 'alternative')]
                for digits, degree in [(32, 48), (48, 64)]})
        check('predeclared_energy_gates_unchanged', all(Decimal(row['relative_energy_drift'])
            < Decimal('1e-20' if row['digits'] == 32 else '1e-34') for row in response['cases']))
        check('predeclared_refinement_gates_unchanged', len(response['refinement']) == 3
            and all(Decimal(row['relative_phase_energy_error']) < Decimal('1e-20')
                and Decimal(row['relative_source_diagnostic_change']) < Decimal('1e-19')
                and row['not_a_physical_force_gate'] for row in response['refinement']))
        check('all_mode_reverse_checks', len(response['reversal']) == 3
            and all(Decimal(row['relative_phase_energy_error']) < Decimal('1e-32') for row in response['reversal']))
        check('source_diagnostic_inertia_positive_without_clipping', len(response['forces']) == 12
            and all(Decimal(row['field_inertia_complement']) >= 0 and Decimal(row['total_inertia']) > 0
                and row['diagnostic_not_coupled'] for row in response['forces']))
        check('nonunique_extension_difference_not_used_to_select_action',
            len(response['extension_sensitivity']) == 1
            and not response['extension_sensitivity'][0]['a_selection_or_rejection_criterion']
            and not response['nonuniform_parent_uniqueness_proven'])
        row_counts = []
        for path, (label, status_index, key, expected_count) in zip(tables, specifications):
            rows = [dict(**row, source_path=str((intake/names[status_index]/'status.json').relative_to(root)))
                for row in statuses[status_index][key]]
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
        note = root/'DERIVATION-20260920-complete-frozen-candidate-and-source-response.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json|csv))`', content)
        check('report_complete_and_cited_paths_exist', 'RESULTS_PENDING' not in content and bool(cited)
            and all((root/name).is_file() for name in cited), cited)
        for name in cited:
            own(root/name)
        own(note)
        for name in ['annular_common_frozen_candidate_20260920.py', 'build_annular_complete_frozen_candidate_20260920.py',
                'validate_annular_complete_candidate_20260920.py', 'run_annular_common_frozen_candidate_20260920.py',
                'seal_annular_complete_frozen_candidate_20260920.py']:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('all_new_sources_compile_without_bytecode', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026, 9, 20, 16, 32, 37, tzinfo=timezone.utc).timestamp()
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
            total_failed_attempts_preserved=previous['total_failed_attempts_preserved'], new_failures=[],
            distinct_files_rehashed=len(cache), table_rows=row_counts,
            prescribed_background_candidate_field_action_qualified=True,
            source_Schur_reaction_derived_and_controlled=True,
            frozen_scalar_response_arithmetic_qualified=True,
            candidate_metric_load_identified_not_solved=True,
            next_target='Joint common-space and Gram-knot refinement of the new candidate with both extensions and the reference, preserving initial physical fields and using the full source diagnostic. Establish whether extension sensitivity shrinks before selecting a numerical rule. Then assemble the candidate radial constraint from its derived bulk/nodal metric load and solve a self-consistent initial metric before a short coupled source/gravity run; no physical force or GR claim from the homogeneous pilot.')
        save()
        print(json.dumps(dict(state='complete', checks=report['implementation_checks'], integrity_checks=len(report['checks']),
            files_rehashed=len(cache), table_rows=row_counts, failures_preserved=report['total_failed_attempts_preserved'])), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
