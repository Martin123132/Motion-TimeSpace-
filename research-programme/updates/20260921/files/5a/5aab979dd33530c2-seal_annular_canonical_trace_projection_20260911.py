import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260911'
    destination = intake / 'annular-canonical-trace-final-integrity.json'
    if destination.exists():
        raise FileExistsError('Completed evidence is immutable.')
    report = {'state': 'running', 'inputs': {}, 'outputs': {}, 'checks': [], 'outcomes': [], 'valid_for_physics_claim': False, 'new_evolution': False, 'interval_certificate': False, 'spatial_convergence_claim': False, 'protected_scan_scope': 'mtime since 2026-09-11T22:42:49Z, not a pre-turn content snapshot', 'resource_scope': 'one BelowNormal single-core Python worker at a time; no agents or GitHub actions'}

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = digest(path)

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        if not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    def inherit(batch):
        for table in ['inputs', 'outputs']:
            for name, expected in batch[table].items():
                path = root / name
                if digest(path) != expected:
                    raise RuntimeError('Saved evidence changed: ' + name)
                report['inputs'][name] = expected

    predecessor = intake / 'annular-canonical-rate-completion-final-integrity.json'
    previous = json.loads(predecessor.read_text())
    own(predecessor)
    check('predecessor_complete', previous['state'] == 'complete')
    inherit(previous)
    batches = {}
    for name in ['annular-canonical-trace-projection-attempt01', 'annular-canonical-trace-projection-attempt02', 'annular-canonical-trace-boundary-control-attempt01']:
        directory = intake / name
        batch = json.loads((directory / 'status.json').read_text())
        batches[name] = batch
        if name.endswith('projection-attempt01'):
            check('failed_normal_equation_attempt_preserved', batch['state'] == 'failed' and any(not row['passed'] for row in batch['checks']) and 'full_family_traces' in batch['error'])
        else:
            check(name + '_all_checks_pass', batch['state'] == 'complete' and all(row['passed'] for row in batch['checks']))
        check(name + '_no_physics_or_evolution_promotion', batch['valid_for_physics_claim'] is False and batch['new_evolution'] is False and batch['interval_certificate'] is False)
        inherit(batch)
        for path in directory.iterdir():
            if path.is_file():
                own(path, 'outputs')
        for path in directory.glob('executed-*.py'):
            check(path.stem + '_executed_source_unchanged', digest(path) == digest(root / 'scripts' / path.name[len('executed-'):]))
        for path in directory.glob('*.npz'):
            with numerical.load(path, allow_pickle=False) as arrays:
                check(path.stem + '_finite_arrays', all(numerical.isfinite(arrays[key]).all() for key in arrays.files))
    trace = batches['annular-canonical-trace-projection-attempt02']
    control = batches['annular-canonical-trace-boundary-control-attempt01']
    check('both_GR_and_MTS_branches', {row['branch'] for row in trace['samples']} == {'GR', 'metric_Gram'} and {row['branch'] for row in control['samples']} == {'GR', 'metric_Gram'})
    for sample in trace['samples']:
        branch = sample['branch']
        diagnostic = sample['extension']
        check(branch + '_full_family_and_two_pairs', diagnostic['parent_family_dimension'] == 16 and diagnostic['no_parent_family_modes_discarded'] and diagnostic['new_phase_dimension'] == 69)
        check(branch + '_well_paired_continuous_lifts', diagnostic['new_coordinate_interior_node_max'] == 0 and diagnostic['new_pairing_condition'] < 2 and diagnostic['block_pairing_error'] < 1e-12)
        check(branch + '_family_trace_and_old_equations', diagnostic['all_kernel_family_trace_error'] < 1e-12 and diagnostic['all_old_moments_preserved_error'] < 1e-12)
        for variant in ['baseline', 'trace_completed', 'overintegrated']:
            path = intake / 'annular-canonical-trace-projection-attempt02' / (branch + '_' + variant + '.npz')
            with numerical.load(path, allow_pickle=False) as arrays:
                check(branch + '_' + variant + '_Cdot_replayed', float(abs(arrays['constraint_rate']).max()) == sample['outcomes'][variant]['constraint_rate_max'])
                if variant != 'baseline':
                    check(branch + '_' + variant + '_every_Cdot_row', abs(arrays['constraint_rate']).max() < 1e-10)
                check(branch + '_' + variant + '_full_boundary_identity', abs(arrays['boundary_prediction'] - arrays['constraint_rate']).max() < 1e-11)
        check(branch + '_actual_kernel_change_checked', sample['actual_kernel_family_change'] < 1e-10)
        if branch != 'GR':
            check('full_Gram_kernel_not_local_substitution', max(sample['kernel_controls'].values()) < 1e-9)
            check('initial_external_drive_gap_was_disclosed', abs(sample['outcomes']['trace_completed']['imposed_inner_mass_drive_gap']) > 1e-9)
        report['outcomes'].append({'branch': branch, 'unchanged_field_outcomes': sample['outcomes'], 'momentum_rate_change': sample['momentum_rate_change'], 'time_link_log_change': sample['time_link_log_change']})
    prepared = control['boundary_preparation']
    report['prepared_MTS'] = prepared
    prepared_directory = intake / 'annular-canonical-trace-boundary-control-attempt01'
    for variant in ['prepared', 'higher']:
        with numerical.load(prepared_directory / ('MTS_' + variant + '_first_jet.npz'), allow_pickle=False) as arrays:
            check(variant + '_all_initial_constraint_rows', max(abs(arrays['constraint']).max(), abs(arrays['constraint_rate']).max()) < 1e-10)
            report[variant + '_sampled_pi_total_variation'] = float(abs(numerical.diff(arrays['field_pi'])).sum())
            radius, geometry = arrays['field_R'], arrays['field_F']
            energy = arrays['field_pi']**2 / (2 * radius**2) + radius**2 * arrays['field_w']**2 / 2
            bulk = arrays['field_mu_r'] / (.1 * numerical.sqrt(geometry)) - numerical.sqrt(geometry) * energy
            report[variant + '_bulk_only_constraint_density_L2_excluding_Gram_point_sources'] = float(numerical.sqrt(arrays['weights'] @ bulk**2))
    check('one_update_boundary_preparation', len(prepared['history']) == 2 and prepared['history'][-1]['iteration'] == 1)
    check('retained_drive_and_clock_conditions', max(abs(prepared[key]) for key in ['parent_inner_mass_drive_gap', 'weak_inner_mass_drive_gap', 'outer_scalar_drive_gap', 'outer_clock_gap']) < 1e-11)
    with numerical.load(prepared_directory / 'MTS_prepared_initial_data.npz', allow_pickle=False) as arrays, numerical.load(intake / 'annular-canonical-inverse-boundary-attempt01/N16_metric_Gram_outer_clock.npz', allow_pickle=False) as old, numerical.load(prepared_directory / 'MTS_preparation_lifts.npz', allow_pickle=False) as lifts:
        check('unchanged_external_drives', numerical.array_equal(arrays['boundary_velocity'], old['boundary_velocity']))
        check('unchanged_chi_and_inner_mass', numerical.array_equal(arrays['configuration'], old['configuration']) and arrays['mass_coefficients'][0] == old['mass_coefficients'][0])
        check('declared_two_global_momentum_lifts', abs(arrays['pi_coefficients'] - old['pi_coefficients'] - lifts['global_cubic_lifts'] @ lifts['amplitudes']).max() < 1e-17)
    check('analytic_mass_J_and_boundary_sensitivity', prepared['analytic_mass_derivative_error'] < 1e-10 and prepared['final_boundary_jacobian_condition'] < 2)
    scripts = ['annular_canonical_trace_context_20260911.py', 'annular_canonical_trace_projection_20260911.py', 'derive_annular_canonical_trace_projection_20260911.py', 'annular_canonical_trace_projection_stable_20260911.py', 'derive_annular_canonical_trace_projection_stable_20260911.py', 'annular_canonical_trace_boundary_data_20260911.py', 'verify_annular_canonical_trace_and_prepare_20260911.py', Path(__file__).name]
    for name in scripts:
        path = root / 'scripts' / name
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    check('eight_scripts_compile_without_bytecode', True)
    note = root / 'DERIVATION-20260911-parent-kernel-trace-projection-and-compatible-MTS-boundary-data.md'
    for citation in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')):
        if citation.endswith(('.py', '.md', '.json', '.npz')):
            check('citation_exists_' + citation, (root / citation).is_file())
    own(note, 'outputs')
    protected = root.parent / 'formalization-workbench'
    check('protected_workbench_exists', protected.is_dir())
    started = datetime.fromisoformat('2026-09-11T22:42:49+00:00').timestamp()
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > started]
    check('protected_changed_count_zero_mtime', not changed, changed)
    report['protected_changed_count'] = len(changed)
    check('no_python_cache', not (root / 'scripts/__pycache__').exists())
    snapshot = intake / 'annular-canonical-trace-resume-snapshot.md'
    if snapshot.exists():
        raise FileExistsError(snapshot)
    snapshot.write_bytes((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    own(snapshot, 'outputs')
    report['state'] = 'complete'
    report['completed_utc'] = datetime.now(timezone.utc).isoformat()
    report['trace_checks'] = len(trace['checks'])
    report['independent_control_checks'] = len(control['checks'])
    destination.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'state': report['state'], 'seal_checks': len(report['checks']), 'trace_checks': report['trace_checks'], 'control_checks': report['independent_control_checks'], 'inputs': len(report['inputs']), 'outputs': len(report['outputs']), 'protected_changed_count': len(changed), 'prepared_Cdot': prepared['constraint_rate_max'], 'prepared_higher_Cdot': prepared['higher_constraint_rate_max'], 'prepared_sampled_pi_TV': report['prepared_sampled_pi_total_variation'], 'bulk_only_L2_excluding_Gram': report['prepared_bulk_only_constraint_density_L2_excluding_Gram_point_sources']}), flush=True)


if __name__ == '__main__':
    run()
