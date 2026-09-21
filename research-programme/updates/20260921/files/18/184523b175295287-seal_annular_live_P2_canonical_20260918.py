from derive_annular_source_gravity_20260914 import EvidenceRun
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import re
import traceback


def main():
    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    destination = intake/'annular-live-P2-canonical-final-integrity.json'
    snapshot = intake/'annular-live-P2-canonical-resume-snapshot.md'
    executed = intake/'annular-live-P2-canonical-executed-sealer.py'
    if any(path.exists() for path in [destination, snapshot, executed]):
        raise FileExistsError('Immutable evidence destination already exists.')
    report = dict(state='running', checks=[], inputs={}, outputs={},
        actual_finite_P2_canonical_inverse_coupled_to_radial_geometry=True,
        fixed_metric_inverse_unique_on_positive_timelike_branch=True,
        global_coupled_fixed_point_uniqueness_proven=False,
        constrained_energy_first_variation_conditionally_derived=True,
        finite_label_collocation_not_exact_Galerkin=True,
        independent_temporal_current_tested=False, no_forward_evolution=True,
        full_live_P2_force_convergence_proven=False, full_GR_limit_proven=False,
        valid_for_physics_claim=False, independently_reviewed_proof=False,
        no_GitHub_action=True, subagents_used=False, implementation_checks_not_physics_passes=True,
        protected_scan_scope='mtime since2026-09-18T12:55:13Z; not a pre-turn full hash baseline')
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

    def own(path, table='inputs'):
        report[table][str(path.resolve().relative_to(root))] = digest(path)

    def save():
        destination.write_text(json.dumps(report, indent=2, allow_nan=False)+'\n', encoding='utf-8')

    def check(name, passed, detail=None):
        report['checks'].append(dict(name=name, passed=bool(passed), detail=detail))
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    def inherit(path):
        status = json.loads(path.read_text())
        for table in ['inputs', 'outputs']:
            for name, expected in status[table].items():
                source = (root/name).resolve()
                key = str(source.relative_to(root))
                if not source.is_file() or digest(source) != expected:
                    raise RuntimeError('Missing or modified sealed source: '+name)
                if key in report['inputs'] and report['inputs'][key] != expected:
                    raise RuntimeError('Conflicting sealed hash: '+name)
                report['inputs'][key] = expected
        own(path)
        return status

    save()
    try:
        previous = inherit(intake/'annular-live-Gram-stress-final-integrity.json')
        check('preceding_seal_complete_and_hash_chain_preserved', previous['state'] == 'complete'
            and all(row['passed'] for row in previous['checks']))
        check('all_previous_failures_retained', previous['inherited_failed_attempts_preserved'] == 31
            and previous['inherited_peak_force_failures_preserved'] == 4)
        failed = inherit(intake/'annular-live-P2-canonical-attempt01/status.json')
        check('executed_partition_failure_retained', failed['state'] == 'failed'
            and [row['name'] for row in failed['checks'] if not row['passed']]
            == ['reference(17, 8, 12, False)_independent_radial_equations'])
        statuses = {}
        for name, count in [('annular-live-P2-canonical-attempt02', 40),
                ('annular-live-P2-edge-diagnosis-attempt01', 8), ('annular-live-P2-reduced-energy-attempt01', 13)]:
            status = inherit(intake/name/'status.json')
            statuses[name] = status
            check(name+'_completed', status['state'] == 'complete' and len(status['checks']) == count
                and all(row['passed'] for row in status['checks']))
            check(name+'_claim_scope_unchanged', not status['valid_for_physics_claim']
                and not status['full_GR_limit_proven'] and status['no_forward_evolution']
                and not status['github_action'] and not status['subagents_used'])
        canonical = statuses['annular-live-P2-canonical-attempt02']
        diagnosis = statuses['annular-live-P2-edge-diagnosis-attempt01']
        energy = statuses['annular-live-P2-reduced-energy-attempt01']
        expected = {(branch, *config) for branch in ['reference', 'MTS']
            for config in [(17, 4, 12, False), (17, 8, 12, False), (17, 6, 18, True), (33, 4, 14, False)]}
        actual = {(row['branch'], row['base_count'], row['layer_degree'], row['radial_degree'], row['deformed'])
            for row in canonical['cases']}
        check('paired_actual_P2_grids_label_refinement_and_deformed_map', actual == expected)
        check('actual_kinetic_inverse_no_pointwise_or_frozen_geometry_shortcut',
            canonical['actual_finite_P2_banded_inverse'] and canonical['continuum_pointwise_momentum_not_substituted']
            and canonical['all_Gram_rows_retained'] and canonical['original_stored_actions_and_data_unchanged']
            and canonical['coupled_live_P2_canonical_snapshots_solved']
            and canonical['natural_norm_bound_not_inverse_mesh_estimate'])
        check('nodal_and_offgrid_radial_controls', all(row['canonical_roundtrip'] < 2e-10
            and row['nodal_momentum_error'] < 2e-10 and row['mass_radial_residual'] < 2e-7
            and row['lapse_radial_residual'] < 2e-7 and row['minimum_source_jacobian'] > 0
            and row['minimum_spatial_jacobian'] > 0 for row in canonical['cases']))
        check('current_convergence_and_global_uniqueness_not_claimed',
            not canonical['independent_temporal_current_tested'] and not canonical['full_live_P2_force_convergence_proven']
            and not canonical['global_coupled_fixed_point_uniqueness_proven']
            and not energy['independent_temporal_current_tested'] and not energy['full_live_P2_force_convergence_proven'])
        check('paired_roundoff_diagnosis_no_equation_data_or_gate_change',
            {row['branch'] for row in diagnosis['cases']} == {'reference', 'MTS'}
            and diagnosis['equations_and_data_unchanged'] and diagnosis['acceptance_threshold_unchanged']
            and diagnosis['radial_partition_roundoff_fix_only']
            and all(row['old_minimum_interval'] < row['edge_tolerance'] < row['new_minimum_interval']
                and row['metric_profile_change'] < 1e-12 and row['momentum_change'] < 1e-12
                and max(row['old_radial_residual']) > 1 and max(row['new_radial_residual']) < 2e-7
                for row in diagnosis['cases']))
        directions = {'field_momentum', 'source_momentum', 'field_coordinate', 'source_coordinate'}
        check('all_four_reduced_mass_variations_paired', {(row['branch'], row['direction']) for row in energy['cases']}
            == {(branch, direction) for branch in ['reference', 'MTS'] for direction in directions}
            and max(row['error'] for row in energy['cases']) < 2e-8)
        check('constrained_mass_not_matter_energy_and_each_perturbation_resolved',
            energy['constrained_mass_not_matter_energy_only'] and energy['pointwise_continuum_momentum_not_substituted']
            and energy['finite_label_collocation_not_exact_Galerkin']
            and energy['coupled_constraint_canonical_solve_used_in_every_perturbation']
            and energy['no_trajectory_or_total_mass_conservation_claim'])
        controls = [row for row in energy['checks'] if row['name'].endswith('_independent_quadrature_radial_control')]
        check('independent_quadrature_radial_controls_both_branches', len(controls) == 2
            and all(max(row['detail'].values()) < 2e-8 for row in controls), controls)
        old = inherit(intake/'annular-initial-corner-response-final-integrity.json')
        check('all_four_original_force_gates_still_fail', len(old['comparison_results']) == 4
            and all(not row['original_peak_force_gate_pass'] for row in old['comparison_results']))
        note = root/'DERIVATION-20260918-coupled-live-P2-canonical-inverse.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json))`', content)
        check('all_cited_local_paths_exist', bool(cited) and all((root/name).is_file() for name in cited), cited)
        check('completed_derivation_records_results_and_limitations', '61 successful implementation checks' in content
            and 'PENDING' not in content and 'not an exact finite-label Galerkin action' in content
            and 'making32 inherited/current failed attempts' in content)
        own(note)
        names = ['annular_live_P2_canonical_20260918.py', 'annular_live_P2_canonical_v2_20260918.py',
            'qualify_annular_live_P2_canonical_20260918.py', 'qualify_annular_live_P2_canonical_v2_20260918.py',
            'diagnose_annular_live_P2_edges_20260918.py', 'qualify_annular_live_P2_reduced_energy_20260918.py',
            'seal_annular_live_P2_canonical_20260918.py']
        for name in names:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('all_new_scripts_compile_and_no_bytecode', not (root/'scripts/__pycache__').exists(), names)
        protected = root.parent/'formalization-workbench'
        timestamp = datetime(2026, 9, 18, 12, 55, 13, tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*')
            if path.is_file() and path.stat().st_mtime >= timestamp]
        check('protected_workbench_mtime_changed_count_zero', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        own(executed, 'outputs')
        check('resume_and_executed_sealer_snapshots_saved', True)
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(),
            total_successful_current_checks=61, distinct_files_rehashed=len(cache),
            inherited_failed_attempts_preserved=32, inherited_peak_force_failures_preserved=4,
            new_failed_attempts_preserved=['annular-live-P2-canonical-attempt01'],
            results={name: status['cases'] for name, status in statuses.items()})
        save()
        print(json.dumps(dict(state='complete', integrity_checks=len(report['checks']), current_checks=61,
            rehashed_files=len(cache), protected_changed=len(changed), failed_attempts_preserved=32)), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
