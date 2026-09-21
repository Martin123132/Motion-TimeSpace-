import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from scipy.integrate import solve_ivp
    from annular_adm_mixed_action_20260909 import MixedActionBasis
    from annular_parent_root_residence_20260910 import canonical_maps

    parser = argparse.ArgumentParser()
    parser.add_argument('--attempt', required=True)
    arguments = parser.parse_args()
    if not arguments.attempt.isalnum():
        raise ValueError('Use a fresh alphanumeric attempt.')
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260911'
    destination = intake / ('annular-canonical-gr-boundary-reference-' + arguments.attempt)
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': {}, 'outputs': {}, 'checks': [], 'valid_for_physics_claim': False, 'interval_certificate': False, 'new_evolution': False, 'finite_initial_system_solved': False, 'scope': 'Constructive GR-plus-canonical-scalar initial first jet, piecewise smooth source profiles; analytic linear radial constraint and algebraic outer clock normalization. Independent reference, not a GR-versus-MTS win or a solution of the previous finite Cdot equations. No Gram force has been dropped from an MTS calculation.'}

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = digest(path)

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        if not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    def save():
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

    save()
    try:
        path = Path(__file__).resolve()
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
        snapshot = destination / ('executed-' + path.name)
        snapshot.write_bytes(path.read_bytes())
        own(snapshot, 'outputs')
        prior_path = intake / 'annular-canonical-inverse-boundary-attempt01/status.json'
        own(prior_path)
        prior = json.loads(prior_path.read_text())
        check('paired_inverse_attempt_complete', prior['state'] == 'complete' and all(row['passed'] for row in prior['checks']))
        source_path = root / 'source-intake/navier-stokes/20260910/annular-parent-root-residence-attempt02/canonical_N16_GR_sample0.npz'
        own(source_path)
        with numerical.load(source_path, allow_pickle=False) as source:
            basis = MixedActionBasis(source['basis_radii'])
            configuration = source['original_configuration'].copy()
            packed = (source['initial_root_box_lower'] + source['initial_root_box_upper']) / 2
            outer_clock = float(source['affine_clock'][0])
        coarse_path = intake / 'annular-canonical-initial-data-nodal01/canonical_N16_GR_sample0.npz'
        own(coarse_path)
        with numerical.load(coarse_path, allow_pickle=False) as source:
            boundary_drive = source['boundary_velocity'].copy()
        for path in [source_path, coarse_path]:
            check(path.stem + '_matches_inherited_hash', digest(path) == prior['inputs'][str(path.relative_to(root))])
        count, face_count = basis.radii.size, basis.faces.size
        original_mass = packed[:face_count]
        original_lapse = packed[face_count:face_count + count]
        original_velocity = packed[face_count + count:]
        inner_radius, outer_radius = basis.radii[[0, -1]]
        inner_mass = original_mass[0]
        inner_geometry = 1 - 2 * inner_mass / inner_radius
        scalar_slopes = basis.derivative @ configuration[:count] + configuration[count:] / basis.spacing
        velocity_slopes = basis.derivative @ original_velocity[:count] + original_velocity[count:] / basis.spacing
        inner_velocity = boundary_drive[0] / (.1 * inner_radius**2 * inner_geometry * scalar_slopes[0])
        velocity_change = inner_velocity - original_velocity[0]

        def hermite(points, nodal_values, nodal_slopes):
            points = numerical.asarray(points)
            left = numerical.clip(numerical.searchsorted(basis.radii, points, side='right') - 1, 0, count - 2)
            width = basis.radii[left + 1] - basis.radii[left]
            fraction = (points - basis.radii[left]) / width
            values = (2 * fraction**3 - 3 * fraction**2 + 1) * nodal_values[left] + (-2 * fraction**3 + 3 * fraction**2) * nodal_values[left + 1]
            values += width * ((fraction**3 - 2 * fraction**2 + fraction) * nodal_slopes[left] + (fraction**3 - fraction**2) * nodal_slopes[left + 1])
            gradients = (6 * fraction**2 - 6 * fraction) * (nodal_values[left] - nodal_values[left + 1]) / width
            gradients += (3 * fraction**2 - 4 * fraction + 1) * nodal_slopes[left] + (3 * fraction**2 - 2 * fraction) * nodal_slopes[left + 1]
            seconds = (12 * fraction - 6) * (nodal_values[left] - nodal_values[left + 1]) / width**2
            seconds += ((6 * fraction - 4) * nodal_slopes[left] + (6 * fraction - 2) * nodal_slopes[left + 1]) / width
            return values, gradients, seconds

        def free_fields(points):
            points = numerical.asarray(points)
            scalar, gradient, second = hermite(points, configuration[:count], scalar_slopes)
            velocity, velocity_r, unused_second = hermite(points, original_velocity[:count], velocity_slopes)
            fraction = (points - inner_radius) / (outer_radius - inner_radius)
            velocity += velocity_change * (1 - 3 * fraction**2 + 2 * fraction**3)
            velocity_r += velocity_change * (-6 * fraction + 6 * fraction**2) / (outer_radius - inner_radius)
            left = numerical.clip(numerical.searchsorted(basis.radii, points, side='right') - 1, 0, count - 2)
            lapse_r = (original_lapse[left + 1] - original_lapse[left]) / (basis.radii[left + 1] - basis.radii[left])
            lapse = original_lapse[left] + lapse_r * (points - basis.radii[left])
            return {'chi': scalar, 'w': gradient, 'w_r': second, 'q': velocity, 'q_r': velocity_r, 'N_seed': lapse, 'N_seed_r': lapse_r}

        scalar_value, scalar_gradient = canonical_maps(basis)
        direct = hermite(basis.quadrature, configuration[:count], scalar_slopes)
        check('independent_source_Hermite_reconstruction', max(abs(direct[0] - scalar_value @ configuration).max(), abs(direct[1] - scalar_gradient @ configuration).max()) < 1e-11)
        endpoints = free_fields(numerical.array([inner_radius, outer_radius]))
        check('inverse_inner_and_original_outer_scalar_drives', abs(endpoints['q'][0] - inner_velocity) < 1e-15 and abs(endpoints['q'][1] - boundary_drive[2]) < 1e-14)
        check('smooth_global_lift_has_zero_endpoint_gradient_changes', abs(endpoints['q_r'][0] - velocity_slopes[0]) < 1e-12 and abs(endpoints['q_r'][1] - velocity_slopes[-1]) < 1e-12)

        radius, mass, mass_r, lapse, lapse_r, momentum, momentum_r, gradient, gradient_r, kappa = symbolic.symbols('R m mr N Nr pi pir w wr kappa', positive=True)
        geometry = 1 - 2 * mass / radius

        def radial_derivative(expression):
            return symbolic.diff(expression, radius) + symbolic.diff(expression, mass) * mass_r + symbolic.diff(expression, lapse) * lapse_r + symbolic.diff(expression, momentum) * momentum_r + symbolic.diff(expression, gradient) * gradient_r

        energy = momentum**2 / (2 * radius**2) + radius**2 * gradient**2 / 2
        scalar_velocity = lapse * symbolic.sqrt(geometry) * momentum / radius**2
        mass_velocity = kappa * lapse * geometry**symbolic.Rational(3, 2) * momentum * gradient
        geometric_rate = lapse * energy / (radius * symbolic.sqrt(geometry)) - lapse_r / (kappa * symbolic.sqrt(geometry)) + lapse * mass / (kappa * radius**2 * geometry**symbolic.Rational(3, 2))
        scalar_rate = radial_derivative(lapse * symbolic.sqrt(geometry) * radius**2 * gradient)
        constraint_rate = radial_derivative(mass_velocity) / (kappa * symbolic.sqrt(geometry))
        constraint_rate += (mass_r / (kappa * radius * geometry**symbolic.Rational(3, 2)) + energy / (radius * symbolic.sqrt(geometry))) * mass_velocity
        constraint_rate -= symbolic.sqrt(geometry) * momentum * scalar_rate / radius**2 + radius**2 * symbolic.sqrt(geometry) * gradient * radial_derivative(scalar_velocity)
        constraint_rate -= kappa * geometry**symbolic.Rational(3, 2) * momentum * gradient * geometric_rate
        check('exact_off_shell_P0_GR_constraint_rate_cancellation', symbolic.simplify(constraint_rate) == 0)
        independent_q = symbolic.symbols('q', real=True)
        mass_rhs = kappa * geometry * energy.subs(momentum, radius**2 * independent_q / (lapse * symbolic.sqrt(geometry)))
        check('exact_linear_radial_mass_equation', symbolic.simplify(mass_rhs + kappa * radius * gradient**2 * mass - kappa * radius**2 * (independent_q**2 / lapse**2 + gradient**2) / 2) == 0)

        rules = {order: numerical.polynomial.legendre.leggauss(order) for order in [4, 8, 12, 16]}
        knots = numerical.unique(numerical.concatenate([basis.radii, basis.faces]))

        def ode_coefficients(points):
            data = free_fields(points)
            return .1 * points * data['w']**2, .05 * points**2 * data['w']**2, .05 * points**2 * data['q']**2 / data['N_seed']**2

        def advance(left, right, state, order):
            if right == left:
                return numerical.asarray(state).copy()
            nodes, weights = rules[order]
            points = (left + right) / 2 + (right - left) / 2 * nodes
            primitive_nodes, primitive_weights = rules[4]
            nested = left + (points[:, None] - left) * (primitive_nodes[None, :] + 1) / 2
            primitive = (points - left) / 2 * (ode_coefficients(nested.ravel())[0].reshape(nested.shape) @ primitive_weights)
            end_points = (left + right) / 2 + (right - left) / 2 * primitive_nodes
            end_primitive = (right - left) / 2 * (primitive_weights @ ode_coefficients(end_points)[0])
            unused_p, source_a, source_b = ode_coefficients(points)
            integrals = (right - left) / 2 * numerical.array([weights @ (numerical.exp(primitive) * source_a), weights @ (numerical.exp(primitive) * source_b)])
            return numerical.exp(-end_primitive) * (state + integrals)

        paths = {}
        for order in [8, 12, 16]:
            values = [numerical.array([inner_mass, 0.])]
            for left, right in zip(knots[:-1], knots[1:]):
                values.append(advance(left, right, values[-1], order))
            paths[order] = numerical.array(values)
        check('radial_integrating_factor_quadrature_control', max(abs(paths[8] - paths[16]).max(), abs(paths[12] - paths[16]).max()) < 1e-12)
        ode_values = [numerical.array([inner_mass, 0.])]
        for left, right in zip(knots[:-1], knots[1:]):
            def right_hand_side(position, state):
                multiplier, source_a, source_b = ode_coefficients(numerical.array([position]))
                return numerical.array([source_a[0], source_b[0]]) - multiplier[0] * state
            solved = solve_ivp(right_hand_side, (left, right), ode_values[-1], method='DOP853', rtol=2e-12, atol=2e-14)
            if not solved.success:
                raise RuntimeError(solved.message)
            ode_values.append(solved.y[:, -1])
        independent_error = float(abs(numerical.array(ode_values) - paths[16]).max())
        check('independent_DOP853_radial_solution_control', independent_error < 1e-11, independent_error)
        final_a, final_b = paths[16][-1]
        clock_factor = outer_clock**2 / original_lapse[-1]**2
        geometry_a = 1 - 2 * final_a / outer_radius
        discriminant = (clock_factor * geometry_a)**2 - 8 * clock_factor * final_b / outer_radius
        check('positive_clock_discriminant', discriminant > 0, float(discriminant))
        scale_squared = (clock_factor * geometry_a + numerical.sqrt(discriminant)) / 2
        small_root = 2 * clock_factor * final_b / (outer_radius * scale_squared)
        sigma = numerical.sqrt(scale_squared)
        sample_points = numerical.sort(numerical.concatenate([knots, (knots[:-1] + knots[1:]) / 2, (3 * knots[:-1] + knots[1:]) / 4, (knots[:-1] + 3 * knots[1:]) / 4]))
        sampled_ab = []
        for point in sample_points:
            segment = min(numerical.searchsorted(knots, point, side='right') - 1, knots.size - 2)
            sampled_ab.append(advance(knots[segment], point, paths[16][segment], 16))
        sampled_ab = numerical.array(sampled_ab)
        data = free_fields(sample_points)
        radial_mass = sampled_ab[:, 0] + sampled_ab[:, 1] / scale_squared
        small_mass = sampled_ab[:, 0] + sampled_ab[:, 1] / small_root
        spatial_f = 1 - 2 * radial_mass / sample_points
        small_f = 1 - 2 * small_mass / sample_points
        lapse_value = sigma * data['N_seed']
        lapse_gradient = sigma * data['N_seed_r']
        pi = sample_points**2 * data['q'] / (lapse_value * numerical.sqrt(spatial_f))
        energy_value = pi**2 / (2 * sample_points**2) + sample_points**2 * data['w']**2 / 2
        multiplier, source_a, source_b = ode_coefficients(sample_points)
        radial_mass_r = source_a + source_b / scale_squared - multiplier * radial_mass
        geometry_r = -2 * radial_mass_r / sample_points + 2 * radial_mass / sample_points**2
        mass_time = .1 * sample_points**2 * spatial_f * data['q'] * data['w']
        mass_time_r = .1 * ((2 * sample_points * spatial_f + sample_points**2 * geometry_r) * data['q'] * data['w'] + sample_points**2 * spatial_f * (data['q_r'] * data['w'] + data['q'] * data['w_r']))
        momentum_time = lapse_value * energy_value / (sample_points * numerical.sqrt(spatial_f)) - lapse_gradient / (.1 * numerical.sqrt(spatial_f)) + lapse_value * radial_mass / (.1 * sample_points**2 * spatial_f**1.5)
        pi_time = (lapse_gradient * numerical.sqrt(spatial_f) + lapse_value * geometry_r / (2 * numerical.sqrt(spatial_f))) * sample_points**2 * data['w'] + lapse_value * numerical.sqrt(spatial_f) * (2 * sample_points * data['w'] + sample_points**2 * data['w_r'])
        constraint = radial_mass_r / (.1 * numerical.sqrt(spatial_f)) - numerical.sqrt(spatial_f) * energy_value
        rate = mass_time_r / (.1 * numerical.sqrt(spatial_f)) + (radial_mass_r / (.1 * sample_points * spatial_f**1.5) + energy_value / (sample_points * numerical.sqrt(spatial_f))) * mass_time
        rate -= numerical.sqrt(spatial_f) * pi * pi_time / sample_points**2 + sample_points**2 * numerical.sqrt(spatial_f) * data['w'] * data['q_r'] + .1 * spatial_f**1.5 * pi * data['w'] * momentum_time
        clock_gap = lapse_value[-1] / numerical.sqrt(spatial_f[-1]) - outer_clock
        inner_flux_gap = mass_time[0] - boundary_drive[0]
        check('large_root_positive_sampled_chart', spatial_f.min() > .1 and lapse_value.min() > .1)
        check('small_root_rejected_by_declared_outer_chart_not_fit_quality', small_f[-1] < .1)
        check('constructed_constraint_and_rate', abs(constraint).max() < 1e-12 and abs(rate).max() < 1e-12, {'constraint': float(abs(constraint).max()), 'rate': float(abs(rate).max())})
        check('constructed_boundary_flux_and_clock', abs(clock_gap) < 1e-13 and abs(inner_flux_gap) < 1e-15)
        report['result'] = {'inner_mass_drive': float(boundary_drive[0]), 'inner_scalar_velocity': float(inner_velocity), 'old_inner_scalar_velocity': float(original_velocity[0]), 'velocity_change': float(velocity_change), 'outer_clock': outer_clock, 'outer_clock_gap': float(clock_gap), 'inner_flux_gap': float(inner_flux_gap), 'scale_squared': float(scale_squared), 'lapse_scale': float(sigma), 'small_clock_root': float(small_root), 'small_root_outer_F': float(small_f[-1]), 'clock_discriminant': float(discriminant), 'minimum_sampled_F': float(spatial_f.min()), 'minimum_sampled_lapse': float(lapse_value.min()), 'constraint_max': float(abs(constraint).max()), 'constraint_rate_max': float(abs(rate).max()), 'independent_integrator_error': independent_error, 'radial_quadrature_difference': float(abs(paths[12] - paths[16]).max()), 'free_velocity_lift': 'q=q_original+(q_inner_required-q_original_inner)*(1-3x^2+2x^3), x normalized across the entire original annulus; fixed physical width, no grid-sized layer.', 'clock_branch_rule': 'Larger positive root continuously connected to finite positive lapse at zero scalar velocity; smaller root also reported and rejected by F_out>.1 chart.', 'regularity_scope': 'Piecewise smooth initial first jet. Source Hermite chi/q are C1; source lapse is positive continuous P1. Global smooth/classical spacetime existence and higher boundary jets not proved.'}
        arrays = {'radii': sample_points, 'mass': radial_mass, 'mass_r': radial_mass_r, 'mass_time': mass_time, 'momentum_time': momentum_time, 'pi': pi, 'pi_time': pi_time, 'lapse': lapse_value, 'F': spatial_f, 'constraint': constraint, 'constraint_rate': rate, 'knots': knots, 'ab_order8': paths[8], 'ab_order12': paths[12], 'ab_order16': paths[16], 'ab_DOP853': numerical.array(ode_values), 'configuration': configuration, 'original_packed': packed, 'boundary_drive': boundary_drive}
        arrays.update(data)
        check('all_reference_arrays_finite', all(numerical.all(numerical.isfinite(value)) for value in arrays.values()))
        output = destination / 'constructed_GR_first_jet.npz'
        numerical.savez_compressed(output, **arrays)
        with numerical.load(output, allow_pickle=False) as saved:
            check('reference_archive_roundtrip', set(saved.files) == set(arrays) and all(numerical.array_equal(value, saved[name]) for name, value in arrays.items()))
        own(output, 'outputs')
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
        print(json.dumps(report['result']), flush=True)
    except Exception as error:
        report['state'] = 'failed'
        report['error'] = repr(error)
        save()
        raise


if __name__ == '__main__':
    run()
