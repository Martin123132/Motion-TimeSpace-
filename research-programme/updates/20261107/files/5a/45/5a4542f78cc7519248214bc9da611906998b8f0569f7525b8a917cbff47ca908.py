from angular_common import *
from source_jet import force_moments


def spectral_shapes(frequency):
    occupation = 1 / np.expm1(frequency)
    weight = occupation * (1 + occupation)
    gradient = frequency * weight
    linear = 1 + 2 * occupation
    first = gradient * (1 - frequency * linear)
    second = gradient * (1 - 3 * frequency * linear + frequency ** 2 * (linear ** 2 + 2 * weight))
    return occupation, gradient, first, second


def linear_correction(kernel, frequency, amplitude):
    occupation, gradient, first, second = spectral_shapes(frequency)
    recoil_map = kernel.recoil_angular(amplitude)
    thermal_map = kernel.thermal_angular(amplitude)
    thermal = ((second + 3 * first + 2 * gradient)[:, None, None, None] * recoil_map
               + gradient[:, None, None, None] * thermal_map)
    recoil = (frequency * (1 + 2 * occupation) * (first + 2 * gradient))[:, None, None, None] * recoil_map
    recoil += (2 * frequency * gradient * (-gradient + 2 * occupation + 1))[:, None, None, None] * amplitude
    return thermal + recoil


def norm(kernel, quadrature, frequency, tensor):
    angular_square = np.einsum('n,xnij,xnij->x', kernel.weights, tensor.conj(), tensor).real
    return math.sqrt(float(np.dot(quadrature * frequency ** 3, angular_square)))


def main():
    modest()
    folder = ROOT / 'results/mode-source-scales'
    assert not folder.exists()
    checks, rows, inputs, output = [], [], [ROOT / 'source_jet.py'], {}
    spectral_integral = 120 * (special.zeta(4, 1) - special.zeta(6, 1))
    drag_coefficient = 2 + 72 * special.zeta(6, 1) / I3_PLANCK - .1 * spectral_integral / I3_PLANCK
    for label in ['heavy', 'cold']:
        for previous, refined in [('eighth', 'sixteenth'), ('quarter', 'angular')]:
            previous_path = ROOT / 'results/saved-modes' / (label + '-' + previous + '.npz')
            refined_path = ROOT / 'results/saved-modes' / (label + '-' + refined + '.npz')
            inputs.extend([previous_path, refined_path])
            with np.load(previous_path) as older, np.load(refined_path) as newer:
                for key in ['full_minus_isotropic_force', 'polarization_contribution']:
                    relative = float(np.linalg.norm(older[key] - newer[key]) / np.linalg.norm(newer[key]))
                    checks.append(dict(name=label + ': separately resolved ' + key + ' ' + previous + '/' + refined,
                                       passed=relative < .001, value=relative, gate=.001))
        path = ROOT / 'results/saved-modes' / (label + '-sixteenth.npz')
        with np.load(path) as saved:
            amplitudes = saved['rest_first_order'].copy()
        kernel = AngularKernel(10, 20)
        thermal_background = inherited.ThermalBackground(label)
        local = thermal_background.at(thermal_background.end)
        for points in [120, 240]:
            nodes, weights = np.polynomial.legendre.leggauss(points)
            frequency = 30 * (nodes + 1)
            quadrature = 30 * weights
            occupation, gradient, first, second = spectral_shapes(frequency)
            for index, amplitude in enumerate(amplitudes):
                energy, flux = kernel.moments(amplitude)
                monopole = .5 * energy * kernel.projector
                anisotropic = amplitude - monopole
                source = linear_correction(kernel, frequency, anisotropic)
                force = force_moments(kernel, frequency, quadrature, source)
                target_force = np.r_[0., 2 * drag_coefficient * flux]
                relative = float(np.linalg.norm(force - target_force) / max(np.linalg.norm(target_force), 1e-100))
                checks.append(dict(name=label + ': independent linear anisotropic four-force p/q=' + str(index) + ',frequency=' + str(points),
                                   passed=relative < 1e-7, value=relative, gate=1e-7))
                cold = gradient[:, None, None, None] * (kernel.scatter(anisotropic) - anisotropic)
                ratio = local['thermal_parameter'] * norm(kernel, quadrature, frequency, source) / norm(kernel, quadrature, frequency, cold)
                full_source = linear_correction(kernel, frequency, amplitude)
                full_force = force_moments(kernel, frequency, quadrature, full_source)
                heat_error = float(abs(full_force[0] + 2 * energy) / max(abs(2 * energy), 1e-100))
                checks.append(dict(name=label + ': monopole heat sensitivity without assuming electron-temperature closure ' + str(index) + ',' + str(points),
                                   passed=heat_error < 1e-7, value=heat_error, gate=1e-7))
                if points == 240:
                    rows.append(dict(model=label, mode=index, thermal_to_cold_collision_norm=ratio,
                        source_excludes_isotropic_temperature_response=True,
                        electron_temperature_heat_law='Q_p/(kappa*rho_ref*theta_ref)=4*(r_p-mean_temperature_p)',
                        photon_mean_temperature_real=float(np.real(energy / 2)),
                        photon_mean_temperature_imaginary=float(np.imag(energy / 2)),
                        thermal_force_per_kappa_theta_real=force.real.tolist(),
                        thermal_force_per_kappa_theta_imaginary=force.imag.tolist()))
                    output[label + '-' + str(index)] = dict(frequency=frequency, source=source, cold_source=cold,
                                                            force=force, anisotropic_amplitude=anisotropic)
    folder.mkdir(parents=True, exist_ok=False)
    for name, payload in output.items():
        np.savez_compressed(folder / (name + '.npz'), **payload)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        rows=rows, planck_temperature_dipole_drag_correction=drag_coefficient,
                        drag_correction_is_relative_to_flux_not_an_empirical_fit=True,
                        electron_temperature_not_assigned_by_monopole_balance=True,
                        source_ratio_not_accumulated_solution_error=True), __file__, inputs)
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']],
                         drag_coefficient=drag_coefficient, rows=rows)), flush=True)


if __name__ == '__main__':
    main()
