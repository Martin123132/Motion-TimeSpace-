from angular_common import *


def angular_fixture(directions):
    projector = screen(directions)
    tensor = np.array([[.4, .1, -.2], [.1, -.3, .13], [-.2, .13, -.1]])
    vector = np.array([.2, -.15, .3])
    scalar = (1 + directions @ vector + .07 * directions[:, 0] * directions[:, 1]
              + .04 * directions[:, 0] * directions[:, 1] * directions[:, 2]
              + .02 * special.eval_legendre(5, directions[:, 2]))
    polarized = transverse_traceless(tensor, projector)
    polarized *= (.1 + .04 * directions[:, 0])[..., None, None]
    handed = np.einsum('ijk,nk->nij', EPSILON, directions)
    circular = .025 * (1 + .2 * directions[:, 1] + .1 * directions[:, 2] ** 2)
    return scalar[:, None, None] * projector + polarized - .5j * circular[:, None, None] * handed


def boost_direction(directions, velocity):
    speed2 = velocity @ velocity
    gamma = 1 / math.sqrt(1 - speed2)
    doppler = gamma * (1 - directions @ velocity)
    correction = ((gamma - 1) * (directions @ velocity) / speed2 - gamma)[:, None] * velocity
    return (directions + correction) / doppler[:, None], doppler


def moving_thomson(output_directions, velocity, power, integration_grid):
    speed2 = velocity @ velocity
    gamma = 1 / math.sqrt(1 - speed2)
    spatial = np.eye(3) + (gamma - 1) * np.outer(velocity, velocity) / speed2
    rest_directions = integration_grid.directions
    lab_incoming, inverse_doppler = boost_direction(rest_directions, -velocity)
    rest_projector = integration_grid.projector
    incoming = rest_projector @ spatial @ angular_fixture(lab_incoming) @ spatial @ rest_projector
    mean = np.einsum('n,n,nij->ij', integration_grid.weights, inverse_doppler ** power, incoming)
    outgoing_rest, doppler = boost_direction(output_directions, velocity)
    outgoing_rest_projector = screen(outgoing_rest)
    gain_rest = 1.5 * outgoing_rest_projector @ mean @ outgoing_rest_projector
    gain_rest *= doppler[:, None, None] ** power
    projector = screen(output_directions)
    gain_lab = projector @ spatial @ gain_rest @ spatial @ projector
    return (1 - output_directions @ velocity)[:, None, None] * (gain_lab - angular_fixture(output_directions))


