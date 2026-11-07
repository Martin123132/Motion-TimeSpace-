from source_jet import anticommutator, force_moments
from angular_common import *


def summarize(label, suffix):
    path = WAVES / 'runs' / (label + '-' + suffix) / 'evolution.npz'
    with np.load(path, allow_pickle=False) as saved:
        maximum = int(saved['angular_maximum'])
        states = saved['final_state'].copy()
        moment = float(saved['times'][-1])
        end_scale = float(saved['end_scale'])
    kernel = AngularKernel(maximum + 4, 2 * (maximum + 4))
    photon = states[:2, 26:26 + 9 * kernel.count].reshape(2, kernel.count, 3, 3)
    velocity = states[:2, 23:26]
    rest = photon / 2 - np.einsum('ni,ai->an', kernel.directions, velocity)[..., None, None] * kernel.projector
    scalar = np.trace(rest, axis1=-2, axis2=-1)
    unpolarized = .5 * scalar[..., None, None] * kernel.projector
    means = np.einsum('n,an->a', kernel.weights, scalar)
    isotropic = .5 * means[:, None, None, None] * kernel.projector
    tensors = {}
    for name, amplitudes in [('full', rest), ('unpolarized', unpolarized), ('isotropic', isotropic)]:
        mapped = kernel.recoil_angular(amplitudes)
        source = .5 * (anticommutator(amplitudes[0], mapped[1]) + anticommutator(amplitudes[1], mapped[0]))
        tensors[name] = source
    bilinear = np.einsum('n,nij,nji->', kernel.weights, rest[0], kernel.recoil_angular(rest[1]))
    isotropic_bilinear = means[0] * means[1] / 2
    spectral_integral = 120 * (special.zeta(4, 1) - special.zeta(6, 1))
    multiplier = -spectral_integral / (4 * I3_PLANCK)
    forces = {name: multiplier * np.r_[kernel.moments(tensor)[0], kernel.moments(tensor)[1]]
              for name, tensor in tensors.items()}
    angular_temperature = spectral_integral / (8 * I3_PLANCK) * (bilinear - isotropic_bilinear)
    thermal_background = inherited.ThermalBackground(label)
    at = thermal_background.at(math.log(end_scale / thermal_background.start_scale))
    per_hubble = at['coefficient'] * forces['full']
    checks = []
    for points in [120, 240]:
        nodes, weights = np.polynomial.legendre.leggauss(points)
        frequency = 30 * (nodes + 1)
        quadrature = 30 * weights
        occupation = 1 / np.expm1(frequency)
        spectral = frequency * occupation * (1 + occupation)
        derivative = spectral * (1 - frequency * (1 + 2 * occupation))
        source = (frequency * spectral * (derivative + 2 * spectral))[:, None, None, None] * tensors['full']
        actual = force_moments(kernel, frequency, quadrature, source)
        error = float(np.linalg.norm(actual - forces['full']) / max(np.linalg.norm(forces['full']), 1e-100))
        checks.append(dict(name=label + '-' + suffix + ': spectral force agrees with exact integral ' + str(points),
                           passed=error < 1e-7, value=error, gate=1e-7))
    heat_error = abs(forces['full'][0] + spectral_integral * bilinear / (2 * I3_PLANCK))
    checks.append(dict(name=label + '-' + suffix + ': tensor and bilinear recoil heat agree',
                       passed=bool(heat_error < 1e-10), value=float(heat_error), gate=1e-10))
    payload = dict(directions=kernel.directions, weights=kernel.weights, rest_first_order=rest,
                   induced_angular_tensor=tensors['full'], unpolarized_tensor=tensors['unpolarized'],
                   isotropic_tensor=tensors['isotropic'], force_per_kappa_theta=forces['full'],
                   full_minus_isotropic_force=forces['full'] - forces['isotropic'],
                   polarization_contribution=forces['full'] - forces['unpolarized'],
                   force_per_hubble=per_hubble, angular_temperature_shift=angular_temperature)
    def components(array):
        return dict(real=np.real(array).tolist(), imaginary=np.imag(array).tolist())
    row = dict(model=label, run_suffix=suffix, angular_maximum=maximum, source=str(path),
        endpoint_scale=end_scale, endpoint_conformal_time=moment,
        induced_force_per_kappa_theta=components(forces['full']),
        full_minus_isotropic_force=components(forces['full'] - forces['isotropic']),
        polarization_contribution=components(forces['full'] - forces['unpolarized']),
        angular_compton_temperature_mixed_correction=components(angular_temperature),
        induced_force_per_hubble=components(per_hubble),
        angular_force_difference_fraction=float(np.linalg.norm(forces['full'] - forces['isotropic']) / max(np.linalg.norm(forces['full']), 1e-100)),
        polarization_force_fraction=float(np.linalg.norm(forces['full'] - forces['unpolarized']) / max(np.linalg.norm(forces['full']), 1e-100)),
        thermal_parameter=at['thermal_parameter'], redistribution_over_hubble=at['coefficient'],
        unit_mode_response_not_observational_amplitude=True,
        second_order_spectrum_not_inferred_from_bolometric_brightness=True,
        isolated_induced_source_not_total_thermal_correction=True)
    return row, payload, checks, path


def main():
    modest()
    folder = ROOT / 'results/saved-modes'
    assert not folder.exists()
    rows, checks, inputs = [], [], [ROOT / 'source_jet.py']
    packets = {}
    for label in ['heavy', 'cold']:
        for suffix in ['sixteenth', 'eighth', 'quarter', 'angular']:
            row, payload, new_checks, path = summarize(label, suffix)
            rows.append(row)
            checks.extend(new_checks)
            inputs.append(path)
            packets[label + '-' + suffix] = payload
    for label in ['heavy', 'cold']:
        for name, previous, refined in [('time', 'eighth', 'sixteenth'), ('angular', 'quarter', 'angular')]:
            first = packets[label + '-' + previous]['force_per_kappa_theta']
            second = packets[label + '-' + refined]['force_per_kappa_theta']
            error = float(np.linalg.norm(first - second) / max(np.linalg.norm(second), 1e-100))
            checks.append(dict(name=label + ': ' + name + ' refinement of physical induced source',
                               passed=error < .001, value=error, gate=.001))
    folder.mkdir(parents=True, exist_ok=False)
    for name, payload in packets.items():
        np.savez_compressed(folder / (name + '.npz'), **payload)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        rows=rows, first_order_spectral_lift_derived_from_cold_Thomson_equation=True,
                        baryon_rest_boost_included_at_first_order=True,
                        independent_quadratic_spectral_state_not_assumed=True,
                        nonparallel_thermal_response_not_evolved=True,
                        spectra_and_primordial_amplitude_not_fitted=True), __file__, inputs)
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']],
                         principal=[row for row in rows if row['run_suffix'] == 'sixteenth'])), flush=True)


if __name__ == '__main__':
    main()
