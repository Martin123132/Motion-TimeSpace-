from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case, load_owned
from annular_background_time_tangent_20260928 import BackgroundLoads
from annular_background_weak_checks_20260928 import material_weak_derivative, radial_weak_derivative
from annular_background_trace_20260928 import repair_background
from annular_background_eulerian_20260928 import complex_radial_response
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_joint_first_tangent_20260922 import RadialResponse, MomentumMetricResponse, MetricResponse
from annular_joint_flow_derivative_v2_20260922 import solve_joint_rhs
from annular_joint_flow_derivative_20260922 import JointMetricTangent
from annular_candidate_full_inverse_20260920 import BandedSourceInverse
from annular_directional_coupled_Euler_20260928 import restore_flow
from annular_horizontal_clock_evolution_20260913 import ChebyshevRule
from annular_physical_native_kernel_20260928 import NativeKernel
from annular_radial_Ward_moments_20260921 import prepare
from annular_support_radial_response_20260928 import gravitational_moments
from derive_annular_instantaneous_support_trial_v3_20260928 import evaluate
from scipy.sparse import load_npz
from decimal import localcontext
from time import perf_counter
from types import SimpleNamespace
import argparse
import csv
import gc
import hashlib
import json
import numpy as np


class CoordinateAdapter:
    def __init__(self, response):
        self.response, self.cache = response, {}

    def values(self, radius):
        return self.response.values(radius)[None, :, :]


class TotalResponse:
    def __init__(self, background, velocity):
        self.background, self.velocity, self.solver = background, velocity, background.solver

    def values(self, radius):
        return self.background.values(radius) + self.velocity.values(radius)


