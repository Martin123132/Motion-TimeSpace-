import hashlib
import json
import re
from datetime import datetime
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as np
    import sympy as sp
    from scipy.integrate import quad
    from annular_interface_layer_clock_20260912 import profile

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260912'
    destination = intake / 'annular-interface-layer-clock-final-integrity.json'
    snapshot = intake / 'annular-interface-layer-clock-resume-snapshot.md'
    if destination.exists() or snapshot.exists():
        raise FileExistsError('Completed evidence cannot be overwritten.')
    report = {'state': 'running', 'checks': [], 'inputs': {}, 'outputs': {},
              'valid_for_physics_claim': False, 'full_first_jet_closed': False,
              'full_GR_limit_proven': False, 'new_evolution': False,
              'regulator_choice_parent_signed': False, 'full_scalar_action_descent_proven': False,
              'endpoint_only_log_mean_action_derived': False,
              'horizontal_transport_is_not_proper_clock_gluing': True,
              'conditional_layer_geometry_and_clock_laws_derived': True,
              'protected_scan_scope': 'mtime since 2026-09-12T22:07:09Z, not pre-turn content hashes'}
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
    for number in [1, 2, 3]:
        name = 'annular-interface-layer-clock-attempt' + str(number).zfill(2)
        directory = intake / name
        batch = json.loads((directory / 'status.json').read_text())
        batches[number] = batch
        check(name + '_expected_state', batch['state'] == ('complete' if number == 3 else 'failed'))
        if number == 3:
            check(name + '_validation_checks_passed', all(item['passed'] for item in batch['checks']))
        else:
            check(name + '_failed_validator_preserved', any(not item['passed'] for item in batch['checks']) and bool(batch['error']))
        check(name + '_no_physics_promotion', not batch['valid_for_physics_claim'] and not batch['full_first_jet_closed'] and not batch['full_scalar_action_descent_proven'])
        for table in ['inputs', 'outputs']:
            for filename, expected in batch[table].items():
                if digest(root / filename) != expected:
                    raise RuntimeError('Changed evidence: ' + filename)
                if filename in report['inputs'] and report['inputs'][filename] != expected:
                    raise RuntimeError('Conflicting evidence hash: ' + filename)
                report['inputs'][filename] = expected
        for path in directory.iterdir():
            if not path.is_file():
                continue
            own(path, 'outputs')
            if path.name.startswith('executed-'):
                check(name + '_executed_source_matches', digest(path) == digest(root / 'scripts' / path.name.removeprefix('executed-')))
            if path.suffix == '.npz':
                with np.load(path, allow_pickle=False) as arrays:
                    check(name + '_' + path.name + '_finite_arrays', all(np.isfinite(arrays[key]).all() for key in arrays.files))
    completed = batches[3]
    check('complete_matched_and_manufactured_matrix', len(completed['layers']) == 54 and len(completed['action_controls']) == 432)
    check('source_values_not_retuned_for_layer_shapes', len(completed['sources']) == 3 and all(len({row['energy'] for row in completed['layers'] if row['branch'] == source['branch']}) == 1 for source in completed['sources']))
    independent = []
    for row in completed['layers']:
        center, width, energy = row['radius'], row['width'], row['energy']
        name = row['profile']
        def exponent(fraction):
            return quad(lambda point: .1 * energy * profile(point, name) / (center + width * (point - .5)), 0, fraction, epsabs=2e-14, epsrel=2e-13)[0]
        source_integral = quad(lambda fraction: .1 * energy * profile(fraction, name) * np.exp(2 * exponent(fraction)), 0, 1, epsabs=2e-14, epsrel=2e-13)[0]
        final_mass = np.exp(-2 * exponent(1.)) * (row['mass_left'] + source_integral)
        prefix = row['branch'] + '_' + name + '_' + str(row['width_index'])
        check(prefix + '_independent_linear_integrating_factor_solution', abs(final_mass - row['mass_right']) < 1e-10)
        path = intake / 'annular-interface-layer-clock-attempt03' / (prefix + '_layer.npz')
        with np.load(path, allow_pickle=False) as arrays:
            weights, radii, root_f, mass = arrays['weights'] * width, arrays['R'], arrays['U'], arrays['mu']
            sigma = weights @ (root_f * arrays['rho'])
            radial_boundary = (center + width / 2) * row['root_right'] - (center - width / 2) * row['root_left_actual']
            jump_identity = .1 * sigma + radial_boundary - weights @ ((root_f + 1 / root_f) / 2)
            momentum_identity = row['lapse_left'] / .1 * (1 / row['root_right'] - 1 / row['root_left_actual'])
            momentum_identity += 2 * row['lapse_left'] / .1 * (weights @ (mass / (radii**2 * root_f**3)))
            check(prefix + '_independent_finite_width_jump_and_impulse_integrals', max(abs(jump_identity), abs(momentum_identity - row['P1_integral']), abs(sigma - row['source_sigma'])) < 1e-10)
            independent.append({'case': prefix, 'mass_integrating_factor_error': float(abs(final_mass - row['mass_right'])), 'finite_jump_identity_error': float(abs(jump_identity)), 'momentum_integral_identity_error': float(abs(momentum_identity - row['P1_integral']))})
    zeta, impulse, background = sp.symbols('zeta impulse background', real=True)
    U_ratio = sp.exp(background - zeta)
    N_ratio = sp.exp(background + zeta - impulse)
    horizontal = sp.exp(impulse)
    proper_map = 1 / N_ratio
    check('symbolic_distinct_clock_maps', sp.simplify(horizontal * N_ratio - sp.exp(background + zeta)) == 0 and sp.simplify(proper_map / horizontal - sp.exp(-background - zeta)) == 0)
    check('proper_clock_pullback_and_radial_density_factor', sp.simplify(proper_map * N_ratio - 1) == 0 and sp.simplify(proper_map * N_ratio * U_ratio - U_ratio) == 0)
    left_lapse, left_root, ratio, velocity = sp.symbols('left_lapse left_root ratio velocity', positive=True)
    induced_left = -left_lapse**2 + velocity**2 / left_root**2
    induced_right_pulled_back = -left_lapse**2 / ratio**2 + velocity**2 / (ratio**2 * left_root**2)
    check('horizontal_map_is_not_generic_timelike_surface_gluing', sp.simplify(induced_right_pulled_back - induced_left / ratio**2) == 0)
    points, weights = np.polynomial.legendre.leggauss(96)
    fraction, weights = (points + 1) / 2, weights / 2
    counterexamples = []
    for source in completed['sources']:
        zeta_value = .1 * source['energy'] / source['radius']
        left_root = np.sqrt(1 - 2 * source['mass_left'] / source['radius'])
        baseline = left_root * np.exp(-zeta_value * fraction)
        alternative = baseline * (1 + .1 * fraction * (1 - fraction))
        mean_difference = weights @ (alternative - baseline)
        action_difference = source['lapse_left'] * source['energy'] * mean_difference
        check(source['branch'] + '_same_traces_do_not_determine_off_shell_matter_action', mean_difference > .001 and action_difference > 1e-8)
        counterexamples.append({'branch': source['branch'], 'same_endpoint_values': [float(left_root), float(left_root * np.exp(-zeta_value))], 'off_shell_shape_amplitude_not_physical_fit': .1, 'mean_difference': float(mean_difference), 'Hamiltonian_difference': float(action_difference), 'profiles_need_not_satisfy_same_constraints_off_shell': True})
    report['off_shell_counterexamples'] = counterexamples
    report['independent_layer_controls'] = independent
    report['completed_run_checks'] = len(completed['checks'])
    report['completed_cases'] = len(completed['layers'])
    report['compact_action_variations'] = len(completed['action_controls']) * 2
    report['maximum_lapse_action_error'] = max(row['lapse_action_constraint_error'] for row in completed['action_controls'])
    report['maximum_mass_action_error'] = max(row['mass_action_force_error'] for row in completed['action_controls'])
    report['actual_source_summary'] = [source for source in completed['sources'] if source['parent_path']]
    report['thinnest_cases'] = [row for row in completed['layers'] if row['width_index'] == 5]
    files = ['annular_interface_layer_clock', 'annular_interface_layer_bounds', 'derive_annular_interface_layer_clock', 'derive_annular_interface_layer_clock_scaled', 'derive_annular_interface_layer_clock_bounded', 'verify_annular_interface_layer_clock']
    for stem in files:
        path = root / 'scripts' / (stem + '_20260912.py')
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    check('six_new_scripts_compile_without_bytecode', True)
    note = root / 'DERIVATION-20260912-interface-logarithmic-trace-and-distinct-clock-maps.md'
    for citation in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')):
        if citation.endswith(('.py', '.md', '.json', '.npz')):
            check('cited_path_exists_' + citation, (root / citation).is_file())
    own(note, 'outputs')
    protected = root.parent / 'formalization-workbench'
    check('protected_workbench_exists', protected.is_dir())
    start = datetime.fromisoformat('2026-09-12T22:07:09+00:00').timestamp()
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > start]
    check('protected_mtime_modified_count_zero', not changed, changed)
    check('no_python_cache', not (root / 'scripts/__pycache__').exists())
    snapshot.write_bytes((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    own(snapshot, 'outputs')
    report['protected_modified_count'] = len(changed)
    report['state'] = 'complete'
    destination.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'state': 'complete', 'seal_checks': len(report['checks']), 'run_checks': report['completed_run_checks'], 'layers': report['completed_cases'], 'compact_action_variations': report['compact_action_variations'], 'max_lapse_action_error': report['maximum_lapse_action_error'], 'max_mass_action_error': report['maximum_mass_action_error'], 'max_independent_mass_error': max(row['mass_integrating_factor_error'] for row in independent), 'max_finite_jump_error': max(row['finite_jump_identity_error'] for row in independent), 'max_momentum_integral_error': max(row['momentum_integral_identity_error'] for row in independent), 'proper_clock_gluing_equals_horizontal_transport': False, 'full_first_jet_closed': False, 'protected_modified_count': len(changed)}), flush=True)


if __name__ == '__main__':
    run()
