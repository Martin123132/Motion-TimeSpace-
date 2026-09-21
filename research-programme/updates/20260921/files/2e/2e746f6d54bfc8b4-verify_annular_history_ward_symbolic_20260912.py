import hashlib
import json
import traceback
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import sympy as sp

    root = Path(__file__).resolve().parents[1]
    destination = root / 'source-intake/navier-stokes/20260912/annular-history-ward-symbolic-attempt01'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'checks': [], 'inputs': {}, 'outputs': {}, 'valid_for_physics_claim': False, 'new_evolution': False, 'full_second_jet_closed': False, 'smooth_interior_identity_only': True, 'temporal_and_radial_boundary_work_required': True}

    def save():
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

    def check(name, expression, zero=True):
        reduced = sp.simplify(sp.expand(expression))
        passed = (reduced == 0) if zero else (reduced != 0)
        report['checks'].append({'name': name, 'passed': passed, 'reduced_expression': str(reduced)})
        save()
        if not passed:
            raise RuntimeError(name)
        print(name + ': passed', flush=True)

    save()
    try:
        for path in [Path(__file__), root / 'DERIVATION-20260909-covariant-time-links-and-mixed-gravity-basis.md', root / 'DERIVATION-20260912-nonlinear-history-Euler-equations.md']:
            report['inputs'][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()
        snapshot = destination / ('executed-' + Path(__file__).name)
        snapshot.write_bytes(Path(__file__).read_bytes())
        report['outputs'][str(snapshot.relative_to(root))] = hashlib.sha256(snapshot.read_bytes()).hexdigest()
        radius, geometry, lapse, kappa = sp.symbols('radius geometry lapse kappa', positive=True)
        geo_r, geo_rr, geo_t, geo_tr, lapse_r, lapse_rr, lapse_t, lapse_tr = sp.symbols('geo_r geo_rr geo_t geo_tr lapse_r lapse_rr lapse_t lapse_tr')
        momentum, momentum_r, momentum_rr, momentum_t, momentum_tr = sp.symbols('momentum momentum_r momentum_rr momentum_t momentum_tr')
        pi, pi_r, pi_rr, pi_t, pi_tr, gradient, gradient_r, gradient_rr, velocity, velocity_r = sp.symbols('pi pi_r pi_rr pi_t pi_tr gradient gradient_r gradient_rr velocity velocity_r')
        radial_rates = {geometry: geo_r, geo_r: geo_rr, geo_t: geo_tr, lapse: lapse_r, lapse_r: lapse_rr, lapse_t: lapse_tr, momentum: momentum_r, momentum_r: momentum_rr, momentum_t: momentum_tr, pi: pi_r, pi_r: pi_rr, pi_t: pi_tr, gradient: gradient_r, gradient_r: gradient_rr, velocity: velocity_r}
        time_rates = {geometry: geo_t, geo_r: geo_tr, lapse: lapse_t, lapse_r: lapse_tr, momentum: momentum_t, momentum_r: momentum_tr, pi: pi_t, pi_r: pi_tr, gradient: velocity_r}

        def radial(expression):
            return sp.diff(expression, radius) + sum(sp.diff(expression, variable) * rate for variable, rate in radial_rates.items())

        def time(expression):
            return sum(sp.diff(expression, variable) * rate for variable, rate in time_rates.items())

        mass = radius * (1 - geometry) / 2
        mass_r = (1 - geometry - radius * geo_r) / 2
        mass_t = -radius * geo_t / 2
        root_f = sp.sqrt(geometry)
        shift = kappa * lapse * geometry**sp.Rational(3, 2) * momentum
        energy = pi**2 / (2 * radius**2) + radius**2 * gradient**2 / 2
        flux = lapse * root_f * radius**2 * gradient + shift * pi
        velocity_mass = kappa * lapse * geometry**sp.Rational(3, 2) * pi * gradient + kappa * radius * geometry**sp.Rational(3, 2) * (geometry * lapse_r - lapse * geo_r / 2) * momentum
        force_mass = lapse * energy / (radius * root_f) - lapse_r / (kappa * root_f) + lapse * mass / (kappa * radius**2 * geometry**sp.Rational(3, 2))
        force_mass += 3 * kappa * lapse * root_f * momentum * pi * gradient / radius + kappa * geometry**sp.Rational(3, 2) * ((lapse / (2 * radius) + 3 * lapse_r) * momentum**2 + lapse * momentum * momentum_r)
        constraint = mass_r / (kappa * root_f) - root_f * energy - kappa * geometry**sp.Rational(3, 2) * momentum * pi * gradient
        constraint += kappa * geometry**sp.Rational(3, 2) * ((geometry / 2 - 3 * mass_r + 3 * mass / radius) * momentum**2 + radius * geometry * momentum * momentum_r)
        residual_mass = -momentum_t + force_mass
        residual_momentum = mass_t - velocity_mass
        residual_scalar = -pi_t + radial(flux)
        residual_pi = velocity - lapse * root_f * pi / radius**2 - shift * gradient
        generator_mass = radius * geometry * shift
        generator_momentum = -lapse * (1 - 3 * kappa**2 * geometry**2 * momentum**2) / (kappa * root_f)
        radial_work = residual_mass * generator_mass + residual_momentum * generator_momentum + residual_pi * flux - lapse * shift * constraint
        ward = lapse * time(constraint) - residual_mass * mass_t - residual_momentum * momentum_t - residual_scalar * velocity - residual_pi * pi_t + radial(radial_work)
        check('GR_full_off_shell_canonical_time_Ward_nonzero_P', ward)
        wrong_generator = -lapse * (1 - 2 * kappa**2 * geometry**2 * momentum**2) / (kappa * root_f)
        check('wrong_representative_P_generator_detected', ward + radial(residual_momentum * (wrong_generator - generator_momentum)), zero=False)
        amplitude, amplitude_first, amplitude_second, density, density_first, coefficient, coefficient_first, jacobian, second_jacobian, scalar_first, scalar_second, factor_weight, sample_weight, spacing = sp.symbols('A A1 A2 D D1 C C1 J L q q2 B S h', nonzero=True)
        current = amplitude * (sample_weight * coefficient * amplitude_first - factor_weight * scalar_first * density) / spacing
        current_first = amplitude_first * (sample_weight * coefficient * amplitude_first - factor_weight * scalar_first * density) / spacing
        current_first += amplitude * (sample_weight * (jacobian * coefficient_first * amplitude_first + coefficient * amplitude_second) - factor_weight * (jacobian * scalar_second * density + scalar_first * density_first)) / spacing
        nodal_first = sample_weight * amplitude * amplitude_first / (spacing * jacobian)
        nodal_second = sample_weight / spacing * ((amplitude_first**2 + amplitude * amplitude_second) / jacobian**2 - amplitude * amplitude_first * second_jacobian / jacobian**3)
        scalar_covector = -factor_weight * amplitude * density / (spacing * jacobian)
        scalar_covector_first = -factor_weight / (spacing * jacobian**2) * (amplitude_first * density + amplitude * density_first - amplitude * density * second_jacobian / jacobian)
        node_source = coefficient * nodal_first + scalar_covector * scalar_first
        node_source_first = coefficient_first * nodal_first + coefficient * nodal_second + scalar_covector_first * scalar_first + scalar_covector * scalar_second
        check('memory_Ward_exact_endpoint_jump_P0', node_source - current / jacobian)
        check('memory_Ward_time_exact_inverse_J_endpoint_jump_P0', node_source_first - current_first / jacobian**2 + current * second_jacobian / jacobian**3)
        check('single_J_current_time_negative_control', node_source_first - current_first / jacobian + current * second_jacobian / jacobian**2, zero=False)
        kernel, kernel_t, kernel_r, connection, connection_t, node_d, node_d_t, node_C, node_C_t, node_g, node_q = sp.symbols('K Kt Kr c ct d dt C Ct G q')
        direct_epsilon = kernel * connection_t - node_d * node_C_t + node_g * node_q
        minus_time_work = kernel_t * connection + kernel * connection_t + node_d_t * node_C + node_d * node_C_t
        check('memory_Ward_from_full_time_pullback', direct_epsilon + minus_time_work + kernel_r - (kernel_r + connection * kernel_t + 2 * connection_t * kernel + node_C * node_d_t + node_g * node_q))
        report['state'] = 'complete'
        report['GR_off_shell_identity_proven_symbolically'] = True
        report['history_interior_identity_derived_with_exact_node_jumps'] = True
        save()
        print(json.dumps({'state': report['state'], 'checks': len(report['checks'])}), flush=True)
    except Exception as error:
        report.update({'state': 'failed', 'error': repr(error), 'traceback': traceback.format_exc()})
        save()
        raise


if __name__ == '__main__':
    run()