def main():
    modest()
    folder = ROOT / 'results/operator'
    assert not folder.exists()
    checks = []

    def check(name, value, gate=1e-10):
        checks.append(dict(name=name, passed=bool(value < gate), value=float(value), gate=gate))

    kernel = AngularKernel(12, 24)
    fixture = angular_fixture(kernel.directions)
    angular_recoil = kernel.recoil_angular(fixture)
    direct = 1.5 * kernel.projector @ np.einsum('nm,m,mij->nij',
        1 - kernel.directions @ kernel.directions.T, kernel.weights, fixture) @ kernel.projector
    check('Recoil angular map agrees with direct pair scattering', np.max(abs(direct - angular_recoil)))
    partner = fixture * (1 + .2 * kernel.directions[:, 1, None, None])
    bilinear_left = np.einsum('n,nij,nji->', kernel.weights, fixture, kernel.recoil_angular(partner))
    bilinear_right = np.einsum('n,nij,nji->', kernel.weights, partner, angular_recoil)
    check('Angular recoil map is self-adjoint in trace pairing', abs(bilinear_left - bilinear_right))
    energy, flux = kernel.moments(fixture)
    recoil_energy, recoil_flux = kernel.moments(angular_recoil)
    thermal_energy, thermal_flux = kernel.moments(kernel.thermal_angular(fixture))
    check('Recoil map preserves scalar angular average', abs(recoil_energy - energy))
    check('Recoil map dipole coefficient is minus two fifths', np.max(abs(recoil_flux + .4 * flux)))
    check('Thermal angular remainder scalar is minus twice intensity', abs(thermal_energy + 2 * energy))
    check('Thermal angular remainder dipole is two fifths', np.max(abs(thermal_flux - .4 * flux)))
    for power in [-2, 0, 3]:
        predicted = (power + 1) * (power + 2) * angular_recoil + kernel.thermal_angular(fixture)
        cold = kernel.scatter(fixture) - fixture
        errors = []
        for step in [.004, .002, .001]:
            derivative = np.zeros_like(cold)
            for axis in range(3):
                velocity = np.eye(3)[axis] * step
                derivative += (moving_thomson(kernel.directions, velocity, power, kernel)
                               + moving_thomson(kernel.directions, -velocity, power, kernel) - 2 * cold) / (2 * step ** 2)
            errors.append(float(np.linalg.norm(derivative - predicted) / np.linalg.norm(predicted)))
        check('Independent moving-electron thermal tensor, spectral power ' + str(power), errors[-1], 1e-4)
        checks.append(dict(name='Velocity-refinement convergence, spectral power ' + str(power),
                           passed=bool(errors[-1] < .4 * errors[-2] and errors[-2] < .4 * errors[-3]), errors=errors))
    nodes, quadrature = np.polynomial.legendre.leggauss(240)
    frequency = 30 * (nodes + 1)
    quadrature *= 30
    spectral = .2 * np.exp(-frequency)
    value = spectral[:, None, None, None] * fixture
    first = -frequency[:, None, None, None] * value
    second = (frequency ** 2 - frequency)[:, None, None, None] * value
    result = kernel.collision(frequency, value, first, second, electron_ratio=.87)
    for label, collision in result.items():
        number = np.dot(quadrature * frequency ** 2, kernel.moments(collision)[0])
        scale = np.dot(quadrature * frequency ** 2, np.abs(kernel.moments(value)[0]))
        check('Photon number moment: ' + label, abs(number) / scale, 1e-7)
        transversality = np.max(abs(np.einsum('ni,xnij->xnj', kernel.directions, collision)))
        check('Polarization transversality: ' + label, transversality)
        check('Physical Hermiticity: ' + label, np.max(abs(collision - np.swapaxes(collision.conj(), -1, -2))))
    energy_spectrum, flux_spectrum = kernel.moments(value)
    energy_integral = np.dot(quadrature * frequency ** 3, energy_spectrum)
    flux_integral = np.einsum('x,xi->i', quadrature * frequency ** 3, flux_spectrum)
    thermal_energy, thermal_flux = kernel.moments(result['thermal'])
    check('Thermal energy transfer is four times photon energy',
          abs(np.dot(quadrature * frequency ** 3, thermal_energy) - 4 * energy_integral) / energy_integral, 1e-7)
    check('Thermal momentum transfer is minus twice photon flux',
          np.linalg.norm(np.einsum('x,xi->i', quadrature * frequency ** 3, thermal_flux) + 2 * flux_integral) / np.linalg.norm(flux_integral), 1e-7)
    pairing = np.einsum('n,xnij,xnji->x', kernel.weights, value, kernel.recoil_angular(value))
    predicted_heat = -np.dot(quadrature * frequency ** 4, energy_spectrum + pairing)
    actual_heat = np.dot(quadrature * frequency ** 3, kernel.moments(result['recoil'])[0])
    check('Induced recoil heat equals angular tensor-pair expression', abs(predicted_heat - actual_heat) / abs(predicted_heat), 1e-7)
    equilibrium_frequency = np.geomspace(.01, 30., 40)
    for electron_ratio, chemical in [(1., 0.), (.8, .3), (1.2, .1)]:
        occupation = 1 / np.expm1(equilibrium_frequency / electron_ratio + chemical)
        derivative = -equilibrium_frequency / electron_ratio * occupation * (1 + occupation)
        second_derivative = derivative + (equilibrium_frequency / electron_ratio) ** 2 * occupation * (1 + occupation) * (1 + 2 * occupation)
        equilibrium = kernel.collision(equilibrium_frequency, occupation[:, None, None, None] * kernel.projector,
            derivative[:, None, None, None] * kernel.projector, second_derivative[:, None, None, None] * kernel.projector, electron_ratio)
        error = np.linalg.norm(equilibrium['correction']) / np.linalg.norm(equilibrium['thermal'])
        check('Planck/Bose detailed balance r=' + str(electron_ratio) + ',mu=' + str(chemical), error)
    folder.mkdir(parents=True, exist_ok=False)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        thermal_U_independently_checked_with_moving_Thomson=True,
                        isotropic_polarized_density_normalization='f=n*screen, trace(f)=2n'), __file__)
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    main()
