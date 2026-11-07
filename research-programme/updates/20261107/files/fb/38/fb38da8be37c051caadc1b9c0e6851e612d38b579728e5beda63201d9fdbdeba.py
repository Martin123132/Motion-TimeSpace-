from dirac_amplitude import *
from mandl_skyrme import differential_weight


def main():
    modest()
    mp.mp.dps = 80
    folder = ROOT / 'results/polarization-amplitude'
    folder.mkdir(parents=True, exist_ok=False)
    checks, rows = [], []
    gamma = gamma_matrices()
    metric = [1, -1, -1, -1]
    for first in range(4):
        for second in range(4):
            residual = gamma[first] * gamma[second] + gamma[second] * gamma[first] - (2 * metric[first] * mp.eye(4) if first == second else mp.zeros(4))
            checks.append(check('Clifford algebra ' + str(first) + str(second), float(mp.norm(residual)), 1e-50))
    configurations = [(.00045962015785263325, .01, [.7, .2, -.3], [-.3, .5, .6]),
        (.1, .2, [.4, -.8, .2], [.3, .2, -.9]), (1., .1, [-.4, .1, .8], [.2, .9, .1]),
        (.00045962015785263325, .4, [.1, -.5, .3], [.7, .3, -.2])]
    for index, (energy, fraction, hard, soft) in enumerate(configurations):
        sample = event(energy, fraction, hard, soft)
        amplitudes = tensor_for_event(sample)
        norm = linalg.norm(amplitudes.ravel())
        actual = float(np.sum(abs(amplitudes) ** 2) / 4)
        directions = sample['directions']
        cosines = [float(sum(directions[first][axis] * directions[second][axis] for axis in range(3))) for first, second in [(0, 1), (0, 2), (1, 2)]]
        reference = differential_weight(energy, fraction, *cosines) * float(sample['denominator'] / sample['photons'][1][0])
        error = abs(actual / reference - 1)
        checks.append(check('Direct spin/polarization sum equals sourced X event=' + str(index), error, 1e-11))
        ward_errors = []
        for leg in range(3):
            ward = tensor_for_event(sample, ward=leg)
            error = linalg.norm(ward.ravel()) / norm
            checks.append(check('Ward identity on leg=' + str(leg) + ' event=' + str(index), error, 1e-45))
            ward_errors.append(error)
        swapped = dict(sample, photons=[sample['photons'][0], sample['photons'][2], sample['photons'][1]],
            frames=[sample['frames'][0], sample['frames'][2], sample['frames'][1]])
        exchange = tensor_for_event(swapped).swapaxes(1, 2)
        checks.append(check('Outgoing Bose exchange symmetry event=' + str(index), linalg.norm((exchange - amplitudes).ravel()) / norm, 1e-14))
        kraus = amplitudes.transpose(3, 4, 1, 2, 0).reshape(4, 4, 2) / math.sqrt(2)
        vector = np.array([1., .3 + .4j])
        density = np.outer(vector, vector.conj()) / (vector.conj() @ vector)
        output = np.einsum('kai,ij,kbj->ab', kraus, density, kraus.conj())
        eigenvalues = linalg.eigvalsh(output)
        checks.append(check('Polarized outgoing pair density positive event=' + str(index), max(0., -min(eigenvalues)) / max(eigenvalues), 1e-12))
        if index == 0:
            broken = tensor_for_event(sample, ward=0, omit=(0, 1, 2))
            failure = linalg.norm(broken.ravel()) / norm
            checks.append(dict(name='Omitting one diagram is detected by Ward negative control', passed=failure > 1e-3, value=float(failure)))
        np.savez_compressed(folder / ('event-' + str(index) + '.npz'), amplitudes=amplitudes,
            kraus=kraus, polarized_pair_density=output, ward_errors=ward_errors)
        rows.append(dict(energy=energy, share=fraction, direct_squared=actual, source_squared=reference, relative_error=abs(actual / reference - 1)))
        print(json.dumps(rows[-1]), flush=True)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
        arithmetic_decimal_places=80, six_diagrams=True, electron_width=0,
        spinor_normalization='ubar u=2m, m=1; incoming spin and photon averaged by1/4 in X.',
        polarization_averaging_deferred_until_requested=True, normalization_fitted=False,
        thermal_phase_space_not_integrated=True), __file__,
        [ROOT / 'dirac_amplitude.py', ROOT / 'sources/2203.05252v1.html', PARENT / 'mandl_skyrme.py',
         BRANCH / 'scaled-spectral-evolution-20261007/sources/2005.06941v1.html'])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    main()
