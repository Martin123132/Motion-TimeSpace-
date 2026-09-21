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
    import sympy as symbolic
    from scipy.linalg import eigvalsh
    from annular_adm_mixed_action_20260909 import MixedActionBasis
    from annular_first_derivative_energy_20260909 import affine_lift_matrix, canonical_matrices
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian
    from annular_paired_variational_energy_20260910 import graph_operators
    from annular_spatial_clock_energy_20260909 import profile
    from annular_endpoint_commutator_bound_20260910 import endpoint_defect_bound, exact_defect

    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['derive', 'seal'])
    arguments = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    old_intake = root / 'source-intake/navier-stokes/20260909'
    intake = root / 'source-intake/navier-stokes/20260910'
    destination = intake / 'annular-endpoint-commutator-bound-derived'
    prior_path = intake / 'annular-boundary-memory-energy-final-integrity.json'
    final_path = intake / 'annular-endpoint-commutator-bound-final-integrity.json'
    prior = json.loads(prior_path.read_text())
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

    if prior['state'] != 'complete':
        raise RuntimeError('Previous gate incomplete.')
    inherit(inputs, prior['inputs'])
    inherit(outputs, prior['outputs'])
    own(prior_path)
    for name in ['annular_endpoint_commutator_bound_20260910.py', 'derive_annular_endpoint_commutator_bound_20260910.py']:
        path = root / 'scripts' / name
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    if arguments.phase == 'derive':
        destination.mkdir(exist_ok=False)
        (destination / 'executed-script.py').write_bytes(Path(__file__).read_bytes())
        report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': inputs, 'outputs': outputs, 'checks': [], 'samples': [], 'controls': [], 'endpoint_commutator_bound_derived': True, 'projection_graph_bound_with_retained_jumps_derived': True, 'parent_jump_identity_derived': True, 'parent_clock_curvature_uniform_propagation_proved': False, 'paired_moving_growth_uniform_proved': False, 'valid_for_physics_claim': False}

        def save():
            (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

        def check(name, passed, detail=None):
            report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
            if not passed:
                raise RuntimeError('Failed check: ' + name + ' ' + repr(detail))

        def close(name, first, second, tolerance=2e-7):
            error = float(numerical.max(abs(numerical.asarray(first) - second)))
            scale = 1 + float(numerical.max(abs(numerical.asarray(second))))
            check(name, error <= tolerance * scale, {'error': error, 'scale': scale})

        def evaluate(label, system, packed, speed, include_gram):
            basis = system.basis
            count = basis.radii.size
            free = numerical.array([index for index in range(2 * count) if index not in [0, count - 1]])
            selection = numerical.ix_(free, free)
            matrices = canonical_matrices(system, packed, speed, include_gram)
            mass, stiffness, mass_time, stiffness_time = [matrices[name][selection] for name in ['M', 'K', 'M_dot', 'K_dot']]
            operators = graph_operators(mass, stiffness, mass_time, stiffness_time)
            value = numerical.concatenate([basis.scalar_value, basis.lift_value / basis.spacing], axis=1)
            data = profile(system, packed, speed, basis.quadrature)
            density = basis.quadrature**2 / data['c'][0]
            bound = endpoint_defect_bound(system, packed, speed, include_gram)
            derived = exact_defect(matrices, free, affine_lift_matrix(basis), operators, value, basis.quadrature_weights * density, data['theta'][0], bound['theta_center'])
            close(label + '_exact_constant_affine_transport_product_decomposition', derived['direct'], derived['reconstructed'])
            close(label + '_theta_slope_jumps_from_actual_parent_fields', bound['curvature']['theta_jump'], bound['curvature']['theta_jump_from_parent_fields'], tolerance=1e-10)
            check(label + '_clock_R_L2_integral_bound', numerical.sqrt(numerical.dot(basis.quadrature_weights, data['theta'][1]**2)) <= bound['curvature']['theta_R_L2_bound'] + 1e-12)
            check(label + '_clock_RR_L2_integral_bound', numerical.sqrt(numerical.dot(basis.quadrature_weights, data['theta'][2]**2)) <= bound['curvature']['theta_RR_broken_L2_bound'] + 1e-12)
            check(label + '_derived_endpoint_operator_bound', derived['M_operator_norm'] <= bound['endpoint_transport_M_bound'] + 1e-10)
            projected_norm = numerical.sqrt(max(float(eigvalsh(derived['product_graph'].T @ mass @ derived['product_graph'])[-1]), 0.))
            projection_upper = bound['projection_constants']['first_constant'] * bound['product_first_L2_bound'] + bound['projection_constants']['curvature_constant'] * bound['product_curvature_bound']
            check(label + '_projected_product_graph_bound', projected_norm <= projection_upper + 1e-10)
            for name, derived_norm in [('elliptic_H1_constant', None)]:
                radial = numerical.concatenate([basis.scalar_gradient, basis.lift_gradient / basis.spacing], axis=1)[:, free]
                derivatives = radial @ derived['potential']
                measured = numerical.sqrt(max(float(eigvalsh(derivatives.T @ (basis.quadrature_weights[:, None] * derivatives))[-1]), 0.))
                check(label + '_elliptic_endpoint_first_bound', measured <= bound['transport'][name] * bound['endpoint_lift_M_bound'] + 1e-10)
            row = {'label': label, 'measured_endpoint_defect': derived['M_operator_norm'], 'derived_endpoint_upper': bound['endpoint_transport_M_bound'], 'clock_R_L2_upper': bound['curvature']['theta_R_L2_bound'], 'clock_RR_broken_L2_upper': bound['curvature']['theta_RR_broken_L2_bound'], 'clock_slope_jump_radius': bound['curvature']['theta_R_jump_radius'], 'clock_curvature_radius': bound['curvature']['clock_curvature_radius'], 'paired_growth_measured': operators['growth_rate'], 'theta_center': bound['theta_center'], 'theta_radius': bound['theta_radius'], 'projection_constants': bound['projection_constants'], 'scope': 'Explicit bound conditional on the sourced clock curvature/jump radius, not a uniform propagation theorem.'}
            return row, derived, bound

        save()
        try:
            source_path = intake / 'annular-boundary-memory-transport-derived/status.json'
            case_path = old_intake / 'annular-constraint-correction-initial/canonical.json'
            own(source_path)
            own(case_path)
            samples = json.loads(source_path.read_text())['samples']
            case = json.loads(case_path.read_text())
            constants = {name: float(symbolic.sympify(value)) for name, value in case['parameters'].items()}
            kappa = float(symbolic.sympify(case['normalization_kappa']))
            for sample in samples:
                label, intervals, branch = sample['label'], sample['intervals'], sample['branch']
                tag = label.split('_sample')[0]
                index = int(label.rsplit('sample', 1)[1])
                steps = 64 if intervals == 64 else 32
                source = loaded(old_intake / 'annular-released-Hermite-initial-derived' / (tag + '.npz'))
                spatial = loaded(old_intake / 'annular-spatial-clock-energy-derived' / (label + '.npz'))
                folder = 'annular-boundary-N64-evolution-smoke' if intervals == 64 else 'annular-released-Hermite-evolution-smoke'
                trajectory = loaded(old_intake / folder / (tag + '_steps' + str(steps) + '.npz'))
                basis = MixedActionBasis(source['radius'])
                count = basis.radii.size
                time, state = trajectory['time'][index], trajectory['state'][index]
                scalar, slope, momentum, slope_momentum = [state[part * count:(part + 1) * count] for part in range(4)]
                packed, speed = state[4 * count:], spatial['packed_speed']
                system = ReleasedHermiteRouthian(basis, scalar, slope, constants, kappa, momentum, slope_momentum, source['outer_clock'][0] + time * source['outer_clock'][1], MetricLinkQuadrature(basis))
                row, derived, bound = evaluate(label, system, packed, speed, branch != 'GR')
                close(label + '_same_prior_endpoint_transport_defect_norm', row['measured_endpoint_defect'], sample['moving_endpoint_transport_defect_M_operator_norm'])
                row.update(intervals=intervals, branch=branch, time=float(time))
                report['samples'].append(row)
                output = destination / (label + '.npz')
                numerical.savez_compressed(output, direct_defect=derived['direct'], reconstructed_defect=derived['reconstructed'], pieces=derived['pieces'], clock_jump=bound['curvature']['theta_jump'], clock_jump_from_parent=bound['curvature']['theta_jump_from_parent_fields'], parent_slope_jumps=bound['curvature']['parent_slope_jumps'], theta_RR_cell_sup=bound['curvature']['theta_RR_cell_sup'])
                artifact(output)
                if index == steps:
                    print(json.dumps(row), flush=True)
                save()
            for intervals in [16, 32, 64, 128]:
                basis = MixedActionBasis(numerical.linspace(47 / 8, 49 / 8, intervals + 1))
                count = basis.radii.size
                system = ReleasedHermiteRouthian(basis, numerical.zeros(count), numerical.zeros(count), constants, kappa, numerical.zeros(count), numerical.zeros(count), 1., MetricLinkQuadrature(basis))
                packed = numerical.zeros(system.count)
                packed[system.slices[0]], packed[system.slices[1]] = 1., .82
                centered = basis.radii - 6.
                for branch in ['GR', 'metric_Gram']:
                    for kind in ['constant', 'linear', 'quadratic']:
                        theta = .001 * (numerical.ones(count) if kind == 'constant' else centered if kind == 'linear' else centered**2)
                        speed = numerical.zeros_like(packed)
                        speed[system.slices[1]] = .82 * theta
                        label = 'control_N' + str(intervals) + '_' + branch + '_' + kind
                        row, derived, bound = evaluate(label, system, packed, speed, branch != 'GR')
                        if kind == 'constant':
                            close(label + '_exact_F_equals_minus_3theta_B', derived['direct'], -.003 * derived['endpoint'])
                            close(label + '_exact_growth_equals_5theta', row['paired_growth_measured'], .005)
                        elif kind == 'linear':
                            check(label + '_no_hidden_clock_curvature', row['clock_curvature_radius'] < 1e-10)
                        else:
                            expected = .002 * numerical.sqrt(.25 - basis.spacing)
                            close(label + '_exact_quadratic_P1_jump_radius', row['clock_slope_jump_radius'], expected, tolerance=1e-10)
                            check(label + '_quadratic_P1_curvature_uniform_in_mesh', row['clock_curvature_radius'] <= numerical.sqrt(6) * .001 + 1e-10)
                        row.update(intervals=intervals, branch=branch, kind=kind, scope='Manufactured coefficient jet in the actual FE spaces; not a parent-constrained trajectory.')
                        report['controls'].append(row)
                        if kind == 'linear':
                            print(json.dumps({'control': label, 'paired_growth': row['paired_growth_measured'], 'curvature': row['clock_curvature_radius'], 'defect': row['measured_endpoint_defect']}), flush=True)
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
            report.update(state='complete', passed=sum(row['passed'] for row in report['checks']), total=len(report['checks']), completed_utc=datetime.now(timezone.utc).isoformat())
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
    if report['state'] != 'complete' or report['passed'] != report['total']:
        raise RuntimeError('Endpoint commutator validation incomplete.')
    inherit(inputs, report['inputs'])
    inherit(outputs, report['outputs'])
    for path in [report_path, destination / 'COMPLETE', destination / 'executed-script.py']:
        own(path)
    note = root / 'DERIVATION-20260910-endpoint-commutator-bound-with-parent-clock-jumps.md'
    cited = [value for value in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')) if value.endswith(('.py', '.md', '.json', '.npz'))]
    missing = [value for value in cited if root / value != final_path and not (root / value).is_file()]
    if missing:
        raise FileNotFoundError(str(missing))
    own(note)
    snapshot = intake / 'annular-endpoint-commutator-bound-resume-snapshot.md'
    with snapshot.open('xb') as handle:
        handle.write((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    artifact(snapshot)
    frozen = root.parent / 'formalization-workbench'
    since = datetime(2026, 9, 10, 0, 34, 0, tzinfo=timezone.utc).timestamp()
    touched = [str(path.relative_to(frozen)) for path in frozen.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    if touched or (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Protected workbench/cache check failed: ' + repr(touched))
    final = {'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'checks': report['total'], 'saved_states': len(report['samples']), 'manufactured_coefficient_controls': len(report['controls']), 'inputs': inputs, 'outputs': outputs, 'cited_local_paths_checked': cited, 'protected_workbench_files_written_since_turn_start': len(touched), 'protected_check_method': 'mtime scan since 2026-09-10T00:34:00Z, not a full pre-turn hash baseline', 'no_bytecode_cache': True, 'endpoint_commutator_bound_with_clock_curvature_derived': True, 'parent_curvature_propagation_and_paired_growth_open': True, 'actual_beta_BV_and_full_evolution_open': True, 'valid_for_physics_claim': False}
    with final_path.open('x') as handle:
        json.dump(final, handle, indent=2)
        handle.write('\n')
    print(json.dumps({name: final[name] for name in ['state', 'checks', 'saved_states', 'manufactured_coefficient_controls', 'protected_workbench_files_written_since_turn_start']}), flush=True)


if __name__ == '__main__':
    run()
