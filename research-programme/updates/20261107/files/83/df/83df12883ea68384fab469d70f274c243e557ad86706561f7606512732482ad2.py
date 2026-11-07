from types import SimpleNamespace
from numpy.polynomial import Polynomial
from dense_geometry_derivative import *


def main():
    modest()
    folder = ROOT / 'results/dense-derivative'
    folder.mkdir(parents=True, exist_ok=False)
    random = np.random.default_rng(790)
    maximum = 0.
    for trial in range(24):
        coefficients = random.normal(size=(7, 6)) * 10 ** (-trial)
        segment = SimpleNamespace(F=coefficients, y_old=np.ones(6) * 1e10, h=.003, t_old=.7)
        coordinate = float(random.uniform(.01, .99))
        polynomials = [Polynomial([0.]) for index in range(6)]
        for index, coefficient in enumerate(reversed(coefficients)):
            factor = Polynomial([0., 1.]) if index % 2 == 0 else Polynomial([1., -1.])
            polynomials = [(polynomial + coefficient[channel]) * factor for channel, polynomial in enumerate(polynomials)]
        expected = np.array([polynomial.deriv()(coordinate) / segment.h for polynomial in polynomials])
        actual = polynomial_derivative(segment, segment.t_old + coordinate * segment.h)
        maximum = max(maximum, float(linalg.norm(actual - expected) / linalg.norm(expected)))
    witness = SimpleNamespace(F=np.array([[1e-20]]), y_old=np.ones(1), h=1., t_old=0.)
    increment_derivative = float(polynomial_derivative(witness, .5)[0])
    finite_difference = ((1. + .6e-20) - (1. + .4e-20)) / .2
    checks = [dict(name='Dense recurrence derivative matches independently expanded polynomials', passed=maximum < 1e-11, value=maximum),
              dict(name='Tiny increment derivative survives an order-one baseline', passed=abs(increment_derivative / 1e-20 - 1) < 1e-14, value=increment_derivative),
              dict(name='Negative control exposes cancellation in differencing total fields', passed=finite_difference == 0, value=finite_difference)]
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
        scope='Differentiates the solver dense increment before addition to the total field; does not change the physical evolution or loosen the ODE gate.'),
        __file__, [ROOT / 'dense_geometry_derivative.py'])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    main()
