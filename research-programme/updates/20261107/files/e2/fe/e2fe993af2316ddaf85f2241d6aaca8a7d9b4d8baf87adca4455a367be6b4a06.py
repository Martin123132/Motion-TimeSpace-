from __future__ import annotations

from pathlib import Path
import sympy as sp

from interior_common import modest_process, save


def main():
    modest_process()
    radius, alpha, metric, field, gradient, rotation, potential, force, second = sp.symbols('r alpha F h hp s W Wh Whh', positive=True)
    kinetic = metric*gradient**2+rotation**2*field**2
    pressure = kinetic/2-potential
    density = kinetic/2+potential
    log_lapse = (1-metric+2*alpha*radius**2*pressure)/(2*radius*metric)
    metric_prime = (1-metric)/radius-2*alpha*radius*density
    field_second = (force-rotation**2*field)/metric-(2/radius+log_lapse+metric_prime/(2*metric))*gradient
    variables = [radius, metric, field, gradient, rotation, potential, force]
    flows = [1, metric_prime, gradient, field_second, -log_lapse*rotation, force*gradient, second*gradient]

    def derivative(expression):
        return sp.factor(sum(sp.diff(expression, variable)*flow for variable, flow in zip(variables, flows)))

    denominator = (7-3*metric)/2-alpha*radius**2*density
    transfer = denominator/metric
    amplitude_shift = radius*gradient/2
    phase_gradient_shift = radius*rotation*field/2
    phase_value_shift = sp.factor(rotation*((sp.Rational(3, 2)-radius*metric_prime/(4*metric)-radius*log_lapse/2)*field+radius*gradient))
    radial_coefficient = 8/radius**2-4*alpha*potential
    angular_coefficient = 4/radius**2+4*alpha*rotation**2*field**2-4*alpha*(rotation*field*phase_value_shift+(force-rotation**2*field)*amplitude_shift+metric*gradient*derivative(amplitude_shift))
    reconstructed_denominator = sp.factor(angular_coefficient-2*metric/radius*derivative(transfer)-radial_coefficient*transfer)
    normalization = sp.factor(-radius**2*metric*reconstructed_denominator/(6*denominator))
    master_coefficient = sp.factor(2*metric/radius*(3*derivative(transfer)/radius-3*transfer/radius**2)+3*radial_coefficient*transfer/radius)
    checks = []

    def check(name, residual):
        residual = sp.factor(residual)
        checks.append(dict(name=name, residual=str(residual), passed=residual == 0))
        assert residual == 0, (name, residual)

    check('matter Kprime source cancellation', rotation*field*phase_gradient_shift-kinetic*radius/2+metric*gradient*amplitude_shift)
    check('radial constraint coefficient simplified', (6+2*metric)/radius**2+2*metric_prime/radius+2*alpha*kinetic-radial_coefficient)
    check('angular derivative coefficient simplified', (6-2*metric)/radius+metric_prime-2*denominator/radius)
    metric_angular_coefficient = sp.factor(-master_coefficient/reconstructed_denominator)
    master_gradient_coefficient = sp.factor(-(6*denominator/radius**2)/reconstructed_denominator)
    source_coefficient = sp.factor(4*alpha/reconstructed_denominator)
    mass = sp.symbols('M', positive=True)
    vacuum = {field:0, gradient:0, potential:0, force:0, metric:1-2*mass/radius}
    check('vacuum normalization', normalization.subs(vacuum)-1)
    check('vacuum master derivative reconstruction', master_gradient_coefficient.subs(vacuum)-(1-2*mass/radius))
    check('vacuum master value reconstruction', metric_angular_coefficient.subs(vacuum)-(6*mass**2+6*mass*radius+6*radius**2)/(radius**2*(2*radius+3*mass)))
    report = save('map-v2', Path(__file__), dict(exact_checks=checks, symbols=[str(value) for value in [radius, alpha, metric, field, gradient, rotation, potential, force, second]],
         beta=str(denominator), amplitude_shift=str(amplitude_shift), phase_gradient_shift=str(phase_gradient_shift), phase_value_shift=str(phase_value_shift),
         constraint_normalization=str(normalization), reconstructed_K_denominator=str(reconstructed_denominator),
         master_gradient_coefficient=str(master_gradient_coefficient), master_value_coefficient=str(metric_angular_coefficient), source_coefficient=str(source_coefficient),
         new_variables='w=u-aK; pibar=pi_v-cKprime-dK; Z=r/3[K+F/beta(H-rKprime)]',
         inverse_map='K=k1 Zprime+k0 Z+ks[s h pibar+(Wh-s^2 h)w+F hp wprime]; H=rKprime+beta/F(3Z/r-K)',
         canonical_transformation_claimed=False, positive_interior_form_claimed=False))
    print(dict(exact_checks=len(checks), normalization=str(normalization), phase_shift=str(phase_value_shift)), flush=True)


if __name__ == '__main__':
    main()
