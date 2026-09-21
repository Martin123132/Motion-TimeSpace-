import hashlib
import json
from fractions import Fraction
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    from scipy.linalg import solve
    from annular_adm_mixed_action_20260909 import MixedActionBasis
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_inherited_knot_link_quadrature_20260912 import InheritedKnotLinkQuadrature
    from annular_canonical_common_profile_aligned_20260912 import CommonProfile, RefinedContext, RefinedPreparation
    from annular_canonical_trace_context_20260911 import load_archive
    from annular_canonical_trace_projection_stable_20260911 import kernel_family, trace_extension, gram_density_control
    from annular_canonical_rate_completion_20260911 import evaluate_initial
    from annular_compatible_current_restoring_20260909 import unit_gram_template

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260912'
    directory = intake / 'annular-common-profile-refinement-control-attempt01'
    directory.mkdir(exist_ok=False)
    report = {'state': 'running', 'inputs': {}, 'outputs': {}, 'checks': [], 'knot_controls': [], 'convergence_ratios': [], 'valid_for_physics_claim': False, 'new_evolution': False, 'interval_certificate': False}

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
        batches = []
        for attempt in ['attempt01', 'attempt02']:
            path = intake / ('annular-common-profile-refinement-' + attempt) / 'status.json'
            own(path)
            batch = json.loads(path.read_text())
            batches.append(batch)
            for table in ['inputs', 'outputs']:
                for name, expected in batch[table].items():
                    if digest(root / name) != expected:
                        raise RuntimeError('Evidence changed: ' + name)
                    report['inputs'][name] = expected
        failed, completed = batches
        check('failed_unaligned_attempt_preserved', failed['state'] == 'complete_with_failures' and sum(not row['passed'] for row in failed['checks']) == 2)
        check('aligned_six_cases_pass', completed['state'] == 'complete' and len(completed['cases']) == 6 and all(row['passed'] for row in completed['checks']))
        for path in [Path(__file__), root / 'scripts/diagnose_annular_refined_kernel_load_20260912.py']:
            own(path)
            compile(path.read_bytes(), str(path), 'exec')
        snapshot = directory / ('executed-' + Path(__file__).name)
        snapshot.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        diagnosis_path = intake / 'annular-refined-kernel-load-diagnosis-attempt01.json'
        own(diagnosis_path)
        diagnosis = json.loads(diagnosis_path.read_text())
        check('load_defect_explains_failed_boundary_rows', diagnosis['state'] == 'complete' and all(row['decomposition_error'] < 1e-15 and max(abs(value) for value in row['family_trace_defect']) < 1e-12 for row in diagnosis['cases']))
        common = CommonProfile(root)
        for intervals in [16, 32, 64]:
            basis = MixedActionBasis(numerical.linspace(common.coarse.basis.radii[0], common.coarse.basis.radii[-1], intervals + 1))
            old = MetricLinkQuadrature(basis)
            aligned = InheritedKnotLinkQuadrature(basis, common.coarse.knots)
            check('N' + str(intervals) + '_same_parent_links', all(numerical.array_equal(getattr(old, key), getattr(aligned, key)) for key in ['anchors', 'targets', 'factor', 'node', 'tweight', 'sweight']))
            check('N' + str(intervals) + '_all_inherited_breaks_retained', numerical.all(numerical.isin(common.coarse.knots, aligned.knots)))
            old_error, new_error, partial_error = [], [], []
            for knot in common.coarse.knots[1:-1]:
                exact = (numerical.maximum(aligned.targets - knot, 0)**2 - numerical.maximum(aligned.anchors - knot, 0)**2) / 2
                old_error.append(float(abs(old.integrate(numerical.maximum(old.points - knot, 0)) - exact).max()))
                new_error.append(float(abs(aligned.integrate(numerical.maximum(aligned.points - knot, 0)) - exact).max()))
                exact_partial = (numerical.maximum(aligned.points - knot, 0)**2 - numerical.maximum(aligned.anchors[aligned.pairs] - knot, 0)**2) / 2
                partial_error.append(float(abs(aligned.partial(numerical.maximum(aligned.points - knot, 0)) - exact_partial).max()))
            check('N' + str(intervals) + '_exact_hinge_integrals', max(new_error + partial_error) < 1e-14)
            if intervals > 16:
                check('N' + str(intervals) + '_old_missing_knot_negative_control', max(old_error) > 1e-10, max(old_error))
            else:
                check('N16_quadrature_unchanged', numerical.array_equal(old.points, aligned.points) and numerical.array_equal(old.weights, aligned.weights))
            report['knot_controls'].append({'intervals': intervals, 'old_hinge_integral_error': max(old_error), 'new_hinge_integral_error': max(new_error), 'new_partial_hinge_error': max(partial_error), 'old_link_points': old.points.size, 'new_link_points': aligned.points.size, 'inherited_knots_absent_from_old_split': numerical.setdiff1d(common.coarse.knots, numerical.unique(numerical.concatenate([basis.radii, basis.faces]))).tolist()})
        base = intake / 'annular-common-profile-refinement-attempt02'
        survey_cache = {}
        for case in completed['cases']:
            label, branch, intervals = case['label'], case['branch'], case['intervals']
            check(label + '_initial_identity_not_just_convergence', case['finite_initial_identity_gate'] and case['state'] == 'complete')
            survey = load_archive(base / (label + '_survey.npz'))
            survey_cache[(intervals, branch)] = survey
            for variant in ['primary', 'higher']:
                saved = load_archive(base / (label + '_' + variant + '.npz'))
                check(label + '_' + variant + '_every_constraint_row_replayed', float(abs(saved['constraint_rate']).max()) == case['outcomes'][variant]['Cdot_max'] and max(abs(saved['constraint']).max(), abs(saved['constraint_rate']).max()) < 1e-10)
            initial = load_archive(base / (label + '_initial_data.npz'))
            check(label + '_same_drives_and_inner_mass', numerical.array_equal(initial['boundary_velocity'], common.prepared['boundary_velocity']) and initial['mass_coefficients'][0] == common.prepared['mass_coefficients'][0])
            check(label + '_no_deleted_phase_or_kernel_modes', all(value['original_modes_removed'] == 0 for value in case['completion'].values()) and case['trace_extension']['no_parent_family_modes_discarded'])
            if branch == 'GR':
                old = load_archive(intake / 'annular-common-profile-refinement-attempt01' / (label + '_primary.npz'))
                new = load_archive(base / (label + '_primary.npz'))
                check(label + '_integration_fix_leaves_GR_identical', all(numerical.array_equal(old[key], new[key]) for key in old))
        for branch in ['GR', 'metric_Gram']:
            first, second = [row for row in completed['comparisons'] if row['branch'] == branch]
            for comparison in [first, second]:
                lower, higher = survey_cache[(comparison['coarse'], branch)], survey_cache[(comparison['fine'], branch)]
                check(branch + '_' + str(comparison['fine']) + '_same_survey_and_weights', numerical.array_equal(lower['R'], higher['R']) and numerical.array_equal(lower['weights'], higher['weights']))
                for key, expected in comparison['physical_L2_differences'].items():
                    observed = float(numerical.sqrt(higher['weights'] @ (higher[key] - lower[key])**2))
                    check(branch + '_' + str(comparison['fine']) + '_' + key + '_physical_difference', abs(observed - expected) < 1e-15)
            ratios = {key: second['physical_L2_differences'][key] / value for key, value in first['physical_L2_differences'].items()}
            report['convergence_ratios'].append({'branch': branch, 'fine_difference_over_coarse_difference': ratios, 'not_asymptotic_proof': True})
            check(branch + '_all_measured_physical_differences_decrease', max(ratios.values()) < 1, ratios)
        context = RefinedContext(common, 32, 'metric_Gram')
        selected = load_archive(base / 'N32_metric_Gram_initial_data.npz')
        data, frames, unused_completion = context.build(selected)
        baseline = evaluate_initial(frames['mass'], frames['scalar'], data, context.basis, context.weights, context.links, True, context.system.outer_clock)
        family, unused_primitive, unused_carrier = kernel_family(context, data, frames['mass'], baseline['P_rate_coeff'])
        extended, unused_diagnostic = trace_extension(context, frames['mass'], family)
        actual = evaluate_initial(extended, frames['scalar'], data, context.basis, context.weights, context.links, True, context.system.outer_clock)
        family, primitive, unused_carrier = kernel_family(context, data, extended, actual['P_rate_coeff'])
        unused_coefficients, gp, controls = gram_density_control(context, data, actual, family, primitive)
        values = data['quad']
        bulk = .1 * values['N'] * values['F']**1.5 * values['pi'] * values['w']
        load_error = extended['quad']['p'].T @ (context.weights * (gp - bulk)) + actual['mass_pair'] @ actual['mass_rate_coeff']
        trace_error = extended['nodes']['q'][[0, -1]] @ solve(actual['mass_pair'], load_error)
        report['fixed_N32_load_control'] = {'kernel_checks': controls, 'weak_load_error': float(abs(load_error).max()), 'propagated_trace_error': trace_error.tolist()}
        check('N32_link_vs_bulk_load_repaired', abs(load_error).max() < 1e-11 and abs(trace_error).max() < 1e-11)
        preparation = RefinedPreparation(context)
        direction = numerical.sin(numerical.arange(preparation.face_count - 1) + .41)
        direction /= numerical.linalg.norm(direction)
        changed = {key: value.copy() for key, value in selected.items()}
        changed['mass_coefficients'] = changed['mass_coefficients'].astype(complex)
        changed['mass_coefficients'][1:preparation.face_count] += 1e-25j * direction
        derivative_error = float(abs(preparation.mass_equations(changed)[0].imag / 1e-25 - preparation.mass_equations(selected)[1] @ direction).max())
        report['mass_derivative_error'] = derivative_error
        check('refined_analytic_mass_derivative', derivative_error < 1e-10)
        endpoint_constant = Fraction(59097, 573104) + Fraction(253, 50568) + Fraction(1, 392)
        for count in [17, 33, 65, 129]:
            margin, adjacent, extras = unit_gram_template(count)
            actual_constant = margin[0] + 2 * abs(adjacent[0]) + 2 * sum(abs(weight) for first, second, weight in extras if first == 0 or second == 0)
            check('endpoint_stencil_bound_constant_' + str(count), abs(actual_constant - float(endpoint_constant)) < 1e-15)
        report['conditional_endpoint_bound'] = {'constant_rational': str(endpoint_constant), 'constant_float': float(endpoint_constant), 'bound': '|Gchi_endpoint| <= constant*Cmax*exp(5*h*sup|g|)*h^2*sup|chi_third|', 'conditions': 'The first/last five mesh spacings must lie in a C3 endpoint neighbourhood; positive bounded metric/lapse and bounded g on the link support. Not a uniform estimate for the entire solved sequence.', 'nested_mesh_inside_original_cubic_endpoint_cell': 128, 'no_N128_solve_claim': True}
        check('no_python_cache', not (root / 'scripts/__pycache__').exists())
        report['state'] = 'complete'
        save()
        print(json.dumps({'state': report['state'], 'checks': len(report['checks']), 'knots': report['knot_controls'], 'ratios': report['convergence_ratios'], 'fixed_load': report['fixed_N32_load_control'], 'endpoint_bound': report['conditional_endpoint_bound']}), flush=True)
    except Exception as error:
        report['state'] = 'failed'
        report['error'] = repr(error)
        save()
        raise


if __name__ == '__main__':
    run()
