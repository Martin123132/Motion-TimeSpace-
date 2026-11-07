from kernel_common import *
from verify_channels import slash


def spinor(energy, momentum):
    return np.sqrt(energy + 1) * np.vstack([np.eye(2), spin(momentum) / (energy + 1)])


def general_channels(electron_energy, electron_momentum, final_electron_energy, final_electron_momentum,
                     energy, initial, final_energy, final, initial_frame, final_frame):
    incident = spinor(electron_energy, electron_momentum)
    outgoing_bar = spinor(final_electron_energy, final_electron_momentum).conj().T @ np.diag([1, 1, -1, -1])
    denominator_initial = 2 * energy * (electron_energy - electron_momentum @ initial)
    denominator_final = 2 * final_energy * (electron_energy - electron_momentum @ final)
    result = np.empty((2, 2, 2, 2), dtype=complex)
    for outgoing in range(2):
        outgoing_slash = slash(0., final_frame[:, outgoing])
        for incoming in range(2):
            incoming_slash = slash(0., initial_frame[:, incoming])
            operator = (outgoing_slash @ (slash(electron_energy + energy, electron_momentum + energy * initial) + np.eye(4)) @ incoming_slash / denominator_initial
                        - incoming_slash @ (slash(electron_energy - final_energy, electron_momentum - final_energy * final) + np.eye(4)) @ outgoing_slash / denominator_final)
            result[outgoing, incoming] = outgoing_bar @ operator @ incident / (2 * np.sqrt(2))
    return result.transpose(2, 3, 0, 1).reshape(4, 2, 2)


def main():
    modest()
    folder = ROOT / 'results/reciprocity'
    assert not folder.exists()
    generator = np.random.default_rng(7302)
    reverse_errors, weight_errors, linear_errors, number_errors = [], [], [], []
    for trial in range(40):
        initial, final = generator.normal(size=(2, 3))
        initial /= np.linalg.norm(initial)
        final /= np.linalg.norm(final)
        initial_frame, final_frame = frames(initial), frames(final)
        theta = .01
        frequency = generator.uniform(.5, 5.)
        energy = theta * frequency
        forward, ratio = rest_channels(energy, initial, final, initial_frame, final_frame)
        final_energy = energy * ratio
        final_frequency = final_energy / theta
        electron_energy = 1 + energy - final_energy
        electron_momentum = energy * initial - final_energy * final
        reverse = general_channels(electron_energy, electron_momentum, 1., np.zeros(3),
                                    final_energy, final, energy, initial, final_frame, initial_frame)
        potential = generator.normal(size=(2, 2)) + 1j * generator.normal(size=(2, 2))
        potential = (potential + potential.conj().T) / 2
        reverse_errors.append(np.linalg.norm(gain(reverse, potential) - adjoint(forward, potential)) / max(np.linalg.norm(potential), 1e-30))
        initial_n, final_n = 1 / np.expm1(frequency), 1 / np.expm1(final_frequency)
        initial_w, final_w = initial_n * (1 + initial_n), final_n * (1 + final_n)
        reverse_electron = np.exp(final_frequency - frequency)
        weight_errors.append(abs(initial_n * (1 + final_n) - reverse_electron * final_n * (1 + initial_n)))
        other = generator.normal(size=(2, 2)) + 1j * generator.normal(size=(2, 2))
        other = (other + other.conj().T) / 2
        def nonlinear(occupation_initial, occupation_final):
            loss_initial = adjoint(forward, np.eye(2) + occupation_final)
            gain_initial = adjoint(forward, occupation_final)
            collision_initial = -(occupation_initial @ loss_initial + loss_initial @ occupation_initial) / 2
            collision_initial += reverse_electron * ((np.eye(2) + occupation_initial) @ gain_initial + gain_initial @ (np.eye(2) + occupation_initial)) / 2
            gain_final = gain(forward, occupation_initial)
            loss_final = gain(forward, np.eye(2) + occupation_initial)
            collision_final = ((np.eye(2) + occupation_final) @ gain_final + gain_final @ (np.eye(2) + occupation_final)) / 2
            collision_final -= reverse_electron * (occupation_final @ loss_final + loss_final @ occupation_final) / 2
            return collision_initial, collision_final
        step = 1e-4
        plus = nonlinear(initial_n * np.eye(2) + step * initial_w * potential,
                         final_n * np.eye(2) + step * final_w * other)
        minus = nonlinear(initial_n * np.eye(2) - step * initial_w * potential,
                          final_n * np.eye(2) - step * final_w * other)
        loss_initial, loss_final = adjoint(forward, np.eye(2)), gain(forward, np.eye(2))
        conductance = initial_n * (1 + final_n)
        target_initial = conductance * (adjoint(forward, other) - (potential @ loss_initial + loss_initial @ potential) / 2)
        target_final = conductance * (gain(forward, potential) - (other @ loss_final + loss_final @ other) / 2)
        linear_errors.append(max(np.linalg.norm((plus[0] - minus[0]) / (2 * step) - target_initial),
                                 np.linalg.norm((plus[1] - minus[1]) / (2 * step) - target_final))
                             / max(np.linalg.norm(target_initial), np.linalg.norm(target_final), 1e-30))
        number_errors.append(abs(np.trace(plus[0] + plus[1])))
    checks = [dict(name=name, passed=float(max(values)) < 1e-9, value=float(max(values)), gate=1e-9)
              for name, values in [('Reverse physical Dirac process equals forward adjoint after spin sum', reverse_errors),
                                   ('Juttner and Bose pair conductance is reciprocal', weight_errors),
                                   ('Reciprocal linear generator derives from induced matrix collision', linear_errors),
                                   ('Nonlinear matrix event transfers opposite photon counts', number_errors)]]
    folder.mkdir(parents=True, exist_ok=False)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        sampled_events=40, reciprocity_not_postulated_by_matrix_symmetrization=True,
                        electron_spin_summed_microreversibility_checked=True), __file__, [ROOT / 'verify_channels.py'])
    print(json.dumps(dict(checks=checks)), flush=True)


if __name__ == '__main__':
    main()
