from consistent_spectral_basis import *
import mpmath as mp


def main():
    modest()
    mp.mp.dps = 70
    folder = ROOT / 'results/consistent-basis'
    folder.mkdir(parents=True, exist_ok=False)
    checks, rows = [], []
    for count in [24, 28, 32, 36]:
        basis, old = ConsistentBasis(count), StableBasis(count)
        reevaluation = float(np.max(abs(basis.evaluate(basis.nodes) - basis.values)))
        coefficients = float(np.max(abs(basis.coefficients - old.coefficients)))
        native = float(np.max(abs(basis.values - old.values)))
        checks.extend([
            dict(name=str(count) + ': native basis and coefficients unchanged', passed=native == 0 and coefficients == 0),
            dict(name=str(count) + ': original absolute re-evaluation gate retained', passed=reevaluation < 1e-7, value=reevaluation),
            dict(name=str(count) + ': mass orthogonality retained', passed=basis.qr_orthogonality < 1e-10, value=basis.qr_orthogonality)])
        frequencies = np.array([.00002, .001, .1, 1., 3., 8., 20., 50., 59.])
        reference = []
        for raw in frequencies:
            frequency = mp.mpf(float(raw))
            compact = (frequency - basis.pivot) / (frequency + basis.pivot)
            values = [1 / mp.mpf(basis.norms[0]), (frequency - basis.mean) / mp.mpf(basis.norms[1])]
            for degree in range(2, count):
                value = compact * values[-1]
                for repeat in range(2):
                    value -= mp.fsum(values[index] * mp.mpf(basis.projections[degree, repeat, index]) for index in range(degree))
                values.append(value / mp.mpf(basis.norms[degree]))
            reference.append([float(value) for value in values])
        reference = np.asarray(reference)
        error = float(np.max(abs(basis.evaluate(frequencies) - reference) / np.maximum(1., abs(reference))))
        checks.append(dict(name=str(count) + ': independent70-digit pointwise reference', passed=error < 1e-10, value=error))
        step = 1e-4 * frequencies
        derivative = (-basis.evaluate(frequencies + 2 * step) + 8 * basis.evaluate(frequencies + step)
                      - 8 * basis.evaluate(frequencies - step) + basis.evaluate(frequencies - 2 * step)) / (12 * step[:, None])
        exact = basis.derivative(frequencies)
        derivative_error = float(linalg.norm(derivative - exact) / linalg.norm(exact))
        checks.append(dict(name=str(count) + ': analytic derivative matches independent finite differences', passed=derivative_error < 1e-6, value=derivative_error))
        rows.append(dict(count=count, old_absolute_reevaluation=float(np.max(abs(old.evaluate(old.nodes) - old.values))),
                         new_absolute_reevaluation=reevaluation, high_precision_error=error, derivative_error=derivative_error))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
                        change='Evaluate the two stored re-orthogonalization passes in their construction order; do not combine their rounded coefficients before subtraction.',
                        old_1e7_absolute_gate_unchanged=True, no_physical_change=True), __file__,
           [ROOT / 'consistent_spectral_basis.py', THERMAL_PARENT / 'stable_spectral_basis.py'])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']], rows=rows)), flush=True)


if __name__ == '__main__':
    main()
