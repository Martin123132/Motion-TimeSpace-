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
    from annular_first_derivative_energy_20260909 import affine_lift_matrix, canonical_matrices
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian
    from annular_spatial_clock_energy_20260909 import linear_series, profile
    from annular_paired_variational_energy_20260910 import scalar_maps

    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['derive', 'seal'])
    arguments = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    old_intake = root / 'source-intake/navier-stokes/20260909'
    intake = root / 'source-intake/navier-stokes/20260910'
    pair_folder = intake / 'annular-paired-variational-energy-derived-attempt03'
    parent_folder = intake / 'annular-boundary-trace-projection-derived'
    destination = intake / 'annular-boundary-source-trace-law-derived'
    final_path = intake / 'annular-paired-variational-energy-final-integrity.json'
    parent_path = parent_folder / 'status.json'
    parent = json.loads(parent_path.read_text())
    if parent['state'] != 'complete' or parent['passed'] != parent['total']:
        raise RuntimeError('Projection gate incomplete.')
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

    inherit(inputs, parent['inputs'])
    inherit(outputs, parent['outputs'])
    for path in [Path(__file__).resolve(), parent_path, parent_folder / 'COMPLETE', parent_folder / 'executed-script.py']:
        own(path)
    compile(Path(__file__).read_bytes(), str(Path(__file__)), 'exec')
    if arguments.phase == 'derive':
        destination.mkdir(exist_ok=False)
        (destination / 'executed-script.py').write_bytes(Path(__file__).read_bytes())
        report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': inputs, 'outputs': outputs, 'checks': [], 'samples': [], 'endpoint_coefficients_derived_from_original_source': True, 'Gram_and_quadrature_remainder_retained': True, 'source_H1_mesh_uniform_bound_proved': False, 'boundary_energy_cancellation_proved': False, 'valid_for_physics_claim': False}

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

        save()
        try:
            case_path = old_intake / 'annular-constraint-correction-initial/canonical.json'
            own(case_path)
            case = json.loads(case_path.read_text())
            constants = {name: float(symbolic.sympify(value)) for name, value in case['parameters'].items()}
            kappa = float(symbolic.sympify(case['normalization_kappa']))
            for sample in parent['samples']:
                label, intervals, branch = sample['label'], sample['intervals'], sample['branch']
                steps = 64 if intervals == 64 else 32
                index = int(label.rsplit('sample', 1)[1])
                tag = label.split('_sample')[0]
                base = loaded(old_intake / 'annular-first-derivative-energy-derived' / (label + '.npz'))
                boundary = loaded(old_intake / 'annular-H1-clock-energy-derived' / (label + '.npz'))
                jets = loaded(old_intake / 'annular-metric-flux-jets-derived' / (label + '.npz'))
                spatial = loaded(old_intake / 'annular-spatial-clock-energy-derived' / (label + '.npz'))
                new = loaded(pair_folder / (label + '.npz'))
                source = loaded(old_intake / 'annular-released-Hermite-initial-derived' / (tag + '.npz'))
                folder = 'annular-boundary-N64-evolution-smoke' if intervals == 64 else 'annular-released-Hermite-evolution-smoke'
                trajectory = loaded(old_intake / folder / (tag + '_steps' + str(steps) + '.npz'))
                basis = MixedActionBasis(source['radius'])
                count = basis.radii.size
                time, state = trajectory['time'][index], trajectory['state'][index]
                scalar, slope, momentum, slope_momentum = [state[part * count:(part + 1) * count] for part in range(4)]
                packed, speed, second = state[4 * count:], spatial['packed_speed'], jets['jet_acceleration']
                system = ReleasedHermiteRouthian(basis, scalar, slope, constants, kappa, momentum, slope_momentum, source['outer_clock'][0] + time * source['outer_clock'][1], MetricLinkQuadrature(basis))
                matrices = canonical_matrices(system, packed, speed, branch != 'GR')
                free = base['free']
                potential = numerical.zeros(2 * count)
                potential[free] = solve(base['K'], boundary['boundary_force'], assume_a='sym')

                def source_profile(points):
                    data = profile(system, packed, speed, points)
                    maps = scalar_maps(basis, points)
                    potential_r, potential_rr = maps[1] @ potential, maps[2] @ potential
                    lift_r = maps[1] @ base['lift']
                    lift_time = maps[0] @ base['lift_velocity']
                    lift_time_r = maps[1] @ base['lift_velocity']
                    lift_second = maps[0] @ base['lift_acceleration']
                    mass = linear_series(basis.faces, packed[system.slices[0]], points, 'right')[0]
                    lapse = linear_series(basis.radii, packed[system.slices[1]], points, 'right')[0]
                    mass_time = linear_series(basis.faces, speed[system.slices[0]], points, 'right')[0]
                    lapse_time = linear_series(basis.radii, speed[system.slices[1]], points, 'right')[0]
                    mass_second = linear_series(basis.faces, second[system.slices[0]], points, 'right')[0]
                    lapse_second = linear_series(basis.radii, second[system.slices[1]], points, 'right')[0]
                    spatial_f = 1 - 2 * mass / points
                    theta_time = lapse_second / lapse - (lapse_time / lapse)**2 - mass_second / (points * spatial_f) - 2 * (mass_time / (points * spatial_f))**2
                    characteristic, characteristic_r = data['c'][:2]
                    theta, theta_r = data['theta'][:2]
                    ratio = 2 * characteristic**2 / points + characteristic * characteristic_r
                    ratio_time_flux = ratio * theta + characteristic**2 * theta_r
                    beta = -ratio_time_flux * (potential_r + lift_r) - characteristic**2 * theta * potential_rr - ratio * lift_time_r - 2 * theta * lift_second + (theta**2 - theta_time) * lift_time
                    return beta, theta_time, maps, characteristic, theta, potential_r, potential_rr, lift_r, lift_time_r, ratio, ratio_time_flux

                beta, theta_time, maps, characteristic, theta, potential_r, potential_rr, lift_r, lift_time_r, ratio, ratio_time_flux = source_profile(basis.quadrature)
                trace = source_profile(basis.radii[[0, -1]])[0]
                mass_density = basis.quadrature**2 / characteristic
                radial_density = basis.quadrature**2 * characteristic
                value, radial = maps[0][:, free], maps[1][:, free]
                volume_rhs = value.T @ (basis.quadrature_weights * mass_density * beta)
                gram_rhs = (matrices['K_Gram_dot'] @ potential)[free]
                rhs = base['K_dot'] @ potential[free] - boundary['boundary_force_time']
                quadrature_rhs = rhs - volume_rhs - gram_rhs
                flux = radial_density * (theta * (potential_r + lift_r) + lift_time_r)
                flux_derivative = mass_density * (ratio_time_flux * (potential_r + lift_r) + characteristic**2 * theta * potential_rr + ratio * lift_time_r)
                direct_ibp = radial.T @ (basis.quadrature_weights * flux) + value.T @ (basis.quadrature_weights * flux_derivative)
                close(label + '_old_theta_time_retained', theta_time, boundary['theta_time'])
                close(label + '_retained_quadrature_remainder_independently_derived', quadrature_rhs, direct_ibp)
                close(label + '_affine_Gram_terms_really_annihilated', (matrices['K_Gram_dot'] @ base['lift'] + matrices['K_Gram'] @ base['lift_velocity'])[free], 0.)
                projected_beta = solve(base['M'], volume_rhs, assume_a='sym')
                gram_part = solve(base['M'], gram_rhs, assume_a='sym')
                quadrature_part = solve(base['M'], quadrature_rhs, assume_a='sym')
                close(label + '_actual_source_from_derived_beta_Gram_and_quadrature', projected_beta + gram_part + quadrature_part, new['source_configuration'])
                lift = affine_lift_matrix(basis) @ trace
                endpoint_part = solve(base['M'], (base['full_M'] @ lift)[free], assume_a='sym')
                remainder_part = projected_beta - endpoint_part
                close(label + '_derived_endpoint_source_decomposition', endpoint_part + remainder_part + gram_part + quadrature_part, new['source_configuration'])
                close(label + '_subtracted_beta_has_zero_endpoint_trace', trace - lift[[0, count - 1]], 0.)
                check(label + '_source_and_endpoints_finite', numerical.all(numerical.isfinite(beta)) and numerical.all(numerical.isfinite(trace)))
                pieces = {'endpoint': endpoint_part, 'zero_trace_volume': remainder_part, 'Gram': gram_part, 'quadrature': quadrature_part}
                norms = {name: float(numerical.sqrt(max(part @ base['K'] @ part, 0.))) for name, part in pieces.items()}
                works = {name: float(new['graph'] @ base['K'] @ part) for name, part in pieces.items()}
                close(label + '_all_source_work_retained', sum(works.values()), new['graph'] @ base['K'] @ new['source_configuration'])
                row = {'label': label, 'intervals': intervals, 'branch': branch, 'time': float(time), 'derived_endpoint_coefficients': trace.tolist(), 'diagnostic_only_coefficients_from_prior': sample['diagnostic_endpoint_coefficients'], 'K_norms': norms, 'signed_source_work': works, 'quadrature_weak_residual_max': float(max(abs(quadrature_rhs))), 'source_projection_H1_uniformity_proved': False}
                report['samples'].append(row)
                output = destination / (label + '.npz')
                numerical.savez_compressed(output, beta=beta, derived_endpoint_coefficients=trace, source_endpoint=endpoint_part, source_zero_trace_volume=remainder_part, source_Gram=gram_part, source_quadrature=quadrature_part, quadrature_rhs=quadrature_rhs)
                artifact(output)
                if index == steps:
                    print(json.dumps(row), flush=True)
                save()
            for module in tuple(sys.modules.values()):
                filename = getattr(module, '__file__', None)
                if filename:
                    path = Path(filename).resolve()
                    if path.parent == root / 'scripts' and path.suffix == '.py':
                        own(path)
            check('all_inherited_sources_preserved', all(digest(root / name) == expected for name, expected in inputs.items()))
            check('all_inherited_and_new_evidence_preserved', all(digest(root / name) == expected for name, expected in outputs.items()))
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
        raise RuntimeError('Boundary source derivation incomplete.')
    inherit(inputs, report['inputs'])
    inherit(outputs, report['outputs'])
    for path in [report_path, destination / 'COMPLETE', destination / 'executed-script.py']:
        own(path)
    note = root / 'DERIVATION-20260910-paired-variational-work-and-graph-energy-correction.md'
    cited = [value for value in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')) if value.endswith(('.py', '.md', '.json', '.npz'))]
    missing = [value for value in cited if root / value != final_path and not (root / value).is_file()]
    if missing:
        raise FileNotFoundError(str(missing))
    own(note)
    for attempt_name in ['annular-paired-variational-energy-derived', 'annular-paired-variational-energy-derived-attempt02']:
        for filename in ['status.json', 'executed-script.py']:
            own(intake / attempt_name / filename)
    snapshot = intake / 'annular-paired-variational-energy-resume-snapshot.md'
    with snapshot.open('xb') as handle:
        handle.write((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    artifact(snapshot)
    frozen = root.parent / 'formalization-workbench'
    since = datetime(2026, 9, 9, 23, 45, 0, tzinfo=timezone.utc).timestamp()
    touched = [str(path.relative_to(frozen)) for path in frozen.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    if touched or (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Protected workbench/cache check failed: ' + repr(touched))
    pair = json.loads((pair_folder / 'status.json').read_text())
    final = {'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'paired_checks': pair['total'], 'projection_checks': parent['total'], 'source_trace_checks': report['total'], 'total_checks': pair['total'] + parent['total'] + report['total'], 'saved_states': len(pair['samples']), 'frozen_controls': len(pair['frozen_controls']), 'inputs': inputs, 'outputs': outputs, 'cited_local_paths_checked': cited, 'protected_workbench_files_written_since_turn_start': len(touched), 'protected_check_method': 'mtime scan since 2026-09-09T23:45:00Z, not a full pre-turn hash baseline', 'no_bytecode_cache': True, 'paired_identity_and_graph_correction_derived': True, 'nonzero_trace_projection_obstruction_derived': True, 'actual_source_trace_coefficients_derived': True, 'boundary_energy_correction_and_uniform_growth_open': True, 'full_evolution_closed': False, 'valid_for_physics_claim': False}
    with final_path.open('x') as handle:
        json.dump(final, handle, indent=2)
        handle.write('\n')
    print(json.dumps({name: final[name] for name in ['state', 'total_checks', 'saved_states', 'frozen_controls', 'protected_workbench_files_written_since_turn_start']}), flush=True)


if __name__ == '__main__':
    run()
