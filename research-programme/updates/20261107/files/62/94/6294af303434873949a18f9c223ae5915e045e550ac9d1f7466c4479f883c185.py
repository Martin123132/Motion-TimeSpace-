from angular_common import *


def anticommutator(left, right):
    return left @ right + right @ left


def collision_jet(kernel, frequency, values, first, second, ratios, densities, theta_ref):
    thermal = kernel.recoil_angular(second + 3 * first + 2 * values) + kernel.thermal_angular(values)
    shifted = kernel.recoil_angular(first + 2 * values)
    thomson = kernel.scatter(values) - values
    recoil = np.empty_like(values, dtype=complex)
    background = values[0] + .5 * kernel.projector
    recoil[0] = anticommutator(background, shifted[0]) + 2 * values[0]
    for index in [1, 2]:
        recoil[index] = (anticommutator(background, shifted[index])
                         + anticommutator(values[index], shifted[0]) + 2 * values[index])
    recoil[3] = (anticommutator(background, shifted[3]) + anticommutator(values[3], shifted[0])
                 + .5 * (anticommutator(values[1], shifted[2]) + anticommutator(values[2], shifted[1]))
                 + 2 * values[3])
    recoil *= frequency[None, :, None, None, None]
    temperature = np.empty_like(thermal)
    temperature[0] = ratios[0] * thermal[0]
    for index in [1, 2]:
        temperature[index] = ratios[0] * thermal[index] + ratios[index] * thermal[0]
    temperature[3] = (ratios[0] * thermal[3] + ratios[3] * thermal[0]
                      + .5 * (ratios[1] * thermal[2] + ratios[2] * thermal[1]))
    raw = thomson + theta_ref * (temperature + recoil)
    output = raw.copy()
    for index in [1, 2]:
        output[index] += densities[index - 1] * raw[0]
    output[3] += densities[2] * raw[0] + .5 * (densities[0] * raw[2] + densities[1] * raw[1])
    return output


def force_moments(kernel, frequency, quadrature, collision):
    heat, force = kernel.moments(collision)
    energy_weight = quadrature * frequency ** 3 / (2 * I3_PLANCK)
    return np.concatenate([np.einsum('x,...x->...', energy_weight, heat)[..., None],
                           np.einsum('x,...xi->...i', energy_weight, force)], axis=-1)


def boost_force(force, velocity):
    speed2 = velocity @ velocity
    if speed2 == 0:
        return force.copy()
    gamma = 1 / math.sqrt(1 - speed2)
    heat = gamma * (force[0] + velocity @ force[1:])
    momentum = force[1:] + ((gamma - 1) * (velocity @ force[1:]) / speed2 + gamma * force[0]) * velocity
    return np.r_[heat, momentum]


def boost_force_jet(forces, velocities):
    output = forces.copy()
    heat0, force0 = forces[0, 0], forces[0, 1:]
    velocity_p, velocity_q, velocity2 = velocities
    for index, velocity in zip([1, 2], [velocity_p, velocity_q]):
        output[index, 0] += velocity @ force0
        output[index, 1:] += heat0 * velocity
    output[3, 0] += (velocity2 @ force0 + .5 * (velocity_p @ forces[2, 1:] + velocity_q @ forces[1, 1:])
                     + .5 * (velocity_p @ velocity_q) * heat0)
    output[3, 1:] += (heat0 * velocity2 + .5 * (forces[1, 0] * velocity_q + forces[2, 0] * velocity_p)
                      + .25 * (velocity_p * (velocity_q @ force0) + velocity_q * (velocity_p @ force0)))
    return output


