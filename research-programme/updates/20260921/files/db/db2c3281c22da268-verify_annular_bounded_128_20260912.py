import hashlib
import json
from fractions import Fraction
from pathlib import Path
from types import SimpleNamespace

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from annular_adm_mixed_action_20260909 import MixedActionBasis, linear_value_gradient
    from annular_canonical_bounded_128_20260912 import CommonProfile, RefinedFields
    from annular_canonical_trace_context_20260911 import load_archive
    from annular_gram_joint_action_20260909 import gram_matrices
    from annular_inherited_knot_link_quadrature_20260912 import InheritedKnotLinkQuadrature

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260912'
    directory = intake / 'annular-bounded-N128-control-attempt01'
    directory.mkdir(exist_ok=False)
    report = {'state': 'running', 'inputs': {}, 'outputs': {}, 'checks': [], 'comparisons': [], 'endpoint_bounds': [], 'boundary_trace_diagnostics': [], 'valid_for_physics_claim': False, 'new_evolution': False, 'interval_certificate': False}

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = digest(path)

    def save():
        (directory / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        save()
        if not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    save()
    try:
        own(Path(__file__))
        snapshot = directory / ('executed-' + Path(__file__).name)
        snapshot.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        base = intake / 'annular-bounded-N128-attempt02'
        status = json.loads((base / 'status.json').read_text())
        own(base / 'status.json')
        for table in ['inputs', 'outputs']:
            for name, expected in status[table].items():
                if digest(root / name) != expected:
                    raise RuntimeError('Changed evidence: ' + name)
                report['inputs'][name] = expected
        check('paired_N128_completed', status['state'] == 'complete' and len(status['cases']) == 2 and all(row['passed'] for row in status['checks']))
        symbolic_radius, symbolic_lapse, symbolic_F, symbolic_P, symbolic_Pdot = symbolic.symbols('R N F P Pdot', positive=True)
        boundary_H = symbolic_radius * symbolic_lapse * symbolic_F**symbolic.Rational(5, 2) * symbolic_P**2 / 20
        boundary_covector = symbolic.diff(boundary_H, symbolic_P)
        check('exact_free_P_boundary_equation', symbolic.simplify(boundary_covector - symbolic_radius * symbolic_lapse * symbolic_F**symbolic.Rational(5, 2) * symbolic_P / 10) == 0)
        check('exact_P0_boundary_tangent', symbolic.simplify(symbolic.diff(boundary_covector, symbolic_P).subs(symbolic_P, 0) * symbolic_Pdot - symbolic_radius * symbolic_lapse * symbolic_F**symbolic.Rational(5, 2) * symbolic_Pdot / 10) == 0)
        old_path = intake / 'annular-common-profile-refinement-attempt02/status.json'
        own(old_path)
        old_status = json.loads(old_path.read_text())
        common = CommonProfile(root)
        basis = MixedActionBasis(numerical.linspace(5.875, 6.125, 129))
        context = SimpleNamespace(common=common, basis=basis)
        factors, sampling = gram_matrices(129)
        check('endpoint_density_weights_zero_but_scalar_factors_retained', numerical.all(sampling[:, [0, -1]] == 0) and numerical.any(factors[:, 0] != 0) and numerical.any(factors[:, -1] != 0))
        knots = numerical.unique(numerical.concatenate([basis.radii, basis.faces, common.coarse.knots]))
        fields_to_compare = ['mu', 'mu_r', 'pi', 'pi_r', 'N', 'mu_t', 'mu_tr', 'P_t', 'q', 'q_r', 'pi_t']
        for branch in ['metric_Gram', 'GR']:
            label = 'N128_' + branch
            selected = load_archive(base / (label + '_initial_data.npz'))
            physical = RefinedFields(context, selected)
            nodes = physical.evaluate(basis.radii)
            amplitude = factors @ nodes['chi']
            gram_density = sampling.T @ amplitude**2 / (2 * basis.spacing)
            check(label + '_no_hidden_mass_bubble_initial_fit', numerical.all(selected['mass_coefficients'][basis.faces.size:] == 0))
            check(label + '_same_coarse_kinetic_owner', int(selected['canonical_common_weight_owner']) == 16)
            for variant, order, link_order in [('primary', 12, 8), ('higher', 16, 12)]:
                saved = load_archive(base / (label + '_' + variant + '.npz'))
                gauss, weights = numerical.polynomial.legendre.leggauss(order)
                halfwidth = numerical.diff(knots) / 2
                points = ((knots[:-1] + knots[1:])[:, None] / 2 + halfwidth[:, None] * gauss).ravel()
                weights = (halfwidth[:, None] * weights).ravel()
                values = physical.evaluate(points)
                eta = linear_value_gradient(basis.radii, points)[0]
                energy = values['pi']**2 / (2 * points**2) + points**2 * values['w']**2 / 2
                constraint = eta.T @ (weights * (values['mu_r'] / (.1 * numerical.sqrt(values['F'])) - numerical.sqrt(values['F']) * energy))
                if branch == 'metric_Gram':
                    constraint -= basis.radii**2 * numerical.sqrt(nodes['F']) * gram_density
                coefficient = values['mu_r'] / (.1 * points * values['F']**1.5) + energy / (points * numerical.sqrt(values['F']))
                density = saved['mu_tr'] / (.1 * numerical.sqrt(values['F'])) + coefficient * saved['mu_t']
                density -= numerical.sqrt(values['F']) * values['pi'] * saved['pi_t'] / points**2 + points**2 * numerical.sqrt(values['F']) * values['w'] * saved['q_r'] + .1 * values['F']**1.5 * values['pi'] * values['w'] * saved['P_t']
                constraint_rate = eta.T @ (weights * density) + saved['gram_constraint_rate']
                check(label + '_' + variant + '_reintegrated_all_C', max(abs(constraint).max(), abs(constraint - saved['constraint']).max()) < 1e-10)
                check(label + '_' + variant + '_recontracted_all_Cdot', max(abs(constraint_rate).max(), abs(constraint_rate - saved['constraint_rate']).max()) < 1e-10)
                links = InheritedKnotLinkQuadrature(basis, common.coarse.knots, order=link_order)
                scalar_covector = numerical.zeros(129)
                if branch == 'metric_Gram':
                    jacobian = numerical.exp(saved['endpoint_log'])
                    coefficient_nodes = basis.radii**2 * nodes['N'] * numerical.sqrt(nodes['F'])
                    density_nodes = links.collect(links.sweight * jacobian * coefficient_nodes[links.node])
                    numerical.add.at(scalar_covector, links.node, -links.tweight * amplitude[links.factor] * density_nodes[links.factor] / (basis.spacing * jacobian))
                    check(variant + '_independent_Gram_scalar_covector', abs(scalar_covector - saved['gram_scalar']).max() < 1e-12)
                    coarse_count = common.coarse.basis.radii.size
                    configuration = common.prepared['configuration']
                    slopes = common.coarse.basis.derivative @ configuration[:coarse_count] + configuration[coarse_count:] / common.coarse.basis.spacing
                    bound_constant = float(Fraction(190279, 1719312))
                    for endpoint, coarse_cell in [(0, 0), (128, coarse_count - 2)]:
                        coarse_h = common.coarse.basis.spacing
                        third = abs(12 * (configuration[coarse_cell] - configuration[coarse_cell + 1]) / coarse_h**3 + 6 * (slopes[coarse_cell] + slopes[coarse_cell + 1]) / coarse_h**2)
                        endpoint_links = numerical.flatnonzero(links.node == endpoint)
                        participating = numerical.unique(links.factor[endpoint_links])
                        supports = numerical.flatnonzero(numerical.any((factors[participating] != 0) | (sampling[participating] != 0), axis=0))
                        within = basis.radii[supports].min() >= common.coarse.basis.radii[coarse_cell] and basis.radii[supports].max() <= common.coarse.basis.radii[coarse_cell + 1]
                        check(variant + '_endpoint_' + str(endpoint) + '_support_inside_single_source_cubic', within)
                        log_ratio = []
                        for link in endpoint_links:
                            candidates = numerical.flatnonzero((links.factor == links.factor[link]) & (links.sweight != 0))
                            log_ratio.extend((saved['endpoint_log'][candidates] - saved['endpoint_log'][link]).tolist())
                        ratio_bound = float(numerical.exp(max(log_ratio)))
                        coefficient_bound = float(coefficient_nodes[supports].max())
                        bound = bound_constant * coefficient_bound * ratio_bound * basis.spacing**2 * third
                        row = {'variant': variant, 'endpoint': endpoint, 'source_cubic_abs_third': float(third), 'finite_max_J_ratio': ratio_bound, 'finite_max_C': coefficient_bound, 'conditional_stencil_bound': bound, 'actual_force': float(abs(scalar_covector[endpoint])), 'force_over_bound': float(abs(scalar_covector[endpoint]) / bound), 'not_uniform_history_or_interval_bound': True}
                        report['endpoint_bounds'].append(row)
                        check(variant + '_endpoint_' + str(endpoint) + '_finite_bound', row['actual_force'] <= bound * (1 + 1e-6), row)
                endpoint_index = [0, -1]
                parent_flux = .1 * nodes['N'][endpoint_index] * nodes['F'][endpoint_index]**1.5 * nodes['pi'][endpoint_index] * nodes['w'][endpoint_index]
                parent_flux += numerical.array([1., -1.]) * .1 * numerical.sqrt(nodes['F'][endpoint_index]) * saved['q_nodes'][endpoint_index] * scalar_covector[endpoint_index] / nodes['N'][endpoint_index]
                check(label + '_' + variant + '_full_parent_boundary_flux', max(abs(parent_flux - saved['mu_t_nodes'][endpoint_index]).max(), abs(saved['mu_t_nodes'][0] - selected['boundary_velocity'][0])) < 1e-10)
                if variant == 'primary':
                    local_energy = nodes['pi']**2 / (2 * basis.radii**2) + basis.radii**2 * nodes['w']**2 / 2
                    desired_log_lapse_derivative = .1 * local_energy / basis.radii + nodes['mu'] / (basis.radii**2 * nodes['F'])
                    actual_log_lapse_derivative = nodes['N_r'] / nodes['N']
                    bulk_Pdot_endpoint = nodes['N'] / (.1 * numerical.sqrt(nodes['F'])) * (desired_log_lapse_derivative - actual_log_lapse_derivative)
                    desired_gradient_change = (nodes['N'] * desired_log_lapse_derivative - nodes['N_r'])[endpoint_index]
                    length = basis.radii[-1] - basis.radii[0]
                    fraction = (basis.radii - basis.radii[0]) / length
                    lapse_lift = length * (desired_gradient_change[0] * (fraction**3 - 2 * fraction**2 + fraction) + desired_gradient_change[1] * (fraction**3 - fraction**2))
                    lift_gradient = desired_gradient_change[0] * (3 * fraction**2 - 4 * fraction + 1) + desired_gradient_change[1] * (3 * fraction**2 - 2 * fraction)
                    bound = 4 * length / 27 * float(abs(desired_gradient_change).sum())
                    strong_corrected = nodes['N'][endpoint_index] / (.1 * numerical.sqrt(nodes['F'][endpoint_index])) * (desired_log_lapse_derivative[endpoint_index] - (nodes['N_r'] + lift_gradient)[endpoint_index] / nodes['N'][endpoint_index])
                    check(label + '_constructed_cubic_lapse_lift_endpoint_values', abs(lapse_lift[endpoint_index]).max() < 1e-15)
                    check(label + '_constructed_cubic_lapse_lift_endpoint_gradients', abs(strong_corrected).max() < 1e-12)
                    candidate_path = directory / (label + '_unapplied_lapse_boundary_candidate.npz')
                    numerical.savez_compressed(candidate_path, radius=basis.radii, original_lapse=nodes['N'], cubic_lift=lapse_lift, cubic_lift_gradient=lift_gradient, required_endpoint_gradient_change=desired_gradient_change, physical_initial_state_changed=numerical.array(False))
                    own(candidate_path, 'outputs')
                    report['boundary_trace_diagnostics'].append({'branch': branch, 'projected_Pdot_endpoints': saved['P_t_nodes'][endpoint_index].tolist(), 'bulk_strong_Pdot_endpoints': bulk_Pdot_endpoint[endpoint_index].tolist(), 'lapse_log_derivative_gap': (actual_log_lapse_derivative - desired_log_lapse_derivative)[endpoint_index].tolist(), 'free_strong_P_boundary_tangent': (.1 * basis.radii * nodes['N'] * nodes['F']**2.5 * saved['P_t_nodes'])[endpoint_index].tolist(), 'candidate_endpoint_gradient_change': desired_gradient_change.tolist(), 'candidate_uniform_lapse_change_bound': bound, 'candidate_analytic_positive_lapse_margin_float_evaluation': float(nodes['N'].min() - bound), 'strong_Pdot_after_candidate': strong_corrected.tolist(), 'candidate_not_applied': True, 'candidate_requires_exact_P1_plus_global_cubic_representation': True, 'conditional_only': 'Nonzero values obstruct a classical free-P endpoint condition P_b(t)=0 with this fixed lapse profile. Finite weak endpoint covectors are coupled; this is not a failed finite first-jet gate. The cubic lift fixes only the strong P0 endpoint gradient law; full Gram adjoint, free boundary work and higher jets require revalidation.'})
            survey = load_archive(base / (label + '_survey.npz'))
            lower_path = intake / 'annular-common-profile-refinement-attempt02' / ('N64_' + branch + '_survey.npz')
            own(lower_path)
            lower = load_archive(lower_path)
            previous = next(row for row in old_status['comparisons'] if row['fine'] == 64 and row['branch'] == branch)
            differences = {key: float(numerical.sqrt(survey['weights'] @ (survey[key] - lower[key])**2)) for key in fields_to_compare}
            reported = next(row for row in status['comparisons'] if row['branch'] == branch)['physical_L2_differences']
            check(label + '_all_survey_differences_recomputed', max(abs(differences[key] - reported[key]) for key in fields_to_compare) < 1e-12)
            ratios = {key: differences[key] / previous['physical_L2_differences'][key] for key in fields_to_compare}
            relative = {key: differences[key] / float(numerical.sqrt(survey['weights'] @ survey[key]**2)) for key in fields_to_compare}
            report['comparisons'].append({'branch': branch, 'differences': differences, 'difference_ratios': ratios, 'relative_changes': relative, 'all_measured_differences_decrease': max(ratios.values()) < 1, 'asymptotic_convergence_proven': False})
            check(label + '_both_branches_reported_without_success_filter', len(ratios) == len(fields_to_compare))
        check('no_python_cache', not (root / 'scripts/__pycache__').exists())
        report['state'] = 'complete'
        save()
        print(json.dumps({'state': report['state'], 'checks': len(report['checks']), 'comparisons': report['comparisons'], 'endpoint_bounds': report['endpoint_bounds'], 'boundary_trace_diagnostics': report['boundary_trace_diagnostics']}), flush=True)
    except Exception as error:
        report['state'], report['error'] = 'failed', repr(error)
        save()
        raise


if __name__ == '__main__':
    run()
