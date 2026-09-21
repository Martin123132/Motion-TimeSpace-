import argparse
import hashlib
import json
import re
import sys
import traceback
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from annular_adm_mixed_action_20260909 import MixedActionBasis
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian
    from annular_boundary_source_variation_20260910 import parent_third_jet, boundary_source, endpoint_time_data
    from annular_first_derivative_energy_20260909 import affine_lift_matrix
    from annular_parent_coefficient_box_20260910 import Box, Taylor, comparison_solve, parent_box_data

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
    destination = intake / ('annular-parent-coefficient-box-' + arguments.attempt)
    prior_path = intake / 'annular-endpoint-metric-adjoint-final-integrity.json'
    final_path = intake / 'annular-parent-coefficient-box-final-integrity.json'
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
    for name in ['annular_parent_coefficient_box_20260910.py', 'derive_annular_parent_coefficient_box_20260910.py']:
        path = root / 'scripts' / name
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    if arguments.phase == 'derive':
        destination.mkdir(exist_ok=False)
        for name in ['annular_parent_coefficient_box_20260910.py', 'derive_annular_parent_coefficient_box_20260910.py']:
            output = destination / ('executed-' + name)
            output.write_bytes((root / 'scripts' / name).read_bytes())
            artifact(output)
        report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': inputs, 'outputs': outputs, 'checks': [], 'samples': [], 'probe_limit': arguments.limit, 'physical_time_interval_certified': False, 'mesh_uniform_neighborhood_proved': False, 'new_evolution': False, 'valid_for_physics_claim': False, 'arithmetic_scope': 'Outward binary64 primitive interval operations for stored finite-mesh basis/weights; real kappa=1/10 enclosed. IEEE correctly-rounded basic operations and sqrt assumed. Not a continuum quadrature or trajectory certificate.'}

        def save():
            (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

        def check(name, passed, detail=None):
            report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
            if not passed:
                raise RuntimeError('Failed check: ' + name + ' ' + repr(detail))

        def encloses(name, enclosure, value):
            value = numerical.asarray(value)
            check(name, numerical.all(enclosure.lo <= value) and numerical.all(value <= enclosure.hi), {'lower_miss': float(max(0., numerical.max(enclosure.lo - value))), 'upper_miss': float(max(0., numerical.max(value - enclosure.hi)))})

        save()
        try:
            random = numerical.random.default_rng(114258)
            for control in range(12):
                first = random.integers(-9, 10, size=(3, 4)).astype(float) / 8
                second = random.integers(-9, 10, size=(4, 2)).astype(float) / 4
                product = Box(first) @ Box(second)
                exact = [[sum((Fraction(float(first[row, inner])) * Fraction(float(second[inner, column])) for inner in range(4)), Fraction(0)) for column in range(2)] for row in range(3)]
                check('exact_rational_matrix_control_' + str(control), all(Fraction(float(product.lo[row, column])) <= exact[row][column] <= Fraction(float(product.hi[row, column])) for row in range(3) for column in range(2)))
            square = Taylor([Box(0.), Box(1.)])**2
            for order, expected in enumerate([0., 0., 1., 0.]):
                encloses('zero_crossing_Taylor_square_' + str(order), square.coefficients[order], expected)
            for name, action in [('division_zero', lambda: Box(1.) / Box(-1., 1.)), ('negative_sqrt', lambda: Box(-1., 1.)**.5), ('invalid_order', lambda: Box(2., 1.)), ('invalid_radius', lambda: Box(float('nan')))]:
                try:
                    action()
                except ValueError:
                    rejected = True
                else:
                    rejected = False
                check(name + '_refused', rejected)
            try:
                comparison_solve(Box(numerical.array([[-1.]]), numerical.array([[3.]])), Box(numerical.array([1.])))
            except ValueError:
                rejected = True
            else:
                rejected = False
            check('inverse_neighborhood_crossing_singularity_refused', rejected)
            safe_solution, safe_diagnostic = comparison_solve(Box(numerical.array([[.99]]), numerical.array([[1.01]])), Box(numerical.array([1.])))
            encloses('scalar_inverse_lower_corner', safe_solution, numerical.array([1 / 1.01]))
            encloses('scalar_inverse_upper_corner', safe_solution, numerical.array([1 / .99]))
            check('scalar_inverse_verified_majorant', safe_diagnostic['componentwise_majorant_verified'])
            case_path = old / 'annular-constraint-correction-initial/canonical.json'
            parent_path = intake / 'annular-boundary-source-variation-derived/status.json'
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
                spatial = loaded(old / 'annular-spatial-clock-energy-derived' / (label + '.npz'))
                jets = loaded(old / 'annular-metric-flux-jets-derived' / (label + '.npz'))
                source = loaded(intake / 'annular-boundary-source-variation-derived' / (label + '.npz'))
                folder = 'annular-boundary-N64-evolution-smoke' if intervals == 64 else 'annular-released-Hermite-evolution-smoke'
                trajectory = loaded(old / folder / (tag + '_steps' + str(steps) + '.npz'))
                basis = MixedActionBasis(initial['radius'])
                count = basis.radii.size
                time, state = trajectory['time'][index], trajectory['state'][index]
                scalar, slope, momentum, slope_momentum = [state[part * count:(part + 1) * count] for part in range(4)]
                packed, speed, second = state[4 * count:], spatial['packed_speed'], jets['jet_acceleration']
                system = ReleasedHermiteRouthian(basis, scalar, slope, constants, kappa, momentum, slope_momentum, initial['outer_clock'][0] + time * initial['outer_clock'][1], MetricLinkQuadrature(basis))
                invalid_second = second.copy()
                invalid_second[system.fixed[1]] = 1.
                try:
                    parent_box_data(system, packed, speed, invalid_second, 1e-6, branch != 'GR')
                except ValueError as error:
                    rejected = str(error).startswith('Quadratic endpoint histories require')
                else:
                    rejected = False
                check(label + '_nonquadratic_history_explicitly_refused', rejected)
                attempts = []
                for radius in [1e-6, 1e-7, 1e-8, 1e-9]:
                    try:
                        data = parent_box_data(system, packed, speed, second, radius, branch != 'GR')
                    except ValueError as error:
                        if not str(error).startswith('Coefficient-box inverse gate failed:'):
                            raise
                        attempts.append({'radius': radius, 'gate': False, 'reason': str(error)})
                        continue
                    attempts.append({'radius': radius, 'gate': True})
                    break
                else:
                    raise RuntimeError('No tested coefficient radius certified.')
                encloses(label + '_original_J_inside_parent_box', data['jacobian'], system.evaluate(packed, branch != 'GR')[2])
                encloses(label + '_original_known_third_inside_parent_box', data['known_third'], source['known_third'])
                encloses(label + '_original_third_inside_parent_box', data['third'], source['third_parent_jet'])
                encloses(label + '_original_theta_tt_inside_parent_box', data['theta_tt'], source['theta_tt'])
                encloses(label + '_original_beta_inside_parent_box', data['boundary']['beta'], source['repacked_beta'])
                encloses(label + '_original_beta_time_inside_parent_box', data['boundary']['beta_time'], source['repacked_beta_time'])
                check(label + '_entire_box_positive_metric', data['minimum_F'] > 0 and data['minimum_N'] > 0)
                for control in range(2):
                    sign = numerical.where(numerical.arange(system.count) % 2 == control, 1., -1.)
                    changed_orders = [order + sign * widths for order, widths in zip([packed, speed, second], data['packed_widths'])]
                    configuration = numerical.concatenate([scalar, slope])
                    configuration_sign = numerical.where(numerical.arange(configuration.size) % 2 == control, 1., -1.)
                    changed_configuration = configuration + configuration_sign * radius * numerical.maximum(1., abs(configuration))
                    changed = ReleasedHermiteRouthian(basis, changed_configuration[:count], changed_configuration[count:], constants, kappa, momentum, slope_momentum, system.outer_clock, system.links)
                    changed_parent = parent_third_jet(changed, *changed_orders, initial['outer_clock'][1], branch != 'GR')
                    lift_map = affine_lift_matrix(basis)
                    lift = lift_map @ changed_configuration[:count][[0, -1]]
                    lift_time = lift_map @ changed_orders[0][system.slices[2]][[0, -1]]
                    lift_second = lift_map @ changed_orders[1][system.slices[2]][[0, -1]]
                    changed_source = boundary_source(changed, *changed_orders, branch != 'GR', lift, lift_time, lift_second)
                    changed_rate = endpoint_time_data(changed, *changed_orders, changed_parent['third'], changed_source, lift, lift_time, lift_second)
                    encloses(label + '_off_constraint_corner_J_' + str(control), data['jacobian'], changed.evaluate(changed_orders[0], branch != 'GR')[2])
                    encloses(label + '_off_constraint_corner_third_' + str(control), data['third'], changed_parent['third'])
                    encloses(label + '_off_constraint_corner_theta_tt_' + str(control), data['theta_tt'], changed_rate['theta_tt'])
                    encloses(label + '_off_constraint_corner_beta_time_' + str(control), data['boundary']['beta_time'], changed_rate['beta_time'])
                arrays = {}
                for name in ['jacobian', 'known_third', 'fixed_third', 'forcing', 'third', 'theta_tt']:
                    arrays[name + '_lower'], arrays[name + '_upper'] = data[name].lo, data[name].hi
                for name in ['beta', 'beta_time', 'potential', 'potential_time', 'force', 'force_time']:
                    arrays[name + '_lower'], arrays[name + '_upper'] = data['boundary'][name].lo, data['boundary'][name].hi
                arrays['packed_widths'] = numerical.stack(data['packed_widths'])
                output = destination / (label + '.npz')
                numerical.savez_compressed(output, **arrays)
                artifact(output)
                beta_magnitude = data['boundary']['beta_time'].magnitude
                squared = (Box(beta_magnitude) * Box(beta_magnitude)) @ Box(numerical.ones(2))
                rate_upper = float((squared**.5).hi)
                row = {'label': label, 'intervals': intervals, 'branch': branch, 'time': float(time), 'radius_attempts': attempts, 'selected_radius': radius, 'minimum_F': data['minimum_F'], 'minimum_N': data['minimum_N'], 'theta_tt_lower': data['theta_tt'].lo.tolist(), 'theta_tt_upper': data['theta_tt'].hi.tolist(), 'beta_time_lower': data['boundary']['beta_time'].lo.tolist(), 'beta_time_upper': data['boundary']['beta_time'].hi.tolist(), 'beta_time_R2_upper': rate_upper, 'parent_inverse': data['inverse_diagnostics'], 'shift_inverses': data['shift_diagnostics'], 'elliptic_inverses': data['boundary']['elliptic_diagnostics'], 'scope': 'Whole finite coefficient/jet box enclosure, including original parent-derived source. No actual trajectory residence time or mesh-uniform radius proved.'}
                report['samples'].append(row)
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
        raise RuntimeError('Full coefficient-box validation incomplete.')
    inherit(inputs, report['inputs'])
    inherit(outputs, report['outputs'])
    for path in [report_path, destination / 'COMPLETE']:
        own(path)
    note = root / 'DERIVATION-20260910-parent-coefficient-box-and-boundary-rate-enclosure.md'
    cited = [value for value in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')) if value.endswith(('.py', '.md', '.json', '.npz'))]
    missing = [value for value in cited if root / value != final_path and not (root / value).is_file()]
    if missing:
        raise FileNotFoundError(str(missing))
    own(note)
    snapshot = intake / 'annular-parent-coefficient-box-resume-snapshot.md'
    with snapshot.open('xb') as handle:
        handle.write((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    artifact(snapshot)
    frozen = root.parent / 'formalization-workbench'
    since = datetime(2026, 9, 10, 11, 42, 58, tzinfo=timezone.utc).timestamp()
    touched = [str(path.relative_to(frozen)) for path in frozen.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    if touched or (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Protected workbench/cache check failed: ' + repr(touched))
    final = {'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'checks': report['total'], 'saved_states': len(report['samples']), 'inputs': inputs, 'outputs': outputs, 'cited_local_paths_checked': cited, 'protected_workbench_files_written_since_turn_start': len(touched), 'protected_check_method': 'mtime scan since 2026-09-10T11:42:58Z, not a full pre-turn hash baseline', 'no_bytecode_cache': True, 'parent_coefficient_box_source_and_inverse_enclosed': True, 'actual_trajectory_residence_and_uniform_mesh_radius_open': True, 'arithmetic_scope': report['arithmetic_scope'], 'valid_for_physics_claim': False}
    with final_path.open('x') as handle:
        json.dump(final, handle, indent=2)
        handle.write('\n')
    print(json.dumps({name: final[name] for name in ['state', 'checks', 'saved_states', 'protected_workbench_files_written_since_turn_start']}), flush=True)


if __name__ == '__main__':
    run()
