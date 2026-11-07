from inclusive_soft import *


def oscillator_characteristic(count, frequency, displacement, conjugate):
    lowering = np.diag(np.sqrt(np.arange(1, count)), 1).astype(complex)
    raising = lowering.conj().T
    unitary = linalg.expm(displacement * raising - displacement.conjugate() * lowering)
    energies = frequency * np.arange(count)
    weights = np.exp(-energies)
    weights /= sum(weights)
    rotation = np.exp(1j * energies * conjugate)
    evolved = rotation[:, None] * unitary * rotation.conj()[None, :]
    characteristic = np.dot(weights, np.diag(unitary.conj().T @ evolved))
    defect = linalg.norm(unitary.conj().T @ unitary - np.eye(count)) / math.sqrt(count)
    return characteristic, defect


def main():
    modest()
    folder = ROOT / 'results/thermal-unitarity-origin'
    folder.mkdir(parents=True, exist_ok=False)
    checks, rows = [], []
    for frequency in [.3, 1., 2.]:
        for displacement in [.04 + .02j, .2 + .1j, .7 - .1j]:
            for conjugate in [0., .2, 1.4]:
                coarse, _ = oscillator_characteristic(100, frequency, displacement, conjugate)
                actual, unitary_error = oscillator_characteristic(140, frequency, displacement, conjugate)
                expected = np.exp(abs(displacement) ** 2 * thermal_bracket(frequency, conjugate))
                checks.extend([check('Exact thermal displacement trace equals derived inclusive bracket', abs(actual - expected), 1e-11),
                    check('Oscillator cutoff refinement', abs(actual - coarse), 1e-10),
                    check('Soft-current displacement is unitary', unitary_error, 1e-12)])
                rows.append(dict(frequency_over_temperature=frequency, displacement_real=displacement.real,
                    displacement_imaginary=displacement.imag, conjugate=conjugate, error=abs(actual - expected)))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
        virtual_coefficient_comes_from_unitarity_not_a_fitted_subtraction=True,
        scope='Independent finite-oscillator verification of the universal linear-current soft sector, not a replacement for finite hard QED loop terms.'), __file__,
        [ROOT / 'inclusive_soft.py', ROOT / 'sources/hep-ph-9308249.html'])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']], maximum=max(row['error'] for row in rows))), flush=True)


if __name__ == '__main__':
    main()
