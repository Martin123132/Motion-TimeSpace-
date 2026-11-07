from kernel_common import *


def slash(temporal, spatial):
    matrix = np.zeros((4, 4), dtype=complex)
    matrix[:2, :2] = temporal * np.eye(2)
    matrix[2:, 2:] = -temporal * np.eye(2)
    matrix[:2, 2:] = -spin(spatial)
    matrix[2:, :2] = spin(spatial)
    return matrix


def dirac_channels(energy, initial, final, initial_frame, final_frame):
    ratio = 1 / (1 + energy * (1 - initial @ final))
    final_energy = energy * ratio
    electron_energy = 1 + energy - final_energy
    electron_momentum = energy * initial - final_energy * final
    initial_spinor = np.sqrt(2) * np.vstack([np.eye(2), np.zeros((2, 2))])
    final_bar = np.sqrt(electron_energy + 1) * np.hstack([np.eye(2), -spin(electron_momentum) / (electron_energy + 1)])
    result = np.empty((2, 2, 2, 2), complex)
    for outgoing in range(2):
        outgoing_slash = slash(0., final_frame[:, outgoing])
        for incoming in range(2):
            incoming_slash = slash(0., initial_frame[:, incoming])
            propagator = (outgoing_slash @ (slash(1 + energy, energy * initial) + np.eye(4)) @ incoming_slash / (2 * energy)
                          - incoming_slash @ (slash(1 - final_energy, -final_energy * final) + np.eye(4)) @ outgoing_slash / (2 * final_energy))
            result[outgoing, incoming] = final_bar @ propagator @ initial_spinor / (2 * np.sqrt(2))
    return result.transpose(2, 3, 0, 1).reshape(4, 2, 2)


def main():
    modest()
    folder = ROOT / 'results/channels'
    assert not folder.exists()
    generator = np.random.default_rng(7301)
    errors = dict(dirac=[], scalar=[], linear=[], positivity=[], frame=[], adjoint=[])
    for index in range(48):
        initial, final = generator.normal(size=(2, 3))
        initial /= np.linalg.norm(initial)
        final /= np.linalg.norm(final)
        initial_frame, final_frame = frames(initial), frames(final)
        energy = 10 ** generator.uniform(-4, 1)
        channels, ratio = rest_channels(energy, initial, final, initial_frame, final_frame)
        direct = dirac_channels(energy, initial, final, initial_frame, final_frame)
        errors['dirac'].append(np.max(abs(channels - direct)))
        cosine = initial @ final
        unpolarized = gain(channels, np.eye(2))
        expected = (ratio + 1 / ratio - 1 + cosine ** 2) / 2
        errors['scalar'].append(abs(np.trace(unpolarized).real / 2 - expected))
        vector = generator.normal(size=2)
        vector /= np.linalg.norm(vector)
        state = np.outer(vector, vector)
        polarized = gain(channels, state)
        expected_linear = (ratio + 1 / ratio - 2 * (final @ initial_frame @ vector) ** 2) / 2
        errors['linear'].append(abs(np.trace(polarized).real - expected_linear))
        errors['positivity'].append(max(0., -float(np.min(np.linalg.eigvalsh(polarized)))))
        arbitrary = generator.normal(size=(2, 2)) + 1j * generator.normal(size=(2, 2))
        arbitrary = (arbitrary + arbitrary.conj().T) / 2
        errors['adjoint'].append(abs(np.trace(arbitrary @ gain(channels, state)) - np.trace(adjoint(channels, arbitrary) @ state)))
        velocity = .15 * generator.normal(size=3)
        rest_direction, _, spatial = boost(initial, velocity)
        rest_frame = transport_frames(rest_direction, initial_frame, spatial)
        errors['frame'].append(np.max(abs(rest_frame.T @ rest_frame - np.eye(2))))
    checks = [dict(name=name + ': independent physical channel identity', passed=float(max(values)) < 1e-9,
                   value=float(max(values)), gate=1e-9) for name, values in errors.items()]
    initial = np.array([0., 0., 1.])
    final = np.array([.6, 0., .8])
    initial_frame, final_frame = frames(initial), frames(final)
    channels, _ = rest_channels(0., initial, final, initial_frame, final_frame)
    state = np.array([[.7, .2 + .1j], [.2 - .1j, .3]])
    jones = final_frame.T @ initial_frame
    thomson_error = float(np.max(abs(gain(channels, state) - jones @ state @ jones.T)))
    checks.append(dict(name='Exact zero-energy polarized Thomson channel', passed=thomson_error < 1e-12, value=thomson_error))
    normalization = []
    for theta in [1e-5, 4.596201578526332e-4, .01]:
        speed, weights = juttner_rule(theta, 12)
        normalization.append(dict(theta=theta, normalization=float(weights.sum()), maximum_speed=float(max(speed)),
                                  mean_gamma=float(np.dot(weights, 1 / np.sqrt(1 - speed ** 2)))))
    checks.append(dict(name='Relativistic electron quadrature positive normalized and strictly subluminal',
                       passed=all(abs(row['normalization'] - 1) < 1e-14 and row['maximum_speed'] < 1 for row in normalization)))
    assert all(row['passed'] for row in checks), checks
    folder.mkdir(parents=True, exist_ok=False)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=True,
                        juttner_rows=normalization, exact_tree_level_spin_channels_not_fitted=True,
                        electron_spin_unpolarized_and_final_spin_summed=True,
                        radiative_loop_corrections_not_included=True), __file__)
    print(json.dumps(dict(checks=checks)), flush=True)


if __name__ == '__main__':
    main()
