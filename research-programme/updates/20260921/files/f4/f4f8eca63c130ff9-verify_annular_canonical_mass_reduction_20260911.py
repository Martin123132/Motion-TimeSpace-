import hashlib
import json
import sys
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from annular_adm_mixed_action_20260909 import MixedActionBasis
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian
    from annular_canonical_nodal_data_20260911 import CanonicalInitialNodalData
    from annular_canonical_mass_reduction_20260911 import MassConstraintReduction

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260911'
    destination = intake / 'annular-canonical-mass-reduction-control-attempt01'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': {}, 'outputs': {}, 'checks': [], 'samples': [], 'valid_for_physics_claim': False, 'new_evolution': False, 'interval_certificate': False, 'curvature_scope': 'Floating-point local quadratic diagnostics of row-scaled residual in the raw coefficient SVD direction. Basis/scaling dependent; no fold, nonexistence or neighborhood theorem claimed.'}

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = digest(path)

    def save():
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        if not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    def archive(path):
        own(path)
        with numerical.load(path, allow_pickle=False) as saved:
            return {name: saved[name].copy() for name in saved.files}

    save()
    try:
        prior_path = intake / 'annular-canonical-mass-reduction-attempt01/status.json'
        own(prior_path)
        prior = json.loads(prior_path.read_text())
        check('main_batch_complete_checks_pass', prior['state'] == 'complete' and all(item['passed'] for item in prior['checks']))
        for table in ['inputs', 'outputs']:
            for name, expected in prior[table].items():
                if digest(root / name) != expected:
                    raise RuntimeError('Completed evidence changed: ' + name)
                report['inputs'][name] = expected
        own(Path(__file__))
        snapshot = destination / ('executed-' + Path(__file__).name)
        snapshot.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        parameter_path = root / 'source-intake/navier-stokes/20260909/annular-constraint-correction-initial/canonical.json'
        own(parameter_path)
        constants = {name: float(symbolic.sympify(value)) for name, value in json.loads(parameter_path.read_text())['parameters'].items()}
        radius_symbol, lapse_symbol, metric_symbol, coupling_symbol = symbolic.symbols('radius lapse F kappa', positive=True)
        geometric_momentum, scalar_momentum, mass_velocity, scalar_velocity, scalar_gradient, mass_gradient, quadratic = symbolic.symbols('P pi mudot q w mur quadratic', real=True)
        density = geometric_momentum * mass_velocity + scalar_momentum * scalar_velocity + lapse_symbol * mass_gradient / (coupling_symbol * symbolic.sqrt(metric_symbol)) - lapse_symbol * symbolic.sqrt(metric_symbol) * (scalar_momentum**2 / (2 * radius_symbol**2) + radius_symbol**2 * scalar_gradient**2 / 2) - coupling_symbol * lapse_symbol * metric_symbol**symbolic.Rational(3, 2) * geometric_momentum * scalar_momentum * scalar_gradient - quadratic * geometric_momentum**2
        momentum_equation = symbolic.diff(density, geometric_momentum).subs(geometric_momentum, 0)
        scalar_equation = symbolic.diff(density, scalar_momentum).subs(geometric_momentum, 0)
        eliminated_pi = symbolic.solve(scalar_equation, scalar_momentum)[0]
        flux_equation = symbolic.simplify(momentum_equation.subs(scalar_momentum, eliminated_pi))
        check('exact_canonical_bulk_boundary_flux_law', symbolic.simplify(flux_equation - (mass_velocity - coupling_symbol * radius_symbol**2 * metric_symbol * scalar_velocity * scalar_gradient)) == 0)
        roots = root / 'source-intake/navier-stokes/20260910/annular-parent-root-residence-attempt02'
        for sample in prior['samples']:
            label = sample['label']
            print('Independent check ' + label, flush=True)
            saved = archive(prior_path.parent / (label + '.npz'))
            source = archive(roots / ('canonical_N' + str(sample['mesh']) + '_' + sample['branch'] + '_sample0.npz'))
            basis = MixedActionBasis(source['basis_radii'])
            count = basis.radii.size
            configuration, momenta = source['original_configuration'], source['original_momenta']
            packed = (source['initial_root_box_lower'] + source['initial_root_box_upper']) / 2
            system = ReleasedHermiteRouthian(basis, configuration[:count], configuration[count:], constants, .1, momenta[:count], momenta[count:], source['affine_clock'][0], MetricLinkQuadrature(basis))
            model = CanonicalInitialNodalData(system, packed, configuration, sample['branch'] != 'GR', saved['boundary_velocity'])
            model.mass_coeff_seed[0] = saved['mass_coefficients'][0]
            model.pi_coeff_seed = saved['pi_coefficients'].copy()
            check(label + '_fixed_geometry_configuration_roundtrip', numerical.array_equal(model.fixed_lapse, saved['fixed_lapse']) and numerical.array_equal(configuration, saved['configuration']))
            state = saved['state']
            residual = model.data_residual(state)
            check(label + '_all_residuals_replayed_including_failures', numerical.array_equal(residual, saved['full_residual']))
            evaluation = model.evaluate(numerical.concatenate([model.fixed_lapse, state[-3:]]))
            exact_radius = Fraction.from_float(float(basis.radii[0]))
            exact_mass = Fraction.from_float(float(model.mass_coeff_seed[0]))
            exact_q = Fraction.from_float(float(model.boundary_velocity[1]))
            exact_gradient = sum((Fraction.from_float(float(coefficient)) * Fraction.from_float(float(value)) for coefficient, value in zip(basis.derivative[0], configuration[:count])), Fraction(0)) + Fraction.from_float(float(configuration[count])) / Fraction.from_float(basis.spacing)
            exact_flux = Fraction(1, 10) * exact_radius**2 * (1 - 2 * exact_mass / exact_radius) * exact_q * exact_gradient
            exact_port = Fraction.from_float(float(model.boundary_velocity[0]))
            exact_difference = exact_port - exact_flux
            endpoint_radius = float(exact_radius)
            endpoint_f = 1 - 2 * float(exact_mass) / endpoint_radius
            endpoint_lapse = float(model.fixed_lapse[0])
            boundary_prediction = {'assumptions': 'P=0 canonical scalar, continuous one-sided traces, no additional P-linear boundary source. Bulk law applies alone only to GR. Stored binary boundary data and basis coefficients treated as exact rational inputs; this is not an experimental error enclosure.', 'gradient_at_inner_boundary': float(exact_gradient), 'prescribed_inner_flux': float(exact_port), 'bulk_flux_from_prescribed_scalar_velocity': float(exact_flux), 'prescribed_minus_bulk_flux': float(exact_difference), 'relative_mismatch': float(exact_difference / exact_flux), 'exact_mismatch_numerator': str(exact_difference.numerator), 'exact_mismatch_denominator': str(exact_difference.denominator), 'is_exactly_zero_for_stored_data': exact_difference == 0}
            gram_trace = 0.
            if model.include_gram:
                links = model.links
                check(label + '_Gram_anchors_strictly_interior', numerical.all(links.anchors > basis.radii[0]) and numerical.all(links.anchors < basis.radii[-1]))
                selected = links.node == 0
                check(label + '_Gram_inner_sampling_zero', numerical.all(links.sweight[selected] == 0))
                jacobian = numerical.exp(evaluation['sources']['endpoint_log'])
                coefficient = basis.radii**2 * model.fixed_lapse * numerical.sqrt(model.node_f)
                density_gram = links.collect(links.sweight * jacobian * coefficient[links.node])
                amplitude_time = links.collect(links.tweight * evaluation['scalar_velocity'][links.node] * jacobian)
                current = model.amplitude[links.factor] * (links.sweight * coefficient[links.node] * amplitude_time[links.factor] - links.tweight * evaluation['scalar_velocity'][links.node] * density_gram[links.factor]) / basis.spacing
                oriented_trace = -numerical.sum(current[selected] / jacobian[selected])
                from_scalar_force = -evaluation['scalar_velocity'][0] * evaluation['sources']['scalar_force'][0]
                check(label + '_Gram_endpoint_current_scalar_force_identity', abs(oriented_trace - from_scalar_force) < 1e-10, float(abs(oriented_trace - from_scalar_force)))
                gram_trace = .1 * numerical.sqrt(endpoint_f) / endpoint_lapse * float(oriented_trace)
                boundary_prediction['Gram_P_force_inner_trace'] = gram_trace
                boundary_prediction['Gram_scalar_force_inner'] = float(evaluation['sources']['scalar_force'][0])
                boundary_prediction['Gram_scope'] = 'One-sided trace derived from full time-link kernel, retaining endpoint Jacobians and orientation; numerical values use the stored finite initial jet, not a certified continuum solution.'
            endpoint_seed_f = 1 - 2 * model.packed[model.system.slices[0]][0] / endpoint_radius
            pi_endpoint = endpoint_radius**2 * saved['pi_coefficients'][0] / (model.lapse_seed[0] * numerical.sqrt(endpoint_seed_f))
            local_q = endpoint_lapse * numerical.sqrt(endpoint_f) * pi_endpoint / endpoint_radius**2
            momentum_flux = .1 * endpoint_lapse * endpoint_f**1.5 * pi_endpoint * float(exact_gradient) - gram_trace
            boundary_prediction['prescribed_q_bulk_flux_minus_Gram_trace'] = float(exact_flux) - gram_trace
            boundary_prediction['local_canonical_EP_flux_from_pi'] = float(momentum_flux)
            boundary_prediction['finite_mass_velocity_trace'] = float(evaluation['mass_rate'][0])
            boundary_prediction['finite_mass_velocity_minus_local_EP_trace'] = float(evaluation['mass_rate'][0] - momentum_flux)
            boundary_prediction['finite_scalar_velocity_minus_local_Legendre_trace'] = float(evaluation['scalar_velocity'][0] - local_q)
            reduction = MassConstraintReduction(model)
            mass_block, other_block = reduction.constraint_blocks(state)
            full_direction = numerical.sin(numerical.arange(state.size) + .9) * numerical.maximum(abs(state), .001)
            analytic = mass_block @ full_direction[:count] + other_block @ full_direction[count:]
            complex_result = reduction.constraint_value(state.astype(complex) + 1e-25j * full_direction).imag / 1e-25
            mass_error = float(abs(analytic - complex_result).max())
            check(label + '_analytic_mass_derivative_away_from_original_roots', mass_error < 1e-10, mass_error)
            direction = numerical.cos(numerical.arange(count + 3) + .6) * numerical.maximum(abs(state[count:]), .001)
            tangent = saved['tangent']
            step = 1e-5
            plus, unused_plus = reduction.project(state + step * (tangent @ direction))
            minus, unused_minus = reduction.project(state - step * (tangent @ direction))
            finite = (model.data_residual(plus)[count:] - model.data_residual(minus)[count:]) / (2 * step)
            predicted = saved['reduced_jacobian'] @ direction
            difference = float(abs(finite - predicted).max() / max(1., float(abs(predicted).max())))
            check(label + '_nonlinear_manifold_Jacobian_including_failed_cases', difference < 1e-7, difference)
            omitted_mass = float(abs(other_block @ direction).max())
            corrected_mass = float(abs(mass_block @ (tangent[:count] @ direction) + other_block @ direction).max())
            check(label + '_omitted_mass_response_negative_control', omitted_mass > 1e-12 and corrected_mass < 1e-12, {'omitted': omitted_mass, 'correct': corrected_mass})
            row_scales = saved['row_scales'][count:]
            base = residual[count:] / row_scales
            left_mode, right_mode = saved['smallest_left_mode'], saved['smallest_right_mode']
            sigma = float(saved['reduced_singular_values'][-1])
            projected_residual = float(left_mode @ base)
            curvature_rows = []
            for step in [1e-3, 5e-4]:
                try:
                    plus, unused_plus = reduction.project(state + step * (tangent @ right_mode))
                    minus, unused_minus = reduction.project(state - step * (tangent @ right_mode))
                    upper = model.data_residual(plus)[count:] / row_scales
                    lower = model.data_residual(minus)[count:] / row_scales
                    slope = float(left_mode @ ((upper - lower) / (2 * step)))
                    curvature = float(left_mode @ ((upper - 2 * base + lower) / step**2))
                    curvature_rows.append({'step': step, 'status': 'evaluated', 'projected_slope': slope, 'projected_second_derivative': curvature, 'quadratic_discriminant': sigma**2 - 2 * curvature * projected_residual, 'plus_full_scaled_residual': float(abs(upper).max()), 'minus_full_scaled_residual': float(abs(lower).max())})
                except (ValueError, RuntimeError) as error:
                    curvature_rows.append({'step': step, 'status': 'chart_or_mass_solver_rejected', 'error': repr(error)})
            model.set_state(state)
            scaled = saved['reduced_jacobian'] / row_scales[:, None]
            column_scales = numerical.maximum(abs(saved['seed_state'][count:]), .001)
            equilibrated_singular = numerical.linalg.svd(scaled * column_scales[None, :], compute_uv=False)
            record = {'label': label, 'solver_status': sample['status'], 'analytic_mass_directional_error': mass_error, 'projected_directional_error': difference, 'smallest_singular_value': sigma, 'projected_residual': projected_residual, 'raw_coefficient_condition': float(saved['reduced_singular_values'][0] / sigma), 'seed_column_scaled_condition': float(equilibrated_singular[0] / equilibrated_singular[-1]), 'column_scaling_rule': 'max(abs(inherited seed z coefficient), .001), diagnostic only; never changes equations or acceptance.', 'curvature_rows': curvature_rows, 'boundary_prediction': boundary_prediction, 'valid_for_physics_claim': False}
            report['samples'].append(record)
            save()
            print(json.dumps({'label': label, 'status': sample['status'], 'derivative_error': difference, 'curvature': curvature_rows}), flush=True)
        for module in tuple(sys.modules.values()):
            filename = getattr(module, '__file__', None)
            if filename:
                path = Path(filename).resolve()
                if path.parent == root / 'scripts' and path.suffix == '.py':
                    own(path)
        check('no_python_cache', not (root / 'scripts/__pycache__').exists())
        report['state'] = 'complete'
        report['completed_utc'] = datetime.now(timezone.utc).isoformat()
        save()
        print('Mass-reduction controls complete.', flush=True)
    except Exception as error:
        report['state'] = 'failed'
        report['error'] = repr(error)
        save()
        raise


if __name__ == '__main__':
    run()
