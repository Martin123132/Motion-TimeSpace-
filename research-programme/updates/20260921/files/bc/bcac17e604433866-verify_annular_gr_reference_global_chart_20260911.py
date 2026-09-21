import hashlib
import json
from fractions import Fraction
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    from annular_adm_mixed_action_20260909 import MixedActionBasis

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260911'
    destination = intake / 'annular-canonical-gr-reference-global-chart.json'
    if destination.exists():
        raise FileExistsError(destination)
    report = {'state': 'running', 'inputs': {}, 'outputs': {}, 'checks': [], 'valid_for_physics_claim': False, 'new_evolution': False, 'interval_spacetime_certificate': False, 'scope': 'Exact rational coefficient bounds proving the integrating-factor GR reference has a large-clock-root solution with F>.1 everywhere on the original annulus. Exact Hermite polynomial with stored binary nodal values/slopes, exact kappa=1/10 and exactly derived rational inner q. Numerical reference quadrature values are not enclosed; spacetime evolution and the finite canonical system are not certified.'}

    def own(path):
        report['inputs'][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    def check(name, passed):
        report['checks'].append({'name': name, 'passed': bool(passed)})
        if not passed:
            raise RuntimeError(name)

    def exact(value):
        return Fraction.from_float(float(value))

    def record(value):
        return {'numerator': str(value.numerator), 'denominator': str(value.denominator), 'approximation': float(value)}

    own(Path(__file__))
    compile(Path(__file__).read_bytes(), __file__, 'exec')
    source_path = root / 'source-intake/navier-stokes/20260910/annular-parent-root-residence-attempt02/canonical_N16_GR_sample0.npz'
    own(source_path)
    with numerical.load(source_path, allow_pickle=False) as saved:
        basis = MixedActionBasis(saved['basis_radii'])
        outer_clock = exact(saved['affine_clock'][0])
    reference_path = intake / 'annular-canonical-gr-boundary-reference-attempt01/constructed_GR_first_jet.npz'
    own(reference_path)
    with numerical.load(reference_path, allow_pickle=False) as saved:
        configuration = saved['configuration'].copy()
        packed = saved['original_packed'].copy()
        drive = exact(saved['boundary_drive'][0])
    count, face_count = basis.radii.size, basis.faces.size
    lapse = [exact(value) for value in packed[face_count:face_count + count]]
    velocity = packed[face_count + count:]
    scalar_slopes_float = basis.derivative @ configuration[:count] + configuration[count:] / basis.spacing
    velocity_slopes_float = basis.derivative @ velocity[:count] + velocity[count:] / basis.spacing
    scalar_slopes = [exact(value) for value in scalar_slopes_float]
    velocity_slopes = [exact(value) for value in velocity_slopes_float]
    radii = [exact(value) for value in basis.radii]
    inner_radius, outer_radius = radii[0], radii[-1]
    length = outer_radius - inner_radius
    inner_mass = exact(packed[0])
    inner_f = 1 - 2 * inner_mass / inner_radius
    kappa = Fraction(1, 10)
    required_velocity = drive / (kappa * inner_radius**2 * inner_f * scalar_slopes[0])
    delta_velocity = required_velocity - exact(velocity[0])
    gradient_bounds = []
    velocity_bounds = []
    for index in range(count - 1):
        width = radii[index + 1] - radii[index]
        gradient_bounds.extend([abs(scalar_slopes[index]), abs(3 * (exact(configuration[index + 1]) - exact(configuration[index])) / width - scalar_slopes[index] - scalar_slopes[index + 1]), abs(scalar_slopes[index + 1])])
        velocity_bounds.extend([abs(exact(velocity[index])), abs(exact(velocity[index]) + width * velocity_slopes[index] / 3), abs(exact(velocity[index + 1]) - width * velocity_slopes[index + 1] / 3), abs(exact(velocity[index + 1]))])
    gradient_upper = max(gradient_bounds)
    velocity_upper = max(velocity_bounds) + abs(delta_velocity)
    lapse_lower = min(lapse)
    check('positive_source_chart_and_mass_barrier', inner_radius > 0 and 0 <= inner_mass < inner_radius / 2 and lapse_lower > 0 and outer_clock > 0)
    upper_a = inner_mass + kappa * outer_radius**2 * gradient_upper**2 * length / 2
    upper_b = kappa * outer_radius**2 * velocity_upper**2 * length / (2 * lapse_lower**2)
    geometry_a_lower = 1 - 2 * upper_a / outer_radius
    clock_factor = outer_clock**2 / lapse[-1]**2
    discriminant_lower = clock_factor**2 * geometry_a_lower**2 - 8 * clock_factor * upper_b / outer_radius
    scale_squared_lower = clock_factor * geometry_a_lower / 2
    check('positive_large_clock_root_exists', geometry_a_lower > 0 and discriminant_lower > 0 and scale_squared_lower > 0)
    mass_upper = upper_a + upper_b / scale_squared_lower
    global_geometry_lower = 1 - 2 * mass_upper / inner_radius
    global_lapse_squared_lower = scale_squared_lower * lapse_lower**2
    check('entire_annulus_F_above_declared_chart', global_geometry_lower > Fraction(1, 10))
    check('entire_annulus_N_above_declared_chart', global_lapse_squared_lower > Fraction(1, 100))
    check('exact_inverse_inner_flux', kappa * inner_radius**2 * inner_f * required_velocity * scalar_slopes[0] == drive)
    report['bounds'] = {name: record(value) for name, value in {'gradient_absolute_upper': gradient_upper, 'velocity_absolute_upper': velocity_upper, 'seed_lapse_lower': lapse_lower, 'A_upper': upper_a, 'B_upper': upper_b, 'Fa_lower': geometry_a_lower, 'clock_discriminant_lower': discriminant_lower, 'large_scale_squared_lower': scale_squared_lower, 'mass_global_upper': mass_upper, 'F_global_lower': global_geometry_lower, 'N_squared_global_lower': global_lapse_squared_lower, 'exact_required_inner_velocity': required_velocity}.items()}
    report['proof'] = ['Quadratic Bernstein coefficients bound w on every Hermite segment; cubic Bernstein coefficients bound q_original. The global lift 1-3x^2+2x^3 lies in [0,1].', 'p=kappa*R*w^2>=0. A_prime=p*(R/2-A), A(in)=m_in, implies 0<=A<=R/2 and A<=m_in+kappa*Rout^2*W^2*length/2.', 'B_prime=b0-p*B, B(in)=0, b0=kappa*R^2*q^2/(2*Nseed^2)>=0, implies 0<=B<=kappa*Rout^2*Q^2*length/(2*Nseed_min^2).', 'Positive discriminant lower bound gives a positive large root y; y>=K*Fa_lower/2. Then m=A+B/y<=mass_global_upper and F=1-2m/R>=1-2*mass_global_upper/Rin.', 'These inequalities enclose the exact formula-defined reference, not rounding errors of its numerical samples and not any finite-dimensional root.']
    report['state'] = 'complete'
    destination.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({name: record['approximation'] for name, record in report['bounds'].items()}), flush=True)


if __name__ == '__main__':
    run()
