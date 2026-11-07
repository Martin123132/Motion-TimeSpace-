from grid_common import *


def main():
    modest()
    folder = ROOT / 'results/angular-blocks'
    assert not folder.exists()
    generator = np.random.default_rng(7401)
    maximum = 0.
    for trial in range(100):
        initial, final = generator.normal(size=(2, 3))
        initial /= np.linalg.norm(initial)
        final /= np.linalg.norm(final)
        initial_frame, final_frame = prior.frames(initial), prior.frames(final)
        energy = 10 ** generator.uniform(-5, 1)
        channels, ratio = prior.rest_channels(energy, initial, final, initial_frame, final_frame)
        state = generator.normal(size=(2, 2)) + 1j * generator.normal(size=(2, 2))
        state = (state + state.conj().T) / 2
        expected = prior.gain(channels, state)
        actual = fano_gain(final_frame.T @ initial_frame, initial @ final, np.asarray(ratio + 1 / ratio - 2), state)
        maximum = max(maximum, float(np.linalg.norm(actual - expected) / max(np.linalg.norm(state), 1e-30)))
    checks = [dict(name='Exact Jones-plus-recoil map matches all physical Dirac spin channels',
                   passed=maximum < 1e-9, value=maximum, gate=1e-9)]
    events = event_geometry(4.596201578526332e-4, 4)
    saved = {}
    for degree in range(5):
        first, second, names = angular_correlations(events, degree)
        refined_first, refined_second, _ = angular_correlations(events, degree, 2)
        difference = float(max(np.max(abs(first - refined_first)), np.max(abs(second - refined_second))))
        checks.append(dict(name='Exact rotation-average axis quadrature degree' + str(degree),
                           passed=difference < 1e-10, value=difference))
        expected_first = (1 + events['cosine'] ** 2) * special.eval_legendre(degree, events['final_direction'][:, 2]) / (2 * degree + 1)
        expected_second = special.eval_legendre(degree, events['final_direction'][:, 2]) / (2 * degree + 1)
        scalar_error = float(max(np.max(abs(first[0, 0] - expected_first)), np.max(abs(second[0, 0] - expected_second))))
        checks.append(dict(name='Independent scalar addition theorem degree' + str(degree), passed=scalar_error < 1e-10, value=scalar_error))
        extra = .013
        total = first + extra * second
        bound = (1 + events['cosine'] ** 2 + extra) / (2 * degree + 1)
        largest = np.linalg.svd(total.transpose(2, 0, 1), compute_uv=False)[:, 0]
        violation = float(max(0., np.max(largest - bound)))
        checks.append(dict(name='Physical modal cross block respects pair-square contraction degree' + str(degree),
                           passed=violation < 1e-10, value=violation))
        saved['first_' + str(degree)] = first
        saved['second_' + str(degree)] = second
    assert all(row['passed'] for row in checks), checks
    folder.mkdir(parents=True, exist_ok=False)
    np.savez_compressed(folder / 'correlations.npz', **saved)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=True,
                        modal_rotation_average_not_fitted_moment_closure=True,
                        exact_Fano_recoil_map_checked_against_spin_amplitude=True), __file__)
    print(json.dumps(dict(checks=checks)), flush=True)


if __name__ == '__main__':
    main()
