import argparse
from kernel_common import *


KINDS = ['intensity', 'linear', 'circular']
POWERS = np.array([0, 1, 2])


def integrate_kernel(frequency, theta, direction, radial=6, electron_polar=4, photon_polar=8):
    electrons = angular.AngularKernel(electron_polar, 2 * electron_polar)
    photons = angular.AngularKernel(photon_polar, 2 * photon_polar)
    speeds, radial_weights = juttner_rule(theta, radial)
    initial_frame = frames(direction)
    initial_values = np.stack([initial_frame.T @ fixture(direction, kind) @ initial_frame for kind in KINDS])
    rest_final = photons.directions
    rest_final_frame = frames(rest_final)
    output = np.zeros((len(POWERS), len(KINDS), 2, 2), dtype=complex)
    for speed, radial_weight in zip(speeds, radial_weights):
        for electron_direction, electron_weight in zip(electrons.directions, electrons.weights):
            beta = speed * electron_direction
            initial_rest, incident_factor, spatial = boost(direction, beta)
            initial_rest_frame = transport_frames(initial_rest, initial_frame, spatial)
            final_lab, final_factor, _ = boost(rest_final, -beta)
            final_lab_frame = transport_frames(final_lab, rest_final_frame, spatial)
            rest_frequency = frequency * incident_factor
            channels, ratio = rest_channels(theta * rest_frequency, initial_rest, rest_final,
                                             initial_rest_frame, rest_final_frame)
            final_frequency = rest_frequency * ratio * final_factor
            final_values = np.stack([final_lab_frame.swapaxes(-1, -2) @ fixture(final_lab, kind) @ final_lab_frame for kind in KINDS])
            mapped = np.einsum('nsai,knab,nsbj->knij', channels.conj(), final_values, channels)
            loss = adjoint(channels, np.eye(2))
            anticommutator = (loss[None, ...] @ initial_values[:, None, ...]
                              + initial_values[:, None, ...] @ loss[None, ...]) / 2
            difference = final_frequency[None, None, :, None, None] ** POWERS[:, None, None, None, None] * mapped[None, ...]
            difference -= frequency ** POWERS[:, None, None, None, None] * anticommutator[None, ...]
            bose = (1 + 1 / np.expm1(final_frequency)) / (1 + 1 / np.expm1(frequency))
            weights = radial_weight * electron_weight * photons.weights * 1.5 * ratio ** 2 * (1 - direction @ beta) * bose
            output += np.einsum('n,pknij->pkij', weights, difference)
    return initial_frame @ output @ initial_frame.T


def parent_values(frequency, output_directions):
    kernel = angular.AngularKernel(12, 24)
    kernel.directions = np.concatenate([kernel.directions, output_directions])
    kernel.weights = np.r_[kernel.weights, np.zeros(len(output_directions))]
    kernel.projector = angular.screen(kernel.directions)
    kernel.epsilon = np.einsum('ijk,nk->nij', angular.EPSILON, kernel.directions)
    kernel.count = len(kernel.weights)
    values = np.stack([fixture(kernel.directions, kind) for kind in KINDS])
    scatter, recoil, thermal = kernel.scatter(values), kernel.recoil_angular(values), kernel.thermal_angular(values)
    occupation = 1 / np.expm1(frequency)
    local = 2 * frequency * (1 + 2 * occupation) - 2 * frequency ** 2 * occupation * (1 + occupation)
    cold, correction = [], []
    for power in POWERS:
        diffusion = power * (power + 3 - frequency * (1 + 2 * occupation)) * frequency ** power
        cold.append(frequency ** power * (scatter - values))
        correction.append(diffusion * recoil + frequency ** power * (thermal + 2 * recoil + local * (values - recoil)))
    return np.array(cold)[..., -len(output_directions):, :, :], np.array(correction)[..., -len(output_directions):, :, :]


def main(name, refined=False, pilot=False):
    modest()
    folder = ROOT / 'results' / name
    assert not folder.exists()
    started = time.perf_counter()
    directions = np.array([[0., 0., 1.], [1., 0., 0.], [.3, -.4, np.sqrt(.75)]])
    frequencies = [1., 3., 8.]
    if pilot:
        directions, frequencies = directions[:1], [3.]
    ladder = [8e-5, 4e-5, 2e-5] if not refined else [4e-5, 2e-5, 1e-5]
    settings = dict(radial=6 if not refined else 8, electron_polar=4 if not refined else 6,
                    photon_polar=8 if not refined else 10)
    rows, checks, saved = [], [], {}
    folder.mkdir(parents=True, exist_ok=False)
    for frequency in frequencies:
        cold, correction = parent_values(frequency, directions)
        for output_index, direction in enumerate(directions):
            calculations = []
            for theta in ladder:
                actual = integrate_kernel(frequency, theta, direction, **settings)
                calculations.append((actual - cold[:, :, output_index]) / theta)
            extrapolated = (calculations[0] - 6 * calculations[1] + 8 * calculations[2]) / 3
            target = correction[:, :, output_index]
            for power_index, power in enumerate(POWERS):
                for kind_index, kind in enumerate(KINDS):
                    error = float(np.linalg.norm(extrapolated[power_index, kind_index] - target[power_index, kind_index])
                                  / max(np.linalg.norm(target[power_index, kind_index]), 1e-8))
                    row = dict(frequency=frequency, output_direction=output_index, power=int(power), kind=kind,
                               relative_coefficient_error=error)
                    rows.append(row)
            saved['coefficient_' + str(frequency) + '_' + str(output_index)] = extrapolated
            saved['target_' + str(frequency) + '_' + str(output_index)] = target
            write_json(folder / 'progress.json', dict(state='running', frequency=frequency, direction=output_index,
                       max_error=max(row['relative_coefficient_error'] for row in rows), elapsed_seconds=time.perf_counter() - started))
            print(json.dumps(dict(frequency=frequency, direction=output_index,
                                 max_error=max(row['relative_coefficient_error'] for row in rows), elapsed=time.perf_counter() - started)), flush=True)
    for kind in KINDS:
        error = max(row['relative_coefficient_error'] for row in rows if row['kind'] == kind)
        checks.append(dict(name=kind + ': finite-shift first-order tensor matches parent', passed=error < 1e-4, value=error, gate=1e-4))
    np.savez_compressed(folder / 'coefficients.npz', **saved)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        rows=rows, settings=settings, temperature_ladder=ladder,
                        exact_spin_channels_and_Juttner_electron_measure=True,
                        first_order_coefficient_test_not_full_grid_evolution=True,
                        elapsed_seconds=time.perf_counter() - started), __file__)
    print(json.dumps(dict(checks=checks)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--refined', action='store_true')
    parser.add_argument('--pilot', action='store_true')
    arguments = parser.parse_args()
    main(arguments.name, arguments.refined, arguments.pilot)
