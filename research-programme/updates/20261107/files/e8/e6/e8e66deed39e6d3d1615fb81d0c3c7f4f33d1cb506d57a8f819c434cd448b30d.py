import sympy as sp
from angular_common import *
from verify_operator import angular_fixture


def main():
    modest()
    folder = ROOT / 'results/derived-limits'
    assert not folder.exists()
    checks = []
    cosine = sp.symbols('cosine', real=True)
    angular = sp.Rational(3, 4) * (1 - cosine) * (1 + cosine ** 2)
    eigenvalues = []
    for degree, expected in enumerate([1, -sp.Rational(2, 5), sp.Rational(1, 10), -sp.Rational(3, 70), 0, 0]):
        actual = sp.integrate(angular * sp.legendre(degree, cosine), (cosine, -1, 1)) / 2
        eigenvalues.append(str(actual))
        checks.append(dict(name='Exact unpolarized recoil angular eigenvalue l=' + str(degree), passed=actual == expected))
    kernel = AngularKernel(12, 24)
    for degree in [1, 2, 3]:
        amplitude = .2
        occupation = (1 + amplitude * special.eval_legendre(degree, kernel.directions[:, 2]))[:, None, None] * kernel.projector
        pair = np.einsum('n,nij,nji->', kernel.weights, occupation, kernel.recoil_angular(occupation))
        expected = 2 * (1 + amplitude ** 2 * float(sp.Rational(eigenvalues[degree])) / (2 * degree + 1))
        checks.append(dict(name='Same-monopole positive angular counterexample l=' + str(degree),
                           passed=bool(abs(pair - expected) < 1e-10 and abs(pair - 2) > 1e-5),
                           recoil_pair=float(pair), mean_only_pair=2., minimum_occupation=float(1 - amplitude)))
    value = angular_fixture(kernel.directions)
    cold = kernel.scatter(value) - value
    for power in [-1, 0, 2]:
        expected = (power + 2) * kernel.recoil_angular(value) + 2 * value
        errors = []
        for energy in [.0002, .0001, .00005]:
            ratio = 1 - energy * (1 - kernel.directions @ kernel.directions.T)
            gain = 1.5 * kernel.projector @ np.einsum('nm,m,mij->nij', ratio ** (-power - 2), kernel.weights, value) @ kernel.projector
            polarized_trace = np.einsum('nij,mji->nm', value, kernel.projector)
            probability = 1.5 * polarized_trace / np.trace(value, axis1=1, axis2=2)[:, None]
            forward_ratio = 1 / (1 + energy * (1 - kernel.directions @ kernel.directions.T))
            total_cross_section = np.einsum('m,nm,nm->n', kernel.weights, probability, forward_ratio ** 2)
            response = gain - total_cross_section[:, None, None] * value
            derivative = (response - cold) / energy
            error = float(np.linalg.norm(derivative - expected) / np.linalg.norm(expected))
            errors.append(error)
        checks.append(dict(name='Recoil from independent energy remapping and phase-space Jacobian power=' + str(power),
                           passed=errors[-1] < .001 and errors[-1] < .6 * errors[-2] < .36 * errors[-3],
                           errors=errors, gate=.001))
    frequency = sp.symbols('frequency', positive=True)
    symbolic_occupation = sp.Function('occupation')(frequency)
    shifted = frequency * sp.diff(symbolic_occupation, frequency) + 2 * symbolic_occupation
    recoil = frequency * ((2 * symbolic_occupation + 1) * shifted + 2 * symbolic_occupation)
    divergence = sp.diff(frequency ** 4 * symbolic_occupation * (1 + symbolic_occupation), frequency) / frequency ** 2
    checks.append(dict(name='Exact isotropic tensor recoil equals Kompaneets divergence',
                       passed=sp.simplify(recoil - divergence) == 0))
    thermal = sp.diff(frequency ** 2 * symbolic_occupation, frequency, 2) - 2 * symbolic_occupation
    expected_thermal = sp.diff(frequency ** 4 * sp.diff(symbolic_occupation, frequency), frequency) / frequency ** 2
    checks.append(dict(name='Exact isotropic tensor thermal term equals Kompaneets diffusion',
                       passed=sp.simplify(thermal - expected_thermal) == 0))
    incorrect = sp.diff(frequency ** 2 * symbolic_occupation, frequency, 2) / frequency ** 2 - 2 * symbolic_occupation
    checks.append(dict(name='Printed extra inverse-energy-squared factor rejected by isotropic identity',
                       passed=sp.simplify(incorrect - expected_thermal) != 0))
    spectral_constant = 120 * (sp.zeta(4) - sp.zeta(6))
    folder.mkdir(parents=True, exist_ok=False)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        exact_angular_eigenvalues=eigenvalues,
                        exact_integral_x4_G_squared=str(spectral_constant),
                        numeric_integral_x4_G_squared=float(spectral_constant),
                        printed_tensor_equation_7_4_extra_factor_not_used=True,
                        component_equations_7_7_and_independent_boost_test_agree=True,
                        recoil_remap_uses_leading_polarized_amplitude_not_full_finite_energy_QED=True), __file__,
           [ROOT / 'verify_operator.py', ROOT / 'sources/pitrou-1902.09456v2.pdf'])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']],
                         spectral_constant=float(spectral_constant))), flush=True)


if __name__ == '__main__':
    main()
