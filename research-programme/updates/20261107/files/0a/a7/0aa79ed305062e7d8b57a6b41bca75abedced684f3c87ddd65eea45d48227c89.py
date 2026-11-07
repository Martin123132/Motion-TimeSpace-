from __future__ import annotations

import hashlib
import json
from pathlib import Path

import psutil
import sympy as sp


ROOT = Path(__file__).resolve().parent


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/derivation'
    output.mkdir(parents=True, exist_ok=False)
    checks = []

    def exact(name, expression):
        remainder = sp.factor(expression)
        assert remainder == 0, (name, remainder)
        checks.append({'name': name, 'passed': True})

    radius, alpha, mass, kinetic, potential = sp.symbols('radius alpha mass kinetic potential', positive=True)
    metric = 1-2*alpha*mass/radius
    density = metric*kinetic/2+potential
    pressure = metric*kinetic/2-potential
    mass_prime = radius**2*density
    metric_prime = 2*alpha*(mass/radius**2-radius*density)
    lapse_log_prime = alpha*(mass+radius**3*pressure)/(radius**2*metric)
    exact('linear_mass_constraint', mass_prime+alpha*radius*kinetic*mass-radius**2*(kinetic/2+potential))
    exact('integrating_factor_is_lapse_over_sqrtF', lapse_log_prime-metric_prime/(2*metric)-alpha*radius*kinetic)
    parameter = sp.Symbol('parameter')
    delta_mass, second_mass, delta_kinetic, second_kinetic, delta_potential, second_potential = sp.symbols(
        'delta_mass second_mass delta_kinetic second_kinetic delta_potential second_potential')
    trial_mass = mass+parameter*delta_mass+parameter**2*second_mass/2
    trial_kinetic = kinetic+parameter*delta_kinetic+parameter**2*second_kinetic/2
    trial_potential = potential+parameter*delta_potential+parameter**2*second_potential/2
    source = radius**2*((1-2*alpha*trial_mass/radius)*trial_kinetic/2+trial_potential)
    first_source = radius**2*(metric*delta_kinetic/2+delta_potential)-alpha*radius*kinetic*delta_mass
    second_source = radius**2*(metric*second_kinetic/2+second_potential)-alpha*radius*kinetic*second_mass-2*alpha*radius*delta_kinetic*delta_mass
    exact('first_constraint_variation', sp.diff(source, parameter).subs(parameter, 0)-first_source)
    exact('second_constraint_variation_cross_term', sp.diff(source, parameter, 2).subs(parameter, 0)-second_source)
    amplitude, gradient, momentum, amplitude_shift, phase_shift, grad_shift, phase_grad, momentum_u, momentum_v = sp.symbols(
        'amplitude gradient momentum amplitude_shift phase_shift grad_shift phase_grad momentum_u momentum_v', real=True)
    trial_cartesian_kinetic = (gradient+parameter*grad_shift)**2+(parameter*phase_grad)**2
    trial_cartesian_kinetic += ((parameter*momentum_u)**2+(momentum+parameter*momentum_v)**2)/radius**4
    exact('cartesian_first_kinetic_variation', sp.diff(trial_cartesian_kinetic, parameter).subs(parameter, 0)-2*gradient*grad_shift-2*momentum*momentum_v/radius**4)
    exact('cartesian_second_kinetic_variation', sp.diff(trial_cartesian_kinetic, parameter, 2)-2*(grad_shift**2+phase_grad**2+(momentum_u**2+momentum_v**2)/radius**4))
    trial_charge = (amplitude+parameter*amplitude_shift)*(momentum+parameter*momentum_v)-parameter**2*phase_shift*momentum_u
    exact('charge_tangent', sp.diff(trial_charge, parameter).subs(parameter, 0)-amplitude*momentum_v-momentum*amplitude_shift)
    exact('charge_second_variation', sp.diff(trial_charge, parameter, 2)-2*(amplitude_shift*momentum_v-phase_shift*momentum_u))
    positive_amplitude = sp.Symbol('positive_amplitude', positive=True)
    potential_formula = sp.Rational(3, 8)*positive_amplitude**sp.Rational(4, 3)+positive_amplitude**4/8
    exact('potential_second_derivative', sp.diff(potential_formula, positive_amplitude, 2)-positive_amplitude**sp.Rational(-2, 3)/6-sp.Rational(3, 2)*positive_amplitude**2)
    exact('transverse_potential_second_derivative', sp.diff(potential_formula, positive_amplitude)/positive_amplitude-positive_amplitude**sp.Rational(-2, 3)/2-positive_amplitude**2/2)
    xi, metric_value, metric_derivative, frequency, force, force_second = sp.symbols('xi metric_value metric_derivative frequency force force_second')
    coefficient = xi*metric_value
    coefficient_derivative = alpha*radius*kinetic*coefficient+xi*metric_derivative
    field_gradients = sp.symbols('field_gradient_a field_gradient_b')
    field_seconds = sp.symbols('field_second_a field_second_b')
    momenta = sp.symbols('momentum_a momentum_b')
    momentum_derivatives = sp.symbols('momentum_prime_a momentum_prime_b')
    forces = sp.symbols('force_a force_b')
    kinetic_time = 0
    potential_time = 0
    flux_product = 0
    flux_product_derivative = 0
    for field_gradient, field_second, field_momentum, momentum_prime, field_force in zip(
            field_gradients, field_seconds, momenta, momentum_derivatives, forces):
        field_time_derivative = coefficient*field_momentum/radius**2
        field_gradient_time = (coefficient_derivative*field_momentum+coefficient*momentum_prime)/radius**2-2*coefficient*field_momentum/radius**3
        momentum_time = (coefficient_derivative*radius**2+2*coefficient*radius)*field_gradient+coefficient*radius**2*field_second-xi*radius**2*field_force
        kinetic_time += 2*field_gradient*field_gradient_time+2*field_momentum*momentum_time/radius**4
        potential_time += field_force*field_time_derivative
        flux_product += field_momentum*field_gradient
        flux_product_derivative += momentum_prime*field_gradient+field_momentum*field_second
    flux = metric_value*coefficient*flux_product
    flux_prime = (metric_derivative*coefficient+metric_value*coefficient_derivative)*flux_product+metric_value*coefficient*flux_product_derivative
    exact('Hamiltonian_flow_preserves_mass_constraint', flux_prime+alpha*radius*kinetic*flux-radius**2*(metric_value*kinetic_time/2+potential_time))
    odd_local = coefficient*radius**2*phase_grad**2+coefficient*momentum_u**2/radius**2+xi*radius**2*force*phase_shift**2/amplitude+2*frequency*phase_shift*momentum_u
    odd_square = coefficient*radius**2*phase_grad**2+(xi*radius**2*force/amplitude-frequency**2*radius**2/coefficient)*phase_shift**2
    odd_square += coefficient/radius**2*(momentum_u+frequency*radius**2*phase_shift/coefficient)**2
    exact('odd_block_complete_square', odd_local-odd_square)
    test_ratio, ratio_prime, weight, weight_prime = sp.symbols('test_ratio ratio_prime weight weight_prime')
    amplitude_second = (xi*radius**2*force-frequency**2*radius**2*amplitude/coefficient-weight_prime*gradient)/weight
    phase_potential = xi*radius**2*force/amplitude-frequency**2*radius**2/coefficient
    phase_density = weight*(gradient*test_ratio+amplitude*ratio_prime)**2+phase_potential*amplitude**2*test_ratio**2
    boundary_derivative = (weight_prime*amplitude*gradient+weight*gradient**2+weight*amplitude*amplitude_second)*test_ratio**2+2*weight*amplitude*gradient*test_ratio*ratio_prime
    exact('phase_ground_state_transform', phase_density-weight*amplitude**2*ratio_prime**2-boundary_derivative)
    inertia, overlap = sp.symbols('inertia overlap', positive=True)
    flat_momentum_residual = -2*frequency*overlap/inertia
    exact('fixed_charge_flat_rank_coefficient', inertia*flat_momentum_residual**2-4*frequency**2*overlap**2/inertia)
    edge_distance, edge_metric = sp.symbols('edge_distance edge_metric', positive=True)
    edge_amplitude = edge_distance**3/(12*edge_metric)**sp.Rational(3, 2)
    exact('amplitude_endpoint_inverse_square', edge_amplitude**sp.Rational(-2, 3)/6-2*edge_metric/edge_distance**2)
    exact('phase_endpoint_inverse_square', edge_amplitude**sp.Rational(-2, 3)/2-6*edge_metric/edge_distance**2)
    real_growth, phase_growth, laplacian_real, laplacian_phase = sp.symbols('real_growth phase_growth laplacian_real laplacian_phase')
    flat_momentum_u = radius**2*(real_growth-frequency*phase_shift)
    flat_momentum_v = radius**2*(phase_growth+frequency*amplitude_shift)
    flat_momentum_u_time = radius**2*(laplacian_real-force_second*amplitude_shift)+frequency*flat_momentum_v
    flat_momentum_v_time = radius**2*(laplacian_phase-force*phase_shift/amplitude)-frequency*flat_momentum_u
    exact('flat_real_gyroscopic_equation', flat_momentum_u_time/radius**2+frequency*phase_growth
          -(laplacian_real-(force_second-frequency**2)*amplitude_shift+2*frequency*phase_growth))
    exact('flat_phase_gyroscopic_equation', flat_momentum_v_time/radius**2-frequency*real_growth
          -(laplacian_phase-(force/amplitude-frequency**2)*phase_shift-2*frequency*real_growth))
    parent = ROOT.parent/'self-gravity-20261003/results/stage-integrity.json'
    report = {'state': 'complete', 'checks': checks, 'exact_check_count': len(checks),
              'parent_seal_sha256': hashlib.sha256(parent.read_bytes()).hexdigest(),
              'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'scope': 'Algebraic identities supporting the derivation; not a theorem about the continuum spectrum.',
              'radial_metric_response_retained': True, 'phase_block_ground_state_identity': True,
              'fixed_charge_flat_limit_derived': True}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'exact_checks': len(checks)}))


if __name__ == '__main__':
    main()
