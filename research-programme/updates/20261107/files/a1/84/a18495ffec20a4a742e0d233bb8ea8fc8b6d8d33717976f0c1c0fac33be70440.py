from emission_angular_common import *
from reaction_geometry import ReactionGeometry
from dense_geometry_derivative import solution_derivative
from leading_pair import leading_coefficients
from stable_pair import coefficients


def main():
    modest()
    folder = ROOT / 'results/reaction-geometry-and-pair'
    folder.mkdir(parents=True, exist_ok=False)
    checks, inputs, rows = [], [], []
    for model in ['heavy', 'cold']:
        geometry = ReactionGeometry(model, model + '-reaction104-6400')
        inputs.extend([geometry.source, geometry.source.parent / 'status.json'])
        samples, defects = [], []
        for expansion in np.linspace(0., geometry.thermal.end, 401):
            local = geometry.at(expansion)
            energy, temperature, energy_prime = geometry.thermal_source(expansion)
            temperature_prime = float(geometry.temperature(expansion, 1))
            photon_prime = local['photon_reference'] * (-4 * (1 + geometry.heat * energy) + geometry.heat * energy_prime)
            internal_prime = geometry.heat * local['photon_reference'] * (-4 * (1 + geometry.heat * temperature) + geometry.heat * temperature_prime)
            scalar_prime = -3 * float(np.sum(local['prime'] ** 2 / local['scale'] ** 2))
            density_prime = photon_prime + internal_prime - 3 * (local['baryon'] + local['cold']) - 4 * local['neutrino'] + scalar_prime
            continuity = abs(density_prime + 3 * (local['density'] + local['pressure'])) / local['density']
            spectral_energy = float(geometry.basis.energy @ geometry.profiles(expansion))
            samples.append([expansion, continuity, abs(energy_prime + 1 + geometry.heat * (temperature + temperature_prime)), abs(spectral_energy - energy), energy])
            if expansion > .01:
                expected = geometry.rhs(expansion, geometry.solution.sol(expansion))
                derivative = solution_derivative(geometry.solution, expansion)
                defects.append(linalg.norm(derivative[:4] - expected[:4]) / max(linalg.norm(expected[:4]), 1e-30))
        samples = np.array(samples)
        checks.extend([check(model + ' total FLRW continuity', max(samples[:, 1]), 1e-12),
            check(model + ' scaled heat continuity', max(samples[:, 2]), 1e-12),
            check(model + ' spectral energy matches conservative stress', max(samples[:, 3]) / max(abs(samples[:, 4])), .002),
            check(model + ' differentiated scalar dense solution obeys parent ODE', max(defects), .002)])
        for expansion in [.05, 1., math.log(10)]:
            theta = geometry.at(expansion)['theta']
            profile = geometry.profiles(expansion)
            gas = float(geometry.temperature(expansion))
            first = np.geomspace(.0001, 20., 57)
            second = first * (1 + .02 * np.sin(np.arange(len(first))))
            gamma = 1 + theta * np.linspace(.1, 9., len(first))
            initial, final = geometry.basis.evaluate(first) @ profile, geometry.basis.evaluate(second) @ profile
            derived = np.asarray(leading_coefficients(first, second, initial, final, gas, theta, gamma))
            errors = []
            for amplitude in [1e-5, 1e-6, geometry.heat]:
                exact = np.asarray(coefficients(first, second, initial, final, amplitude, amplitude * gas, theta, gamma)[:3]) / amplitude
                error = float(np.max(abs(exact - derived)) / max(np.max(abs(derived)), 1e-100))
                checks.append(check(model + ' emitting Compton pair s=' + str(expansion) + ' chi=' + str(amplitude), error, max(50 * amplitude, 1e-8)))
                errors.append(error)
            rows.append(dict(model=model, expansion=expansion, compton_pair_errors=errors))
        np.savez_compressed(folder / (model + '.npz'), geometry_samples=samples, scalar_defects=defects)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
        common_parent_and_emitting_background=True, finite_k_solution=False), __file__,
        [*inputs, ROOT / 'reaction_geometry.py', BACKGROUND / 'increment_emitting_geometry.py',
         BACKGROUND / 'dense_geometry_derivative.py', PARENT / 'leading_pair.py', BRANCH / 'mixed-bath-transport-20261007/stable_pair.py'])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    main()
