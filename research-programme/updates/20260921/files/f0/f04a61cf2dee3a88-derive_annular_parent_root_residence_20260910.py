import argparse
import hashlib
import json
import re
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import scipy
    import sympy as symbolic
    from scipy.linalg import solve
    from annular_adm_mixed_action_20260909 import MixedActionBasis
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_gram_joint_action_20260909 import gram_matrices
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian
    from annular_paired_variational_energy_20260910 import scalar_maps
    from annular_parent_coefficient_box_20260910 import Box
    from annular_parent_root_residence_20260910 import canonical_maps, action_enclosure, root_inclusion, parameter_root_tube

    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['derive', 'seal'])
    parser.add_argument('--attempt', default='derived')
    parser.add_argument('--limit', type=int, default=0)
    arguments = parser.parse_args()
    if not re.fullmatch('[a-z0-9-]+', arguments.attempt) or arguments.limit < 0:
        raise ValueError('Invalid attempt/limit.')
    root = Path(__file__).resolve().parents[1]
    old = root / 'source-intake/navier-stokes/20260909'
    intake = root / 'source-intake/navier-stokes/20260910'
    destination = intake / ('annular-parent-root-residence-' + arguments.attempt)
    prior_path = intake / 'annular-parent-coefficient-box-final-integrity.json'
    final_path = intake / 'annular-parent-root-residence-final-integrity.json'
    inputs, outputs = {}, {}

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def own(path):
        inputs[str(path.relative_to(root))] = digest(path)

    def artifact(path):
        outputs[str(path.relative_to(root))] = digest(path)

    def inherit(table, inherited):
        for name, expected in inherited.items():
            actual = digest(root / name)
            if actual != expected or name in table and table[name] != actual:
                raise RuntimeError('Changed evidence: ' + name)
            table[name] = actual

    def loaded(path):
        own(path)
        with numerical.load(path) as handle:
            return {name: handle[name].copy() for name in handle.files}

    prior = json.loads(prior_path.read_text())
    if prior['state'] != 'complete':
        raise RuntimeError('Prior gate incomplete.')
    inherit(inputs, prior['inputs'])
    inherit(outputs, prior['outputs'])
    own(prior_path)
    for name in ['annular_parent_root_residence_20260910.py', 'derive_annular_parent_root_residence_20260910.py']:
        path = root / 'scripts' / name
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    if arguments.phase == 'derive':
        destination.mkdir(exist_ok=False)
        for name in ['annular_parent_root_residence_20260910.py', 'derive_annular_parent_root_residence_20260910.py']:
            output = destination / ('executed-' + name)
            output.write_bytes((root / 'scripts' / name).read_bytes())
            artifact(output)
        report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': inputs, 'outputs': outputs, 'checks': [], 'samples': [], 'probe_limit': arguments.limit, 'original_states_unchanged': True, 'new_numerical_evolution': False, 'entire_saved_trajectory_validated': False, 'higher_jet_box_residence_verified': False, 'boundary_TV_transfer_verified': False, 'all_shift_equations_verified': False, 'valid_for_physics_claim': False, 'scope': 'Parameterized free-constraint roots and local reduced-DAE existence/residence in finite real action with original stored assembly maps; inner shift drives inner mass only. Not a solution certificate for all shift equations. Outward primitives under inherited IEEE assumptions; no continuum or all-mesh claim.'}

        def save():
            (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

        def check(name, passed, detail=None):
            report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
            if not passed:
                raise RuntimeError('Failed check: ' + name + ' ' + repr(detail))

        report['runtime'] = {'python': sys.version, 'numpy': numerical.__version__, 'scipy': scipy.__version__, 'sympy': symbolic.__version__}
        save()
        try:
            scalar_center, scalar_radius = numerical.array([1.4]), numerical.array([.1])
            scalar_domain = Box(scalar_center) + Box(-scalar_radius, scalar_radius)
            scalar_jacobian = 2 * scalar_domain[None, :]
            scalar = root_inclusion(scalar_center, Box(scalar_center)**2 - 2, scalar_jacobian, scalar_radius)
            check('known_scalar_root_strict_inclusion', scalar['gate'])
            check('known_scalar_root_enclosed', scalar['root'].lo[0] <= numerical.sqrt(2.) <= scalar['root'].hi[0])
            absent = root_inclusion(scalar_center, Box(scalar_center)**2 + 1, scalar_jacobian, scalar_radius)
            check('no_root_inclusion_refused', not absent['gate'])
            for invalid_width in [0., -1., numerical.nan]:
                try:
                    root_inclusion(numerical.array([1.4]), Box(numerical.array([0.])), Box(numerical.array([[1.]])), numerical.array([invalid_width]))
                except ValueError:
                    rejected = True
                else:
                    rejected = False
                check('invalid_root_radius_refused_' + str(invalid_width), rejected)
            case_path = old / 'annular-constraint-correction-initial/canonical.json'
            parent_path = intake / 'annular-parent-coefficient-box-attempt02/status.json'
            own(case_path)
            own(parent_path)
            case = json.loads(case_path.read_text())
            constants = {name: float(symbolic.sympify(value)) for name, value in case['parameters'].items()}
            kappa = float(symbolic.sympify(case['normalization_kappa']))
            samples = json.loads(parent_path.read_text())['samples']
            if arguments.limit:
                samples = samples[:arguments.limit]
            for sample in samples:
                label, intervals, branch = sample['label'], sample['intervals'], sample['branch']
                report['active_sample'] = label
                save()
                print('Starting ' + label, flush=True)
                tag, index = label.split('_sample')[0], int(label.rsplit('sample', 1)[1])
                steps = 64 if intervals == 64 else 32
                initial = loaded(old / 'annular-released-Hermite-initial-derived' / (tag + '.npz'))
                folder = 'annular-boundary-N64-evolution-smoke' if intervals == 64 else 'annular-released-Hermite-evolution-smoke'
                trajectory = loaded(old / folder / (tag + '_steps' + str(steps) + '.npz'))
                basis = MixedActionBasis(initial['radius'])
                count = basis.radii.size
                time, state = trajectory['time'][index], trajectory['state'][index]
                scalar_values, slope, momentum, slope_momentum = [state[part * count:(part + 1) * count] for part in range(4)]
                packed = state[4 * count:]
                system = ReleasedHermiteRouthian(basis, scalar_values, slope, constants, kappa, momentum, slope_momentum, initial['outer_clock'][0] + time * initial['outer_clock'][1], MetricLinkQuadrature(basis))
                system.residence_clock_rate = initial['outer_clock'][1]
                endpoint_acceleration = initial['endpoint_acceleration']
                attempts = []
                report['active_parameter_attempts'] = attempts
                for parameter_width in [1e-8, 1e-9, 1e-10, 1e-11, 1e-12]:
                    time_horizon = 100 * parameter_width
                    data = parameter_root_tube(system, packed, parameter_width, time_horizon, endpoint_acceleration, branch != 'GR')
                    attempts.append({'relative_parameter_width': parameter_width, 'time_horizon': time_horizon, 'gate': data['gate'], 'contraction': data['inclusion']['contraction'], 'inclusion_ratio': data['inclusion']['inclusion_ratio']})
                    save()
                    print(json.dumps(attempts[-1]), flush=True)
                    if data['gate']:
                        break
                else:
                    raise RuntimeError('No tested parameterized root tube closes.')
                check(label + '_parameterized_root_strict_inclusion', data['inclusion']['gate'] and data['inclusion']['inclusion_ratio'] < 1)
                check(label + '_initial_root_strict_inclusion', data['initial']['gate'] and data['initial']['inclusion_ratio'] < 1)
                check(label + '_unique_root_contraction', data['inclusion']['contraction'] < 1)
                check(label + '_positive_chart_throughout_root_tube', data['minimum_F'] > 0 and data['minimum_N'] > 0)
                check(label + '_positive_residence_time', 0 < data['residence_time'] < data['time_horizon'])
                dynamic = data['distance_lower'] > 0
                check(label + '_strict_coordinate_first_exit_bound', numerical.all(data['displacement_upper'][dynamic] < data['distance_lower'][dynamic]))
                check(label + '_zero_width_momenta_invariant', numerical.all(data['vector_field'].magnitude[data['constant_coordinate_indices']] == 0))
                check(label + '_initial_fixed_data_unchanged', numerical.array_equal(data['initial_root_box'].lo[system.fixed], packed[system.fixed]) and numerical.array_equal(data['initial_root_box'].hi[system.fixed], packed[system.fixed]))
                check(label + '_inner_shift_inverse_verified', data['shift_diagnostic']['componentwise_majorant_verified'])
                check(label + '_initial_root_bounded_not_overwritten', data['initial']['maximum_correction'] < 1e-6)
                original_residual = system.evaluate(packed, branch != 'GR', hessian=False)[1][system.free]
                agreement = float(max(abs(original_residual - data['initial_residual'].midpoint)))
                check(label + '_rounded_original_evaluator_agrees', agreement < 1e-8)
                configuration_point = numerical.concatenate([scalar_values, slope])
                momentum_point = numerical.concatenate([momentum, slope_momentum])
                point = action_enclosure(system, Box(packed), Box(configuration_point), Box(momentum_point), Box(system.outer_clock), branch != 'GR')
                original_jacobian = system.evaluate(packed, branch != 'GR')[2]
                jacobian_difference = float(abs(original_jacobian - point['jacobian'].midpoint).max())
                check(label + '_rounded_original_Hessian_agrees', jacobian_difference < 1e-8)
                original_force = numerical.concatenate([system.scalar_force(packed, branch != 'GR'), system.slope_force(packed, branch != 'GR')])
                original_force[[0, count - 1]] = 0.
                force_difference = float(abs(original_force - point['momentum_rate'].midpoint).max())
                check(label + '_rounded_original_canonical_force_agrees', force_difference < 1e-8)
                tangent = system.constraint_tangent(data['initial_root_box'].midpoint, branch != 'GR', endpoint_acceleration, system.residence_clock_rate)
                shift_residual_max = float(abs(tangent['shift_residual']).max())
                value_map, gradient_map = canonical_maps(basis)
                polynomial = scalar_maps(basis, basis.quadrature)
                map_differences = [float(max(abs(value_map - polynomial[0]).ravel())), float(max(abs(gradient_map - polynomial[1]).ravel()))]
                corner_residuals = []
                for corner in range(2):
                    endpoint = 'lo' if corner == 0 else 'hi'
                    configuration = getattr(data['configuration_box'], endpoint)
                    momenta = getattr(data['momentum_box'], endpoint)
                    local_time = corner * data['time_horizon']
                    trial = packed.copy()
                    trial[system.fixed] = getattr(data['root_box'], endpoint)[system.fixed]
                    changed = ReleasedHermiteRouthian(basis, configuration[:count], configuration[count:], constants, kappa, momenta[:count], momenta[count:], system.outer_clock + system.residence_clock_rate * local_time, system.links)
                    for iteration in range(5):
                        unused, gradient, jacobian = changed.evaluate(trial, branch != 'GR')
                        correction = solve(jacobian[numerical.ix_(system.free, system.free)], -gradient[system.free], assume_a='sym')
                        trial[system.free] += correction
                    final_residual = float(max(abs(changed.evaluate(trial, branch != 'GR', hessian=False)[1][system.free])))
                    corner_residuals.append(final_residual)
                    check(label + '_independent_corner_Newton_residual_' + str(corner), final_residual < 1e-8)
                    tolerance = 2e-10 * (1 + abs(trial))
                    check(label + '_rounded_corner_root_consistency_' + str(corner), numerical.all(trial >= data['root_box'].lo - tolerance) and numerical.all(trial <= data['root_box'].hi + tolerance))
                arrays = {}
                for name in ['initial_root_box', 'initial_residual', 'root_box', 'configuration_box', 'momentum_box', 'dynamic_box', 'vector_field', 'jacobian_box']:
                    arrays[name + '_lower'], arrays[name + '_upper'] = data[name].lo, data[name].hi
                for name in ['distance_lower', 'displacement_upper', 'constant_coordinate_indices', 'original_packed']:
                    arrays[name] = data[name]
                for name in ['preconditioner', 'majorant', 'search_radii', 'image_bound']:
                    arrays['root_' + name] = data['inclusion'][name]
                arrays['parameter_residual_lower'] = data['inclusion']['residual_box'].lo
                arrays['parameter_residual_upper'] = data['inclusion']['residual_box'].hi
                arrays['original_configuration'], arrays['original_momenta'] = configuration_point, momentum_point
                arrays['affine_clock'] = numerical.array([system.outer_clock, system.residence_clock_rate])
                arrays['endpoint_acceleration'] = endpoint_acceleration
                arrays['free_indices'], arrays['fixed_indices'] = system.free, system.fixed
                arrays['kappa_rational'] = numerical.array([1, 10])
                arrays['include_gram'] = numerical.array(branch != 'GR')
                arrays['assembly_value_map'], arrays['assembly_gradient_map'] = value_map, gradient_map
                arrays['local_action_maps'], arrays['nodal_action_maps'] = numerical.stack(system.maps), numerical.stack(system.node_maps)
                arrays['gram_factors'], arrays['gram_sampling'] = gram_matrices(count)
                for name in ['radii', 'faces', 'quadrature', 'quadrature_weights', 'spacing', 'face_value', 'face_gradient', 'face_to_node', 'node_value']:
                    arrays['basis_' + name] = numerical.asarray(getattr(basis, name))
                for name in ['factor', 'node', 'tweight', 'sweight', 'points', 'weights', 'pairs', 'face_value', 'node_value']:
                    arrays['links_' + name] = getattr(system.links, name)
                output = destination / (label + '.npz')
                numerical.savez_compressed(output, **arrays)
                with numerical.load(output) as saved:
                    check(label + '_certificate_array_roundtrip_exact', set(saved.files) == set(arrays) and all(numerical.array_equal(saved[name], value) for name, value in arrays.items()))
                artifact(output)
                row = {'label': label, 'intervals': intervals, 'branch': branch, 'saved_time': float(time), 'attempts': attempts, 'selected_parameter_width': parameter_width, 'root_search_relative_width': data['unknown_radius'], 'time_parameter_horizon': data['time_horizon'], 'certified_local_residence_time': data['residence_time'], 'limiting_dynamic_index': data['limiting_dynamic_index'], 'initial_max_root_correction_upper': data['initial']['maximum_correction'], 'initial_root_enclosure_width_max': data['initial']['maximum_enclosure_width'], 'initial_inclusion_ratio': data['initial']['inclusion_ratio'], 'parameterized_inclusion_ratio': data['inclusion']['inclusion_ratio'], 'parent_contraction': data['inclusion']['contraction'], 'minimum_F': data['minimum_F'], 'minimum_N': data['minimum_N'], 'shift_diagnostic': data['shift_diagnostic'], 'stored_residual_max': float(max(abs(original_residual))), 'original_evaluator_midpoint_difference': agreement, 'assembly_vs_polynomial_map_max_difference': map_differences, 'corner_Newton_residuals': corner_residuals, 'scope': report['scope'], 'saved_trajectory_validated': False, 'previous_higher_jet_box_residence_verified': False, 'boundary_TV_transfer_verified': False}
                row.update(original_Hessian_midpoint_difference=jacobian_difference, original_force_midpoint_difference=force_difference, full_shift_residual_at_rounded_root_midpoint=shift_residual_max, all_shift_equations_verified=False)
                report['samples'].append(row)
                report.pop('active_parameter_attempts', None)
                save()
                print(json.dumps(row), flush=True)
            for module in tuple(sys.modules.values()):
                filename = getattr(module, '__file__', None)
                if filename:
                    path = Path(filename).resolve()
                    if path.parent == root / 'scripts' and path.suffix == '.py':
                        own(path)
            check('all_inherited_inputs_preserved', all(digest(root / name) == expected for name, expected in inputs.items()))
            check('all_inherited_and_new_outputs_preserved', all(digest(root / name) == expected for name, expected in outputs.items()))
            check('no_bytecode_cache', not (root / 'scripts/__pycache__').exists())
            report.update(state='complete', passed=sum(row['passed'] for row in report['checks']), total=len(report['checks']), completed_utc=datetime.now(timezone.utc).isoformat())
            report.pop('active_sample', None)
            save()
            (destination / 'COMPLETE').write_text(report['completed_utc'] + '\n')
            print(json.dumps({name: report[name] for name in ['state', 'passed', 'total', 'completed_utc']}), flush=True)
            return
        except Exception as error:
            report.update(state='failed', failure=repr(error), traceback=traceback.format_exc())
            save()
            raise
    report_path = destination / 'status.json'
    report = json.loads(report_path.read_text())
    if report['state'] != 'complete' or report['passed'] != report['total'] or len(report['samples']) != 18 or report['probe_limit']:
        raise RuntimeError('Full root/residence validation incomplete.')
    inherit(inputs, report['inputs'])
    inherit(outputs, report['outputs'])
    for path in [report_path, destination / 'COMPLETE']:
        own(path)
    note = root / 'DERIVATION-20260910-compatible-parent-root-and-local-residence.md'
    cited = [value for value in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')) if value.endswith(('.py', '.md', '.json', '.npz'))]
    missing = [value for value in cited if root / value != final_path and not (root / value).is_file()]
    if missing:
        raise FileNotFoundError(str(missing))
    own(note)
    snapshot = intake / 'annular-parent-root-residence-resume-snapshot.md'
    with snapshot.open('xb') as handle:
        handle.write((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    artifact(snapshot)
    frozen = root.parent / 'formalization-workbench'
    since = datetime(2026, 9, 10, 12, 8, 23, tzinfo=timezone.utc).timestamp()
    touched = [str(path.relative_to(frozen)) for path in frozen.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    if touched or (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Protected workbench/cache check failed: ' + repr(touched))
    final = {'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'checks': report['total'], 'saved_states': len(report['samples']), 'inputs': inputs, 'outputs': outputs, 'cited_local_paths_checked': cited, 'protected_workbench_files_written_since_turn_start': len(touched), 'protected_check_method': 'mtime scan since 2026-09-10T12:08:23Z, not a full pre-turn hash baseline', 'no_bytecode_cache': True, 'compatible_finite_free_constraint_roots_and_local_residence': True, 'all_shift_equations_verified': False, 'higher_jet_box_and_boundary_TV_transfer_open': True, 'scope': report['scope'], 'valid_for_physics_claim': False}
    with final_path.open('x') as handle:
        json.dump(final, handle, indent=2)
        handle.write('\n')
    print(json.dumps({name: final[name] for name in ['state', 'checks', 'saved_states', 'protected_workbench_files_written_since_turn_start']}), flush=True)


if __name__ == '__main__':
    run()
