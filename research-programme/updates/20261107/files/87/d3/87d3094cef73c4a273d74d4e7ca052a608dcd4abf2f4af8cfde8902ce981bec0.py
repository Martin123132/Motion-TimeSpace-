from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_joint_first_tangent_20260922 import MetricResponse
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_background_time_tangent_20260928 import BackgroundLoads, FIELD_NAMES
from annular_radial_time_forcing_20260928 import explicit_time_forcing
from annular_candidate_radial_constraint_20260920 import radial_rhs
from annular_support_radial_response_20260928 import gravitational_moments
from time import perf_counter
import csv
import hashlib
import json
import numpy as np
import sympy as sp


def main():
    evidence = EvidenceRun('annular-direct-background-current-validation-attempt01', __file__)
    started = perf_counter()
    try:
        parent_path = evidence.output.parent / 'annular-direct-background-coupled-current-attempt01/status.json'
        parent = json.loads(parent_path.read_text())
        evidence.own(parent_path)
        evidence.check('coupled_run_complete', parent['state'] == 'complete' and all(row['passed'] for row in parent['checks']))
        digests, bad = {}, []
        for category in ['inputs', 'outputs']:
            for relative, expected in parent[category].items():
                if relative == 'CURRENT_LOCAL_RESUME.md':
                    continue
                path = evidence.root / relative
                digest = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
                if digest != expected:
                    bad.append(relative)
                else:
                    evidence.own(path)
                    digests[relative] = expected
        evidence.check('owned_inputs_and_results_unchanged', not bad, bad)

        def read(relative):
            evidence.check('owned:' + relative, relative in digests)
            with np.load(evidence.root / relative, allow_pickle=False) as archive:
                return {key: archive[key] for key in archive.files}

        label, center, width, speed = sp.symbols('lambda b width v', real=True)
        weight = 6 * (label + sp.Rational(1, 2)) * (sp.Rational(1, 2) - label)
        evidence.check('exact_material_normalization', sp.integrate(weight, (label, -sp.Rational(1, 2), sp.Rational(1, 2))) == 1)
        for power in range(3):
            weak = sp.integrate(-speed * sp.diff(weight, label) * (center + width * label)**power / width,
                (label, -sp.Rational(1, 2), sp.Rational(1, 2)))
            expected = [0, speed, 2 * center * speed][power]
            evidence.check('exact_source_transport_moment:' + str(power), sp.simplify(weak - expected) == 0)
        evidence.check('nonzero_interior_endpoint_derivatives', sp.diff(weight, label).subs(label, -sp.Rational(1, 2)) == 6
            and sp.diff(weight, label).subs(label, sp.Rational(1, 2)) == -6)
        coefficient, coefficient_r, coefficient_mu, coefficient_nu, coefficient_v = sp.symbols('A A_R A_mu A_nu A_V')
        density, density_r, velocity, velocity_r, acceleration, mass_r, lapse_r = sp.symbols('rho rho_R V V_R a mu_R nu_R')
        direct_source = -coefficient * (density_r * velocity + density * velocity_r)
        direct_source += density * coefficient_v * (acceleration - velocity * velocity_r)
        coefficient_along_r = coefficient_r + coefficient_mu * mass_r + coefficient_nu * lapse_r
        flux_r = density * velocity * (coefficient_along_r + coefficient_v * velocity_r)
        flux_r += coefficient * (density_r * velocity + density * velocity_r)
        conservative_source = -flux_r + density * velocity * coefficient_along_r + density * coefficient_v * acceleration
        evidence.check('exact_dust_flux_plus_smooth_source', sp.expand(direct_source - conservative_source) == 0)

        comparison = []
        off_grid_rows = []
        affine_rows = []
        live_path = evidence.output.parent / 'annular-live-support-acceleration-attempt01/status.json'
        evidence.check('prior_support_response_owned', str(live_path.relative_to(evidence.root)) in digests)
        live = json.loads(live_path.read_text())
        old_path = evidence.output.parent / 'annular-archived-probe-baseline-comparison-attempt01/paired-probe-baseline-sensitivity.csv'
        evidence.check('old_baseline_owned', str(old_path.relative_to(evidence.root)) in digests)
        with old_path.open(newline='', encoding='utf-8') as stream:
            old_rows = list(csv.DictReader(stream))
        current_path = evidence.output.parent / 'annular-direct-background-coupled-current-attempt01/direct-current-moments.csv'
        with current_path.open(newline='', encoding='utf-8') as stream:
            new_rows = list(csv.DictReader(stream))
        evidence.check('four_matched_cases', {(row['branch'], row['level']) for row in parent['cases']} ==
            {(branch, level) for branch in ['reference-reference', 'MTS-primary'] for level in ['fine', 'third']})
        for case in parent['cases']:
            name = case['branch'] + '-' + case['level']
            archive = read(case['paths']['background_response'])
            solver, solution = reconstructed_solver(archive)
            response = MetricResponse(solver, solution, archive['forcing'], 0., [])
            state = read(case['sources']['state'])
            boundary = response.values(solver.edges[[0, -1]])
            scale = max(float(np.max(abs(solution['state']))), 1e-30)
            error = max(abs(boundary[0, 0]), abs(boundary[1, -1] + boundary[0, -1] / (solver.edges[-1] - 2 * state['state'][0, -1, -1])))
            evidence.check(name + ':independent_boundary', error <= 2e-12 * scale + 1e-25, float(error))
            primitive = solution['primitives']
            lower = solution['left'][:, 1:] + np.array([np.polynomial.chebyshev.chebval(-1., values[1:].T) for values in primitive])
            upper = solution['left'][:, :-1] + np.array([np.polynomial.chebyshev.chebval(1., values[:-1].T) for values in primitive])
            evidence.check(name + ':integrated_tangent_continuous', np.max(abs(lower - upper)) <= 2e-12 * scale + 1e-25,
                float(np.max(abs(lower - upper))))
            weak = read(case['paths']['weak'])
            evidence.check(name + ':number_conservation', abs(float(weak['radial'][3, 0])) <= 2e-11, float(weak['radial'][3, 0]))
            flow = read(case['paths']['flow'])
            evidence.check(name + ':finite_full_jet', np.isfinite(flow['acceleration']).all() and np.isfinite(flow['metric_rate']).all())
            acceleration_change = float(np.max(abs(flow['acceleration'] - flow['archived_accelerations'][-1])))
            evidence.check(name + ':saved_acceleration_change', acceleration_change == case['summary']['acceleration_change'])
            loads, action, unused = restore_case(evidence, digests, case['branch'], case['level'], perf_counter() + 1800)
            loads.owner.label_order = 28
            engine = BackgroundLoads(loads, action)
            points, weights = np.polynomial.legendre.leggauss(4)
            radius = (solver.centers[:, None] + solver.lengths[:, None] * points / 2).ravel()
            fields, rates = engine.sample(radius)
            base = action.solver.values(action.solution, radius)[0]
            tangent_values, tangent_radial = solver.values(solution, radius)
            unused, local = radial_rhs(radius, *base, *[fields[key] for key in FIELD_NAMES],
                action.owner.coupling, action.owner.source_mass, jacobian=True)
            forcing = explicit_time_forcing(radius, *base, fields['source_density'], fields['velocity'],
                *[rates[key] for key in FIELD_NAMES], action.owner.coupling, action.owner.source_mass)
            predicted = np.einsum('abn,bn->an', local, tangent_values) + forcing
            difference = tangent_radial - predicted
            off_grid_scale = np.maximum(np.max(abs(predicted), axis=1), 1e-30)
            off_grid_error = np.max(abs(difference), axis=1)
            evidence.check(name + ':independent_off_grid_linearized_equations',
                np.all(off_grid_error <= 2e-8 * off_grid_scale + 1e-15),
                dict(error=off_grid_error.tolist(), scale=off_grid_scale.tolist(), points=len(radius)))
            off_path = evidence.output / (name + '-off-grid-response.npz')
            np.savez_compressed(off_path, radius=radius, tangent=tangent_values, derivative=tangent_radial,
                predicted=predicted, difference=difference)
            evidence.own(off_path, 'outputs')
            off_grid_rows.append(dict(branch=case['branch'], level=case['level'], points=len(radius),
                mass_error=float(off_grid_error[0]), mass_scale=float(off_grid_scale[0]),
                lapse_error=float(off_grid_error[1]), lapse_scale=float(off_grid_scale[1])))
            print(json.dumps(dict(case=name, off_grid=off_grid_rows[-1])), flush=True)
            prior = next(row for row in live['cases'] if row['branch'] == case['branch'] and row['level'] == case['level'])
            prior_response = read(prior['paths']['live_response'])
            old_solver, old_solution = reconstructed_solver(prior_response)
            support_response = MetricResponse(old_solver, old_solution, prior_response['forcing'], 0., [])
            gravity_slope = gravitational_moments(action, support_response, 32)
            projection = read(prior['paths']['projection'])
            final_iteration = read(case['iterations'][-1]['path'])
            removed_old_work = float(projection['correction'].ravel() @ final_iteration['residual'].ravel())
            for order in [48, 64]:
                coefficient_packet = read(prior['paths']['compensated_material' + str(order)])
                coefficient = float(coefficient_packet['average'][-1])
                evidence.check(name + ':positive_support_coefficient:' + str(order), coefficient > 0)
                selected = [row for row in new_rows if row['branch'] == case['branch'] and row['level'] == case['level'] and int(row['material_order']) == order]
                force = float(selected[0]['support_force']) - removed_old_work
                amplitude = -force / coefficient
                for row in selected:
                    power = int(row['power'])
                    slope = float(coefficient_packet['current'][power, -1] + gravity_slope[power])
                    baseline = float(row['total'])
                    prediction = baseline + amplitude * slope
                    affine_rows.append(dict(branch=case['branch'], level=case['level'], material_order=order,
                        power=power, force=force, coefficient=coefficient, derived_acceleration=amplitude,
                        force_after=force + amplitude * coefficient, current_before=baseline,
                        current_slope=slope, current_change=amplitude * slope, current_after_affine=prediction,
                        numerical_target_met=abs(prediction) <= 3e-17, valid_for_physics_claim=False,
                        evaluation='Order-matched affine consequence of validated acceleration block; no new large-amplitude direct trial or trajectory'))
            for power in range(3):
                select = lambda row: row['branch'] == case['branch'] and row['level'] == case['level'] and int(row['material_order']) == 64 and int(row['power']) == power
                old = next(row for row in old_rows if select(row))
                new = next(row for row in new_rows if select(row))
                total = float(new['matter']) + float(new['gravity'])
                evidence.check(name + ':unsubtracted_total:' + str(power), total == float(new['total']))
                comparison.append(dict(branch=case['branch'], level=case['level'], power=power,
                    old_earlier=float(old['earlier_baseline']), old_later=float(old['later_baseline']),
                    old_paired_difference=float(old['paired_difference']), new_direct=total,
                    direct_support_force=float(new['support_force']),
                    baseline_subtracted=False, observed_difference_is_error_bound=False))
            evidence.report['cases'].append(dict(branch=case['branch'], level=case['level'], summary=case['summary']))
        path = evidence.output / 'old-probes-versus-direct-current.csv'
        with path.open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(comparison[0]))
            writer.writeheader()
            writer.writerows(comparison)
        evidence.own(path, 'outputs')
        affine_path = evidence.output / 'order-matched-support-acceleration-compatibility.csv'
        with affine_path.open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(affine_rows[0]))
            writer.writeheader()
            writer.writerows(affine_rows)
        evidence.own(affine_path, 'outputs')
        evidence.report.update(seconds=perf_counter() - started, comparison=comparison, new_trajectories=0,
            off_grid_checks=off_grid_rows,
            support_acceleration_affine_rows=affine_rows, large_amplitude_direct_trial_performed=False,
            conservative_source_formula='B_dust=-partial_R(A*rho*V)+rho*V*(partial_R A at fixed Y,V + A_Y*Y_R)+rho*A_V*a; with Z=Y_t+A*rho*V, Z_R=f_Y Z+B_wave+smooth-f_Y*(A*rho*V)',
            conservative_source_implemented=False,
            github_action=False, subagents_used=False, original_workbench_modified=False,
            protected_since='2026-09-28T15:08:14+00:00')
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
