import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as np
    from scipy.linalg import lstsq
    from annular_canonical_common_profile_aligned_20260912 import CommonProfile
    from annular_covariant_joint_preparation_20260912 import JointPreparation

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260912'
    target = intake / 'annular-covariant-joint-final-integrity.json'
    snapshot = intake / 'annular-covariant-joint-resume-snapshot.md'
    if target.exists() or snapshot.exists():
        raise FileExistsError('Seals and snapshots are immutable.')
    report = {'state': 'running', 'checks': [], 'inputs': {}, 'outputs': {}, 'valid_for_physics_claim': False, 'new_evolution': False, 'interval_certificate': False, 'full_first_jet_closed': False, 'full_second_jet_closed': False, 'full_GR_limit_proven': False, 'joint_initial_compatibility_solved': True, 'boundary_energy_law_derived': True, 'scalar_ports_parent_signed_full_histories': False, 'row_fitted_scalar_forces_adopted': False, 'working_numerical_branch': 'annular-acceleration-trace-completion-attempt02', 'protected_scan_scope': 'mtime since 2026-09-12T19:13:07Z, not a pre-turn content snapshot'}
    hashes = {}

    def digest(path):
        if path not in hashes:
            hashes[path] = hashlib.sha256(path.read_bytes()).hexdigest()
        return hashes[path]

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = digest(path)

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        if not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    batches = {}
    for name in ['annular-covariant-joint-preparation-attempt01', 'annular-covariant-joint-control-attempt01']:
        directory = intake / name
        batch = json.loads((directory / 'status.json').read_text())
        batches[name] = batch
        check(name + '_completed_all_validation_checks', batch['state'] == 'complete' and all(row['passed'] for row in batch['checks']))
        check(name + '_no_physics_or_second_jet_claim', not batch['valid_for_physics_claim'] and not batch['new_evolution'] and not batch['full_second_jet_closed'] and not batch['interval_certificate'])
        for table in ['inputs', 'outputs']:
            for name_input, expected in batch[table].items():
                if digest(root / name_input) != expected:
                    raise RuntimeError('Changed immutable evidence: ' + name_input)
                if name_input in report['inputs'] and report['inputs'][name_input] != expected:
                    raise RuntimeError('Conflicting source signature: ' + name_input)
                report['inputs'][name_input] = expected
        for path in directory.iterdir():
            if not path.is_file():
                continue
            own(path, 'outputs')
            if path.name.startswith('executed-'):
                check(name + '_executed_runner_matches', digest(path) == digest(root / 'scripts' / path.name.removeprefix('executed-')))
            if path.suffix == '.npz':
                with np.load(path, allow_pickle=False) as arrays:
                    check(name + '_' + path.name + '_all_numeric_arrays_finite', all(np.isfinite(arrays[key]).all() for key in arrays.files))
    check('unique_inherited_evidence_hashes_match', True, {'unique_files': len(report['inputs'])})
    initial = batches['annular-covariant-joint-preparation-attempt01']
    control = batches['annular-covariant-joint-control-attempt01']
    for case in initial['cases']:
        check(case['branch'] + '_joint_C0_solved_without_promoting_full_first_jet', all(row['C0_max'] < 1e-10 and not row['full_first_jet_gate'] for row in case['quadratures']))
        check(case['branch'] + '_nonzero_projected_mass_flux_defect_kept', all(row['all_endpoint_mass_projection_defect'] > 1e-10 for row in case['quadratures']))
        check(case['branch'] + '_unchanged_scalar_inner_mass_and_nontrivial_dependent_p', case['scalar_profile_change'] == 0 and abs(case['inner_mass_change']) < 1e-14 and case['momentum_change_max'] > .1)
    for case in control['cases']:
        prefix = case['branch'] + '_' + case['quadrature']
        check(prefix + '_final_derived_port_candidate_fails_unchanged_gate', case['C1_energy_balanced_ports_max'] > 1e-10 and not case['first_jet_gate'] and not case['port_histories_parent_signed'])
        check(prefix + '_Ward_corrected_not_omitting_source_power', case['corrected_Ward_reconstruction'] < 1e-11 and case['retained_radial_port_work_max'] > .01)
        check(prefix + '_independent_controls_resolve_equation_not_trajectory', case['direct_constraint_curve_error'] < 1e-12 and case['metric_force_variation_max'] < 1e-11)
        check(prefix + '_negative_controls_detect_missing_terms', case['untransported_scalar_density_negative_control'] > 1e-6 and case['omit_connection_load_negative_control'] > 1e-7)
    common = CommonProfile(root)
    source_checks = []
    for branch in ['GR', 'metric_Gram']:
        model = JointPreparation(common, branch)
        path = intake / 'annular-covariant-joint-preparation-attempt01' / (branch + '_joint_candidate.npz')
        with np.load(path, allow_pickle=False) as arrays:
            new_momentum = arrays['momentum']
            scalar = arrays['scalar']
        free = common.physical_free(model.radii)
        coefficients, unused_residual, rank, unused_singular = lstsq(model.momentum_lifts, new_momentum - free['pi'])
        error = float(abs(new_momentum - free['pi'] - model.momentum_lifts @ coefficients).max())
        check(branch + '_actual_common_free_profile_retained_modulo_declared_boundary_lifts', error < 1e-11 and rank == 2 and abs(scalar - free['chi']).max() < 1e-13, {'reconstruction_error': error, 'total_common_profile_boundary_amplitudes': coefficients.tolist()})
        source_checks.append({'branch': branch, 'free_profile_error': error, 'total_common_profile_boundary_amplitudes': coefficients.tolist()})
    stems = ['annular_covariant_joint_preparation', 'derive_annular_covariant_joint_preparation', 'verify_annular_covariant_joint_preparation', 'seal_annular_covariant_joint']
    for stem in stems:
        path = root / 'scripts' / (stem + '_20260912.py')
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    check('four_new_scripts_compile_without_bytecode', True)
    note = root / 'DERIVATION-20260912-joint-covariant-initial-data-and-boundary-energy-law.md'
    for citation in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')):
        if citation.endswith(('.py', '.md', '.json', '.npz')):
            check('source_path_exists_' + citation, (root / citation).is_file())
    own(note, 'outputs')
    protected = root.parent / 'formalization-workbench'
    check('protected_workbench_exists', protected.is_dir())
    start = datetime.fromisoformat('2026-09-12T19:13:07+00:00').timestamp()
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > start]
    check('protected_modified_count_zero_mtime', not changed, changed)
    check('no_python_cache', not (root / 'scripts/__pycache__').exists())
    snapshot.write_bytes((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    own(snapshot, 'outputs')
    report['run_check_counts'] = {name: len(batch['checks']) for name, batch in batches.items()}
    report['initial_cases'] = initial['cases']
    report['final_derived_port_cases'] = control['cases']
    report['source_profile_controls'] = source_checks
    report['protected_modified_count'] = len(changed)
    report['state'] = 'complete'
    report['completed_utc'] = datetime.now(timezone.utc).isoformat()
    target.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'state': report['state'], 'seal_checks': len(report['checks']), 'run_checks': report['run_check_counts'], 'source_profile_controls': source_checks, 'protected_modified_count': len(changed), 'physics_claim': False, 'full_first_jet_closed': False}), flush=True)


if __name__ == '__main__':
    run()