def verify():
    from verify_operator import angular_fixture
    modest()
    folder = ROOT / 'results/source-jet'
    assert not folder.exists()
    kernel = AngularKernel(8, 16)
    nodes, weights = np.polynomial.legendre.leggauss(160)
    frequency = 30 * (nodes + 1)
    quadrature = 30 * weights
    directions = kernel.directions
    fixture = angular_fixture(directions)
    shapes = np.stack([fixture, .03 * fixture * (1 + directions[:, 0, None, None]),
                       -.02 * fixture * (1 + directions[:, 1, None, None]),
                       .004 * fixture * (1 + directions[:, 2, None, None])])
    exponential = np.exp(-frequency)
    powers = np.array([0., 1., 2., 1.])
    factors = frequency[None, :] ** powers[:, None] * exponential
    values = factors[:, :, None, None, None] * shapes[:, None]
    first = (powers[:, None] - frequency)[..., None, None, None] * values
    second = ((powers[:, None] - frequency) ** 2 - frequency)[..., None, None, None] * values
    ratios = np.array([.93, .03, -.02, .005])
    densities = np.array([.02, -.03, .007])
    theta = .0003
    velocities = np.array([[.02, .01, -.005], [-.01, .015, .007], [.001, -.002, .003]])
    predicted = collision_jet(kernel, frequency, values, first, second, ratios, densities, theta)
    forces = force_moments(kernel, frequency, quadrature, predicted)
    boosted = boost_force_jet(forces, velocities)
    def exact(left, right):
        amplitudes = np.array([1., left, right, 2 * left * right])
        spectrum = np.einsum('a,axnij->xnij', amplitudes, values)
        derivative = np.einsum('a,axnij->xnij', amplitudes, first)
        derivative2 = np.einsum('a,axnij->xnij', amplitudes, second)
        ratio = amplitudes @ ratios
        density = 1 + np.array([left, right, 2 * left * right]) @ densities
        velocity = np.array([left, right, 2 * left * right]) @ velocities
        collision = kernel.collision(frequency, spectrum, derivative, derivative2, ratio)
        response = density * (collision['thomson'] + theta * collision['correction'])
        force = force_moments(kernel, frequency, quadrature, response)
        return response, boost_force(force, velocity)
    checks = []
    for step in [.02, .01, .005]:
        probes = [exact(step, step), exact(step, -step), exact(-step, step), exact(-step, -step)]
        mixed = (probes[0][0] - probes[1][0] - probes[2][0] + probes[3][0]) / (8 * step ** 2)
        mixed_force = (probes[0][1] - probes[1][1] - probes[2][1] + probes[3][1]) / (8 * step ** 2)
        tensor_error = float(np.linalg.norm(mixed - predicted[3]) / np.linalg.norm(predicted[3]))
        force_error = float(np.linalg.norm(mixed_force - boosted[3]) / np.linalg.norm(boosted[3]))
        checks.extend([
            dict(name='Independent density/temperature/polarized collision mixed derivative ' + str(step),
                 passed=tensor_error < 1e-5, value=tensor_error, gate=1e-5),
            dict(name='Independent full four-force boost mixed derivative ' + str(step),
                 passed=force_error < 1e-5, value=force_error, gate=1e-5),
        ])
    matter = -boosted
    checks.append(dict(name='Opposite four-force sources cancel in every perturbative column',
                       passed=bool(np.max(abs(matter + boosted)) == 0)))
    source_number = np.einsum('x,ax->a', quadrature * frequency ** 2, kernel.moments(predicted)[0])
    number_error = float(np.max(abs(source_number)))
    checks.append(dict(name='Quadratic source conserves photon number independently',
                       passed=number_error < 1e-10, value=number_error, gate=1e-10))
    folder.mkdir(parents=True, exist_ok=False)
    np.savez_compressed(folder / 'source.npz', frequency=frequency, forces=forces, boosted=boosted,
                        matter=matter, quadratic_collision=predicted[3])
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        coefficient_convention='f=f0+u*fp+v*fq+2*u*v*f_pq; stored pq is half mixed derivative',
                        force_units='Multiply by kappa0*rho_ref for conformal tetrad force; divide by a for proper force',
                        equilibrium_source_not_fitted=True, cosmological_evolution_not_run_here=True), __file__,
           [ROOT / 'verify_operator.py'])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    verify()
