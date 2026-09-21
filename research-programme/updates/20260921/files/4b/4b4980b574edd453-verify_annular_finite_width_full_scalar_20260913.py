import hashlib
import json
import re
import traceback
from datetime import datetime
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as np
    from annular_nonlinear_history_20260912 import ManufacturedHistory
    from annular_finite_width_full_scalar_20260913 import FiniteWidthScalar, TranslatedScalarAction, LayerModeHistory, smear_rule

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260913'
    destination = intake / 'annular-finite-width-full-scalar-final-integrity.json'
    snapshot = intake / 'annular-finite-width-full-scalar-resume-snapshot.md'
    if destination.exists() or snapshot.exists():
        raise FileExistsError('Completed or failed evidence cannot be overwritten.')
    report = {'state': 'running', 'checks': [], 'inputs': {}, 'outputs': {},
              'independent_layer_mode_cases': [], 'independent_endpoint_cases': [],
              'valid_for_physics_claim': False, 'new_spacetime_evolution': False,
              'full_first_jet_closed': False, 'full_GR_limit_proven': False,
              'unique_parent_regularizer_derived': False,
              'full_physical_radial_port_action_signed': False,
              'off_shell_complete_quadratic_scalar_regularization_constructed': True,
              'manufactured_history_tests_not_coupled_initial_data': True,
              'expanded_scalar_layer_phase_not_identical_to_old_17_pairs': True,
              'protected_scan_scope': 'mtime since 2026-09-12T23:36:27Z; not pre-turn content hashes'}
    hashes = {}

    def save():
        destination.write_text(json.dumps(report, indent=2) + '\n')

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

    def derivative_control(evaluate):
        actual = evaluate(0.)
        differences = []
        for step in [2e-4, 1e-4]:
            differences.append((evaluate(step)['action'] - evaluate(-step)['action']) / (2 * step))
        extrapolated = (4 * differences[1] - differences[0]) / 3
        return {'finite_difference': float(extrapolated), 'raw': actual['raw'],
                'action_derivative_error': float(abs(extrapolated - actual['raw'])),
                'adjoint_error': float(abs(actual['raw'] - actual['adjoint'])),
                'minimum_F': actual['minimum_F'], 'minimum_J': actual['minimum_J'],
                'minimum_chart_d': actual['minimum_chart_d']}

    save()
    try:
        batches = {}
        for number in [1, 2]:
            directory = intake / ('annular-finite-width-full-scalar-attempt' + str(number).zfill(2))
            batch = json.loads((directory / 'status.json').read_text())
            batches[number] = batch
            check(directory.name + '_expected_state', batch['state'] == ('failed' if number == 1 else 'complete'))
            for flag in ['valid_for_physics_claim', 'new_spacetime_evolution', 'full_first_jet_closed', 'full_GR_limit_proven', 'unique_parent_regularizer_derived', 'full_physical_radial_port_action_signed']:
                check(directory.name + '_' + flag + '_remains_false', batch[flag] is False)
            if number == 1:
                check('failed_asymmetric_validator_retained', 'GR_beta23_smooth_point_limit_not_constraint_pass' in batch['error'] and any(not item['passed'] for item in batch['checks']))
            else:
                check('completed_sixty_checks_pass', len(batch['checks']) == 60 and all(item['passed'] for item in batch['checks']))
            verified = 0
            for table in ['inputs', 'outputs']:
                for filename, expected in batch[table].items():
                    if digest(root / filename) != expected:
                        raise RuntimeError('Changed evidence: ' + filename)
                    if filename in report['inputs'] and report['inputs'][filename] != expected:
                        raise RuntimeError('Conflicting evidence hash: ' + filename)
                    report['inputs'][filename] = expected
                    verified += 1
            check(directory.name + '_all_inherited_hashes_match', verified > 0, verified)
            for path in directory.iterdir():
                if not path.is_file():
                    continue
                own(path, 'outputs')
                if path.name.startswith('executed-'):
                    check(directory.name + '_' + path.name + '_matches', digest(path) == digest(root / 'scripts' / path.name.removeprefix('executed-')))
                if path.suffix == '.npz':
                    with np.load(path, allow_pickle=False) as arrays:
                        check(directory.name + '_' + path.name + '_finite_arrays', all(np.isfinite(arrays[key]).all() for key in arrays.files))
                        check(directory.name + '_' + path.name + '_positive_live_energy', arrays['energy'].min() > 0 and arrays['weights'].min() > 0 and abs(arrays['weights'].sum() - 1) < 1e-13)
        completed = batches[2]
        for key, count in [('variation_cases', 10), ('proper_clock_cases', 2), ('covariance_cases', 2), ('point_limit_cases', 16), ('energy_density_cases', 8), ('layer_mode_cases', 2)]:
            check('complete_' + key, len(completed[key]) == count)
        for branch in ['GR', 'metric_Gram']:
            check(branch + '_same_five_variations', len([row for row in completed['variation_cases'] if row['branch'] == branch]) == 5)
            for shape in ['beta22', 'beta23']:
                rows = [row for row in completed['point_limit_cases'] if row['branch'] == branch and row['shape'] == shape]
                finest = min(rows, key=lambda row: row['width'])
                check(branch + '_' + shape + '_first_moment_remainder_small', max(finest['action_after_derived_first_moment'], finest['variation_after_derived_first_moment']) < 1e-9)
                if shape == 'beta23':
                    check(branch + '_nonzero_asymmetric_displacement_not_hidden', min(finest['action_point_error'], finest['variation_point_error']) > 1e-8 and finest['first_translation_moment'] == -.1)
        for shape, expected_mean in [('beta22', 0.), ('beta23', -.1)]:
            offsets, weights = smear_rule(12, shape)
            check(shape + '_independent_normalization_and_mean', max(abs(weights.sum() - 1), abs(weights @ offsets - expected_mean)) < 1e-13)
        history = ManufacturedHistory(soluble=False)
        width = 1 / 128
        for gram in [False, True]:
            branch = 'GR' if not gram else 'metric_Gram'
            mode = FiniteWidthScalar(LayerModeHistory(history), gram, width, smear_order=8)
            result = derivative_control(lambda amplitude: mode.integrated([0, 0, 0, 1], amplitude, time_order=18))
            result['branch'] = branch
            check(branch + '_hidden_layer_mode_independent_action_difference', result['action_derivative_error'] < 1e-8 and result['adjoint_error'] < 1e-10 and abs(result['raw']) > 1e-8, result)
            report['independent_layer_mode_cases'].append(result)
            for displacement in [-width / 2, width / 2]:
                action = TranslatedScalarAction(history, gram, displacement)
                result = derivative_control(lambda amplitude: action.full_integrated([1, 1, 1, 1], amplitude, order=18))
                result.update({'branch': branch, 'displacement': displacement})
                check(branch + '_support_endpoint_' + str(displacement) + '_independent_action_difference', result['action_derivative_error'] < 1e-8 and result['adjoint_error'] < 1e-10 and min(result[key] for key in ['minimum_F', 'minimum_J', 'minimum_chart_d']) > 0, result)
                report['independent_endpoint_cases'].append(result)
            print(json.dumps({'branch': branch, 'independent_layer_and_support_endpoint_checks': 'complete'}), flush=True)
            save()
        check('temporal_boundaries_not_declared_silent', max(abs(row['spatial_time_boundary']) for row in completed['variation_cases']) > 1e-9 and max(abs(row['kinetic_time_boundary']) for row in completed['variation_cases']) > 1e-9)
        for stem in ['annular_finite_width_full_scalar', 'derive_annular_finite_width_full_scalar', 'derive_annular_finite_width_full_scalar_moments', 'verify_annular_finite_width_full_scalar']:
            path = root / 'scripts' / (stem + '_20260913.py')
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('four_new_scripts_compile_without_bytecode', True)
        note = root / 'DERIVATION-20260913-off-shell-finite-width-action-and-clock-coframe.md'
        for citation in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')):
            if citation.endswith(('.py', '.md', '.json', '.npz')):
                check('cited_path_exists_' + citation, (root / citation).is_file())
        own(note, 'outputs')
        protected = root.parent / 'formalization-workbench'
        check('protected_workbench_exists', protected.is_dir())
        start = datetime.fromisoformat('2026-09-12T23:36:27+00:00').timestamp()
        changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > start]
        check('protected_mtime_modified_count_zero', not changed, changed)
        check('no_python_cache', not (root / 'scripts/__pycache__').exists())
        snapshot.write_bytes((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
        own(snapshot, 'outputs')
        report['protected_modified_count'] = len(changed)
        report['completed_run_checks'] = len(completed['checks'])
        report['maximum_action_derivative_error'] = max(row['action_derivative_error'] for row in completed['variation_cases'])
        report['maximum_independent_derivative_error'] = max(row['action_derivative_error'] for row in report['independent_layer_mode_cases'] + report['independent_endpoint_cases'])
        report['maximum_proper_clock_action_error'] = max(row['difference'] for row in completed['proper_clock_cases'])
        report['maximum_live_energy_variation_error'] = max(row['density_variation_error'] for row in completed['energy_density_cases'])
        report['state'] = 'complete'
        save()
        print(json.dumps({key: report[key] for key in ['state', 'completed_run_checks', 'maximum_action_derivative_error', 'maximum_independent_derivative_error', 'maximum_proper_clock_action_error', 'maximum_live_energy_variation_error', 'protected_modified_count', 'full_first_jet_closed']} | {'seal_checks': len(report['checks'])}), flush=True)
    except Exception as error:
        report.update({'state': 'failed', 'error': repr(error), 'traceback': traceback.format_exc()})
        save()
        raise


if __name__ == '__main__':
    run()
