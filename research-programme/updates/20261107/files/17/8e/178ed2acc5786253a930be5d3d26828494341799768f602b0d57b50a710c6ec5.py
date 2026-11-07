from observer_common import *
from spectral_readout import SpectralReadout


def main():
    modest()
    folder = ROOT / 'results/physical-readout'
    folder.mkdir(parents=True, exist_ok=False)
    checks, rows, inputs = [], [], []
    for model in ['heavy', 'cold']:
        system = MixedSystem(model, 24, 8, 'event8')
        readout = SpectralReadout(system)
        basis = system.basis
        frequencies = basis.nodes
        occupation = 1 / np.expm1(frequencies)
        planck_weight = occupation * (1 + occupation)
        inputs.extend(readout.inputs)
        for expansion in [.1, 1., 2.1]:
            background = readout.background(expansion)
            values = basis.values @ background['profile']
            slopes = basis.derivative(frequencies) @ background['profile']
            dilation_change = frequencies * ((1 + 2 * occupation) * values - slopes)
            expected_age = basis.values @ background['profile_prime'] - dilation_change
            age_errors, boost_errors = [], []
            for size in [2e-4, 1e-4]:
                changed = []
                for sign in [-1, 1]:
                    shifted = readout.background(expansion + sign * size)
                    energy = frequencies * math.exp(sign * size)
                    planck = 1 / np.expm1(energy)
                    changed.append(planck * (1 + planck) * (basis.evaluate(energy) @ shifted['profile']) / planck_weight)
                derivative = (changed[1] - changed[0]) / (2 * size)
                age_errors.append(float(np.sqrt(np.dot(basis.measure, abs(derivative - expected_age) ** 2)
                                                / np.dot(basis.measure, abs(expected_age) ** 2))))
                angles, weights = np.polynomial.legendre.leggauss(20)
                energy = frequencies[:, None] * (1 + size * angles) / math.sqrt(1 - size ** 2)
                planck = 1 / np.expm1(energy)
                boosted = planck * (1 + planck) * (basis.evaluate(energy) @ background['profile']) / planck_weight[:, None]
                dipole = 1.5 * boosted @ (weights * angles) / size
                boost_errors.append(float(np.sqrt(np.dot(basis.measure, abs(dipole + dilation_change) ** 2)
                                                  / np.dot(basis.measure, abs(dilation_change) ** 2))))
            checks.append(dict(name=model + ':' + str(expansion) + ': fixed-physical-energy Taylor derivative matches clock tangent',
                               passed=age_errors[-1] < .002 and age_errors[-1] < .4 * age_errors[0], values=age_errors))
            checks.append(dict(name=model + ':' + str(expansion) + ': finite Lorentz boost matches distorted-bath dilation',
                               passed=boost_errors[-1] < .002 and boost_errors[-1] < .4 * boost_errors[0], values=boost_errors))
            test = .07 * (frequencies ** 2 - 2 * frequencies) + .03 * dilation_change
            dilation = frequencies + background['heat'] * dilation_change
            physical_measure = basis.measure / planck_weight
            temperature = np.dot(physical_measure, planck_weight * test) / np.dot(physical_measure, planck_weight * dilation)
            physical_shape = planck_weight * (test - dilation * temperature)
            for factor in [.93, 1.08]:
                coordinate = frequencies / factor
                coordinate_measure = physical_measure / factor ** 3
                new_temperature = np.dot(coordinate_measure, planck_weight * test) / np.dot(coordinate_measure, planck_weight * dilation)
                new_shape = planck_weight * (test - dilation * new_temperature)
                brightness = frequencies ** 3 * physical_shape
                new_brightness = factor ** 3 * coordinate ** 3 * new_shape
                error = float(np.max(abs(new_brightness - brightness)) / np.max(abs(brightness)))
                checks.append(dict(name=model + ':' + str(expansion) + ': physical brightness independent of reference-energy units ' + str(factor),
                                   passed=error < 1e-12, value=error))
            rows.append(dict(model=model, expansion=expansion, age_errors=age_errors, boost_errors=boost_errors))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
                        finite_transform_tests_not_only_algebraic_relabeling=True,
                        frequency_reference_test_holds_physical_band_fixed=True), __file__,
           [ROOT / 'spectral_readout.py', *sorted(set(inputs))])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    main()
