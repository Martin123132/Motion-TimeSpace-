from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case, load_owned
from annular_compensated_position_20260928 import PositionLoads
from annular_position_two_newton_oracle_20260928 import complex_position
from annular_position_oracle_20260928 import complex_position as six_newton
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_horizontal_clock_evolution_20260913 import ChebyshevRule
from annular_candidate_canonical_response_20260920 import solve_tangent
from annular_background_weak_checks_20260928 import radial_weak_derivative
from annular_background_time_tangent_20260928 import FIELD_NAMES
from annular_radial_time_forcing_20260928 import explicit_time_forcing
from annular_joint_first_tangent_20260922 import MetricResponse
from annular_physical_native_kernel_20260928 import NativeKernel
from decimal import localcontext
from time import perf_counter
import argparse
import csv
import hashlib
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-seconds', type=float, default=3000)
    args = parser.parse_args()
    evidence = EvidenceRun('annular-compensated-position-attempt04', __file__)
    started, deadline = perf_counter(), perf_counter() + args.max_seconds
    try:
        parent_path = evidence.output.parent / 'annular-compensated-position-attempt03/status.json'
        parent = json.loads(parent_path.read_text())
        evidence.own(parent_path)
        evidence.own(evidence.root / 'DERIVATION-20260928-position-safe-resume.md')
        evidence.check('only_resume_saved_safe_boundary', parent['state'] == 'failed' and len(parent['cases']) == 3
            and 'Safe position-response boundary' in parent.get('error', ''), parent.get('error'))
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
        evidence.check('all_parent_artifacts_rehashed', not bad, bad)
        read = lambda relative: load_owned(evidence, digests, evidence.root / relative)
        live = read(str((evidence.output.parent / 'annular-live-support-acceleration-attempt01/status.json').relative_to(evidence.root)))
        evidence.report.update(scope='Resume saved final-case position oracle; do not repeat completed cases',
            reused_cases=[row['branch'] + '-' + row['level'] for row in parent['cases']],
            cases=parent['cases'].copy(), position_density_precision_diagnostics=parent['position_density_precision_diagnostics'],
            inherited_mixed_time_precision_warning_count=4, inherited_pointwise_mixed_time_accuracy_pass=False,
            full_velocity_current_column_computed=False, github_action=False, subagents_used=False, new_trajectories=0,
            original_workbench_write=False, resumed_oracle_newton_iterations=2)
        for case in parent['cases']:
            prefix = case['branch'] + '-' + case['level'] + ':'
            inherited_checks = [row for row in parent['checks'] if row['name'].startswith(prefix)]
            evidence.check(prefix + 'reuse_complete_case_checks', bool(inherited_checks) and all(row['passed'] for row in inherited_checks), len(inherited_checks))

        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter() - started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)
            if perf_counter() > deadline:
                raise RuntimeError('Safe resumed position boundary')

        def save(name, **arrays):
            path = evidence.output / (name + '.npz')
            np.savez_compressed(path, **arrays)
            evidence.own(path, 'outputs')
            return str(path.relative_to(evidence.root))

        done = {(row['branch'], row['level']) for row in parent['cases']}
        remaining = [row for row in live['cases'] if (row['branch'], row['level']) not in done]
        evidence.check('exactly_one_pending_case', len(remaining) == 1)
        case = remaining[0]
        branch, level = case['branch'], case['level']
        name = branch + '-' + level
        with localcontext() as context:
            context.prec = 70
            progress(name + ':restore_saved_phase')
            loads, action, sources = restore_case(evidence, digests, branch, level, deadline)
            loads.owner.label_order = 28
            packet = read(sources['packet'])
            native = NativeKernel(packet['mesh'], packet['gram_support'], branch == 'MTS-primary')
            directions = read(case['direction_path'])
            correction = read(case['paths']['projection'])['correction']
            engine = PositionLoads(loads, action, native, directions, correction)
            paths = {}
            for key, suffix in [('native', '-native-label-expansion.npz'), ('native_validation', '-native-validation.npz'),
                ('density_check', '-density-check.npz'), ('resolved', '-resolved-control.npz'), ('response', '-position-response.npz')]:
                paths[key] = next(relative for relative in parent['outputs'] if relative.endswith(name + suffix))
            expansion = read(paths['native'])
            engine.image_coefficients, engine.image_direction_coefficients = expansion['image_coefficients'], expansion['image_direction_coefficients']
            archive = read(paths['response'])
            solver, solution = reconstructed_solver(archive)
            solver.owner, solver.loads, solver.rule, solver.nodes = loads.owner, loads, ChebyshevRule(22), archive['nodes']
            fields = {key: archive['base_' + key] for key in FIELD_NAMES}
            rates = {key: archive['tangent_' + key] for key in FIELD_NAMES}
            solver.fields = dict(fields, gram={engine.extension: fields['gram']})
            response = MetricResponse(solver, solution, archive['forcing'], 0., [])
            response.fields, response.field_rates = fields, rates
            passed = {row['name']: row for row in parent['checks'] if row['passed']}
            required = ['linear_residual', 'near_translated_seed_replay', 'nonlinear_radial_oracle', 'outer_boundary', 'resolved_gradient_direction']
            evidence.check('saved_final_radial_phase_passed', all(name + ':' + key in passed for key in required))
            probe = read(paths['density_check'])['radius']
            fast, slow = complex_position(engine, probe, 1j * 1e-24), six_newton(engine, probe, 1j * 1e-24)
            differences = {key: float(np.max(abs(fast[key].imag / 1e-24 - slow[key].imag / 1e-24))) for key in fast}
            paths['iteration_comparison'] = save(name + '-two-six-Newton-comparison', radius=probe,
                **{'two_' + key: value.imag / 1e-24 for key, value in fast.items()}, **{'six_' + key: value.imag / 1e-24 for key, value in slow.items()})
            resolved = PositionLoads(loads, action, native, dict(directions, field_vertices=directions['field_vertices'] + .1 * np.asarray(loads.coordinates[:, :-1], float)), correction)
            resolved_analytic = read(paths['resolved'])['analytic']
            resolved_oracle = complex_position(resolved, probe, 1j * 1e-24)['gradient_square'].imag / 1e-24
            resolved_error = float(np.max(abs(resolved_analytic - resolved_oracle)))
            evidence.check('two_Newton_resolved_direction', resolved_error <= 2e-8 * np.max(abs(resolved_analytic)) + 1e-23, resolved_error)
            radius = solver.nodes.ravel()
            alternate_rates = {key: value.copy() for key, value in rates.items()}
            for start in range(0, len(radius), 32):
                section = slice(start, start + 32)
                alternate = complex_position(engine, radius[section], 1j * 1e-24)
                for key in ['temporal_square', 'gradient_square']:
                    alternate_rates[key][section] = alternate[key].imag / 1e-24
                if start % 8192 == 0:
                    progress(name + ':resumed-full-map-oracle-' + str(start) + '-of-' + str(len(radius)))
            delta_forcing = explicit_time_forcing(radius, *action.solution['state'].reshape(2, -1), fields['source_density'], fields['velocity'],
                *[alternate_rates[key] - rates[key] for key in FIELD_NAMES], engine.owner.coupling, engine.owner.source_mass)
            delta_state, unused, unused2 = solve_tangent(solver, action.solution['state'], engine.extension, delta_forcing)
            position_error, scale = float(np.max(abs(delta_state))), float(np.max(abs(solution['state'])))
            evidence.check('full_grid_position_sensitivity', position_error <= 2e-6 * scale + 1e-25, dict(error=position_error, scale=scale))
            paths['sensitivity'] = save(name + '-full-grid-position-sensitivity', delta_state=delta_state, delta_forcing=delta_forcing,
                oracle_temporal=alternate_rates['temporal_square'], oracle_gradient=alternate_rates['gradient_square'])
            material48, material64, radial = engine.weak(48), engine.weak(64), radial_weak_derivative(response)
            paths['weak'] = save(name + '-weak-density', material48=material48, material64=material64, radial=radial)
            for index, key in enumerate(['temporal_square', 'gradient_square', 'gram', 'source_density']):
                for power in range(3):
                    tolerance = 2e-7 * abs(float(material64[index, power])) + (1e-21 if key == 'gram' else 2e-11 if key == 'source_density' else 2e-14)
                    error = abs(float(radial[index, power] - material64[index, power]))
                    quad = abs(float(material48[index, power] - material64[index, power]))
                    evidence.check(name + ':weak:' + key + ':' + str(power), error <= tolerance, dict(error=error, tolerance=tolerance))
                    evidence.check(name + ':material48_64:' + key + ':' + str(power), quad <= tolerance, quad)
            summary = dict(branch=branch, level=level, position_mass_max=float(np.max(abs(solution['state'][0]))), position_lapse_max=float(np.max(abs(solution['state'][1]))),
                linear_residual=passed[name + ':linear_residual']['detail']['error'], nonlinear_radial_error=passed[name + ':nonlinear_radial_oracle']['detail']['error'],
                seed_replay_residual=passed[name + ':near_translated_seed_replay']['detail'], weak_max_error=float(np.max(abs(radial - material64))),
                density_oracle_points=len(probe), full_grid_position_sensitivity=position_error, full_grid_oracle_entries=len(radius))
            evidence.report['cases'].append(dict(branch=branch, level=level, paths=paths, summary=summary))
            evidence.report['two_six_Newton_probe_differences'] = differences
        summaries = [row['summary'] for row in evidence.report['cases']]
        weak_rows = []
        for case in evidence.report['cases']:
            relative = case['paths']['weak']
            saved = np.load(evidence.root / relative, allow_pickle=False)
            for index, key in enumerate(['temporal_square', 'gradient_square', 'gram', 'source_density']):
                for power in range(3):
                    weak_rows.append(dict(branch=case['branch'], level=case['level'], field=key, power=power, radial=float(saved['radial'][index, power]),
                        material=float(saved['material64'][index, power]), error=abs(float(saved['radial'][index, power] - saved['material64'][index, power])),
                        quadrature=abs(float(saved['material48'][index, power] - saved['material64'][index, power]))))
            saved.close()
        for name, rows in [('position-summary', summaries), ('position-weak-checks', weak_rows)]:
            path = evidence.output / (name + '.csv')
            with path.open('x', newline='', encoding='utf-8') as stream:
                writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            evidence.own(path, 'outputs')
        evidence.report.update(summaries=summaries, seconds=perf_counter() - started,
            new_position_density_precision_warning_count=sum(not row['passed'] for row in evidence.report['position_density_precision_diagnostics']))
        evidence.check('all_four_cases_owned', len(evidence.report['cases']) == 4)
        evidence.complete()
    except BaseException as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
