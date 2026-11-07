from thermal_wave_common import *
from thermal_wave_system import ThermalWaveSystem
from stable_spectral_basis import load_basis


def main():
    modest()
    folder = ROOT / 'results/expanding-background'
    assert not folder.exists()
    checks, rows, inputs = [], [], []
    frequency, measure = frequency_quadrature(420)
    for model in ['heavy', 'cold']:
        system = ThermalWaveSystem(model, 24, 8, 'physical')
        basis = system.basis
        samples = np.linspace(.02, system.geometry.thermal.end, 45)
        continuity, correction, redshift_tail, number_tail, kinetic_residual, kinetic_size = [], [], [], [], [], []
        for expansion in samples:
            local = system.background(expansion)
            background = system.geometry.solution.sol(expansion)
            slope = system.geometry.rhs(expansion, background)
            scalar_derivative = np.sum((background[2:4] * slope[2:4] - background[2:4] ** 2) / local['scale'] ** 2
                                       + system.geometry.mass2 * background[:2] * slope[:2])
            density_derivative = (-3 * (local['baryon'] + local['cold']) - 4 * (local['photon'] + local['neutrino'])
                                  + local['heat'] * local['photon_reference'] * local['photon_energy_prime']
                                  + local['heat'] * local['photon_reference'] * (local['ratio_prime'] - 4 * local['temperature_ratio'])
                                  + scalar_derivative)
            continuity.append(abs(density_derivative + 3 * (local['density'] + local['pressure'])) / local['density'])
            raw = system.geometry.profiles(expansion)
            raw_derivative = system.geometry.profiles(expansion, 1)
            target = local['photon_energy_scaled']
            correction.append(abs(target - basis.energy @ raw))
            endpoints = np.array([basis.minimum, basis.maximum])
            values = basis.evaluate(endpoints) @ raw
            planck = 1 / np.expm1(endpoints)
            distortion = local['heat'] * planck * (1 + planck) * values
            redshift_tail.append(float(np.max(abs(endpoints ** 4 * distortion / I3))))
            number_tail.append(float(np.max(abs(endpoints ** 3 * distortion / I3))))
            matrix = system.ladder.at(local['theta'], 0)[:basis.count, :basis.count]
            temperature = float(system.geometry.temperature(expansion))
            kinetic = local['opacity'] / local['hubble'] * linalg.solve(
                basis.mass, matrix @ (raw - basis.temperature * temperature), assume_a='pos')
            kinetic_residual.append(float(np.linalg.norm(raw_derivative - kinetic)))
            kinetic_size.append(float(np.linalg.norm(kinetic)))
        checks.append(dict(name=model + ': expanding total background obeys continuity', passed=max(continuity) < 1e-9,
                           value=max(continuity)))
        checks.append(dict(name=model + ': dense-output energy correction stays below spectrum accuracy budget',
                           passed=max(correction) < .002, value=max(correction)))
        residual = max(kinetic_residual) / max(kinetic_size)
        checks.append(dict(name=model + ': interpolated physical kinetic source remains resolved away from initial layer',
                           passed=residual < .002, value=residual, first_tested_log_expansion=.02))
        checks.append(dict(name=model + ': finite-band redshift endpoint terms negligible at physical amplitude',
                           passed=max(redshift_tail) < 1e-12 and max(number_tail) < 1e-12,
                           energy_endpoint=max(redshift_tail), number_endpoint=max(number_tail)))
        rows.append(dict(model=model, background_continuity=max(continuity), dense_energy_correction=max(correction),
                         kinetic_dense_relative=residual, energy_endpoint=max(redshift_tail), number_endpoint=max(number_tail)))
        inputs.extend([system.geometry.source, system.geometry.parent.source, *system.ladder.inputs])
        for tag, coarse_name, fine_name in [
            ('time16-800-1600', model + '16-800', model + '16-1600'),
            ('time24-1600-3200', model + '24-1600', model + '24-3200'),
            ('basis16-24', model + '16-1600', model + '24-3200'),
        ]:
            histories = []
            for name in [coarse_name, fine_name]:
                path = ROOT / 'backgrounds' / name / 'history.npz'
                packet = json.loads((path.parent / 'status.json').read_text())
                assert packet['all_checks_passed']
                own_basis = load_basis(ROOT / 'banks' / ('stable' + str(packet['basis_count']) + '-late'))
                inputs.extend([path, path.parent / 'status.json'])
                with np.load(path) as saved:
                    history = interpolate.CubicSpline(saved['expansion'], saved['profiles'])(samples)
                    histories.append(history @ own_basis.evaluate(frequency).T)
            numerator = float(np.sqrt(np.max(np.sum(measure * abs(histories[0] - histories[1]) ** 2, axis=1))))
            denominator = float(np.sqrt(np.max(np.sum(measure * abs(histories[1]) ** 2, axis=1))))
            relative = numerator / denominator
            checks.append(dict(name=model + ':' + tag + ': physical background spectrum refinement',
                               passed=relative < .002, value=relative))
            rows.append(dict(model=model, comparison=tag, relative=relative))
    folder.mkdir(parents=True, exist_ok=False)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
                        initial_very_fast_electron_layer_not_time_resolved=True, photon_production_not_included=True),
           __file__, [ROOT / 'background_geometry.py', ROOT / 'thermal_wave_system.py', ROOT / 'kernel_ladder.py',
                      ROOT / 'stable_spectral_basis.py', *sorted(set(inputs))])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']], rows=rows)), flush=True)


if __name__ == '__main__':
    main()
