from step_common import *


def scalar_compton(frequency, power, degree, theta, radial=10, angular=12, azimuthal=24):
    radius, radial_weights = special.roots_genlaguerre(radial, .5)
    radial_weights /= special.gamma(1.5)
    electron_cosine, electron_weights = np.polynomial.legendre.leggauss(angular)
    scattering_cosine, scattering_weights = np.polynomial.legendre.leggauss(angular)
    azimuth = 2 * np.pi * (np.arange(azimuthal) + .5) / azimuthal
    outgoing_cosine = scattering_cosine[:, None]
    outgoing_sine = np.sqrt(1 - outgoing_cosine ** 2)
    initial_direction = np.array([0., 0., 1.])
    total = 0.
    for radial_node, radial_weight in zip(radius, radial_weights):
        speed_squared = 2 * theta * radial_node
        assert speed_squared < 1
        gamma = 1 / np.sqrt(1 - speed_squared)
        for electron_node, electron_weight in zip(electron_cosine, electron_weights / 2):
            beta = np.sqrt(speed_squared) * np.array([np.sqrt(1 - electron_node ** 2), 0., electron_node])
            incident_factor = gamma * (1 - beta[2])
            rest_frequency = frequency * incident_factor
            incident_rest = (initial_direction + ((gamma - 1) * beta[2] / speed_squared - gamma) * beta) / incident_factor
            transverse = np.array([incident_rest[2], 0., -incident_rest[0]])
            second = np.cross(incident_rest, transverse)
            outgoing_rest = (outgoing_cosine[..., None] * incident_rest
                             + outgoing_sine[..., None] * (np.cos(azimuth)[None, :, None] * transverse
                                                         + np.sin(azimuth)[None, :, None] * second))
            energy_ratio = 1 / (1 + theta * rest_frequency * (1 - outgoing_cosine))
            boost_dot = np.einsum('...i,i->...', outgoing_rest, beta)
            outgoing_factor = gamma * (1 + boost_dot)
            final_frequency = rest_frequency * energy_ratio * outgoing_factor
            final_direction = (outgoing_rest + (((gamma - 1) * boost_dot / speed_squared + gamma)[..., None] * beta)) / outgoing_factor[..., None]
            rate = 3 / 8 * energy_ratio ** 2 * (energy_ratio + 1 / energy_ratio - 1 + outgoing_cosine ** 2)
            rate = rate * (1 - beta[2])
            induced = (1 + 1 / np.expm1(final_frequency)) / (1 + 1 / np.expm1(frequency))
            difference = final_frequency ** power * special.eval_legendre(degree, final_direction[..., 2]) - frequency ** power
            total += radial_weight * electron_weight * np.sum(scattering_weights[:, None] * rate * induced * difference) / azimuthal
    return float(total)


def main():
    modest()
    folder = ROOT / 'results/moving-kernel'
    assert not folder.exists()
    maps = AxisymmetricMaps(10)
    rows, checks = [], []
    for degree in range(4):
        angular_vector = np.r_[special.eval_legendre(degree, maps.cosine), np.zeros(maps.polar)]
        projector = maps.number * angular_vector * (2 * degree + 1)
        scatter = float(projector @ maps.scatter @ angular_vector)
        recoil = float(projector @ maps.recoil @ angular_vector)
        thermal = float(projector @ maps.thermal @ angular_vector)
        for frequency in [1., 3., 8.]:
            occupation = 1 / np.expm1(frequency)
            local = 2 * frequency * (1 + 2 * occupation) - 2 * frequency ** 2 * occupation * (1 + occupation)
            for power in [0, 1, 2]:
                potential = frequency ** power
                diffusion = power * (power + 3 - frequency * (1 + 2 * occupation)) * potential
                cold = (scatter - 1) * potential
                target = recoil * diffusion + (thermal + 2 * recoil) * potential + local * (1 - recoil) * potential
                coefficients = [(scalar_compton(frequency, power, degree, theta) - cold) / theta for theta in [4e-5, 2e-5, 1e-5]]
                extrapolated = (coefficients[0] - 6 * coefficients[1] + 8 * coefficients[2]) / 3
                relative = abs(extrapolated - target) / max(1, abs(target))
                rows.append(dict(degree=degree, frequency=frequency, power=power, cold_coefficient=cold,
                                 parent_coefficient=target, finite_kernel_coefficients=coefficients,
                                 extrapolated_coefficient=extrapolated, relative_mismatch=relative))
    maximum = max(row['relative_mismatch'] for row in rows)
    checks.append(dict(name='Actual moving-electron Klein-Nishina scalar expansion matches parent on 36 probes',
                       passed=maximum < 1e-5, value=maximum, gate=1e-5))
    refinement = []
    for degree in range(4):
        first = scalar_compton(8., 2, degree, 1e-5)
        second = scalar_compton(8., 2, degree, 1e-5, 12, 16, 32)
        refinement.append(abs(first - second) / 1e-5)
    checks.append(dict(name='Independent radial/angular scattering quadrature refinement',
                       passed=max(refinement) < 1e-6, value=max(refinement), gate=1e-6))
    folder.mkdir(parents=True, exist_ok=False)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        rows=rows, expansion_matching_passed=maximum < 1e-5,
                        full_polarized_kernel=False, exact_boost_and_recoil_kinematics=True,
                        normalized_nonrelativistic_Maxwell_velocity_used_for_first_order_limit=True,
                        finite_temperature_exact_detailed_balance_requires_Juttner_and_reciprocal_measure=True,
                        no_coefficients_fitted=True), __file__)
    print(json.dumps(dict(checks=checks, largest=sorted(rows, key=lambda row: -row['relative_mismatch'])[:5])), flush=True)


if __name__ == '__main__':
    main()
