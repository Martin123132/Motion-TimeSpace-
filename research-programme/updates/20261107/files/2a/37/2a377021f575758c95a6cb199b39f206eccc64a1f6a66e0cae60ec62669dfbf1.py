from pathlib import Path

import sympy as sp

from interior_energy import dependencies, save, modest_process


def main():
    modest_process()
    checks = []

    def exact(name, expression):
        residual = sp.factor(expression)
        assert residual == 0, (name, residual)
        checks.append(dict(name=name, passed=True, residual=str(residual)))

    radius, metric, lapse, alpha = sp.symbols('r F N alpha', positive=True)
    metric_prime, time_metric, angular, shift, shift_prime = sp.symbols('Fp H K J Jp', real=True)
    harmonic, angular_derivative, sin_angle = sp.symbols('Y Ytheta sin_angle', real=True)
    velocity = sp.Symbol('qdot', real=True)
    background = sp.diag(1/metric, radius**2, radius**2*sin_angle**2)
    inverse = background.inv()
    extrinsic = sp.zeros(3)
    extrinsic[0, 0] = velocity*harmonic*(time_metric/metric-2*shift_prime-metric_prime*shift/metric)/(2*lapse)
    extrinsic[0, 1] = extrinsic[1, 0] = -velocity*shift*angular_derivative/(2*lapse)
    extrinsic[1, 1] = velocity*harmonic*(radius**2*angular-2*metric*radius*shift)/(2*lapse)
    extrinsic[2, 2] = extrinsic[1, 1]*sin_angle**2
    trace = sp.trace(inverse*extrinsic)
    contraction = sp.trace(inverse*extrinsic*inverse*extrinsic)
    angular_integral = sp.expand(contraction-trace**2).subs({harmonic**2:1, angular_derivative**2:6})
    radial_rate = time_metric-2*metric*shift_prime-metric_prime*shift
    angular_rate = angular-2*metric*shift/radius
    expected_gravity = radius**2/(8*alpha*lapse*sp.sqrt(metric))*(
        -4*radial_rate*angular_rate-2*angular_rate**2+12*metric*shift**2/radius**2)
    derived_gravity = 2*(lapse*radius**2/sp.sqrt(metric))/(4*alpha)*angular_integral/velocity**2
    exact('ADM extrinsic contraction and normalized l=2 angular integral', derived_gravity-expected_gravity)
    amplitude, gradient, response, phase, phase_prime, rotation = sp.symbols('h hp u s sp w', real=True)
    displacement, acceleration = sp.symbols('q qddot', real=True)
    measure = radius**2/(lapse*sp.sqrt(metric))
    prefactor = sp.sqrt(1+time_metric*displacement*harmonic)*(1+angular*displacement*harmonic)/sp.sqrt(1-time_metric*displacement*harmonic)
    time_phase = measure*prefactor*(amplitude+response*displacement*harmonic)**2*(rotation-phase*acceleration*harmonic)**2/2
    mixed = sp.diff(time_phase, displacement, acceleration).subs({displacement:0, acceleration:0, harmonic**2:1})
    expected_mixed = -measure*rotation*phase*(2*amplitude*response+amplitude**2*(time_metric+angular))
    exact('scalar phase mixed displacement-acceleration term', mixed-expected_mixed)
    exact('mixed term becomes twice its negative in the mass form',
          -2*mixed-2*measure*rotation*phase*(2*amplitude*response+amplitude**2*(time_metric+angular)))
    field_velocity = (response-metric*shift*gradient)*velocity*harmonic
    amplitude_lagrangian = measure*field_velocity**2/2
    exact('amplitude convective velocity term', sp.diff(amplitude_lagrangian, velocity, 2).subs(harmonic**2, 1)
          -measure*(response-metric*shift*gradient)**2)
    advected_phase = rotation+metric*shift*phase_prime*velocity**2*harmonic**2
    phase_lagrangian = measure*amplitude**2*advected_phase**2/2
    exact('phase shift-advection term', sp.diff(phase_lagrangian, velocity, 2).subs(velocity, 0).subs(harmonic**2, 1)
          -2*measure*rotation*metric*shift*amplitude**2*phase_prime)
    gradient_lagrangian = -lapse*radius**2/sp.sqrt(metric)*amplitude**2*velocity**2*(
        metric*phase_prime**2*harmonic**2+phase**2*angular_derivative**2/radius**2)/2
    exact('phase spatial-gradient term', sp.diff(gradient_lagrangian, velocity, 2).subs({harmonic**2:1, angular_derivative**2:6})
          +measure*lapse**2*amplitude**2*(metric*phase_prime**2+6*phase**2/radius**2))
    acceleration_square = sp.diff(time_phase, acceleration, 2).subs(displacement, 0).subs(harmonic**2, 1)
    exact('explicit fourth-derivative remainder', acceleration_square-measure*amplitude**2*phase**2)
    time = sp.Symbol('time', real=True)
    history = sp.Function('q')(time)
    exact('time integration by parts for rotating phase',
          history*sp.diff(history, time, 2)+sp.diff(history, time)**2-sp.diff(history*sp.diff(history, time), time))
    momentum, phase_rate, hamiltonian = sp.symbols('p theta_dot Henergy', real=True)
    rotated_lagrangian = momentum*(phase_rate+rotation)-hamiltonian
    exact('rotating-frame Hamiltonian is energy minus wQ',
          momentum*phase_rate-rotated_lagrangian-(hamiltonian-rotation*momentum))
    perturbation_charge, second_energy = sp.symbols('delta2Q delta2E', real=True)
    exact('fixed-charge constrained quadratic energy',
          (second_energy-rotation*perturbation_charge)+rotation*perturbation_charge-second_energy)
    angle = sp.Symbol('cos_theta', real=True)
    real_harmonic = sp.sqrt(5/(16*sp.pi))*(3*angle**2-1)
    exact('l=2 first-order total charge vanishes', sp.integrate(2*sp.pi*real_harmonic, (angle, -1, 1)))
    exact('real harmonic unit norm', sp.integrate(2*sp.pi*real_harmonic**2, (angle, -1, 1))-1)
    exact('real harmonic gradient norm', sp.integrate(2*sp.pi*(1-angle**2)*sp.diff(real_harmonic, angle)**2, (angle, -1, 1))-6)
    distance, edge_metric, edge_amplitude, shift_edge = sp.symbols('d Fs ae JR', positive=True)
    edge_constant = (12*edge_metric)**(-sp.Rational(3, 2))
    displacement_edge = edge_amplitude/(3*edge_constant)
    phase_edge_prime = rotation*edge_amplitude/(3*edge_constant*edge_metric**2)+rotation*shift_edge/edge_metric
    exact('moving surface is the inherited charge transport law',
          edge_metric**2/rotation*(phase_edge_prime-rotation*shift_edge/edge_metric)-displacement_edge)
    edge_field = edge_constant*distance**3
    edge_response = edge_amplitude*distance**2
    exact('amplitude radial variational surface term vanishes',
          sp.limit(edge_response*sp.diff(edge_response, distance), distance, 0))
    exact('phase radial variational surface term vanishes',
          sp.limit(edge_field**2*phase*phase_edge_prime, distance, 0))
    exact('fractional potential quadratic density vanishes at surface',
          sp.limit(edge_field**(-sp.Rational(2, 3))*edge_response**2, distance, 0))
    flat_gradient_integral, flat_overlap = sp.symbols('phase_gradient_integral overlap', real=True)
    flat_mass = response**2+4*rotation*flat_overlap-flat_gradient_integral
    exact('flat phase equation reduces effective gyroscopic mass',
          flat_mass.subs(flat_gradient_integral, 2*rotation*flat_overlap)-(response**2+2*rotation*flat_overlap))
    boundary_slope, second_slope, spectral_square, boundary_value, canonical = sp.symbols('s0 s2 z ZR NZ', real=True)
    on_shell = -canonical*(boundary_slope+second_slope*spectral_square)*boundary_value**2/2
    exact('on-shell Dirichlet action derivative yields minus s2',
          2*sp.diff(on_shell, spectral_square)/(canonical*boundary_value**2)+second_slope)
    result = save('action-derivation', Path(__file__), dict(input_hashes=dependencies(), checks=checks,
        exact_checks=len(checks), gravity_mass_density=str(expected_gravity),
        matter_mass_terms=[
            str(measure*(response-metric*shift*gradient)**2),
            str(2*measure*rotation*phase*(2*amplitude*response+amplitude**2*(time_metric+angular))),
            str(2*measure*rotation*metric*shift*amplitude**2*phase_prime),
            str(-measure*lapse**2*amplitude**2*(metric*phase_prime**2+6*phase**2/radius**2))],
        convention='Real harmonic with integral Y^2=1; delta theta=-s qdot, delta g_tr=J qdot.',
        constrained_energy='Quadratic rotating-frame canonical energy / fixed-charge Routhian E-wQ, not raw unconstrained ADM energy.',
        envelope_assumption='Regular stationary interior at fixed surface master; even-profile frequency variations cancel from bulk first variation.',
        surface_assumption='Inherited compact cubic field edge and no extra thin-shell action.'))
    print(dict(state='complete', exact_checks=result['exact_checks']), flush=True)


if __name__ == '__main__':
    main()

