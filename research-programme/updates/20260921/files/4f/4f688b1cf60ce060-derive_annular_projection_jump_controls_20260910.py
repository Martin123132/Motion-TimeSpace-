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
    from scipy.linalg import solve
    from annular_adm_mixed_action_20260909 import MixedActionBasis
    from annular_first_derivative_energy_20260909 import canonical_matrices
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian
    from annular_paired_variational_energy_20260910 import scalar_maps
    from annular_uniform_energy_bounds_20260909 import metric_envelope
    from annular_endpoint_commutator_bound_20260910 import projection_graph_constants

    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['derive', 'seal'])
    arguments = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260910'
    parent_folder = intake / 'annular-endpoint-commutator-bound-derived'
    destination = intake / 'annular-projection-jump-controls-derived'
    parent_path = parent_folder / 'status.json'
    final_path = intake / 'annular-endpoint-commutator-bound-final-integrity.json'
    parent = json.loads(parent_path.read_text())
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

    if parent['state'] != 'complete' or parent['passed'] != parent['total']:
        raise RuntimeError('Endpoint commutator gate incomplete.')
    inherit(inputs, parent['inputs'])
    inherit(outputs, parent['outputs'])
    for path in [parent_path, parent_folder / 'COMPLETE', parent_folder / 'executed-script.py', Path(__file__).resolve()]:
        own(path)
    compile(Path(__file__).read_bytes(), str(Path(__file__)), 'exec')
    if arguments.phase == 'derive':
        destination.mkdir(exist_ok=False)
        (destination / 'executed-script.py').write_bytes(Path(__file__).read_bytes())
        report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': inputs, 'outputs': outputs, 'checks': [], 'controls': [], 'symbolic_shape_certificates': {}, 'valid_for_physics_claim': False}

        def save():
            (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

        def check(name, passed, detail=None):
            report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
            if not passed:
                raise RuntimeError('Failed check: ' + name + ' ' + repr(detail))

        save()
        try:
            coordinate = symbolic.Symbol('coordinate', real=True)
            shapes = [3 * coordinate**2 - 2 * coordinate**3, coordinate**3 - 2 * coordinate**2 + coordinate, coordinate**3 - coordinate**2]
            for index, shape in enumerate(shapes):
                for order, bound in [(0, 1), (1, symbolic.Rational(3, 2) if index == 0 else 1), (2, 6 if index == 0 else 4)]:
                    polynomial = symbolic.diff(shape, coordinate, order)
                    critical = [symbolic.S.Zero, symbolic.S.One] + [value for value in symbolic.solve(symbolic.diff(polynomial, coordinate), coordinate) if value.is_real and 0 <= value <= 1]
                    maximum = max(abs(polynomial.subs(coordinate, value)) for value in critical)
                    label = 'shape_' + str(index) + '_derivative_' + str(order)
                    report['symbolic_shape_certificates'][label] = {'exact_supremum': str(maximum), 'bound': str(bound)}
                    check(label, maximum <= bound)
            constants = {'b2': 0., 'b3': 0., 'm_chi': 0., 'Lambda': 0.}
            for intervals in [16, 32, 64, 128]:
                basis = MixedActionBasis(numerical.linspace(47 / 8, 49 / 8, intervals + 1))
                count, length, spacing = basis.radii.size, .25, basis.spacing
                system = ReleasedHermiteRouthian(basis, numerical.zeros(count), numerical.zeros(count), constants, .1, numerical.zeros(count), numerical.zeros(count), 1., MetricLinkQuadrature(basis))
                packed = numerical.zeros(system.count)
                packed[system.slices[0]], packed[system.slices[1]] = 1., .82
                speed = numerical.zeros_like(packed)
                maps = scalar_maps(basis, basis.quadrature)
                free = numerical.array([index for index in range(2 * count) if index not in [0, count - 1]])
                selection = numerical.ix_(free, free)
                nodes = basis.radii - basis.radii[0]
                points = basis.quadrature - basis.radii[0]
                envelope = metric_envelope(basis, packed[system.slices[0]], packed[system.slices[1]], speed[system.slices[0]], speed[system.slices[1]])
                density = basis.quadrature**2 / (.82 * numerical.sqrt(1 - 2 / basis.quadrature))
                for kind in ['smooth_quadratic', 'scalar_node_kink', 'mass_face_kink']:
                    if kind == 'smooth_quadratic':
                        values, slopes = nodes * (length - nodes), length - 2 * nodes
                        target, derivative = points * (length - points), length - 2 * points
                        curvature_radius = 2 * numerical.sqrt(length)
                    else:
                        kink = length / 2 + (spacing / 2 if kind == 'mass_face_kink' else 0.)
                        linear_slope = (length - 2 * kink) / length
                        values = abs(nodes - kink) - kink - linear_slope * nodes
                        slopes = numerical.sign(nodes - kink) - linear_slope
                        target = abs(points - kink) - kink - linear_slope * points
                        derivative = numerical.sign(points - kink) - linear_slope
                        curvature_radius = numerical.sqrt(6) * 2 / numerical.sqrt(spacing)
                    interpolant = numerical.concatenate([values, spacing * (slopes - basis.derivative @ values)])
                    norm = lambda values: float(numerical.sqrt(numerical.dot(basis.quadrature_weights, values**2)))
                    error = norm(target - maps[0] @ interpolant)
                    first_error = norm(derivative - maps[1] @ interpolant)
                    interpolant_second = norm(maps[2] @ interpolant)
                    label = 'N' + str(intervals) + '_' + kind
                    check(label + '_pointwise_to_L2_interpolation_error_bound', error <= 4 * spacing**2 * curvature_radius + 1e-12)
                    check(label + '_interpolated_first_derivative_error_bound', first_error <= 5 * spacing * curvature_radius + 1e-12)
                    check(label + '_interpolated_second_derivative_bound', interpolant_second <= 14 * curvature_radius + 1e-10)
                    check(label + '_only_endpoint_values_fixed', max(abs(interpolant[[0, count - 1]])) < 1e-12)
                    for branch in ['GR', 'metric_Gram']:
                        include_gram = branch != 'GR'
                        matrices = canonical_matrices(system, packed, speed, include_gram)
                        mass, stiffness = matrices['M'][selection], matrices['K'][selection]
                        projection = solve(mass, maps[0][:, free].T @ (basis.quadrature_weights * density * target), assume_a='sym')
                        graph = solve(mass, stiffness @ projection, assume_a='sym')
                        measured = float(numerical.sqrt(graph @ mass @ graph))
                        coefficients = projection_graph_constants(envelope, include_gram)
                        upper = coefficients['first_constant'] * norm(derivative) + coefficients['curvature_constant'] * curvature_radius
                        check(label + '_' + branch + '_full_projection_graph_bound_with_jumps', measured <= upper)
                        report['controls'].append({'label': label, 'branch': branch, 'interpolation_error': error, 'interpolation_derivative_error': first_error, 'interpolant_second_norm': interpolant_second, 'curvature_radius': float(curvature_radius), 'actual_projected_graph_norm': measured, 'derived_upper': float(upper), 'scope': 'Manufactured scalar function on actual FE/quadrature spaces; not parent evolution.'})
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
        raise RuntimeError('Projection jump controls incomplete.')
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
    final = {'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'commutator_checks': parent['total'], 'projection_checks': report['total'], 'checks': parent['total'] + report['total'], 'saved_states': len(parent['samples']), 'coefficient_controls': len(parent['controls']), 'projection_controls': len(report['controls']), 'inputs': inputs, 'outputs': outputs, 'cited_local_paths_checked': cited, 'protected_workbench_files_written_since_turn_start': len(touched), 'protected_check_method': 'mtime scan since 2026-09-10T00:34:00Z, not a full pre-turn hash baseline', 'no_bytecode_cache': True, 'endpoint_commutator_bound_with_clock_curvature_derived': True, 'parent_curvature_propagation_and_paired_growth_open': True, 'actual_beta_BV_and_full_evolution_open': True, 'valid_for_physics_claim': False}
    with final_path.open('x') as handle:
        json.dump(final, handle, indent=2)
        handle.write('\n')
    print(json.dumps({name: final[name] for name in ['state', 'checks', 'saved_states', 'coefficient_controls', 'projection_controls', 'protected_workbench_files_written_since_turn_start']}), flush=True)


if __name__ == '__main__':
    run()
