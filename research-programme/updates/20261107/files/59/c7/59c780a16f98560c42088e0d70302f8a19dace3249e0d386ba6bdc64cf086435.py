from gould_angles import *
import sympy as symbolic


def main():
    modest()
    folder = ROOT / 'results/analytic-gould-angles'
    folder.mkdir(parents=True, exist_ok=False)
    share, cosine = symbolic.symbols('share cosine', real=True)
    first = 2 * (1 - share) ** 2 * (3 - 7 * share + 13 * share ** 2 - 7 * share ** 3 + 3 * share ** 4)
    second = 11 - 21 * share + 30 * share ** 3 - 21 * share ** 5 + 11 * share ** 6
    polynomial = first + second * (1 - cosine ** 2) - 10 * share ** 3 * cosine * (1 - cosine) ** 2
    exact = [symbolic.factor(symbolic.integrate(polynomial * symbolic.legendre(degree, cosine), (cosine, -1, 1)) * symbolic.Rational(2 * degree + 1, 2)) for degree in range(7)]
    product = share * (1 - share)
    normalization = symbolic.Rational(40, 3) * (1 - 3 * product + symbolic.Rational(3, 2) * product ** 2 - product ** 3)
    checks = [dict(name='Angular average exactly reproduces Gould energy factor', passed=symbolic.simplify(exact[0] - normalization) == 0),
              dict(name='No Legendre power above cubic in source marginal', passed=all(value == 0 for value in exact[4:]))]
    nodes, weights = np.polynomial.legendre.leggauss(32)
    for fraction in [1e-8, .001, .01, .1, .25, .5]:
        spectrum = angle_polynomial(fraction, nodes)
        checks.append(dict(name='Positive differential Gould marginal share=' + str(fraction), passed=bool(np.min(spectrum) > 0)))
        for degree in range(7):
            numerical = np.dot(weights * spectrum, special.eval_legendre(degree, nodes)) / np.dot(weights, spectrum)
            checks.append(check('Legendre angular eigenvalue share=' + str(fraction) + ' degree=' + str(degree), abs(numerical - marginal_eigenvalue(fraction, degree)), 1e-13))
            hard, incoming, companion = correlations(fraction, degree)
            gram = np.array([[1., hard, incoming], [hard, 1., companion], [incoming, companion, 1.]])
            checks.append(check('Three-direction angular Gram positivity share=' + str(fraction) + ' degree=' + str(degree), max(0., -np.min(linalg.eigvalsh(gram))), 1e-12))
    limiting = [symbolic.simplify(exact[degree].subs(share, 0) / ((2 * degree + 1) * exact[0].subs(share, 0))) for degree in range(4)]
    checks.append(dict(name='Soft ambient eigenvalues1,0,-11/100,0 derived exactly', passed=limiting == [1, 0, -symbolic.Rational(11, 100), 0]))
    crossed = symbolic.factor(exact[0].subs(share, -share / (1 - share)) * (1 - share) ** 6)
    checks.append(dict(name='Crossing preserves normalized angular average with phase factor', passed=symbolic.simplify(crossed - exact[0]) == 0))
    write_json(folder / 'exact.json', dict(coefficients=[str(value) for value in exact], soft_eigenvalues=[str(value) for value in limiting],
                                          companion_crossing='share -> -share/(1-share); verify independently against full matrix element.'))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks)), __file__,
        [ROOT / 'gould_angles.py', BRANCH / 'scaled-spectral-evolution-20261007/sources/2005.06941v1.html'])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    main()
