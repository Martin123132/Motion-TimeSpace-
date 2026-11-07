from __future__ import annotations

from pathlib import Path
import sympy as sp

from polar_energy import modest_process, save, dependencies


def main():
    modest_process()
    checks = []

    def check(name, expression):
        residual = sp.factor(expression)
        checks.append(dict(name=name, residual=str(residual), passed=residual == 0))
        assert residual == 0, (name, residual)

    radius, alpha, frequency = sp.symbols('r alpha w', positive=True)
    perturbation, harmonic, eigenvalue = sp.symbols('epsilon Y L')
    metric = sp.Function('F')(radius)
    lapse = sp.Function('N')(radius)
    radial = sp.Function('H')(radius)
    angular = sp.Function('K')(radius)
    field = sp.Function('h')(radius)
    amplitude = sp.Function('u')(radius)
    phase_momentum = sp.symbols('pi_v')
    potential, force, second = sp.symbols('W W_h W_hh')
    root_radial = sp.sqrt(1+perturbation*radial*harmonic)/sp.sqrt(metric)
    root_angular = radius*sp.sqrt(1+perturbation*angular*harmonic)
    volume = sp.sqrt(1+perturbation*radial*harmonic)*(1+perturbation*angular*harmonic)

    def coefficient(expression, order=2):
        return sp.diff(expression, perturbation, order).subs(perturbation, 0)/sp.factorial(order)

    check('volume first variation', coefficient(volume, 1)/harmonic-radial/2-angular)
    check('volume second variation', coefficient(volume)/harmonic**2-radial*angular/2+radial**2/8)
    inverse_expected = 3*radial**2/8+angular**2+radial*angular/2
    check('inverse volume second variation', coefficient(1/volume)/harmonic**2-inverse_expected)
    curvature = 2/root_angular**2-2*sp.diff(root_angular, radius)**2/(root_radial**2*root_angular**2)-4*sp.diff(root_angular, radius, 2)/(root_radial**2*root_angular)+4*sp.diff(root_radial, radius)*sp.diff(root_angular, radius)/(root_radial**3*root_angular)
    curvature_first = coefficient(curvature, 1)/harmonic+eigenvalue*(radial+angular)/radius**2
    expected_first = 2*metric*sp.diff(radial, radius)/radius+((eigenvalue+2*metric)/radius**2+2*sp.diff(metric, radius)/radius)*radial+(eigenvalue-2)*angular/radius**2-(6*metric/radius+sp.diff(metric, radius))*sp.diff(angular, radius)-2*metric*sp.diff(angular, radius, 2)
    check('linear spatial curvature', curvature_first-expected_first)
    curvature_bulk = 2*lapse*root_radial+2*lapse*sp.diff(root_angular, radius)**2/root_radial+4*sp.diff(lapse, radius)*root_angular*sp.diff(root_angular, radius)/root_radial
    expected_bulk = lapse/sp.sqrt(metric)*(-radial**2/4+eigenvalue*radial*angular/2)+2*lapse*sp.sqrt(metric)*(radius**2*sp.diff(angular, radius)**2/4-radial*(angular+radius*sp.diff(angular, radius))/2+3*radial**2/8)+4*sp.diff(lapse, radius)*radius*sp.sqrt(metric)*(3*radial**2/8-radial*angular/2-radial*radius*sp.diff(angular, radius)/4)
    check('quadratic Ricci bulk', coefficient(curvature_bulk)/harmonic**2+lapse*eigenvalue*radial*angular/(2*sp.sqrt(metric))-expected_bulk)
    check('radial Ricci boundary identity', lapse*root_radial*root_angular**2*curvature-curvature_bulk-sp.diff(-4*lapse*root_angular*sp.diff(root_angular, radius)/root_radial, radius))
    scalar_momentum = frequency*field**2/lapse+perturbation*field*phase_momentum*harmonic
    scalar_field = field+perturbation*amplitude*harmonic
    charge_energy = scalar_momentum**2/(2*volume*scalar_field**2)
    charge_expected = (phase_momentum**2-2*frequency/lapse*phase_momentum*(2*amplitude+field*(radial/2+angular))+frequency**2/lapse**2*(3*amplitude**2+2*field*amplitude*(radial/2+angular)+field**2*inverse_expected))/2
    check('canonical phase energy second variation', coefficient(charge_energy)/harmonic**2-charge_expected)
    amplitude_energy = metric*volume/(2*(1+perturbation*radial*harmonic))*(sp.diff(field, radius)+perturbation*sp.diff(amplitude, radius)*harmonic)**2
    amplitude_expected = metric/2*(sp.diff(amplitude, radius)**2+2*sp.diff(field, radius)*sp.diff(amplitude, radius)*(angular-radial/2)+sp.diff(field, radius)**2*(3*radial**2/8-radial*angular/2))
    check('amplitude radial energy second variation', coefficient(amplitude_energy)/harmonic**2-amplitude_expected)
    check('potential energy second variation', coefficient(volume*(potential+force*perturbation*amplitude*harmonic+second*perturbation**2*amplitude**2*harmonic**2/2))/harmonic**2-(second*amplitude**2/2+force*amplitude*(radial/2+angular)+potential*(radial*angular/2-radial**2/8)))
    density_first = coefficient(charge_energy/volume+amplitude_energy/volume+potential+force*perturbation*amplitude*harmonic, 1)/harmonic
    density_expected = frequency*field*phase_momentum/lapse-frequency**2/lapse**2*(field**2*(radial+2*angular)/2+field*amplitude)-metric*sp.diff(field, radius)**2*radial/2+metric*sp.diff(field, radius)*sp.diff(amplitude, radius)+force*amplitude
    check('Hamiltonian matter constraint first variation', density_first-density_expected)
    geometric = sp.Function('Q_geom')(radius)
    rotation2 = frequency**2/lapse**2
    metric_prime = (1-metric)/radius-alpha*radius*(metric*sp.diff(field, radius)**2+rotation2*field**2+2*potential)
    constraint = (expected_first-4*alpha*density_expected).subs(radial, geometric+angular).doit().subs(sp.diff(metric, radius), metric_prime)
    operator = -metric*sp.diff(angular, radius, 2)-(2*metric/radius+metric_prime/2)*sp.diff(angular, radius)+(eigenvalue/radius**2+2*alpha*(rotation2*field**2-potential))*angular
    source = -metric*sp.diff(geometric, radius)/radius-((eigenvalue/2+1)/radius**2-2*alpha*potential)*geometric+2*alpha*((force-rotation2*field)*amplitude+metric*sp.diff(field, radius)*sp.diff(amplitude, radius)+frequency*field*phase_momentum/lapse)
    check('elliptic conformal constraint after background equations', constraint-2*(operator-source))
    pressure = (metric*sp.diff(field, radius)**2+rotation2*field**2)/2-potential
    log_lapse_prime = ((1-metric)/2+alpha*radius**2*pressure)/(radius*metric)
    field_second = (force-rotation2*field)/metric-(2/radius+log_lapse_prime+metric_prime/(2*metric))*sp.diff(field, radius)
    log_second = sp.diff(log_lapse_prime, radius).subs(sp.diff(potential, radius), force*sp.diff(field, radius))
    log_second += sp.diff(log_lapse_prime, potential)*force*sp.diff(field, radius)
    log_second = log_second.subs({sp.diff(field, radius, 2):field_second, sp.diff(lapse, radius):lapse*log_lapse_prime, sp.diff(metric, radius):metric_prime})
    check('background lapse ground state D0 N=0', -metric*(log_second+log_lapse_prime**2)-(2*metric/radius+metric_prime/2)*log_lapse_prime+2*alpha*(rotation2*field**2-potential))
    coefficient_a = sp.Function('a')(radius)
    ground = sp.Function('N0')(radius)
    test = sp.Function('f')(radius)
    ground_potential = sp.diff(coefficient_a*sp.diff(ground, radius), radius)/ground
    check('ground state quadratic form identity including boundary', coefficient_a*sp.diff(test, radius)**2+ground_potential*test**2-coefficient_a*ground**2*sp.diff(test/ground, radius)**2-sp.diff(coefficient_a*sp.diff(ground, radius)/ground*test**2, radius))
    momentum_radial, momentum_trace, momentum_mixed, momentum_tensor = sp.symbols('p k j g')
    dewitt = (momentum_radial**2+2*momentum_trace**2+2*metric*eigenvalue*momentum_mixed**2/radius**2+eigenvalue*(eigenvalue-2)*momentum_tensor**2/2-(momentum_radial+2*momentum_trace)**2/2)
    check('maximal slicing removes conformal momentum', (4*alpha*dewitt).subs({momentum_trace:-momentum_radial/2, eigenvalue:6})-(6*alpha*momentum_radial**2+48*alpha*metric*momentum_mixed**2/radius**2+48*alpha*momentum_tensor**2))
    check('unreduced pure trace negative control', dewitt.subs({momentum_trace:momentum_radial, momentum_mixed:0, momentum_tensor:0})+3*momentum_radial**2/2)
    dgeometric, dangular = sp.symbols('dQ_geom dK')
    check('reduced canonical one form', (momentum_radial*(dgeometric+dangular)+2*momentum_trace*dangular).subs(momentum_trace, -momentum_radial/2)-momentum_radial*dgeometric)
    momentum_radial_f = sp.Function('p')(radius)
    momentum_amplitude = sp.Function('pi_u')(radius)
    phase_cartesian = sp.Function('v')(radius)
    mixed = radius**2/6*(sp.diff(momentum_radial_f, radius)+3*momentum_radial_f/radius-sp.diff(field, radius)*momentum_amplitude/2-frequency/(2*lapse)*(field*sp.diff(phase_cartesian, radius)-sp.diff(field, radius)*phase_cartesian))
    tensor = (metric*sp.diff(mixed, radius)+(sp.diff(metric, radius)/2+2*metric/radius)*mixed-momentum_radial_f/2-frequency*field*phase_cartesian/(2*lapse))/2
    check('radial momentum constraint solved', sp.diff(momentum_radial_f, radius)+3*momentum_radial_f/radius-6*mixed/radius**2-sp.diff(field, radius)*momentum_amplitude/2-frequency/(2*lapse)*(field*sp.diff(phase_cartesian, radius)-sp.diff(field, radius)*phase_cartesian))
    check('angular momentum constraint solved', metric*sp.diff(mixed, radius)+(sp.diff(metric, radius)/2+2*metric/radius)*mixed-momentum_radial_f/2-2*tensor-frequency*field*phase_cartesian/(2*lapse))
    isotropic, mass = sp.symbols('rho M', positive=True)
    conformal = 1+mass/(2*isotropic)
    areal = isotropic*conformal**2
    exterior = 1-2*mass/areal
    exterior_field = isotropic**(-3)/conformal
    derivative_r = sp.diff(exterior_field, isotropic)/sp.diff(areal, isotropic)
    second_r = sp.diff(derivative_r, isotropic)/sp.diff(areal, isotropic)
    check('exact decaying l2 exterior constraint tail', -exterior*second_r-(2*exterior/areal+mass/areal**2)*derivative_r+6*exterior_field/areal**2)
    amplitude_flat, phase_flat, momentum_flat, momentum_phase_flat, plus, minus = sp.symbols('u v pi_u pi_v L_plus L_minus')
    udot = momentum_flat
    vdot = momentum_phase_flat-2*frequency*amplitude_flat
    uddot = 2*frequency*momentum_phase_flat-(plus+4*frequency**2)*amplitude_flat
    vddot = -minus*phase_flat-2*frequency*udot
    check('flat amplitude gyroscopic equation', uddot-2*frequency*vdot+plus*amplitude_flat)
    check('flat phase gyroscopic equation', vddot+2*frequency*udot+minus*phase_flat)
    report = save('exact', Path(__file__), dict(input_hashes=dependencies(), exact_checks=len(checks), checks=checks,
        linear_constraint=str(source), energy_convention='Canonical rotating-frame E-wQ; global U(1), not electric charge.',
        positive_odd_block_derived=True, constraint_ground_state_identity=True,
        even_block_global_positivity_proved=False))
    print(dict(state=report['state'], exact_checks=len(checks)), flush=True)


if __name__ == '__main__':
    main()
