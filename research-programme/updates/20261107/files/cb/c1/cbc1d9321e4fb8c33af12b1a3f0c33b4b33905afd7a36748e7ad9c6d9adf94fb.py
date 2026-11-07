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

    beta = (7-3*metric)/2-alpha*radius**2*density
    omega = sp.factor(beta+alpha*radius**2*(metric*gradient**2+rotation**2*field**2))
    amplitude_shift = radius*gradient/2
    phase_derivative_shift = radius*rotation*field/2
    phase_shift = sp.factor(rotation*((sp.Rational(3, 2)-radius*metric_prime/(4*metric)-radius*log_lapse/2)*field+radius*gradient))
    amplitude_shift_prime = derivative(amplitude_shift)
    master, master_prime, scalar, scalar_prime, phase, angular, angular_prime = sp.symbols('Z Zp w wp pibar K Kp')
    difference = beta/metric*(3*master/radius-angular)
    radial = radius*angular_prime+difference
    amplitude = scalar+amplitude_shift*angular
    amplitude_prime = scalar_prime+amplitude_shift_prime*angular+amplitude_shift*angular_prime
    momentum = phase+phase_derivative_shift*angular_prime+phase_shift*angular
    energy = -(1-2*alpha*radius**2*potential)*radial**2/(8*alpha*radius**2)+(-1/(2*alpha*radius**2)+rotation**2*field**2/2)*radial*angular+metric*(1+radius*log_lapse)*radial*angular_prime/(4*alpha*radius)-metric*angular_prime**2/(8*alpha)+rotation**2*field**2*angular**2/2
    energy += metric*amplitude_prime**2/2+(6/radius**2+second+3*rotation**2)*amplitude**2/2+(force+rotation**2*field)*amplitude*(radial/2+angular)+metric*gradient*amplitude_prime*(angular-radial/2)-rotation*momentum*(2*amplitude+field*(radial/2+angular))+momentum**2/2
    checks = []

    def check(name, expression):
        residual = sp.factor(expression)
        checks.append(dict(name=name, residual=str(residual), passed=residual == 0))
        assert residual == 0, (name, residual)

    print('Collecting local quadratic coefficients', flush=True)
    expanded = sp.Poly(sp.expand(energy), angular_prime)
    check('Kprime squared cancels exactly', expanded.coeff_monomial(angular_prime**2))
    derivative_coefficient = sp.factor(expanded.coeff_monomial(angular_prime))
    check('no scalar derivative times Kprime', sp.diff(derivative_coefficient, scalar_prime))
    check('no independent phase momentum times Kprime', sp.diff(derivative_coefficient, phase))
    contact_angular = sp.factor(sp.diff(derivative_coefficient, angular))
    contact_master = sp.factor(sp.diff(derivative_coefficient, master))
    contact_scalar = sp.factor(sp.diff(derivative_coefficient, scalar))
    check('master contact coefficient', contact_master+3*beta*log_lapse/(4*alpha*radius))
    check('scalar contact coefficient', contact_scalar-radius*(force-rotation**2*field)/2)
    log_measure = log_lapse+2/radius-metric_prime/(2*metric)
    remainder = expanded.coeff_monomial(1)-(derivative(contact_angular)+log_measure*contact_angular)*angular**2/2-(derivative(contact_master)+log_measure*contact_master)*angular*master-contact_master*angular*master_prime-(derivative(contact_scalar)+log_measure*contact_scalar)*angular*scalar-contact_scalar*angular*scalar_prime
    coordinates = [master_prime, master, scalar_prime, scalar, phase, angular]
    base_hessian = [[sp.factor(sp.diff(remainder, left, right)) for right in coordinates] for left in coordinates]
    master_derivative_coefficient = sp.factor(metric*beta/omega)
    master_value_coefficient = sp.factor((metric*derivative(beta)+beta*(3/radius+alpha*radius*kinetic))/omega)
    source_coefficient = sp.factor(-2*alpha*radius**2*metric/(3*omega))
    angular_row = [master_derivative_coefficient, master_value_coefficient, source_coefficient*metric*gradient,
                   source_coefficient*(force-rotation**2*field), source_coefficient*rotation*field]
    coefficient_names = ['a','c','d','a_prime','beta','omega','k_Zprime','k_Z','k_wprime','k_w','k_pibar']
    coefficient_values = [amplitude_shift, phase_derivative_shift, phase_shift, amplitude_shift_prime, beta, omega, *angular_row]
    derivatives = {name: str(derivative(value)) for name, value in zip(coefficient_names, coefficient_values) if name.startswith('k_') or name in ['beta','a','c','d']}
    check('positive reconstruction denominator', omega-beta-alpha*radius**2*(metric*gradient**2+rotation**2*field**2))
    print('Saving local form recipe', flush=True)
    save('energy-v2', Path(__file__), dict(exact_checks=checks, symbols=[str(value) for value in [radius, alpha, metric, field, gradient, rotation, potential, force, second]],
        base_coordinates=[str(value) for value in coordinates], local_coordinates=[str(value) for value in coordinates[:-1]],
        base_hessian=[[str(value) for value in row] for row in base_hessian],
        coefficients={name:str(value) for name,value in zip(coefficient_names, coefficient_values)}, derivatives=derivatives,
        contact_coefficients=[str(contact_angular),str(contact_master),str(contact_scalar)],
        density_recipe='E_local=a/2*x6^T B x6, x6=(Zprime,Z,wprime,w,pibar,K), K=k dot x5; contact=a[A K^2/2+B K Z+C K w]',
        measure='a_measure=N r^2/sqrtF; amplitude shift coefficient also a but kept separate in implementation',
        canonical_transformation_claimed=False, full_local_positivity_proved=False))
    print(dict(exact_checks=len(checks)), flush=True)


if __name__ == '__main__':
    main()
