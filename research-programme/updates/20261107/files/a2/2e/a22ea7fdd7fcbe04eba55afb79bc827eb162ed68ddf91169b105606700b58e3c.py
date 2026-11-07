from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case, load_owned
from annular_background_eulerian_20260928 import BackgroundLoads, assemble_background, FIELD_NAMES, complex_radial_response
from annular_background_complex_oracle_20260928 import complex_loads
from time import perf_counter
import argparse
import csv
import gc
import hashlib
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', default='annular-background-time-tangent-attempt02')
    parser.add_argument('--cases', nargs='+', default=['reference-reference:fine', 'reference-reference:third', 'MTS-primary:fine', 'MTS-primary:third'])
    parser.add_argument('--max-seconds', type=float, default=6000)
    args = parser.parse_args()
    evidence = EvidenceRun(args.label, __file__)
    started, deadline = perf_counter(), perf_counter() + args.max_seconds
    try:
        evidence.report.update(scope='Analytic Eulerian background derivative including moving label cuts, discretized on the owned central partition',
            new_trajectories=0, subagents_used=False, github_action=False, analytic_old_convection_computed=False,
            protected_since='2026-09-28T15:08:14+00:00')
        evidence.own(evidence.root / 'DERIVATION-20260928-direct-background-time-tangent.md')
        evidence.own(evidence.root / 'DERIVATION-20260928-coincident-grid-correction.md')
        seal_path = evidence.output.parent / 'annular-live-support-acceleration-final-integrity-20260928.json'
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
        evidence.check('previous_scientific_evidence_unchanged', seal['state'] == 'complete' and not bad, bad)

        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter() - started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)

        def save(name, **arrays):
            path = evidence.output / (name + '.npz')
            np.savez_compressed(path, **arrays)
            evidence.own(path, 'outputs')
            return str(path.relative_to(evidence.root))

        summaries, validations = [], []
        for specification in args.cases:
            branch, level = specification.split(':')
            name = branch + '-' + level
            progress(name + ':restore')
            loads, action, sources = restore_case(evidence, digests, branch, level, deadline)
            loads.owner.label_order = 28
            engine = BackgroundLoads(loads, action)
            selected = np.linspace(0, len(action.solver.lengths) - 1, 79, dtype=int)
            labels = np.linspace(-.473, .471, 47)
            source_samples = loads.material.node_geometry(loads.owner.model.anchor, labels)[0]
            radius = np.unique(np.r_[action.solver.centers[selected], source_samples])
            radial_rate = .013 * np.sin(radius)
            fields, rates = engine.sample(radius, radial_rate)
            original = loads.sample(radius, 28, [engine.extension])
            original['gram'] = original['gram'][engine.extension]
            oracle = complex_loads(engine, radius, radial_rate, 1j * 1e-25)
            oracle2 = complex_loads(engine, radius, radial_rate, 1j * 1e-30)
            paths = {}
            paths['sample_validation'] = save(name + '-sample-validation', radius=radius, radius_rate=radial_rate,
                **{prefix + key: value for prefix, collection in [('base_', fields), ('tangent_', rates),
                    ('original_', original), ('complex_', oracle), ('complex2_', oracle2)] for key, value in collection.items()})
            for key in FIELD_NAMES:
                base_error = float(np.max(abs(fields[key] - original[key])))
                scale = max(float(np.max(abs(fields[key]))), 1e-30)
                evidence.check(name + ':original_density:' + key, base_error <= 2e-12 * scale + 1e-28, dict(error=base_error, scale=scale))
                derivative_error = float(np.max(abs(rates[key] - oracle[key].imag / 1e-25)))
                derivative_scale = max(float(np.max(abs(rates[key]))), 1e-30)
                evidence.check(name + ':independent_complex_density:' + key, derivative_error <= 2e-8 * derivative_scale + 1e-26,
                    dict(error=derivative_error, scale=derivative_scale))
                precision_error = float(np.max(abs(oracle[key].imag / 1e-25 - oracle2[key].imag / 1e-30)))
                evidence.check(name + ':complex_step_stability:' + key, precision_error <= 2e-8 * derivative_scale + 1e-26, precision_error)
                validations.append(dict(branch=branch, level=level, field=key, base_error=base_error,
                    derivative_error=derivative_error, derivative_scale=derivative_scale, complex_step_difference=precision_error))
            unfrozen = engine.wave(radius, radial_rate)
            frozen = engine.wave(radius, radial_rate, True)
            transport = [float(np.max(abs(unfrozen[index] - frozen[index]))) for index in [2, 3]]
            progress(name + ':sample-checks-passed')
            response = assemble_background(engine, action, lambda stage: progress(name + ':' + stage))
            scale = max(float(np.max(abs(response.solution['state']))), 1e-30)
            checked = complex_radial_response(response, action, engine.extension)
            error = float(np.max(abs(checked - response.solution['state'])))
            evidence.check(name + ':complex_radial_response', error <= 2e-8 * scale + 1e-25, dict(error=error, scale=scale))
            paths['complex_radial'] = save(name + '-complex-radial', checked=checked, difference=checked - response.solution['state'])
            evidence.check(name + ':background_replay', response.background_residual <= 2e-12, response.background_residual)
            evidence.check(name + ':linear_equation', response.residual <= 1e-12 * scale + 1e-25, dict(residual=response.residual, scale=scale))
            boundary = response.values(action.solver.edges[[0, -1]])
            boundary_error = max(abs(boundary[0, 0]), abs(boundary[1, -1] + boundary[0, -1] / (action.solver.edges[-1] - 2 * action.solution['state'][0, -1, -1])))
            evidence.check(name + ':boundary_conditions', boundary_error <= 2e-13 * scale + 1e-25, float(boundary_error))
            primitive = response.solution['primitives']
            right = response.solution['left'][:, :-1] + np.array([np.polynomial.chebyshev.chebval(1., values[:-1].T) for values in primitive])
            left = response.solution['left'][:, 1:] + np.array([np.polynomial.chebyshev.chebval(-1., values[1:].T) for values in primitive])
            continuity_error = float(np.max(abs(right - left)))
            evidence.check(name + ':moving_primitive_continuity', continuity_error <= 2e-12 * scale + 1e-25, continuity_error)
            base_coefficients = action.solution['rhs_coefficients']
            base_right = np.array([np.polynomial.chebyshev.chebval(1., values[:-1].T) for values in base_coefficients])
            base_left = np.array([np.polynomial.chebyshev.chebval(-1., values[1:].T) for values in base_coefficients])
            jump = (left - base_left * response.edge_rates[1:-1]) - (right - base_right * response.edge_rates[1:-1])
            expected_jump = -response.edge_rates[1:-1] * (base_left - base_right)
            jump_error = float(np.max(abs(jump - expected_jump)))
            evidence.check(name + ':Eulerian_interface_jump', jump_error <= 2e-12 * scale + 1e-25, jump_error)
            paths['response'] = save(name + '-background-response', **response.solution, forcing=response.forcing,
                edges=response.solver.edges, nodes=response.solver.nodes, edge_rates=response.edge_rates, grid_rate=response.grid_rate,
                **{prefix + key: value for prefix, collection in [('base_', response.fields), ('tangent_', response.field_rates)] for key, value in collection.items()})
            summary = dict(branch=branch, level=level, radial_points=response.solver.nodes.size,
                background_residual=response.background_residual, linear_residual=response.residual,
                max_mass_rate=float(np.max(abs(response.values(radius)[0]))), max_lapse_rate=float(np.max(abs(response.values(radius)[1]))),
                boundary_error=float(boundary_error), interface_jump_error=jump_error,
                clustered_edge_velocity_spread=response.edge_velocity_spread,
                omitted_cut_temporal_error=transport[0], omitted_cut_gradient_error=transport[1],
                iterations=len(response.history))
            summaries.append(summary)
            evidence.report['cases'].append(dict(branch=branch, level=level, sources=sources, paths=paths, summary=summary))
            evidence.save()
            progress(name + ':saved')
            del response, engine, loads, action
            gc.collect()
        for filename, rows in [('direct-background-summary.csv', summaries), ('density-tangent-validation.csv', validations)]:
            path = evidence.output / filename
            with path.open('w', encoding='utf-8', newline='') as stream:
                writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            evidence.own(path, 'outputs')
        evidence.report.update(seconds=perf_counter() - started, summaries=summaries, full_background_derivative_assembled=True, moving_grid_algorithm_differentiated=False,
            coupled_acceleration_recomputed=False, continuum_error_enclosed=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()