class ZeroResponse:
    def values(self, radius):
        return np.zeros((2, len(radius)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', default='annular-direct-background-coupled-current-attempt01')
    parser.add_argument('--parent', default='annular-background-time-tangent-attempt02')
    parser.add_argument('--max-seconds', type=float, default=6600)
    args = parser.parse_args()
    evidence = EvidenceRun(args.label, __file__)
    started, deadline = perf_counter(), perf_counter() + args.max_seconds
    try:
        evidence.report.update(scope='Matched coupled accelerations and weak currents using direct Eulerian background derivative',
            new_trajectories=0, subagents_used=False, github_action=False, nonlinear_evolution_solves=0,
            protected_since='2026-09-28T15:08:14+00:00', residual_baseline_subtracted=False,
            source_affine_action_unchanged=True, support_acceleration_added=False)
        evidence.own(evidence.root / 'DERIVATION-20260928-coincident-grid-correction.md')
        evidence.own(evidence.root / 'DERIVATION-20260928-one-sided-source-traces.md')
        parent_path = evidence.output.parent / args.parent / 'status.json'
        parent = json.loads(parent_path.read_text())
        evidence.own(parent_path)
        evidence.check('direct_background_complete', parent['state'] == 'complete' and all(row['passed'] for row in parent['checks']))
        digests, bad = {}, []
        for category in ['inputs', 'outputs']:
            for relative, expected in parent[category].items():
                if relative == 'CURRENT_LOCAL_RESUME.md':
                    continue
                path = evidence.root / relative
                if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                    bad.append(relative)
                else:
                    digests[str(path.relative_to(evidence.root))] = expected
                    evidence.own(path)
        evidence.check('inputs_unchanged', not bad, bad)
        read = lambda relative: load_owned(evidence, digests, evidence.root / relative)
        live = read(str((evidence.output.parent / 'annular-live-support-acceleration-attempt01/status.json').relative_to(evidence.root)))

        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter() - started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)
            if perf_counter() > deadline:
                raise RuntimeError('Safe completed-block current boundary')

        def save(name, **arrays):
            path = evidence.output / (name + '.npz')
            np.savez_compressed(path, **arrays)
            evidence.own(path, 'outputs')
            return str(path.relative_to(evidence.root))

        summaries, currents, weak_rows = [], [], []
        with localcontext() as context:
            context.prec = 70
            for case in parent['cases']:
                branch, level = case['branch'], case['level']
                name = branch + '-' + level
                progress(name + ':restore')
                loads, action, sources = restore_case(evidence, digests, branch, level, deadline)
                archive = read(case['paths']['response'])
                solver, solution = reconstructed_solver(archive)
                solver.rule, solver.nodes = ChebyshevRule(22), archive['nodes']
                background = MetricResponse(solver, solution, archive['forcing'], case['summary']['linear_residual'], [])
                background.field_rates = {key: archive['tangent_' + key] for key in ['temporal_square', 'gradient_square', 'gram', 'source_density', 'velocity']}
                engine = BackgroundLoads(loads, action)
                untraced = radial_weak_derivative(background)
                background = repair_background(engine, action, archive)
                checked = complex_radial_response(background, action, engine.extension)
                response_scale = max(float(np.max(abs(background.solution['state']))), 1e-30)
                complex_error = float(np.max(abs(checked - background.solution['state'])))
                evidence.check(name + ':traced_complex_radial', complex_error <= 2e-8 * response_scale + 1e-25,
                    dict(error=complex_error, scale=response_scale))
                evidence.check(name + ':traced_linear_residual', background.residual <= 1e-12 * response_scale + 1e-25, background.residual)
                evidence.check(name + ':traced_background_replay', background.background_residual <= 2e-12, background.background_residual)
                direct48 = material_weak_derivative(engine, 48)
                direct64 = material_weak_derivative(engine, 64)
                radial = radial_weak_derivative(background)
                paths = dict(weak=save(name + '-weak-density', direct48=direct48, direct64=direct64, radial=radial, untraced=untraced))
                paths['background_response'] = save(name + '-traced-background', **background.solution,
                    forcing=background.forcing, edges=background.solver.edges, nodes=background.solver.nodes,
                    **{prefix + key: value for prefix, collection in [('base_', background.fields), ('tangent_', background.field_rates)] for key, value in collection.items()})
                for index, field in enumerate(['temporal_square', 'gradient_square', 'gram', 'source_density']):
                    for power in range(3):
                        error = abs(float(radial[index, power] - direct64[index, power]))
                        quad_error = abs(float(direct48[index, power] - direct64[index, power]))
                        tolerance = (2e-11 if field == 'source_density' else 2e-14) + 2e-7 * abs(float(direct64[index, power]))
                        if field == 'gram':
                            tolerance = 1e-21 + 2e-7 * abs(float(direct64[index, power]))
                        evidence.check(name + ':weak_transport:' + field + ':' + str(power), error <= tolerance, dict(error=error, tolerance=tolerance))
                        evidence.check(name + ':material_weak:' + field + ':' + str(power), quad_error <= tolerance, quad_error)
                        weak_rows.append(dict(branch=branch, level=level, field=field, power=power,
                            radial=float(radial[index, power]), material=float(direct64[index, power]), error=error, material_error=quad_error))
                evidence.check(name + ':trace_repair_reduces_resolved_source_error',
                    abs(float(untraced[3, 0])) <= 2e-11 or abs(float(radial[3, 0])) < .01 * abs(float(untraced[3, 0])),
                    dict(untraced_number_rate=float(untraced[3, 0]), traced_number_rate=float(radial[3, 0]),
                        negative_control_resolved=abs(float(untraced[3, 0])) > 2e-11))
                flow, old_tangent, centre = restore_flow(evidence, digests, action, sources, level)
                matrix_path = evidence.root / centre['matrix_path']
                evidence.check(name + ':matrix_owned', str(matrix_path.relative_to(evidence.root)) in digests)
                matrix = load_npz(matrix_path)
                inverse = BandedSourceInverse(matrix, loads.rates.shape)
                momentum = MomentumMetricResponse(action, deadline, lambda stage: progress(name + ':' + stage))
                coordinate_momentum = momentum.accumulate(background.values)
                response = RadialResponse(loads, action, branch.split('-')[1], deadline, lambda stage: progress(name + ':' + stage))
                evidence.check(name + ':radial_velocity_background', response.base_constraint_residual <= 2e-12, response.base_constraint_residual)
                rhs = flow['force'] - flow['coordinate_convection'] - coordinate_momentum
                system = dict(matrix=matrix, inverse=inverse)
                iteration_paths = []

                def record(row, acceleration, coupling, residual, metric):
                    path = save(name + '-joint-iteration' + str(row['iteration']), acceleration=acceleration, coupling=coupling,
                        residual=residual, forcing=metric.forcing, **{'metric_' + key: value for key, value in metric.solution.items()})
                    iteration_paths.append(dict(row, path=path))
                    evidence.report['latest_iteration'] = dict(case=name, **iteration_paths[-1])
                    progress(name + ':joint-' + str(row['iteration']))

                acceleration, velocity_response, coupling, unused, history = solve_joint_rhs(system, response, momentum, rhs, record)
                evidence.check(name + ':coupled_old_Euler', history[-1]['relative_residual'] <= 2e-11 and history[-1]['maximum_correction'] <= 2e-12, history[-1])
                tangent = JointMetricTangent(CoordinateAdapter(background), [velocity_response])
                total = TotalResponse(background, velocity_response)
                sampled_radius = flow['radius']
                paths['flow'] = save(name + '-direct-flow', acceleration=acceleration, coordinate_momentum=coordinate_momentum,
                    archived_accelerations=flow['accelerations'], archived_coordinate_momentum=flow['coordinate_momentum'],
                    rhs=rhs, force=flow['force'], coordinate_convection=flow['coordinate_convection'], coupling=coupling,
                    radius=sampled_radius, metric_rate=total.values(sampled_radius), archived_metric_rate=flow['metric_rate'])
                paths['velocity_response'] = save(name + '-velocity-response', **velocity_response.solution,
                    edges=velocity_response.solver.edges, forcing=velocity_response.forcing)
                gravity24 = gravitational_moments(action, total, 24)
                gravity32 = gravitational_moments(action, total, 32)
                gravity_error = float(np.max(abs(gravity24 - gravity32)))
                evidence.check(name + ':gravity24_32', gravity_error <= 2e-17, gravity_error)
                previous = next(row for row in live['cases'] if row['branch'] == branch and row['level'] == level)
                directions = read(previous['direction_path'])
                packet = read(sources['packet'])
                native = NativeKernel(packet['mesh'], packet['gram_support'], branch == 'MTS-primary')
                polynomial, unused = prepare(action, loads, acceleration)
                correction = np.zeros_like(acceleration)
                material_paths, material_forces, material_currents = [], [], []
                for order in [48, 64]:
                    labels, weights = np.polynomial.legendre.leggauss(order)
                    labels, weights = labels / 2, weights / 2
                    weights *= 6 * (labels + .5) * (.5 - labels)
                    forces, moments = [], []
                    for index, label in enumerate(labels):
                        if index % 16 == 0:
                            progress(name + ':current-material' + str(order) + ':' + str(index))
                        force, current = evaluate(native, loads, action, tangent, acceleration, polynomial,
                            directions, correction, ZeroResponse(), 0., label, 12)
                        forces.append(force)
                        moments.append(current)
                    forces, moments = np.array(forces), np.array(moments)
                    mean_force = weights @ forces
                    mean_current = np.tensordot(weights, moments, axes=(0, 0))
                    material_forces.append(mean_force)
                    material_currents.append(mean_current)
                    material_paths.append(save(name + '-current-material' + str(order), labels=labels, weights=weights,
                        forces=forces, moments=moments, average_force=mean_force, average_current=mean_current,
                        gravity24=gravity24, gravity32=gravity32))
                    evidence.check(name + ':Euler_identity:' + str(order), np.max(abs(forces[:, 0] - forces[:, 2])) <= 2e-15,
                        float(np.max(abs(forces[:, 0] - forces[:, 2]))))
                    for power in range(3):
                        currents.append(dict(branch=branch, level=level, material_order=order, power=power,
                            wave=float(mean_current[power, 0]), gram=float(mean_current[power, 1]), dust=float(mean_current[power, 2]),
                            matter=float(mean_current[power, 3]), gravity=float(gravity32[power]),
                            total=float(mean_current[power, 3] + gravity32[power]), support_force=float(mean_force[0])))
                current_error = float(np.max(abs(material_currents[1] - material_currents[0])))
                force_error = float(np.max(abs(material_forces[1] - material_forces[0])))
                evidence.check(name + ':material_current48_64', current_error <= 3e-17, current_error)
                evidence.check(name + ':material_force48_64', force_error <= 2e-17, force_error)
                summary = dict(branch=branch, level=level, current_h0=float(material_currents[-1][0, 3] + gravity32[0]),
                    source_force=float(material_forces[-1][0]), maximum_acceleration=float(np.max(abs(acceleration))),
                    acceleration_change=float(np.max(abs(acceleration - flow['accelerations'][-1]))),
                    coordinate_momentum_change=float(np.max(abs(coordinate_momentum - flow['coordinate_momentum'][-1]))),
                    coupled_relative_residual=history[-1]['relative_residual'], current_material_error=current_error,
                    force_material_error=force_error, gravity_error=gravity_error)
                summaries.append(summary)
                evidence.report['cases'].append(dict(branch=branch, level=level, sources=sources,
                    background_path=case['paths']['response'], paths=paths, material_paths=material_paths,
                    iterations=iteration_paths, summary=summary))
                evidence.save()
                progress(name + ':saved')
                del loads, action, response, momentum, inverse, matrix, old_tangent, background, native, engine
                gc.collect()
        for filename, rows in [('direct-coupled-summary.csv', summaries), ('direct-current-moments.csv', currents), ('weak-density-transport.csv', weak_rows)]:
            path = evidence.output / filename
            with path.open('w', newline='', encoding='utf-8') as stream:
                writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            evidence.own(path, 'outputs')
        evidence.report.update(seconds=perf_counter() - started, summaries=summaries,
            direct_background_coupled=True, same_four_current_cases_complete=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
