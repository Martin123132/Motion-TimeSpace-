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
    destination = intake/'annular-live-P2-current-final-integrity.json'
    snapshot = intake/'annular-live-P2-current-resume-snapshot.md'
    executed = intake/'annular-live-P2-current-executed-sealer.py'
    if any(path.exists() for path in [destination, snapshot, executed]):
        raise FileExistsError('Immutable evidence destination already exists.')
    report = dict(state='running', checks=[], inputs={}, outputs={},
        action_derived_moving_P2_current_qualified=True, explicit_horizontal_extension=True,
        unique_parent_shift_extension_proven=False, arbitrary_covariance_proven=False,
        tangent_current_is_implicit_equation_test=True, short_coupled_P2_evolution=True,
        full_live_P2_force_convergence_proven=False, full_GR_limit_proven=False,
        valid_for_physics_claim=False, independently_reviewed_proof=False,
        no_GitHub_action=True, subagents_used=False, implementation_checks_not_physics_passes=True,
        protected_scan_scope='mtime since2026-09-18T15:14:44Z; not a pre-turn full hash baseline')
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
        previous = inherit(intake/'annular-live-P2-canonical-final-integrity.json')
        check('previous_complete_seal_and_hash_chain', previous['state'] == 'complete'
            and all(row['passed'] for row in previous['checks']))
        check('all_inherited_failures_retained', previous['inherited_failed_attempts_preserved'] == 32
            and previous['inherited_peak_force_failures_preserved'] == 4)
        failed = inherit(intake/'annular-P2-current-tangent-resolution-attempt01/status.json')
        check('failed_resolution_expectation_preserved_not_relabelled', failed['state'] == 'failed'
            and [row['name'] for row in failed['checks'] if not row['passed']]
            == ['reference_offgrid_scalar_residual_label_refinement'])
        statuses = {}
        for name, count in [('annular-P2-moving-shift-variation-attempt01', 12),
                ('annular-live-P2-independent-current-attempt01', 20),
                ('annular-P2-current-label-diagnosis-attempt01', 21),
                ('annular-live-P2-current-evolution-attempt01', 44)]:
            status = inherit(intake/name/'status.json')
            statuses[name] = status
            check(name+'_complete', status['state'] == 'complete' and len(status['checks']) == count
                and all(row['passed'] for row in status['checks']))
            check(name+'_private_nonclaim_scope', not status['valid_for_physics_claim']
                and not status['full_GR_limit_proven'] and not status['github_action'] and not status['subagents_used'])
        shift = statuses['annular-P2-moving-shift-variation-attempt01']
        current = statuses['annular-live-P2-independent-current-attempt01']
        resolution = statuses['annular-P2-current-label-diagnosis-attempt01']
        evolution = statuses['annular-live-P2-current-evolution-attempt01']
        check('actual_nonzero_shift_variation_not_diagonal_inference', shift['finite_nonzero_shift_action_tested']
            and shift['explicit_source_anchored_horizontal_extension'] and not shift['unique_parent_shift_extension_proven']
            and not shift['arbitrary_time_coordinate_covariance_proven']
            and {row['branch'] for row in shift['cases']} == {'reference', 'MTS'})
        check('moving_transport_and_node_clock_negative_controls', all(row['finite_error'] < 2e-9
            and row['adjoint_error'] < 2e-9 and row['wrong_node_clock_error'] > 1e-10
            and row['wrong_transport_error'] > 1e-10 for row in shift['cases']))
        check('paired_affine_and_deformed_current_checks', {(row['branch'], row['deformed']) for row in current['cases']}
            == {(branch, deformed) for branch in ['reference', 'MTS'] for deformed in [False, True]}
            and all(row['maximum_error'] < 2e-8 and row['maximum_on_shell_error'] < 2e-8
                and row['maximum_frozen_mesh_error'] > 20*max(row['maximum_error'], 1e-12) for row in current['cases']))
        check('current_is_action_derived_but_implicit_test_disclosed', current['current_not_defined_from_radial_mass_derivative']
            and current['tangent_metric_in_current_is_an_implicit_equation_test'])
        check('resolution_miss_and_wider_control_distinguished', resolution['original_6_to_10_gate_not_relabeled_passed']
            and resolution['equations_and_current_gates_unchanged']
            and not resolution['resolution_results']['reference']['original_6_to_10_gate_pass']
            and all(row['ratio_6_to_18'] < .5 for row in resolution['resolution_results'].values()))
        check('both_branches_all_three_label_degrees', {(row['branch'], row['label_degree']) for row in resolution['cases']}
            == {(branch, degree) for branch in ['reference', 'MTS'] for degree in [6, 10, 18]})
        check('all_eight_evolutions_with_separate_controls', {(row['branch'], row['mode']) for row in evolution['cases']}
            == {(branch, mode) for branch in ['reference', 'MTS'] for mode in ['principal', 'half_step', 'label_refined', 'zero_wave']}
            and all(row['solver_success'] and row['duration'] == .004 for row in evolution['cases']))
        check('no_projection_and_no_force_accuracy_upgrade', not evolution['mass_or_current_projection_used']
            and not evolution['full_live_P2_force_convergence_proven']
            and not evolution['continuum_force_accuracy_or_long_time_stability_claim'])
        check('evolved_mass_and_independent_current_gates', all(row['mass_drift'] < 2e-9 for row in evolution['cases'])
            and all(max(item['error'] for item in row['final_current']) < 2e-8
                for row in evolution['cases'] if row['mode'] == 'principal'))
        old = inherit(intake/'annular-initial-corner-response-final-integrity.json')
        check('all_four_original_force_gates_still_fail', len(old['comparison_results']) == 4
            and all(not row['original_peak_force_gate_pass'] for row in old['comparison_results']))
        note = root/'DERIVATION-20260918-moving-P2-current-and-live-evolution.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json))`', content)
        check('all_cited_paths_exist', bool(cited) and all((root/name).is_file() for name in cited), cited)
        check('note_complete_and_limits_disclosed', '97 successful implementation checks' in content
            and 'will be filled' not in content and 'PENDING' not in content
            and 'IMPLICIT temporal-equation residual test' in content and '0.5257788755' in content)
        own(note)
        names = ['annular_live_P2_current_20260918.py', 'qualify_annular_P2_shift_variation_20260918.py',
            'qualify_annular_live_P2_current_20260918.py', 'qualify_annular_P2_current_tangent_resolution_20260918.py',
            'diagnose_annular_P2_current_label_resolution_20260918.py', 'run_annular_live_P2_current_evolution_20260918.py',
            'seal_annular_live_P2_current_20260918.py']
        for name in names:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('new_sources_compile_without_bytecode', not (root/'scripts/__pycache__').exists(), names)
        protected = root.parent/'formalization-workbench'
        timestamp = datetime(2026, 9, 18, 15, 14, 44, tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*')
            if path.is_file() and path.stat().st_mtime >= timestamp]
        check('protected_mtime_changed_count_zero', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        own(executed, 'outputs')
        check('resume_and_executed_sealer_snapshots_saved', True)
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(),
            total_successful_current_checks=97, distinct_files_rehashed=len(cache),
            inherited_failed_attempts_preserved=33, inherited_peak_force_failures_preserved=4,
            new_failed_attempts_preserved=['annular-P2-current-tangent-resolution-attempt01'],
            results={name: status['cases'] for name, status in statuses.items()})
        save()
        print(json.dumps(dict(state='complete', integrity_checks=len(report['checks']), current_checks=97,
            rehashed_files=len(cache), protected_changed=len(changed), failed_attempts_preserved=33)), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
