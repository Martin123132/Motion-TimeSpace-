from integrated_dc import *


def ambient_functional(frequency, occupation):
    def integrand(incident):
        fraction = frequency / incident
        product = fraction * (1 - fraction)
        gould = (1 - 3 * product + 1.5 * product ** 2 - product ** 3) / (1 - fraction)
        return incident ** 4 * occupation(incident) * (1 + occupation(incident - frequency)) * gould
    return integrate.quad(integrand, 2 * frequency, max(100., 2 * frequency + 80.), epsabs=1e-11, epsrel=2e-11, limit=300)[0]


def main():
    modest()
    folder = ROOT / 'results/integrated-dc'
    folder.mkdir(parents=True, exist_ok=False)
    checks, samples = [], []
    planck = lambda frequency: 1 / np.expm1(frequency)
    perturbation = lambda frequency: frequency * np.exp(-frequency) / (1 + frequency)
    for frequency in [1e-5, .001, .01, .1, 1., 3., 8., 30.]:
        base = ambient_functional(frequency, planck)
        direct = base * np.expm1(frequency) / frequency ** 3 / (4 * math.pi ** 4 / 15)
        sampled = float(integrated_dc_absorption_shape(frequency))
        error = abs(sampled / direct - 1)
        checks.append(dict(name='Planck Gaunt integral agrees with independent adaptive quadrature at ' + str(frequency), passed=error < 1e-7, value=error))
        step = 1e-4
        plus = ambient_functional(frequency, lambda coordinate: planck(coordinate) + step * perturbation(coordinate))
        minus = ambient_functional(frequency, lambda coordinate: planck(coordinate) - step * perturbation(coordinate))
        def derivative_integrand(incident):
            fraction = frequency / incident
            product = fraction * (1 - fraction)
            gould = (1 - 3 * product + 1.5 * product ** 2 - product ** 3) / (1 - fraction)
            return incident ** 4 * gould * ((1 + planck(incident - frequency)) * perturbation(incident) + planck(incident) * perturbation(incident - frequency))
        derivative = integrate.quad(derivative_integrand, 2 * frequency, max(100., 2 * frequency + 80.), epsabs=1e-12, epsrel=1e-11)[0]
        finite_difference = (plus - minus) / (2 * step)
        derivative_error = abs(finite_difference - derivative) / max(abs(derivative), 1e-30)
        checks.append(dict(name='Frequency-dependent ambient functional derivative at ' + str(frequency), passed=derivative_error < 1e-7, value=derivative_error))
        samples.append([frequency, sampled, float(dc_absorption_shape(frequency, 'dc')), derivative, finite_difference])
    soft_ratio = float(integrated_dc_absorption_shape(1e-7) * 1e-14)
    checks.append(dict(name='Integrated DC has correct low-frequency absorption limit', passed=abs(soft_ratio - 1) < 1e-6, value=soft_ratio))
    np.savez_compressed(folder / 'functional-checks.npz', samples=samples)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
        integrated_finite_frequency_ambient_functional=True, ambient_jacobian_rank_one=False,
        scope='Leading resting-electron Gould source; consistent parent of background matrix. Full DC redistribution not included.'), __file__,
        [ROOT / 'integrated_dc.py', ROOT / 'sourced_emission.py', ROOT / 'emission_rates.py', ROOT / 'sources/1109.6552.html'])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    main()
