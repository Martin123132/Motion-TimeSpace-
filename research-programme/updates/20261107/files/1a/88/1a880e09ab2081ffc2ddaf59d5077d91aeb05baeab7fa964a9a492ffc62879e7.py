from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case, load_owned
from annular_compensated_position_20260928 import PositionLoads
from annular_background_time_tangent_20260928 import BackgroundLoads, FIELD_NAMES
from annular_position_time_eulerian_v2_20260929 import PositionTimeLoads
from annular_physical_native_kernel_20260928 import NativeKernel
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_joint_first_tangent_20260922 import MetricResponse
from derive_annular_direct_background_coupled_current_20260928 import TotalResponse
from annular_candidate_radial_constraint_20260920 import radial_rhs
from annular_radial_time_forcing_20260928 import explicit_time_forcing
from annular_live_compensation_derivative_20260928 import response_from_rhs
from annular_horizontal_clock_evolution_20260913 import ChebyshevRule
from decimal import localcontext
from time import perf_counter
from copy import copy
import argparse
import csv
import gc
import hashlib
import json
import numpy as np


def solve_jumps(solver, local, forcing, factor, boundary, jumps):
    prefix = np.cumsum(jumps[:, :-1], axis=1)[:, :, None]
    tangent = np.zeros((2, *solver.nodes.shape))
    scale = max(float(np.max(abs(forcing))), float(np.max(abs(prefix))), abs(boundary), 1e-30)
    history = []
    for iteration in range(100):
        rhs = np.einsum('abn,bn->an', local, tangent.reshape(2, -1)) + forcing
        integrated = np.array([solver.integrated(value) for value in rhs]) + prefix
        integrated[1] += boundary - integrated[0, -1, -1] / factor - integrated[1, -1, -1]
        error = float(np.max(abs(integrated - tangent)))
        history.append(error)
        tangent = integrated
        if error <= 2e-14 * scale:
            break
    else:
        raise RuntimeError('Mixed jump inverse did not converge')
    rhs = (np.einsum('abn,bn->an', local, tangent.reshape(2, -1)) + forcing).reshape(tangent.shape)
    integrated = np.array([solver.integrated(value.ravel()) for value in rhs]) + prefix
    integrated[1] += boundary - integrated[0, -1, -1] / factor - integrated[1, -1, -1]
    residual = float(np.max(abs(integrated - tangent)))
    response = response_from_rhs(solver, tangent, rhs, forcing, factor, boundary, residual, history)
    response.solution['left'][0] += prefix[0, :, 0]
    response.solution['left'][1] += prefix[1, :, 0] - prefix[1, -1, 0] - prefix[0, -1, 0] / factor
    return response


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--parent', default='annular-position-time-loads-attempt01')
    parser.add_argument('--label', default='annular-position-time-radial-attempt03')
    parser.add_argument('--max-seconds', type=float, default=10000)
    parser.add_argument('--case-limit', type=int, default=4)
    parser.add_argument('--probe-only', action='store_true')
    args = parser.parse_args()
    evidence = EvidenceRun(args.label, __file__)
    started, deadline = perf_counter(), perf_counter() + args.max_seconds
    try:
        evidence.report.update(scope='Position-time radial inverse with physical moving-interface jumps',
            github_action=False, subagents_used=False, original_workbench_write=False, new_trajectories=0,
            C0_old_reaction_solved=False, C0_current_column_computed=False, probe_only=args.probe_only,
            inherited_position_density_precision_warnings=4, inherited_mixed_time_precision_warnings=4,
            inherited_raw_C2_warnings=2, uncertainty_is_rigorous_bound=False)
        evidence.own(evidence.root / 'DERIVATION-20260929-position-time-radial-response.md')
        parent_path = evidence.output.parent / args.parent / 'status.json'
        parent = json.loads(parent_path.read_text())
        evidence.own(parent_path)
        evidence.check('parent_complete', parent['state'] == 'complete' and len(parent['cases']) == 4)
        digests, bad = {}, []
        for category in ['inputs', 'outputs']:
            for relative, expected in parent[category].items():
                if relative == 'CURRENT_LOCAL_RESUME.md':
                    continue
                path = evidence.root / relative
                if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                    bad.append(relative)
                else:
                    digests[relative] = expected
                    evidence.own(path)
        evidence.check('parent_inputs_unchanged', not bad, bad)
        read = lambda relative: load_owned(evidence, digests, evidence.root / relative)
        status = lambda name: read(str((evidence.output.parent / name / 'status.json').relative_to(evidence.root)))
        live, jets, direct, positions = [status(name) for name in ['annular-live-support-acceleration-attempt01',
            'annular-position-metric-jet-validation-attempt01', 'annular-direct-background-coupled-current-attempt01',
            'annular-compensated-position-attempt04']]
        with (evidence.output.parent / args.parent / 'mixed-endpoint-atoms.csv').open(newline='', encoding='utf-8') as stream:
            endpoints = list(csv.DictReader(stream))
        moment_table = evidence.output.parent / args.parent / 'mixed-weak-moments.csv'
        with moment_table.open(newline='', encoding='utf-8') as stream:
            moments = list(csv.DictReader(stream))

        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter() - started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)
            if perf_counter() > deadline:
                raise RuntimeError('Safe radial position-time boundary')

        def save(name, **arrays):
            path = evidence.output / (name + '.npz')
            np.savez_compressed(path, **arrays)
            evidence.own(path, 'outputs')
            return str(path.relative_to(evidence.root))

        summaries = []
        with localcontext() as context:
            context.prec = 70
            for case in parent['cases'][:args.case_limit]:
                branch, level = case['branch'], case['level']
                name = branch + '-' + level
                progress(name + ':restore')
                loads, action, sources = restore_case(evidence, digests, branch, level, deadline)
                loads.owner.label_order = 28
                match = lambda report: next(row for row in report['cases'] if row['branch'] == branch and row['level'] == level)
                previous, jet, flow, position_case = map(match, [live, jets, direct, positions])
                directions, correction = read(previous['direction_path']), read(previous['paths']['projection'])['correction']
                mode_rate = read(jet['paths']['completed_metric_time'])['mode_rate']
                acceleration = read(flow['paths']['flow'])['acceleration']
                packet = read(sources['packet'])
                native = NativeKernel(action.mesh, packet['gram_support'], branch.startswith('MTS'))
                position_engine = PositionLoads(loads, action, native, directions, correction)
                expansion = read(case['paths']['native']) if native.enabled else None
                if native.enabled:
                    position_engine.image_coefficients = expansion['coefficients'][0]
                    position_engine.image_direction_coefficients = expansion['coefficients'][1]
                engine = PositionTimeLoads(position_engine, mode_rate, acceleration,
                    None if expansion is None else expansion['coefficients'])
                probe = np.linspace(action.solver.edges[0] + .021, action.solver.edges[-1] - .017, 17)
                probe = np.r_[probe, np.mean(position_engine.material.coordinates[:, -1]) + np.array([-.29, .11, .31]) * loads.owner.width]
                values = engine.sample(probe)
                unused, position_fields = position_engine.sample(probe)
                rate_engine = BackgroundLoads(loads, action, coordinate_direction=np.zeros_like(loads.rates), velocity_direction=mode_rate)
                unused, rate_fields = rate_engine.sample(probe)
                time_engine = BackgroundLoads(loads, action, velocity_direction=acceleration)
                unused, time_fields = time_engine.sample(probe)
                errors = {}
                for key in FIELD_NAMES:
                    scale = max(float(np.max(abs(position_fields[key] + rate_fields[key]))), float(np.max(abs(time_fields[key]))))
                    first_error = float(np.max(abs(values[key][1] - position_fields[key] - rate_fields[key])))
                    time_error = float(np.max(abs(values[key][2] - time_fields[key])))
                    tolerance = 2e-7 * scale + (2e-14 if key in ['temporal_square', 'gradient_square'] else 1e-21 if key == 'gram' else 2e-9)
                    evidence.check(name + ':independent_first_derivatives:' + key,
                        max(first_error, time_error) <= tolerance, dict(position_error=first_error, time_error=time_error, tolerance=tolerance))
                    errors[key] = [first_error, time_error, tolerance]
                paths = dict(probes=save(name + '-interior-probes', radius=probe, **values))
                if args.probe_only:
                    evidence.report['cases'].append(dict(branch=branch, level=level, paths=paths, errors=errors))
                    progress(name + ':probe-complete')
                    continue
                restore = lambda archive: MetricResponse(*reconstructed_solver(archive), archive.get('forcing'), 0., [])
                position_response = TotalResponse(restore(read(position_case['paths']['response'])), restore(read(jet['paths']['transported_old_metric'])))
                time_response = TotalResponse(restore(read(flow['paths']['background_response'])), restore(read(flow['paths']['velocity_response'])))
                solver = copy(action.solver)
                solver.nodes = read(position_case['paths']['response'])['nodes']
                solver.rule = ChebyshevRule(solver.nodes.shape[1] - 1)
                degree = solver.nodes.shape[1] - 1
                gauss = -np.cos((np.arange(degree + 1) + .5) * np.pi / (degree + 1))
                radius = (solver.centers[:, None] + solver.lengths[:, None] * gauss / 2).ravel()
                fields = {key: np.zeros((4, len(radius))) for key in FIELD_NAMES}
                for start in range(0, len(radius), 32):
                    if perf_counter() > deadline:
                        raise RuntimeError('Safe mixed Eulerian density boundary')
                    section = slice(start, start + 32)
                    sampled = engine.sample(radius[section])
                    for key in FIELD_NAMES:
                        fields[key][:, section] = sampled[key]
                    if start % 2048 == 0:
                        progress(name + ':mixed-nodes-' + str(start) + '-of-' + str(len(radius)))
                paths['density'] = save(name + '-gauss-mixed-loads', radius=radius, gauss=gauss, **fields)
                inverse = np.linalg.inv(np.polynomial.chebyshev.chebvander(gauss, degree))
                project = lambda array: np.asarray(array).reshape(-1, len(solver.lengths), degree + 1) @ inverse.T
                coefficients = {key: project(value) for key, value in fields.items()}
                integral_weights = np.array([0 if power % 2 else 2 / (1 - power**2) for power in range(degree + 3)])
                weak_checks = []
                for key in ['temporal_square', 'gradient_square', 'gram', 'source_density']:
                    for power in range(3):
                        profile = (radius - 6)**power
                        weighted = project(fields[key][3] * profile)[0]
                        regular = float(np.sum((weighted @ integral_weights[:degree + 1]) * solver.lengths / 2))
                        candidates = [row for row in moments if row['branch'] == branch and row['level'] == level and row['channel'] == key and int(row['power']) == power]
                        target = float(candidates[0]['weak_mixed']) if candidates else 0.
                        atoms = sum(float(row['atom']) * (float(row['radius']) - 6)**power for row in endpoints
                            if row['branch'] == branch and row['level'] == level and row['channel'] == key)
                        error = abs(regular + atoms - target)
                        tolerance = 2e-7 * abs(target) + (2e-13 if key in ['temporal_square', 'gradient_square'] else 2e-20)
                        evidence.check(name + ':mixed_weak:' + key + ':' + str(power), error <= tolerance,
                            dict(regular=regular, atoms=atoms, material=target, error=error, tolerance=tolerance))
                        weak_checks.append([regular, atoms, target, error, tolerance])
                values = action.solver.values(action.solution, radius)[0]
                position_values, time_values = position_response.values(radius), time_response.values(radius)
                amount = 1e-25j
                unused, local = radial_rhs(radius, *values, *[fields[key][0] for key in FIELD_NAMES],
                    action.owner.coupling, action.owner.source_mass, True)
                changed = {key: fields[key][0] + amount * fields[key][1] for key in FIELD_NAMES}
                unused, changed_local = radial_rhs(radius, *(values + amount * position_values), *[changed[key] for key in FIELD_NAMES],
                    action.owner.coupling, action.owner.source_mass, True)
                forcing_change = explicit_time_forcing(radius, *(values + amount * position_values),
                    changed['source_density'], changed['velocity'],
                    *[fields[key][2] + amount * fields[key][3] for key in FIELD_NAMES],
                    action.owner.coupling, action.owner.source_mass).imag / 1e-25
                forcing = np.einsum('abn,bn->an', changed_local.imag / 1e-25, time_values) + forcing_change
                vandermonde = np.polynomial.chebyshev.chebvander(solver.rule.points, degree)
                projected_local = (project(local) @ vandermonde.T).reshape(2, 2, -1)
                projected_forcing = (project(forcing) @ vandermonde.T).reshape(2, -1)
                jumps = np.zeros((2, len(solver.edges)))
                for endpoint in endpoints:
                    if endpoint['branch'] != branch or endpoint['level'] != level:
                        continue
                    index = int(np.argmin(abs(solver.edges - float(endpoint['radius']))))
                    if abs(solver.edges[index] - float(endpoint['radius'])) > 64 * np.finfo(float).eps * max(abs(solver.edges)):
                        raise RuntimeError('Unmatched mixed endpoint owner')
                    jumps[:, index] += [float(endpoint['metric_mass_jump']), float(endpoint['metric_lapse_jump'])]
                evidence.check(name + ':fixed_exterior_jumps_zero', np.max(abs(jumps[:, [0, -1]])) == 0)
                factor = solver.edges[-1] - 2 * action.solution['state'][0, -1, -1]
                outer = np.array([solver.edges[-1]])
                boundary = -2 * position_response.values(outer)[0, 0] * time_response.values(outer)[0, 0] / factor**2
                response = solve_jumps(solver, projected_local, projected_forcing, factor, boundary, jumps)
                scale = float(np.max(abs(response.solution['state'])))
                lower_local, lower_forcing = project(local), project(forcing)
                lower_local[:, :, -2:], lower_forcing[:, :, -2:] = 0., 0.
                lower_response = solve_jumps(solver, (lower_local @ vandermonde.T).reshape(2, 2, -1),
                    (lower_forcing @ vandermonde.T).reshape(2, -1), factor, boundary, jumps)
                polynomial_error = float(np.max(abs(lower_response.solution['state'] - response.solution['state'])))
                evidence.check(name + ':regular_polynomial_resolution', polynomial_error <= 2e-6 * scale + 1e-18,
                    dict(error=polynomial_error, scale=scale, lower_degree=degree - 2, degree=degree))
                no_jumps = solve_jumps(solver, projected_local, projected_forcing, factor, boundary, np.zeros_like(jumps))
                omitted_jump_effect = float(np.max(abs(no_jumps.solution['state'] - response.solution['state'])))
                evidence.check(name + ':integrated_mixed_inverse', response.residual <= 2e-11 * scale + 1e-24,
                    dict(error=response.residual, scale=scale))
                boundary_error = abs(response.solution['state'][1, -1, -1] + response.solution['state'][0, -1, -1] / factor - boundary)
                evidence.check(name + ':outer_normalization', boundary_error <= 2e-11 * scale + 1e-24, float(boundary_error))
                increments = np.array([np.polynomial.chebyshev.chebval(1., value.T) for value in response.solution['primitives']])
                jump_error = float(np.max(abs(response.solution['left'][:, 1:] - response.solution['left'][:, :-1] - increments[:, :-1] - jumps[:, 1:-1])))
                evidence.check(name + ':interface_jump_replay', jump_error <= 2e-11 * scale + 1e-24, jump_error)
                paths['response'] = save(name + '-B0-response', **response.solution, forcing=projected_forcing, jumps=jumps,
                    edges=solver.edges, nodes=solver.nodes, weak_checks=np.array(weak_checks),
                    lower_polynomial_state=lower_response.solution['state'], no_jump_state=no_jumps.solution['state'])
                summary = dict(branch=branch, level=level, B0_mass_max=float(np.max(abs(response.solution['state'][0]))),
                    B0_lapse_max=float(np.max(abs(response.solution['state'][1]))), jump_max=float(np.max(abs(jumps))),
                    radial_residual=response.residual, boundary_error=float(boundary_error), jump_error=jump_error,
                    polynomial_resolution_error=polynomial_error, omitted_jump_effect=omitted_jump_effect,
                    valid_for_claim=False)
                summaries.append(summary)
                evidence.report['cases'].append(dict(branch=branch, level=level, paths=paths, summary=summary, first_derivative_errors=errors))
                progress(name + ':complete')
                del engine, position_engine, loads, action, fields, coefficients
                gc.collect()
        if summaries:
            table = evidence.output / 'position-time-radial-summary.csv'
            with table.open('x', encoding='utf-8', newline='') as stream:
                writer = csv.DictWriter(stream, fieldnames=list(summaries[0]))
                writer.writeheader()
                writer.writerows(summaries)
            evidence.own(table, 'outputs')
        evidence.report['seconds'] = perf_counter() - started
        evidence.complete()
    except BaseException as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
