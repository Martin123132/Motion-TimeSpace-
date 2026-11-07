from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case, load_owned
from annular_compensated_position_20260928 import PositionLoads
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_candidate_radial_constraint_20260920 import radial_rhs
from annular_background_time_tangent_20260928 import FIELD_NAMES
from annular_radial_time_forcing_20260928 import explicit_time_forcing
from annular_joint_first_tangent_20260922 import MetricResponse, RadialResponse
from annular_physical_native_kernel_20260928 import NativeKernel
from annular_live_P2_canonical_v2_20260918 import material_weight
from decimal import localcontext
from time import perf_counter
import argparse
import csv
import gc
import hashlib
import json
import numpy as np
import sympy as sp


def symbolic_jet(evidence):
    time, variation = sp.symbols('time variation')
    amplitude = sp.Function('amplitude')(time)
    field = sp.Function('field')(time)
    mode = sp.Function('mode')(time)
    support = sp.Function('support')(time)
    eta = sp.symbols('eta')
    old_field, old_rate, old_support, old_support_rate = sp.symbols('old_field old_rate old_support old_support_rate')
    metric = old_field**2 * old_rate + old_field * old_support_rate**2 + old_support**2 * old_rate**2 + old_support_rate * old_rate
    base = {old_field: field, old_rate: sp.diff(field, time), old_support: support, old_support_rate: sp.diff(support, time)}
    moved_field, moved_support = field + variation * amplitude * mode, support + variation * amplitude * eta
    moved = metric.subs({old_field: moved_field, old_rate: sp.diff(moved_field, time), old_support: moved_support, old_support_rate: sp.diff(moved_support, time)})
    position = sp.diff(metric, old_field).subs(base) * mode + sp.diff(metric, old_support).subs(base) * eta
    velocity = sp.diff(metric, old_rate).subs(base) * mode + sp.diff(metric, old_support_rate).subs(base) * eta
    transported = sp.diff(metric, old_rate).subs(base) * sp.diff(mode, time)
    first = sp.diff(moved, variation).subs(variation, 0)
    evidence.check('nonlinear_polynomial_metric_full_first_jet', sp.expand(first - amplitude * (position + transported) - sp.diff(amplitude, time) * velocity) == 0)
    expected = position + transported + sp.diff(velocity, time)
    actual = sp.diff(first, time).subs({sp.diff(amplitude, time, 2): 0, sp.diff(amplitude, time): 1, amplitude: 0})
    evidence.check('nonlinear_polynomial_metric_velocity_time_jet', sp.expand(actual - expected) == 0)
    acceleration = sp.diff(moved_field, time, 2).diff(variation).subs(variation, 0)
    acceleration = acceleration.subs({sp.diff(amplitude, time, 2): 0, sp.diff(amplitude, time): 1, amplitude: 0})
    evidence.check('field_acceleration_twice_transported_mode', sp.simplify(acceleration - 2 * sp.diff(mode, time)) == 0)
    position, velocity, acceleration, support_rate, support_acceleration, inertia = sp.symbols('position velocity acceleration support_rate support_acceleration inertia')
    connection = sp.Function('connection')(position)
    potential = sp.Function('potential')(position)
    lagrangian = (velocity - connection * support_rate)**2 / 2 + inertia * support_rate**2 / 2 - potential
    momentum = sp.diff(lagrangian, velocity)
    momentum_rate = sp.diff(momentum, position) * velocity + sp.diff(momentum, velocity) * acceleration + sp.diff(momentum, support_rate) * support_acceleration
    euler = momentum_rate - sp.diff(lagrangian, position)
    mode_rate = sp.diff(connection, position) * velocity
    pure_velocity_momentum = sp.diff(momentum, velocity) * connection + sp.diff(momentum, support_rate)
    changed_euler = euler.subs({velocity: velocity + variation * connection, acceleration: acceleration + 2 * variation * mode_rate, support_rate: variation, support_acceleration: 0}, simultaneous=True)
    residual = sp.diff(changed_euler, variation).subs(variation, 0)
    evidence.check('orthogonal_mode_counterexample_zero_momentum', sp.simplify(pure_velocity_momentum) == 0)
    evidence.check('orthogonal_mode_counterexample_nonzero_Euler', sp.simplify(residual - 2 * mode_rate) == 0)
    evidence.check('orthogonal_mode_counterexample_reaction', sp.simplify(residual - 2 * mode_rate * sp.diff(momentum, velocity)) == 0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--parent', default='annular-compensated-position-attempt03')
    parser.add_argument('--label', default='annular-position-metric-jet-validation-attempt01')
    parser.add_argument('--max-seconds', type=float, default=4800)
    args = parser.parse_args()
    evidence = EvidenceRun(args.label, __file__)
    started, deadline = perf_counter(), perf_counter() + args.max_seconds
    try:
        evidence.report.update(scope='Off-grid position response and completed kinematic metric-time jet',
            github_action=False, subagents_used=False, new_trajectories=0, original_workbench_write=False,
            inherited_mixed_time_precision_warning_count=4, inherited_pointwise_mixed_time_accuracy_pass=False,
            full_force_current_column_computed=False, old_Euler_velocity_reaction_solved=False)
        evidence.own(evidence.root / 'DERIVATION-20260928-position-metric-jet-and-old-reaction.md')
        path = evidence.output.parent / args.parent / 'status.json'
        parent = json.loads(path.read_text())
        evidence.own(path)
        evidence.check('position_parent_complete', parent['state'] == 'complete' and len(parent['cases']) == 4 and all(row['passed'] for row in parent['checks']))
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
        evidence.check('parent_hashes_unchanged', not bad, bad)
        read = lambda relative: load_owned(evidence, digests, evidence.root / relative)
        status = lambda name: read(str((evidence.output.parent / name / 'status.json').relative_to(evidence.root)))
        live = status('annular-live-support-acceleration-attempt01')
        transport = status('annular-live-compensation-time-attempt04')
        direct = status('annular-direct-background-coupled-current-attempt01')
        symbolic_jet(evidence)

        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter() - started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)
            if perf_counter() > deadline:
                raise RuntimeError('Safe metric-jet validation boundary')

        def save(name, **arrays):
            path = evidence.output / (name + '.npz')
            np.savez_compressed(path, **arrays)
            evidence.own(path, 'outputs')
            return str(path.relative_to(evidence.root))

        summaries = []
        with localcontext() as context:
            context.prec = 70
            for case in parent['cases']:
                branch, level = case['branch'], case['level']
                name = branch + '-' + level
                progress(name + ':restore')
                loads, action, sources = restore_case(evidence, digests, branch, level, deadline)
                loads.owner.label_order = 28
                select = lambda authority: next(row for row in authority['cases'] if row['branch'] == branch and row['level'] == level)
                previous, timed, flow = select(live), select(transport), select(direct)
                directions = read(previous['direction_path'])
                correction = read(previous['paths']['projection'])['correction']
                packet = read(sources['packet'])
                native = NativeKernel(packet['mesh'], packet['gram_support'], branch == 'MTS-primary')
                engine = PositionLoads(loads, action, native, directions, correction)
                if native.enabled:
                    expansion = read(case['paths']['native'])
                    engine.image_coefficients = expansion['image_coefficients']
                    engine.image_direction_coefficients = expansion['image_direction_coefficients']
                archive = read(case['paths']['response'])
                solver, solution = reconstructed_solver(archive)
                position = MetricResponse(solver, solution, archive['forcing'], 0., [])
                selected = np.linspace(0, len(solver.lengths) - 1, 257, dtype=int)
                radius = (solver.centers[selected, None] + solver.lengths[selected, None] * np.array([-.273, .037, .311])).ravel()
                fields, rates = engine.sample(radius)
                state = action.solver.values(action.solution, radius)[0]
                unused, local = radial_rhs(radius, *state, *[fields[key] for key in FIELD_NAMES], engine.owner.coupling, engine.owner.source_mass, True)
                forcing = explicit_time_forcing(radius, *state, fields['source_density'], fields['velocity'], *[rates[key] for key in FIELD_NAMES], engine.owner.coupling, engine.owner.source_mass)
                values, derivative = solver.values(solution, radius)
                expected = np.einsum('abn,bn->an', local, values) + forcing
                paths = dict(off_grid=save(name + '-off-grid-position', radius=radius, derivative=derivative, expected=expected, values=values))
                strong_errors = []
                for component, title in enumerate(['mass', 'lapse']):
                    error = float(np.max(abs(derivative[component] - expected[component])))
                    scale = float(np.max(abs(expected[component])))
                    tolerance = 2e-6 * scale + 1e-25
                    evidence.check(name + ':offgrid_position_' + title, error <= tolerance, dict(error=error, scale=scale, tolerance=tolerance))
                    strong_errors.append(error)
                if native.enabled:
                    labels, weights = np.polynomial.legendre.leggauss(48)
                    labels, weights = labels / 2, weights / 2
                    weights *= material_weight(labels)
                    direct_native, fitted_native = np.zeros(3), np.zeros(3)
                    for index, (label, weight) in enumerate(zip(labels, weights)):
                        if index % 16 == 0:
                            progress(name + ':independent-native-weak-' + str(index))
                        image, change, data, edges, unused = engine.native_direct(label)
                        load = np.asarray(native.apply('sampling', image**2 / 2, True), float)
                        delta_load = np.asarray(native.apply('sampling', image * change, True), float)
                        physical = np.asarray(data['edges'][native.native_edges], float)
                        movement = np.asarray(edges[native.native_edges], float)
                        fitted_image = np.polynomial.chebyshev.chebval(2 * label, engine.image_coefficients)
                        fitted_change = np.polynomial.chebyshev.chebval(2 * label, engine.image_direction_coefficients)
                        fitted_load = np.asarray(native.sampling.T @ (fitted_image**2 / 2)).ravel()
                        fitted_delta = np.asarray(native.sampling.T @ (fitted_image * fitted_change)).ravel()
                        for power in range(3):
                            direct_native[power] += weight * np.sum(physical**power * delta_load)
                            fitted_native[power] += weight * np.sum(physical**power * fitted_delta)
                            if power:
                                direct_native[power] += weight * np.sum(power * physical**(power - 1) * movement * load)
                                fitted_native[power] += weight * np.sum(power * physical**(power - 1) * movement * fitted_load)
                    paths['native_weak'] = save(name + '-direct-native-weak', direct=direct_native, fitted=fitted_native)
                    evidence.check(name + ':direct_native_weak', np.max(abs(direct_native - fitted_native)) <= 2e-9 * np.max(abs(direct_native)) + 1e-23,
                        dict(error=float(np.max(abs(direct_native - fitted_native))), scale=float(np.max(abs(direct_native)))))
                progress(name + ':complete-metric-time-jet')
                saved = read(timed['paths']['derivative'])
                mode_rate = np.column_stack([saved['completed_field_rate'], saved['completed_source_rate']])
                radial = RadialResponse(loads, action, branch.split('-')[1], deadline, lambda stage: progress(name + ':' + stage))
                old_rate = radial.apply(mode_rate)
                mixed = read(timed['paths']['mixed_response'])
                final = read(timed['iterations'][-1]['path'])
                keys = ['state', 'rhs_coefficients', 'primitives', 'left']
                velocity_rate = {key: mixed[key] - final['metric_' + key] for key in keys}
                total = {key: solution[key] + old_rate.solution[key] + velocity_rate[key] for key in keys}
                paths['transported_old_metric'] = save(name + '-transported-old-metric', **old_rate.solution, forcing=old_rate.forcing, edges=solver.edges)
                paths['completed_metric_time'] = save(name + '-completed-kinematic-metric-time', **total, edges=solver.edges,
                    position_state=solution['state'], transported_old_state=old_rate.solution['state'], velocity_time_state=velocity_rate['state'],
                    old_acceleration_change=2 * mode_rate, mode_rate=mode_rate)
                base_time = read(flow['paths']['background_response'])['state'] + read(flow['paths']['velocity_response'])['state']
                velocity = read(previous['paths']['live_response'])['state']
                outer = solver.edges[-1] - 2 * action.solution['state'][0, -1, -1]
                boundary = total['state'][1, -1, -1] + total['state'][0, -1, -1] / outer
                boundary += 2 * base_time[0, -1, -1] * velocity[0, -1, -1] / outer**2
                scale = float(np.max(abs(total['state'])))
                position_sensitivity = read(case['paths']['sensitivity'])['delta_state']
                position_sensitivity_max = float(np.max(abs(position_sensitivity)))
                paths['completed_jet_sensitivity'] = save(name + '-position-to-completed-jet-sensitivity', delta_metric_time_state=position_sensitivity)
                boundary_operand_scale = sum(abs(component[1, -1, -1]) + abs(component[0, -1, -1] / outer)
                    for component in [solution['state'], old_rate.solution['state'], velocity_rate['state']])
                boundary_roundoff = 128 * np.finfo(float).eps * boundary_operand_scale
                evidence.check(name + ':completed_metric_time_outer_boundary', abs(boundary) <= 2e-12 * scale + boundary_roundoff + 1e-25,
                    dict(error=float(abs(boundary)), scale=scale, arithmetic_roundoff_allowance=float(boundary_roundoff)))
                evidence.check(name + ':fixed_inner_mass', np.max(abs(total['state'][0, 0, 0])) <= 1e-25)
                summary = dict(branch=branch, level=level, offgrid_points=len(radius), mass_equation_error=strong_errors[0], lapse_equation_error=strong_errors[1],
                    completed_metric_time_max=scale, position_max=float(np.max(abs(solution['state']))),
                    transported_old_metric_max=float(np.max(abs(old_rate.solution['state']))), velocity_time_max=float(np.max(abs(velocity_rate['state']))),
                    omitted_position_and_transport_max=float(np.max(abs(solution['state'] + old_rate.solution['state']))),
                    old_acceleration_change_max=float(np.max(abs(2 * mode_rate))), outer_boundary_error=float(abs(boundary)))
                summary.update(position_oracle_to_completed_time_max=position_sensitivity_max,
                    position_oracle_to_completed_time_relative=position_sensitivity_max / max(scale, 1e-300),
                    sensitivity_is_rigorous_bound=False)
                summaries.append(summary)
                evidence.report['cases'].append(dict(branch=branch, level=level, paths=paths, summary=summary))
                progress(name + ':complete')
                del engine, loads, action, radial
                gc.collect()
        path = evidence.output / 'position-and-completed-metric-jet.csv'
        with path.open('x', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(summaries[0]))
            writer.writeheader()
            writer.writerows(summaries)
        evidence.own(path, 'outputs')
        evidence.report.update(seconds=perf_counter() - started, summaries=summaries)
        evidence.complete()
        print(json.dumps(dict(state='complete', seconds=perf_counter() - started, checks=len(evidence.report['checks']))), flush=True)
    except BaseException as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
