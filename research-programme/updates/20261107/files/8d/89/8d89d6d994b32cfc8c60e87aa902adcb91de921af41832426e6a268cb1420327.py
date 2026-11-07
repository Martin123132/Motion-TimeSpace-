from angular_common import *
from source_jet import collision_jet, force_moments, boost_force, boost_force_jet
from verify_operator import angular_fixture
from check_mode_source_scales import spectral_shapes


def main():
    import heat_source_jet as earlier
    modest()
    folder = ROOT / 'results/bridges'
    assert not folder.exists()
    checks, inputs = [], [ROOT / 'source_jet.py', ROOT / 'verify_operator.py',
                          ROOT / 'check_mode_source_scales.py', PARENT / 'heat_source_jet.py']
    def check(name, error, gate=1e-10):
        checks.append(dict(name=name, passed=bool(error < gate), value=float(error), gate=gate))
    kernel = AngularKernel(10, 20)
    nodes, weights = np.polynomial.legendre.leggauss(200)
    frequency, quadrature = 30 * (nodes + 1), 30 * weights
    occupation, gradient, derivative, derivative2 = spectral_shapes(frequency)
    first0 = -gradient
    second0 = -derivative
    coefficients = np.array([.03, -.02, .004])
    scalar_values = np.vstack([occupation, coefficients[:, None] * gradient])
    scalar_first = np.vstack([first0, coefficients[:, None] * derivative])
    scalar_second = np.vstack([second0, coefficients[:, None] * derivative2])
    values = scalar_values[:, :, None, None, None] * kernel.projector
    first = scalar_first[:, :, None, None, None] * kernel.projector
    second = scalar_second[:, :, None, None, None] * kernel.projector
    ratios, densities = [1.01, .03, -.02, .004], [.02, -.03, .007]
    full = collision_jet(kernel, frequency, values, first, second, ratios, densities, 1.)
    forces = force_moments(kernel, frequency, quadrature, full)
    old_heat = earlier.heat_jet(frequency, quadrature, *scalar_values, ratios, densities) / I3_PLANCK
    check('General tensor source recovers saved Stage70 isotropic heat jet', np.max(abs(forces[:, 0] - old_heat)), 1e-9)
    check('Isotropic heat jet has no spurious rest momentum', np.max(abs(forces[:, 1:])))
    velocities = np.array([[.02, .01, -.005], [-.01, .015, .007], [.001, -.002, .003]])
    old_force = earlier.conformal_force_jet(old_heat, *velocities)
    check('General force boost recovers Stage70 isotropic boosted source', np.max(abs(boost_force_jet(forces, velocities) - old_force)), 1e-9)
    rotation, _ = np.linalg.qr(np.array([[.4, -.7, .2], [.3, .1, -.5], [.8, .3, .7]]))
    if np.linalg.det(rotation) < 0:
        rotation[:, 0] *= -1
    rotated = AngularKernel(10, 20)
    rotated.directions = kernel.directions @ rotation.T
    rotated.projector = screen(rotated.directions)
    rotated.epsilon = np.einsum('ijk,nk->nij', EPSILON, rotated.directions)
    fixture = angular_fixture(kernel.directions)
    transformed = rotation @ fixture @ rotation.T
    for name in ['scatter', 'recoil_angular', 'thermal_angular']:
        expected = rotation @ getattr(kernel, name)(fixture) @ rotation.T
        actual = getattr(rotated, name)(transformed)
        check('Tensor rotation covariance: ' + name, np.max(abs(actual - expected)))
    base_force = np.array([.7, -.1, .3, .2])
    velocity = np.array([.2, -.1, .05])
    changed = boost_force(base_force, velocity)
    invariant = lambda vector: -vector[0] ** 2 + vector[1:] @ vector[1:]
    check('General four-force boost preserves Lorentz norm', abs(invariant(changed) - invariant(base_force)))
    check('General four-force boost is invertible', np.max(abs(boost_force(changed, -velocity) - base_force)))
    for label in ['heavy', 'cold']:
        wave_path = WAVES / 'runs' / (label + '-sixteenth') / 'evolution.npz'
        with np.load(wave_path) as saved:
            states = saved['final_state']
        photons = states[:2, 26:26 + 9 * kernel.count].reshape(2, kernel.count, 3, 3)
        velocities = states[:2, 23:26]
        for index in range(2):
            rest = photons[index] / 2 - (kernel.directions @ velocities[index])[:, None, None] * kernel.projector
            lifted = gradient[:, None, None, None] * rest
            spectral_cold = kernel.scatter(lifted) - lifted
            integrated = np.einsum('x,xnij->nij', quadrature * frequency ** 3 / (2 * I3_PLANCK), spectral_cold)
            expected = (kernel.scatter(photons[index]) - photons[index]
                        + 2 * (kernel.directions @ velocities[index])[:, None, None] * kernel.projector)
            error = np.linalg.norm(integrated - expected) / np.linalg.norm(expected)
            check(label + ': first-order spectral lift recovers retained moving-baryon cold collision ' + str(index), error, 1e-7)
        inputs.append(wave_path)
    folder.mkdir(parents=True, exist_ok=False)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        earlier_isotropic_and_moving_baryon_limits_preserved=True,
                        second_order_spectral_reconstruction_not_assumed=True), __file__, inputs)
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    main()
