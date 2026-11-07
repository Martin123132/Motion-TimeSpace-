from dirac_amplitude import *


def main():
    modest()
    mp.mp.dps = 80
    folder = ROOT / 'results/polarized-soft-factor'
    folder.mkdir(parents=True, exist_ok=False)
    checks, rows = [], []
    for energy in [.00045962015785263325, .1, 1.]:
        hard, soft = [.7, .2, -.3], [-.3, .5, .6]
        single, final = single_tensor(energy, hard)
        initial = mp.matrix([1, 0, 0, 0])
        errors = []
        for share in [1e-3, 1e-5, 1e-7]:
            sample = event(energy, share, hard, soft)
            exact = tensor_for_event(sample)
            soft_momentum = sample['photons'][2]
            current = final / dot(final, soft_momentum) - initial / dot(initial, soft_momentum)
            coefficients = [float(dot(current, polarization)) for polarization in sample['frames'][2]]
            predicted = single[:, :, None, :, :] * np.array(coefficients)[None, None, :, None, None]
            error = linalg.norm((exact - predicted).ravel()) / linalg.norm(exact.ravel())
            checks.append(check('Soft theorem in every spin/polarization channel energy=' + str(energy) + ' share=' + str(share), error, 10 * share))
            checks.append(check('Eikonal current Ward contraction energy=' + str(energy) + ' share=' + str(share), abs(float(dot(current, soft_momentum))), 1e-60))
            errors.append(float(error))
            rows.append(dict(energy=energy, share=share, relative_tensor_error=float(error)))
        checks.append(dict(name='Soft tensor error decreases linearly energy=' + str(energy), passed=errors[1] < .02 * errors[0] and errors[2] < .02 * errors[1], errors=errors))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
        scalar_soft_factor_times_polarized_hard_amplitude=True, no_polarization_average_used_for_soft_test=True,
        arithmetic_decimal_places=80), __file__, [ROOT / 'dirac_amplitude.py', ROOT / 'sources/hep-ph-9308249.html'])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']], rows=rows)), flush=True)


if __name__ == '__main__':
    main()
