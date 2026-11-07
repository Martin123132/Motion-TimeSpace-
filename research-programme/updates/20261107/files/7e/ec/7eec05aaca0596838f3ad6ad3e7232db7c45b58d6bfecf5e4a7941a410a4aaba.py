from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case, load_owned
from annular_compensated_position_20260928 import PositionLoads
from annular_position_oracle_20260928 import complex_position
from annular_background_eulerian_20260928 import assemble_background, complex_radial_response
from annular_background_weak_checks_20260928 import radial_weak_derivative
from annular_background_time_tangent_20260928 import FIELD_NAMES
from annular_candidate_canonical_response_20260920 import solve_tangent
from annular_radial_time_forcing_20260928 import explicit_time_forcing
from annular_live_compensation_derivative_20260928 import response_from_rhs
from annular_physical_native_kernel_20260928 import NativeKernel, maximum
from decimal import Decimal, localcontext
from time import perf_counter
import argparse
import csv
import gc
import hashlib
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', default='annular-compensated-position-attempt03')
    parser.add_argument('--max-seconds', type=float, default=8400)
    parser.add_argument('--case-limit', type=int, default=4)
    args = parser.parse_args()
    evidence = EvidenceRun(args.label, __file__)
    started, deadline = perf_counter(), perf_counter() + args.max_seconds
    try:
        evidence.report.update(scope='Compensated position metric response with physical native shape derivative',
            github_action=False, subagents_used=False, new_trajectories=0, original_workbench_write=False,
            inherited_mixed_time_precision_warning_count=4, inherited_pointwise_mixed_time_accuracy_pass=False,
            full_velocity_current_column_computed=False, position_density_precision_diagnostics=[])
        evidence.own(evidence.root / 'DERIVATION-20260928-compensated-position-response.md')
        evidence.own(evidence.root / 'DERIVATION-20260928-position-precision-protocol.md')
        seal_path = evidence.output.parent / 'annular-compensation-time-final-integrity-20260928.json'
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
        evidence.check('prior_scientific_evidence_unchanged', seal['state'] == 'complete' and not bad, bad)
        evidence.check('prior_precision_warnings_retained', seal['precision_warning_count'] == 4 and not seal['pointwise_mixed_radial_accuracy_pass'])
        read = lambda relative: load_owned(evidence, digests, evidence.root / relative)
        status = lambda name: read(str((evidence.output.parent / name / 'status.json').relative_to(evidence.root)))
        live = status('annular-live-support-acceleration-attempt01')

        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter() - started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)
            if perf_counter() > deadline:
                raise RuntimeError('Safe position-response boundary; completed case arrays preserved')

        def save(name, **arrays):
            path = evidence.output / (name + '.npz')
            np.savez_compressed(path, **arrays)
            evidence.own(path, 'outputs')
            return str(path.relative_to(evidence.root))

        summaries, weak_rows = [], []
        with localcontext() as context:
            context.prec = 70
            for case in live['cases'][:args.case_limit]:
                branch, level = case['branch'], case['level']
                name = branch + '-' + level
                progress(name + ':restore')
                loads, action, sources = restore_case(evidence, digests, branch, level, deadline)
                loads.owner.label_order = 28
                packet = read(sources['packet'])
                native = NativeKernel(packet['mesh'], packet['gram_support'], branch == 'MTS-primary')
                directions = read(case['direction_path'])
                correction = read(case['paths']['projection'])['correction']
                engine = PositionLoads(loads, action, native, directions, correction)
                evidence.check(name + ':support_pinned', np.max(abs(directions['edge_vertices'][:, [0, native.anchor, -1]])) <= 1e-25)
                evidence.check(name + ':native_sampling_compatible', (not native.enabled and loads.factor.shape[0] == 0) or (native.sampling.shape == loads.sampling.shape and np.max(abs((native.sampling - loads.sampling).data), initial=0.) <= 1e-15))
                paths = {}
                if native.enabled:
                    paths['native'] = save(name + '-native-label-expansion', **engine.prepare_native(24, lambda stage: progress(name + ':' + stage)))
                    native_errors = []
                    for label in [-.413, -.217, .071, .289, .447]:
                        image, derivative, data, edges, fields = engine.native_direct(label)
                        image_fit = np.polynomial.chebyshev.chebval(2 * label, engine.image_coefficients)
                        derivative_fit = np.polynomial.chebyshev.chebval(2 * label, engine.image_direction_coefficients)
                        error = float(np.max(abs(derivative_fit - np.asarray(derivative, float))))
                        scale = float(maximum(derivative))
                        evidence.check(name + ':native_offgrid:' + str(label), error <= 2e-9 * scale + 1e-23, dict(error=error, scale=scale))
                        evidence.check(name + ':native_base_offgrid:' + str(label), np.max(abs(image_fit - np.asarray(image, float))) <= 2e-10 * float(maximum(image)) + 1e-23)
                        step = Decimal('1e-16')
                        moved = []
                        for sign in [-1, 1]:
                            positions = data['edges'] + sign * step * edges
                            values = data['field'] + sign * step * fields
                            moved.append(native.apply('template', native.kernel_values(positions, native.atoms(positions, values))))
                        direct = (moved[1] - moved[0]) / (2 * step)
                        difference = float(maximum(direct - derivative))
                        evidence.check(name + ':native_real_direction:' + str(label), difference <= 2e-10 * scale + 1e-25, dict(error=difference, scale=scale))
                        native_errors.append([label, error, difference, scale])
                    paths['native_validation'] = save(name + '-native-validation', errors=np.array(native_errors))
                probe = np.linspace(action.solver.edges[0] + .017, action.solver.edges[-1] - .013, 41)
                source_center = float(np.mean(engine.material.coordinates[:, -1]))
                probe = np.sort(np.r_[probe, source_center + np.array([-.31, .07, .29]) * engine.owner.width])
                fields, rates = engine.sample(probe)
                oracle = complex_position(engine, probe, 1j * 1e-24)
                paths['density_check'] = save(name + '-density-check', radius=probe,
                    **{'analytic_' + key: rates[key] for key in oracle}, **{'oracle_' + key: value.imag / 1e-24 for key, value in oracle.items()})
                for key in oracle:
                    difference = float(np.max(abs(rates[key] - oracle[key].imag / 1e-24)))
                    scale = float(np.max(abs(rates[key])))
                    tolerance = 2e-8 * scale + (1e-23 if key not in ['source_density', 'velocity'] else 1e-24)
                    diagnostic = dict(case=name, field=key, error=difference, scale=scale, tolerance=tolerance, passed=bool(difference <= tolerance))
                    evidence.report['position_density_precision_diagnostics'].append(diagnostic)
                    if key != 'gradient_square':
                        evidence.check(name + ':moving_map_oracle:' + key, difference <= tolerance, diagnostic)
                resolved_directions = dict(directions, field_vertices=directions['field_vertices'] + .1 * np.asarray(loads.coordinates[:, :-1], float))
                resolved = PositionLoads(loads, action, native, resolved_directions, correction)
                resolved_gradient = resolved.wave(probe, np.zeros_like(probe))[3]
                resolved_oracle = complex_position(resolved, probe, 1j * 1e-24)['gradient_square'].imag / 1e-24
                resolved_error = float(np.max(abs(resolved_gradient - resolved_oracle)))
                evidence.check(name + ':resolved_gradient_direction', resolved_error <= 2e-8 * np.max(abs(resolved_gradient)) + 1e-23,
                    dict(error=resolved_error, scale=float(np.max(abs(resolved_gradient)))))
                paths['resolved'] = save(name + '-resolved-control', radius=probe, analytic=resolved_gradient, oracle=resolved_oracle)
                progress(name + ':full-radial-position')
                response = assemble_background(engine, action, lambda stage: progress(name + ':' + stage))
                solver = response.solver
                indices = np.arange(solver.nodes.size).reshape(solver.nodes.shape)[:, [0, -1]].ravel()
                side = np.tile([1., -1.], len(solver.lengths))
                gram, gram_rate, source_rate, source_velocity, velocity_rate = engine.trace(solver.nodes.ravel()[indices], side)
                response.fields['gram'][indices], response.field_rates['gram'][indices] = gram, gram_rate
                response.fields['velocity'][indices] = source_velocity
                response.field_rates['source_density'][indices], response.field_rates['velocity'][indices] = source_rate, velocity_rate
                solver.fields = dict(response.fields, gram={engine.extension: response.fields['gram']})
                forcing = explicit_time_forcing(solver.nodes.ravel(), *action.solution['state'].reshape(2, -1), response.fields['source_density'], response.fields['velocity'],
                    *[response.field_rates[key] for key in FIELD_NAMES], engine.owner.coupling, engine.owner.source_mass)
                state, residual, history = solve_tangent(solver, action.solution['state'], engine.extension, forcing)
                unused, local = solver.rhs(action.solution['state'], engine.extension, True)
                rhs = (np.einsum('abn,bn->an', local, state.reshape(2, -1)) + forcing).reshape(2, *solver.nodes.shape)
                outer_factor = solver.edges[-1] - 2 * action.solution['state'][0, -1, -1]
                repaired = response_from_rhs(solver, state, rhs, forcing, outer_factor, 0., residual, history)
                repaired.fields, repaired.field_rates = response.fields, response.field_rates
                response = repaired
                scale = float(np.max(abs(response.solution['state'])))
                evidence.check(name + ':linear_residual', residual <= 1e-12 * scale + 1e-25, dict(error=residual, scale=scale))
                replay = float(np.max(abs(solver.residual(action.solution['state'], engine.extension))))
                evidence.check(name + ':near_translated_seed_replay', replay <= 2e-12, replay)
                complex_state = complex_radial_response(response, action, engine.extension)
                complex_error = float(np.max(abs(complex_state - state)))
                evidence.check(name + ':nonlinear_radial_oracle', complex_error <= 2e-8 * scale + 1e-25, dict(error=complex_error, scale=scale))
                boundary = abs(float(state[1, -1, -1] + state[0, -1, -1] / (solver.edges[-1] - 2 * action.solution['state'][0, -1, -1])))
                evidence.check(name + ':outer_boundary', boundary <= 1e-12 * scale + 1e-25, boundary)
                paths['response'] = save(name + '-position-response', **response.solution, forcing=forcing, edges=solver.edges, nodes=solver.nodes,
                    **{prefix + key: value for prefix, collection in [('base_', response.fields), ('tangent_', response.field_rates)] for key, value in collection.items()})
                alternate_rates = {key: value.copy() for key, value in response.field_rates.items()}
                radius = solver.nodes.ravel()
                for start in range(0, len(radius), 32):
                    section = slice(start, start + 32)
                    alternate = complex_position(engine, radius[section], 1j * 1e-24)
                    for key in ['temporal_square', 'gradient_square']:
                        alternate_rates[key][section] = alternate[key].imag / 1e-24
                    if start % 4096 == 0:
                        progress(name + ':full-map-oracle-' + str(start) + '-of-' + str(len(radius)))
                difference_rates = [alternate_rates[key] - response.field_rates[key] for key in FIELD_NAMES]
                delta_forcing = explicit_time_forcing(radius, *action.solution['state'].reshape(2, -1),
                    response.fields['source_density'], response.fields['velocity'], *difference_rates,
                    engine.owner.coupling, engine.owner.source_mass)
                delta_state, delta_residual, delta_history = solve_tangent(solver, action.solution['state'], engine.extension, delta_forcing)
                position_error = float(np.max(abs(delta_state)))
                evidence.check(name + ':full_grid_position_sensitivity', position_error <= 2e-6 * scale + 1e-25,
                    dict(error=position_error, scale=scale, interpretation='Measured two-algorithm sensitivity, not rigorous enclosure'))
                paths['sensitivity'] = save(name + '-full-grid-position-sensitivity', delta_state=delta_state,
                    delta_forcing=delta_forcing, oracle_temporal=alternate_rates['temporal_square'],
                    oracle_gradient=alternate_rates['gradient_square'])
                direct48, direct64, radial = engine.weak(48), engine.weak(64), radial_weak_derivative(response)
                paths['weak'] = save(name + '-weak-density', material48=direct48, material64=direct64, radial=radial)
                for index, key in enumerate(['temporal_square', 'gradient_square', 'gram', 'source_density']):
                    for power in range(3):
                        error = abs(float(radial[index, power] - direct64[index, power]))
                        quad = abs(float(direct48[index, power] - direct64[index, power]))
                        tolerance = 2e-7 * abs(float(direct64[index, power])) + (1e-21 if key == 'gram' else 2e-11 if key == 'source_density' else 2e-14)
                        evidence.check(name + ':weak:' + key + ':' + str(power), error <= tolerance, dict(error=error, tolerance=tolerance))
                        evidence.check(name + ':material48_64:' + key + ':' + str(power), quad <= tolerance, quad)
                        weak_rows.append(dict(branch=branch, level=level, field=key, power=power, radial=float(radial[index, power]), material=float(direct64[index, power]), error=error, quadrature=quad))
                summary = dict(branch=branch, level=level, position_mass_max=float(np.max(abs(state[0]))), position_lapse_max=float(np.max(abs(state[1]))),
                    linear_residual=residual, nonlinear_radial_error=complex_error, seed_replay_residual=replay,
                    weak_max_error=float(np.max(abs(radial - direct64))), density_oracle_points=len(probe),
                    full_grid_position_sensitivity=position_error, full_grid_oracle_entries=len(radius))
                summaries.append(summary)
                evidence.report.setdefault('cases', []).append(dict(branch=branch, level=level, paths=paths, summary=summary))
                progress(name + ':complete')
                del engine, loads, action, response
                gc.collect()
        for name, rows in [('position-summary', summaries), ('position-weak-checks', weak_rows)]:
            path = evidence.output / (name + '.csv')
            with path.open('x', newline='', encoding='utf-8') as stream:
                writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            evidence.own(path, 'outputs')
        evidence.report['summaries'] = summaries
        evidence.report['new_position_density_precision_warning_count'] = sum(not row['passed'] for row in evidence.report['position_density_precision_diagnostics'])
        evidence.report['seconds'] = perf_counter() - started
        evidence.complete()
        print(json.dumps(dict(state='complete', seconds=perf_counter() - started, checks=len(evidence.report['checks']))), flush=True)
    except BaseException as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
