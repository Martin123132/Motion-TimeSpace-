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
    from annular_adm_mixed_action_20260909 import MixedActionBasis
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian
    from annular_gram_joint_action_20260909 import gram_matrices
    from annular_parent_coefficient_box_20260910 import Box, Taylor
    from annular_parent_root_residence_20260910 import canonical_maps
    from annular_implicit_parent_jets_20260910 import implicit_jet_enclosure, set_coordinates

    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['derive', 'seal'])
    parser.add_argument('--attempt', default='attempt01')
    parser.add_argument('--limit', type=int, default=0)
    arguments = parser.parse_args()
    if not re.fullmatch('[a-z0-9-]+', arguments.attempt) or arguments.limit < 0:
        raise ValueError('Invalid attempt/limit.')
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260910'
    destination = intake / ('annular-implicit-parent-jets-' + arguments.attempt)
    prior_path = intake / 'annular-parent-root-residence-final-integrity.json'
    parent_path = intake / 'annular-parent-root-residence-attempt02/status.json'
    final_path = intake / 'annular-implicit-parent-jets-final-integrity.json'
    script_names = ['annular_implicit_parent_jets_20260910.py', 'derive_annular_implicit_parent_jets_20260910.py']
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

    def bounds(value):
        lower = numerical.maximum(0., numerical.maximum(value.lo, -value.hi))
        excluded = numerical.flatnonzero(lower > 0)
        return {'absolute_upper': float(value.magnitude.max()), 'absolute_lower': float(lower.max()), 'components_excluding_zero': excluded.tolist(), 'maximum_radius': float(((value.hi - value.lo) / 2).max())}

    prior = json.loads(prior_path.read_text())
    if prior['state'] != 'complete':
        raise RuntimeError('Initial root and residence gate incomplete.')
    inherit(inputs, prior['inputs'])
    inherit(outputs, prior['outputs'])
    own(prior_path)
    own(parent_path)
    for name in script_names:
        path = root / 'scripts' / name
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    parent = json.loads(parent_path.read_text())
    if arguments.phase == 'derive':
        destination.mkdir(exist_ok=False)
        for name in script_names:
            path = destination / ('executed-' + name)
            path.write_bytes((root / 'scripts' / name).read_bytes())
            artifact(path)
        report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': inputs, 'outputs': outputs, 'checks': [], 'samples': [], 'probe_limit': arguments.limit, 'runtime': {'python': sys.version, 'numpy': numerical.__version__, 'scipy': scipy.__version__}, 'original_states_unchanged': True, 'new_numerical_evolution': False, 'all_shift_equations_verified': False, 'entire_saved_trajectory_validated': False, 'boundary_TV_transfer_verified': False, 'valid_for_physics_claim': False, 'scope': 'Outward first/second implicit jets and full shift defect on the archived free-root tubes, finite canonical stored-map action. A nonzero defect is a finite reduction consistency result, not a continuum or MTS no-go theorem.'}

        def save():
            (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

        def check(name, passed, detail=None):
            report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
            if not passed:
                raise RuntimeError('Failed check: ' + name + ' ' + repr(detail))

        save()
        try:
            scalar = Taylor([Box(2.), Box(3.), Box(5.)])**2
            check('normalized_Taylor_second_derivative_control', scalar.coefficients[2].lo <= 29 <= scalar.coefficients[2].hi)
            positive = bounds(Box(numerical.array([.1, -.4]), numerical.array([.2, -.3])))
            uncertain = bounds(Box(numerical.array([-.1]), numerical.array([.2])))
            check('nonzero_classifier_two_signs', positive['components_excluding_zero'] == [0, 1])
            check('zero_containment_not_a_zero_proof', not uncertain['components_excluding_zero'] and uncertain['absolute_upper'] > 0)
            case_path = root / 'source-intake/navier-stokes/20260909/annular-constraint-correction-initial/canonical.json'
            own(case_path)
            case = json.loads(case_path.read_text())
            constants = {name: float(symbolic.sympify(value)) for name, value in case['parameters'].items()}
            samples = parent['samples'][:arguments.limit] if arguments.limit else parent['samples']
            for sample in samples:
                label, branch = sample['label'], sample['branch']
                report['active_sample'] = label
                save()
                print('Starting ' + label, flush=True)
                archived = loaded(parent_path.parent / (label + '.npz'))
                basis = MixedActionBasis(archived['basis_radii'])
                links = MetricLinkQuadrature(basis)
                count = basis.radii.size
                configuration, momenta = archived['original_configuration'], archived['original_momenta']
                clock, clock_rate = archived['affine_clock']
                acceleration = archived['endpoint_acceleration']
                system = ReleasedHermiteRouthian(basis, configuration[:count], configuration[count:], constants, .1, momenta[:count], momenta[count:], clock, links)
                maps_equal = True
                for name, value in archived.items():
                    if name.startswith('basis_'):
                        maps_equal = maps_equal and numerical.array_equal(value, numerical.asarray(getattr(basis, name[6:])))
                    if name.startswith('links_'):
                        maps_equal = maps_equal and numerical.array_equal(value, getattr(links, name[6:]))
                value_map, gradient_map = canonical_maps(basis)
                factors, sampling = gram_matrices(count)
                maps_equal = maps_equal and all(numerical.array_equal(archived[name], value) for name, value in [('assembly_value_map', value_map), ('assembly_gradient_map', gradient_map), ('local_action_maps', numerical.stack(system.maps)), ('nodal_action_maps', numerical.stack(system.node_maps)), ('gram_factors', factors), ('gram_sampling', sampling)])
                check(label + '_archived_maps_exactly_reused', maps_equal)
                check(label + '_normalization_and_boundary_indices_unchanged', numerical.array_equal(archived['kappa_rational'], [1, 10]) and numerical.array_equal(archived['free_indices'], system.free) and numerical.array_equal(archived['fixed_indices'], system.fixed))
                if not report.get('stationary_algebraic_control'):
                    stationary_packed = archived['original_packed'].copy()
                    stationary_packed[system.slices[2].start:] = 0.
                    zero_nodes = numerical.zeros(count)
                    stationary_system = ReleasedHermiteRouthian(basis, zero_nodes, zero_nodes, constants, .1, zero_nodes, zero_nodes, clock, links)
                    stationary = implicit_jet_enclosure(stationary_system, Box(stationary_packed), Box(numerical.zeros(2 * count)), Box(numerical.zeros(2 * count)), Box(clock), 0., numerical.zeros(2), True)
                    for name in ['first', 'second', 'shift_defect', 'shift_defect_time']:
                        check('stationary_zero_motion_' + name + '_contains_zero', numerical.all(stationary[name].lo <= 0) and numerical.all(stationary[name].hi >= 0))
                    report['stationary_algebraic_control'] = {'performed': True, 'initial_constraints_not_asserted': True, 'description': 'Frozen geometry, zero scalar and momenta, constant boundary data; tests derivative algebra, not a certified vacuum root.'}
                scopes, arrays, scope_data = {}, {}, {}
                for scope in ['initial', 'tube']:
                    report['active_scope'] = scope
                    save()
                    prefix = 'initial_root_box' if scope == 'initial' else 'root_box'
                    packed = Box(archived[prefix + '_lower'], archived[prefix + '_upper'])
                    position = Box(configuration) if scope == 'initial' else Box(archived['configuration_box_lower'], archived['configuration_box_upper'])
                    momentum = Box(momenta) if scope == 'initial' else Box(archived['momentum_box_lower'], archived['momentum_box_upper'])
                    clock_box = Box(clock) if scope == 'initial' else Box(clock) + Box(0., sample['time_parameter_horizon']) * clock_rate
                    data = implicit_jet_enclosure(system, packed, position, momentum, clock_box, clock_rate, acceleration, branch != 'GR')
                    scope_data[scope] = data
                    key = label + '_' + scope
                    for name, diagnostic in data['diagnostics'].items():
                        check(key + '_' + name + '_verified_inverse', diagnostic['componentwise_majorant_verified'] and diagnostic['contraction'] < 1)
                    for name in ['constraint_value', 'constraint_first', 'constraint_second']:
                        check(key + '_' + name + '_contains_zero', numerical.all(data[name].lo <= 0) and numerical.all(data[name].hi >= 0))
                    check(key + '_quadratic_boundary_first_exact', numerical.array_equal(data['first'].lo[system.fixed[1:]], acceleration) and numerical.array_equal(data['first'].hi[system.fixed[1:]], acceleration))
                    check(key + '_quadratic_boundary_second_exact', numerical.all(data['second'].magnitude[system.fixed[1:]] == 0))
                    check(key + '_only_inner_velocity_relations_imposed', data['mass_velocity_mismatch'].magnitude[0] == 0 and data['mass_acceleration_mismatch'].magnitude[0] == 0)
                    check(key + '_endpoint_momentum_rates_invariant', numerical.all(data['force'].magnitude[[0, count - 1]] == 0) and numerical.all(data['force_time'].magnitude[[0, count - 1]] == 0))
                    scopes[scope] = {name: bounds(data[name]) for name in ['first', 'second', 'shift_defect', 'shift_defect_time', 'mass_velocity_mismatch', 'mass_acceleration_mismatch']}
                    scopes[scope].update(diagnostics=data['diagnostics'], minimum_F=data['minimum_F'], minimum_N=data['minimum_N'])
                    for name, value in data.items():
                        if isinstance(value, Box):
                            arrays[scope + '_' + name + '_lower'], arrays[scope + '_' + name + '_upper'] = value.lo, value.hi
                    print(json.dumps({'label': label, 'scope': scope, 'shift': scopes[scope]['shift_defect'], 'shift_time': scopes[scope]['shift_defect_time']}), flush=True)
                midpoint = Box(archived['initial_root_box_lower'], archived['initial_root_box_upper']).midpoint
                tangent = system.constraint_tangent(midpoint, branch != 'GR', acceleration, clock_rate)
                first_control = tangent['packed_speed']
                first_error = float((abs(first_control - scope_data['initial']['first'].midpoint) / numerical.maximum(1., abs(first_control))).max())
                check(label + '_independent_original_tangent_agreement', first_error < 1e-8, first_error)
                control_defect = tangent['shift_residual']
                defect_error = float(abs(control_defect - scope_data['initial']['shift_defect'].midpoint).max())
                check(label + '_independent_original_shift_agreement', defect_error < 1e-12, defect_error)
                velocity = midpoint[system.slices[2].start:]
                force = numerical.concatenate([tangent['momentum_speed'], tangent['slope_momentum_speed']])
                controls = []
                for step in [2e-5, 1e-5]:
                    values = []
                    for sign in [-1, 1]:
                        changed_x, changed_pi = configuration + sign * step * velocity, momenta + sign * step * force
                        changed = ReleasedHermiteRouthian(basis, changed_x[:count], changed_x[count:], constants, .1, changed_pi[:count], changed_pi[count:], clock + sign * step * clock_rate, links)
                        values.append(changed.constraint_tangent(midpoint + sign * step * first_control, branch != 'GR', acceleration, clock_rate)['packed_speed'])
                    second_control = (values[1] - values[0]) / (2 * step)
                    error = float((abs(second_control - scope_data['initial']['second'].midpoint) / numerical.maximum(1., abs(second_control))).max())
                    controls.append({'step': step, 'normalized_maximum_error': error})
                    check(label + '_independent_centered_second_control_' + str(step), error < 1e-5, error)
                initial_defect = scope_data['initial']['shift_defect']
                component_lower = numerical.maximum(0., numerical.maximum(initial_defect.lo, -initial_defect.hi))
                nonzero_component = int(numerical.argmax(component_lower))
                lower = float(component_lower[nonzero_component])
                derivative_upper = float(scope_data['tube']['shift_defect_time'].magnitude[nonzero_component])
                nonzero_time = 0.
                if lower > 0:
                    candidate = sample['certified_local_residence_time'] if derivative_upper == 0 else float((Box(lower) / (2 * Box(derivative_upper))).lo)
                    nonzero_time = min(candidate, sample['certified_local_residence_time'])
                    check(label + '_nonzero_defect_time_certified', nonzero_time > 0 and float((Box(nonzero_time) * Box(derivative_upper)).hi) < lower)
                output = destination / (label + '.npz')
                numerical.savez_compressed(output, **arrays)
                with numerical.load(output) as saved:
                    check(label + '_enclosure_archive_roundtrip_exact', set(saved.files) == set(arrays) and all(numerical.array_equal(saved[name], value) for name, value in arrays.items()))
                artifact(output)
                row = {'label': label, 'intervals': sample['intervals'], 'branch': branch, 'saved_time': sample['saved_time'], 'scopes': scopes, 'original_tangent_error': first_error, 'original_shift_error': defect_error, 'second_derivative_controls': controls, 'reduced_residence_time': sample['certified_local_residence_time'], 'nonzero_shift_component': nonzero_component if lower > 0 else None, 'nonzero_shift_component_lower': lower, 'certified_nonzero_shift_time': nonzero_time, 'all_shift_equations_verified': False, 'finite_full_shift_zero_rejected_at_initial_root': lower > 0, 'boundary_TV_transfer_verified': False}
                report['samples'].append(row)
                save()
            for module in tuple(sys.modules.values()):
                filename = getattr(module, '__file__', None)
                if filename:
                    path = Path(filename).resolve()
                    if path.parent == root / 'scripts' and path.suffix == '.py':
                        own(path)
            check('all_inherited_inputs_preserved', all(digest(root / name) == expected for name, expected in inputs.items()))
            check('all_inherited_and_new_outputs_preserved', all(digest(root / name) == expected for name, expected in outputs.items()))
            check('no_bytecode_cache', not (root / 'scripts/__pycache__').exists())
            report.update(state='complete', passed=sum(row['passed'] for row in report['checks']), total=len(report['checks']), initial_nonzero_shift_roots=sum(row['finite_full_shift_zero_rejected_at_initial_root'] for row in report['samples']), completed_utc=datetime.now(timezone.utc).isoformat())
            report.pop('active_sample', None)
            report.pop('active_scope', None)
            save()
            (destination / 'COMPLETE').write_text(report['completed_utc'] + '\n')
            print(json.dumps({name: report[name] for name in ['state', 'passed', 'total', 'initial_nonzero_shift_roots', 'completed_utc']}), flush=True)
            return
        except Exception as error:
            report.update(state='failed', failure=repr(error), traceback=traceback.format_exc())
            save()
            raise
    report_path = destination / 'status.json'
    report = json.loads(report_path.read_text())
    if report['state'] != 'complete' or report['passed'] != report['total'] or len(report['samples']) != 18 or report['probe_limit']:
        raise RuntimeError('Full implicit-jet validation incomplete.')
    inherit(inputs, report['inputs'])
    inherit(outputs, report['outputs'])
    own(report_path)
    own(destination / 'COMPLETE')
    note = root / 'DERIVATION-20260910-implicit-parent-jets-and-full-shift-defect.md'
    cited = [value for value in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')) if value.endswith(('.py', '.md', '.json', '.npz'))]
    missing = [value for value in cited if root / value != final_path and not (root / value).is_file()]
    if missing:
        raise FileNotFoundError(str(missing))
    own(note)
    snapshot = intake / 'annular-implicit-parent-jets-resume-snapshot.md'
    with snapshot.open('xb') as handle:
        handle.write((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    artifact(snapshot)
    frozen = root.parent / 'formalization-workbench'
    since = datetime(2026, 9, 10, 13, 58, 30, tzinfo=timezone.utc).timestamp()
    touched = [str(path.relative_to(frozen)) for path in frozen.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    if touched or (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Protected workbench/cache gate failed: ' + repr(touched))
    final = {'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'checks': report['total'], 'saved_states': len(report['samples']), 'initial_nonzero_shift_roots': report['initial_nonzero_shift_roots'], 'inputs': inputs, 'outputs': outputs, 'cited_local_paths_checked': cited, 'protected_workbench_files_written_since_turn_start': len(touched), 'protected_check_method': 'mtime scan since 2026-09-10T13:58:30Z, not a full pre-turn hash baseline', 'no_bytecode_cache': True, 'compatible_first_second_jets_enclosed': True, 'all_shift_equations_verified': False, 'boundary_TV_transfer_verified': False, 'scope': report['scope'], 'valid_for_physics_claim': False}
    with final_path.open('x') as handle:
        json.dump(final, handle, indent=2)
        handle.write('\n')
    print(json.dumps({name: final[name] for name in ['state', 'checks', 'saved_states', 'initial_nonzero_shift_roots', 'protected_workbench_files_written_since_turn_start']}), flush=True)


if __name__ == '__main__':
    run()
