import argparse
from emitting_geometry import *
from dense_geometry_derivative import solution_derivative


def main(arguments):
    modest()
    folder = ROOT / 'results' / arguments.name
    folder.mkdir(parents=True, exist_ok=False)
    geometry = EmittingGeometry(arguments.model, arguments.background)
    reference = EmittingGeometry(arguments.model, arguments.background, 0.)
    coordinates = np.linspace(0., geometry.thermal.end, 401)
    rows, residuals = [], []
    for expansion in coordinates:
        background = geometry.at(expansion)
        base = reference.at(expansion)
        energy, temperature, energy_prime = geometry.thermal_source(expansion)
        temperature_prime = float(geometry.temperature(expansion, 1))
        reference_density = background['photon_reference']
        photon_prime = reference_density * (-4 * (1 + geometry.heat * energy) + geometry.heat * energy_prime)
        internal_prime = geometry.heat * reference_density * (-4 * (1 + geometry.heat * temperature) + geometry.heat * temperature_prime)
        scalar_prime = -3 * float(np.sum(background['prime'] ** 2 / background['scale'] ** 2))
        density_prime = photon_prime + internal_prime - 3 * (background['baryon'] + background['cold']) - 4 * background['neutrino'] + scalar_prime
        continuity = float(abs(density_prime + 3 * (background['density'] + background['pressure'])) / background['density'])
        thermal_residual = energy_prime + 1 + geometry.heat * (temperature + temperature_prime)
        spectral_energy = float(geometry.basis.energy @ geometry.profiles(expansion))
        residuals.append([continuity, abs(thermal_residual), abs(spectral_energy - energy)])
        rows.append([expansion, background['scale'], background['hubble'], base['hubble'],
                     background['density'], background['pressure'], energy, temperature, float(geometry.number(expansion)),
                     float(geometry.solution.sol(expansion)[-1]), float(reference.solution.sol(expansion)[-1])])
    residuals, rows = np.array(residuals), np.array(rows)
    defects = []
    for expansion in coordinates[2:]:
        state = geometry.solution.sol(expansion)
        derivative = solution_derivative(geometry.solution, expansion)
        expected = geometry.rhs(expansion, state)
        defects.append(float(linalg.norm(derivative[:4] - expected[:4]) / max(linalg.norm(expected[:4]), 1e-30)))
    projection_relative = float(np.max(residuals[:, 2]) / max(abs(rows[:, 6])))
    step = geometry.expansion[1] - geometry.expansion[0]
    kinetic_dense_balance = []
    for expansion in coordinates[coordinates > 2 * step]:
        residual = float(geometry.basis.energy @ geometry.profiles(expansion, 1)) + geometry.heat * float(geometry.temperature(expansion, 1)) + 1 + geometry.heat * float(geometry.temperature(expansion))
        kinetic_dense_balance.append(abs(residual))
    checks = [
        dict(name='Scalar equations integrate successfully with emitting radiation and finite gas stress', passed=geometry.solution.success and reference.solution.success),
        dict(name='Total FLRW matter-radiation-scalar continuity', passed=float(max(residuals[:, 0])) < 1e-12, value=float(max(residuals[:, 0]))),
        dict(name='Scaled thermal continuity avoids masking by dominant density', passed=float(max(residuals[:, 1])) < 1e-12, value=float(max(residuals[:, 1]))),
        dict(name='Conservative dense energy agrees with evolved spectral moment', passed=projection_relative < .002, value=projection_relative),
        dict(name='Raw spectral spline obeys energy law after initial stiff layer', passed=max(kinetic_dense_balance) < .002, value=max(kinetic_dense_balance)),
        dict(name='Analytically differentiated dense scalar polynomial satisfies the ODE', passed=max(defects) < .002, value=max(defects)),
        dict(name='Density and expanding Hubble branch remain positive', passed=bool(np.all(rows[:, 2] > 0) and np.all(rows[:, 4] > 0))),
        dict(name='Photon number response retained in geometry inputs', passed=abs(rows[-1, 8]) > 1e-6, value=float(rows[-1, 8])),
        dict(name='Reference-to-emitting geometry feedback is perturbative', passed=float(max(abs(rows[:, 2] / rows[:, 3] - 1))) < .002, value=float(max(abs(rows[:, 2] / rows[:, 3] - 1))))]
    np.savez_compressed(folder / 'geometry.npz', samples=rows, residuals=residuals, scalar_ode_defects=defects)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
        model=arguments.model, background=arguments.background, final_hubble_fraction=float(rows[-1, 2] / rows[-1, 3] - 1),
        final_proper_time_fraction=float(rows[-1, -2] / rows[-1, -1] - 1),
        number_unchanged_by_conservative_energy_reconstruction=True,
        background_field_order='Leading sourced heat order, with finite capacity and conserved dense stress retained; no nonlinear iteration of emission kinetics on corrected H.',
        initial_stiff_layer_resolved_pointwise=False), __file__,
        [ROOT / 'dense_geometry_derivative.py', ROOT / 'emitting_geometry.py', THERMAL_STAGE / 'background_geometry.py', geometry.source,
         geometry.source.parent / 'status.json', geometry.parent.source, geometry.thermal.native_constants])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', choices=['heavy', 'cold'], required=True)
    parser.add_argument('--background', required=True)
    parser.add_argument('--name', required=True)
    main(parser.parse_args())
