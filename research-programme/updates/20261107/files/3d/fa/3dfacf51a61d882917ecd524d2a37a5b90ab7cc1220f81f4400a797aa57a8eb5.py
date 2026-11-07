from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case, load_owned
from annular_live_compensation_derivative_20260928 import mixed_radial, material_derivative, OldResponse
from annular_compensation_cardinal_source_20260928 import CompensationLoads
from annular_compensation_complex_oracle_v2_20260928 import complex_mixed_wave
from annular_support_radial_response_20260928 import SupportRadialResponse
from annular_compensation_oracle_transport_20260928 import full_oracle, resolved_control
from annular_joint_first_tangent_20260922 import MetricResponse, MomentumMetricResponse
from annular_joint_flow_derivative_v2_20260922 import solve_joint_rhs
from derive_annular_direct_background_coupled_current_20260928 import TotalResponse
from annular_candidate_full_inverse_20260920 import BandedSourceInverse
from scipy.sparse import load_npz
from decimal import localcontext
from time import perf_counter
from pathlib import Path
import argparse
import csv
import gc
import hashlib
import json
import numpy as np
import sympy as sp


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', default='annular-live-compensation-time-attempt04')
    parser.add_argument('--max-seconds', type=float, default=9000)
    parser.add_argument('--case-limit', type=int, default=4)
    args = parser.parse_args()
    evidence = EvidenceRun(args.label, __file__)
    started, deadline = perf_counter(), perf_counter() + args.max_seconds
    try:
        evidence.report.update(scope='Differentiate the live compensator along the direct coupled jet',
            github_action=False, subagents_used=False, new_trajectories=0,
            original_workbench_write=False, full_velocity_current_column_computed=False)
        evidence.own(evidence.root / 'DERIVATION-20260928-live-compensation-time-derivative.md')
        evidence.own(evidence.root / 'DERIVATION-20260928-compensation-source-replay-correction.md')
        evidence.own(evidence.root / 'DERIVATION-20260928-compensation-oracle-convention.md')
        evidence.own(evidence.root / 'DERIVATION-20260928-compensation-end-to-end-precision.md')
        seal_path = evidence.output.parent / 'annular-direct-background-final-integrity-20260928.json'
        seal = json.loads(seal_path.read_text())
        evidence.own(seal_path)
        digests, bad = {}, []
        for relative, expected in seal['hashes'].items():
            if relative == 'CURRENT_LOCAL_RESUME.md':
                continue
            path = evidence.root / relative
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                bad.append(relative)
            else:
                digests[str(path.relative_to(evidence.root))] = expected
                evidence.own(path)
        evidence.check('all_prior_scientific_inputs_unchanged', seal['state'] == 'complete' and not bad, bad)
        read = lambda relative: load_owned(evidence, digests, evidence.root / relative)
        status = lambda name: read(str((evidence.output.parent / name / 'status.json').relative_to(evidence.root)))
        parent = status('annular-direct-background-coupled-current-attempt01')
        live = status('annular-live-support-acceleration-attempt01')
        geometric = status('annular-geometric-support-jet-attempt01')
        time = sp.symbols('time')
        mass, response, radius = sp.Function('mass')(time), sp.Function('response')(time), sp.symbols('radius')
        boundary = sp.diff(-response / (radius - 2 * mass), time)
        expected = -sp.diff(response, time) / (radius - 2 * mass) - 2 * response * sp.diff(mass, time) / (radius - 2 * mass)**2
        evidence.check('differentiated_outer_boundary_identity', sp.simplify(boundary - expected) == 0)
        amplitude, mode = sp.Function('s')(time), sp.Function('mode')(time)
        jet = sp.diff(amplitude * mode, time, 2).subs({amplitude: 0, sp.diff(amplitude, time): 1, sp.diff(amplitude, time, 2): 0})
        evidence.check('completed_velocity_jet_factor_two', sp.simplify(jet - 2 * sp.diff(mode, time)) == 0)

        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter() - started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)
            if perf_counter() > deadline:
                raise RuntimeError('Safe live-compensation block boundary')

        def save(name, **arrays):
            path = evidence.output / (name + '.npz')
            np.savez_compressed(path, **arrays)
            evidence.own(path, 'outputs')
            return str(path.relative_to(evidence.root))

        summaries, iteration_rows = [], []
        with localcontext() as context:
            context.prec = 70
            for case in parent['cases'][:args.case_limit]:
                branch, level = case['branch'], case['level']
                name = branch + '-' + level
                progress(name + ':restore')
                loads, action, sources = restore_case(evidence, digests, branch, level, deadline)
                previous = next(item for item in live['cases'] if item['branch'] == branch and item['level'] == level)
                original = next(item for item in geometric['cases'] if item['branch'] == branch and item['level'] == level)
                directions = read(previous['direction_path'])
                projection = read(previous['paths']['projection'])
                correction = projection['correction']
                transport_rate = read(original['vertex_path'])['vertices'] / 2
                flow = read(case['paths']['flow'])
                background_archive = read(case['paths']['background_response'])
                velocity_archive = read(case['paths']['velocity_response'])
                support_archive = read(previous['paths']['live_response'])
                owner = read(sources['parent'])
                centre = next(item for item in owner['centres'] if item.get('route') == 'resampled') if level == 'fine' else owner['centres'][0]
                matrix_path = evidence.root / centre['matrix_path']
                evidence.check(name + ':matrix_owned', str(matrix_path.relative_to(evidence.root)) in digests)
                matrix = load_npz(matrix_path)
                inverse = BandedSourceInverse(matrix, loads.rates.shape)
                radial = SupportRadialResponse(loads, action, branch.split('-')[1], directions, deadline, lambda stage: progress(name + ':' + stage))
                evidence.check(name + ':radial_background', radial.base_residual <= 2e-12, radial.base_residual)
                keys = ['state', 'rhs_coefficients', 'primitives', 'left']
                restore = lambda archive: MetricResponse(radial.solver, {key: archive[key] for key in keys}, archive['forcing'], 0., [])
                background, velocity, support = [restore(archive) for archive in [background_archive, velocity_archive, support_archive]]
                time_response = TotalResponse(background, velocity)
                replay = radial.apply(-correction)
                replay_error = float(np.max(abs(replay.solution['state'] - support.solution['state'])))
                evidence.check(name + ':live_response_replay', replay_error <= 1e-25 + 2e-9 * np.max(abs(support.solution['state'])), replay_error)
                engine = CompensationLoads(loads, action, flow['acceleration'], directions, correction, transport_rate)
                engine.velocity_response_temporal = radial.temporal @ flow['acceleration'].ravel()
                engine.velocity_response_velocity = radial.velocity @ flow['acceleration'].ravel()
                probe_indices = np.linspace(0, len(radial.solver.lengths) - 1, 41, dtype=int)
                radii = radial.solver.centers[probe_indices] + .173 * radial.solver.lengths[probe_indices]
                base_probe, rate_probe = engine.mixed_wave(radii)
                oracle = complex_mixed_wave(engine, radii, 1j * 1e-25)
                probe_error = float(np.max(abs(oracle.imag / 1e-25 - rate_probe)))
                probe_scale = float(np.max(abs(rate_probe)))
                relative_density_pass = probe_error <= 1e-23 + 2e-7 * probe_scale
                controlled, controlled_oracle = resolved_control(engine, radii)
                control_error = float(np.max(abs(controlled - controlled_oracle)))
                control_scale = float(np.max(abs(controlled)))
                evidence.check(name + ':resolved_nonlinear_complex_mixed_density', control_error <= 1e-23 + 2e-7 * control_scale,
                    dict(error=control_error, scale=control_scale, samples=len(radii)))
                paths = dict(sample=save(name + '-mixed-density-oracle', radius=radii, base=base_probe,
                    analytic=rate_probe, complex_derivative=oracle.imag / 1e-25,
                    frozen_cuts=engine.mixed_wave(radii, True)[1],
                    resolved_control=controlled, resolved_control_oracle=controlled_oracle))
                mixed = engine.mixed_sample(radial.solver, lambda stage: progress(name + ':' + stage))
                oracle_rate = full_oracle(engine, radial.solver, lambda stage: progress(name + ':' + stage))
                paths['density'] = save(name + '-mixed-density', **mixed, oracle_temporal_rate=oracle_rate, nodes=radial.solver.nodes, edges=radial.solver.edges)
                density_error = float(np.max(abs(mixed['temporal'] - support_archive['delta_temporal'])))
                density_scale = float(np.max(abs(support_archive['delta_temporal'])))
                evidence.check(name + ':compensated_density_replay', density_error <= 2e-21 + 2e-8 * density_scale,
                    dict(error=density_error, scale=density_scale))
                derivative_response = mixed_radial(engine, action, background_archive, time_response, support, mixed)
                alternate_mixed = dict(mixed, temporal_rate=oracle_rate)
                alternate_response = mixed_radial(engine, action, background_archive, time_response, support, alternate_mixed)
                paths['mixed_response'] = save(name + '-mixed-response', **derivative_response.solution,
                    forcing=derivative_response.forcing, forcing_rate=derivative_response.forcing_rate,
                    complex_check=derivative_response.complex_check, boundary=derivative_response.boundary,
                    nodes=radial.solver.nodes, edges=radial.solver.edges,
                    **{'alternate_' + key: value for key, value in alternate_response.solution.items()})
                radial_scale = float(np.max(abs(derivative_response.solution['state'])))
                radial_error = float(np.max(abs(derivative_response.solution['state'] - derivative_response.complex_check)))
                evidence.check(name + ':mixed_radial_complex_linear_system', radial_error <= 1e-25 + 2e-8 * radial_scale,
                    dict(error=radial_error, scale=radial_scale))
                evidence.check(name + ':mixed_radial_equation', derivative_response.residual <= 1e-25 + 1e-12 * radial_scale, derivative_response.residual)
                boundary_values = derivative_response.values(np.array([radial.solver.edges[0], radial.solver.edges[-1]]))
                outer_factor = radial.solver.edges[-1] - 2 * action.solution['state'][0, -1, -1]
                boundary_error = max(abs(boundary_values[0, 0]), abs(boundary_values[1, -1] + boundary_values[0, -1] / outer_factor - derivative_response.boundary))
                evidence.check(name + ':mixed_outer_boundary', boundary_error <= 1e-25 + 1e-12 * radial_scale, float(boundary_error))
                packets = {}
                for order in [48, 64]:
                    progress(name + ':material' + str(order))
                    packet = material_derivative(engine, action, time_response, support, derivative_response, order)
                    paths['material' + str(order)] = save(name + '-material' + str(order), **packet)
                    packets[order] = packet
                    error = float(np.max(abs(packet['derivative'] - packet['complex_derivative'])))
                    scale = float(np.max(abs(packet['derivative'])))
                    evidence.check(name + ':material_complex:' + str(order), error <= 1e-24 + 2e-10 * scale,
                        dict(error=error, scale=scale))
                quadrature_error = float(np.max(abs(packets[64]['derivative'] - packets[48]['derivative'])))
                derivative_scale = float(np.max(abs(packets[48]['derivative'])))
                evidence.check(name + ':material48_64', quadrature_error <= 2e-18 + 2e-7 * derivative_scale,
                    dict(error=quadrature_error, scale=derivative_scale))
                momentum = MomentumMetricResponse(action, deadline, lambda stage: progress(name + ':' + stage))
                iteration_paths = []

                def record(row, direction, coupling, residual, metric):
                    path = save(name + '-iteration' + str(row['iteration']), derivative=direction, coupling=coupling,
                        residual=residual, **{'metric_' + key: value for key, value in metric.solution.items()})
                    iteration_paths.append(dict(row, path=path))
                    iteration_rows.append(dict(branch=branch, level=level, **row))
                    progress(name + ':projection-derivative-' + str(row['iteration']))

                derivative, response, coupled, unused, history = solve_joint_rhs(dict(inverse=inverse, matrix=matrix),
                    OldResponse(radial), momentum, packets[48]['derivative'], record)
                alternate_packet = material_derivative(engine, action, time_response, support, alternate_response, 48)
                paths['alternate_material'] = save(name + '-alternate-material48', **alternate_packet)
                alternate_rhs = alternate_packet['derivative'] - packets[48]['derivative']
                sensitivity_rows = []
                def record_sensitivity(row, direction, coupling, residual, metric):
                    sensitivity_rows.append(row)
                sensitivity, unused_response, unused_coupling, unused_rhs, sensitivity_history = solve_joint_rhs(
                    dict(inverse=inverse, matrix=matrix), OldResponse(radial), momentum, alternate_rhs, record_sensitivity)
                sensitivity_max = float(np.max(abs(sensitivity)))
                evidence.check(name + ':full_grid_oracle_to_live_inverse', sensitivity_max <= 2e-12,
                    dict(maximum_wdot_change=sensitivity_max, full_grid_density_discrepancy=float(np.max(abs(oracle_rate - mixed['temporal_rate']))),
                        relative_density_gate_pass=bool(relative_density_pass)))
                paths['sensitivity'] = save(name + '-full-grid-oracle-sensitivity', delta_rhs=alternate_rhs, delta_wdot=sensitivity)
                amplified_quad = inverse.solve((packets[64]['derivative'] - packets[48]['derivative']).ravel())
                maximum_derivative = float(np.max(abs(derivative)))
                quadrature_inverse = float(np.max(abs(amplified_quad)))
                evidence.check(name + ':inverse_amplified_material_quadrature', quadrature_inverse <= 2e-8 + 1e-5 * maximum_derivative,
                    dict(error=quadrature_inverse, scale=maximum_derivative))
                evidence.check(name + ':live_derivative_solved', history[-1]['relative_residual'] <= 2e-11 and history[-1]['maximum_correction'] <= 2e-12, history[-1])
                completed_field_rate = transport_rate - derivative[:, :-1]
                paths['derivative'] = save(name + '-compensation-time-derivative', correction=correction, derivative=derivative,
                    original_transport_rate=transport_rate, completed_field_rate=completed_field_rate,
                    completed_source_rate=-derivative[:, -1], raw_rhs=packets[48]['derivative'],
                    inverse_amplified_quadrature=amplified_quad,
                    completed_metric_rate=derivative_response.solution['state'] - response.solution['state'])
                summary = dict(branch=branch, level=level, maximum_wdot=maximum_derivative,
                    maximum_field_wdot=float(np.max(abs(derivative[:, :-1]))),
                    maximum_source_wdot=float(np.max(abs(derivative[:, -1]))),
                    original_zdot_max=float(np.max(abs(transport_rate))), completed_zdot_max=float(np.max(abs(completed_field_rate))),
                    frozen_projection_rate=derivative_scale,
                    metric_feedback_rhs_max=float(np.max(abs(packets[48]['metric_feedback_derivative']))),
                    material48_64_max=quadrature_error, inverse_amplified_material_error=quadrature_inverse,
                    mixed_radial_max=radial_scale, mixed_radial_oracle_error=radial_error,
                    outer_boundary_extra=float(derivative_response.boundary),
                    solved_relative_residual=history[-1]['relative_residual'], solved_maximum_correction=history[-1]['maximum_correction'],
                    compensated_density_relative_gate_pass=bool(relative_density_pass), density_probe_error=probe_error,
                    density_probe_scale=probe_scale, full_grid_density_oracle_error=float(np.max(abs(oracle_rate - mixed['temporal_rate']))),
                    independent_oracle_wdot_change=sensitivity_max, valid_for_physics_claim=False)
                summaries.append(summary)
                evidence.report['cases'].append(dict(branch=branch, level=level, paths=paths, sources=sources,
                    iterations=iteration_paths, summary=summary))
                evidence.save()
                progress(name + ':saved')
                del radial, engine, momentum, matrix, inverse, replay, support, background, velocity, time_response, derivative_response, alternate_response
                gc.collect()
        for filename, rows in [('compensation-time-summary.csv', summaries), ('projection-time-iterations.csv', iteration_rows)]:
            path = evidence.output / filename
            with path.open('w', newline='', encoding='utf-8') as stream:
                writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            evidence.own(path, 'outputs')
        evidence.report.update(seconds=perf_counter() - started, summaries=summaries, full_four_cases=len(summaries) == 4)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
