from verify_integrated_dc import ambient_functional
from integrated_dc import *


def main():
    modest()
    folder = ROOT / 'results/emission-temperature-identity'
    folder.mkdir(parents=True, exist_ok=False)
    checks, samples = [], []
    planck = lambda frequency: 1 / np.expm1(frequency)
    for frequency in [.001, .01, .1, 1., 3., 8.]:
        base = ambient_functional(frequency, planck)
        temperature_ratio = 1.17
        actual = ambient_functional(frequency, lambda coordinate: planck(coordinate / temperature_ratio))
        scaled = temperature_ratio ** 5 * ambient_functional(frequency / temperature_ratio, planck)
        error = abs(actual / scaled - 1)
        checks.append(dict(name='Finite-temperature ambient functional transforms as xi^5 R(x/xi) at ' + str(frequency), passed=error < 1e-9, value=error))
        step = 1e-5
        upper = ambient_functional(frequency, lambda coordinate: planck(coordinate / (1 + step)))
        lower = ambient_functional(frequency, lambda coordinate: planck(coordinate / (1 - step)))
        derivative = (upper - lower) / (2 * step)
        logarithmic_derivative = (ambient_functional(frequency * math.exp(step), planck) - ambient_functional(frequency * math.exp(-step), planck)) / (2 * step)
        predicted = 5 * base - logarithmic_derivative
        error = abs(derivative - predicted) / max(abs(predicted), 1e-30)
        checks.append(dict(name='Ambient temperature derivative equals 5R-xRprime at ' + str(frequency), passed=error < 1e-6, value=error))
        occupation = planck(frequency / temperature_ratio)
        detailed_balance = 1 - occupation * np.expm1(frequency / temperature_ratio)
        checks.append(dict(name='Emission equilibrium along finite-temperature family at ' + str(frequency), passed=abs(detailed_balance) < 1e-14, value=abs(detailed_balance)))
        samples.append([frequency, base, actual, scaled, derivative, predicted])
    np.savez_compressed(folder / 'identities.npz', samples=samples)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
        derived_identity='R[n_P(t/xi)](x)=xi^5 R[n_P](x/xi), hence delta_R[x w]=5R-xRprime.',
        no_fitted_radiation_temperature=True), __file__,
        [ROOT / 'verify_integrated_dc.py', ROOT / 'integrated_dc.py', ROOT / 'sources/1109.6552.html'])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    main()
