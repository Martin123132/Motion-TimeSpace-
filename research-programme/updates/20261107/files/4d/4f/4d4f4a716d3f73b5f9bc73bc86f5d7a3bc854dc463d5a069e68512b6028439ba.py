import mpmath as arbitrary
from mixed_common import *
from stable_pair import coefficients
from derive_matrix_pair import matrix_pair


def entropy_derivative(matrix):
    values, vectors = linalg.eigh(matrix)
    return (vectors * np.log1p(1 / values)) @ vectors.conj().T


def main():
    modest()
    folder = ROOT / 'results/stable-pair'
    assert not folder.exists()
    arbitrary.mp.dps = 65
    random = np.random.default_rng(7602)
    errors = np.zeros(4)
    minimum_entropy, entropy_error = math.inf, 0.
    checks, samples = [], []
    for index in range(32):
        first = math.exp(random.uniform(math.log(1e-5), math.log(50.)))
        second = first * math.exp(random.uniform(-.12, .12))
        theta = math.exp(random.uniform(math.log(4e-5), math.log(5e-4)))
        gamma = 1 + theta * random.uniform(.1, 18.)
        heat, shift = 5.755472902372619e-10, random.uniform(-2e-9, 2e-9)
        initial, final = random.uniform(-2., 2., size=2)
        actual = np.array(coefficients(first, second, initial, final, heat, shift, theta, gamma), dtype=float)
        incoming, outgoing, initial_mp, final_mp, heat_mp, shift_mp, theta_mp, gamma_mp = [
            arbitrary.mpf(float(value)) for value in [first, second, initial, final, heat, shift, theta, gamma]]
        planck_i, planck_j = 1 / arbitrary.expm1(incoming), 1 / arbitrary.expm1(outgoing)
        occupation_i = planck_i + heat_mp * planck_i * (1 + planck_i) * initial_mp
        occupation_j = planck_j + heat_mp * planck_j * (1 + planck_j) * final_mp
        theta_e = theta_mp * (1 + shift_mp)
        forward = (theta_mp * arbitrary.besselk(2, 1 / theta_mp) / (theta_e * arbitrary.besselk(2, 1 / theta_e))
                   * arbitrary.exp(gamma_mp * (1 / theta_mp - 1 / theta_e)))
        gamma_final = gamma_mp + theta_mp * (incoming - outgoing)
        reverse = (theta_mp * arbitrary.besselk(2, 1 / theta_mp) / (theta_e * arbitrary.besselk(2, 1 / theta_e))
                   * arbitrary.exp(gamma_final * (1 / theta_mp - 1 / theta_e)))
        left = forward * (1 + planck_i) * (1 + occupation_j) / (1 + planck_j) - reverse * planck_i * occupation_j / planck_j - 1
        right = reverse * (1 + planck_j) * (1 + occupation_i) / (1 + planck_i) - forward * planck_j * occupation_i / planck_i - 1
        forward_occupation = occupation_i / planck_i * (1 + occupation_j) / (1 + planck_j)
        reverse_occupation = occupation_j / planck_j * (1 + occupation_i) / (1 + planck_i)
        mean_gamma = arbitrary.besselk(1, 1 / theta_e) / arbitrary.besselk(2, 1 / theta_e) + 3 * theta_e
        derivative = (forward * (gamma_mp - mean_gamma) * forward_occupation
                      - reverse * (gamma_final - mean_gamma) * reverse_occupation) / (theta_mp * (1 + shift_mp) ** 2)
        defect = forward * forward_occupation - reverse * reverse_occupation - heat_mp * (initial_mp - final_mp) + (incoming - outgoing) * shift_mp
        expected = np.array([float(left), float(right), float(derivative + incoming - outgoing), float(defect)])
        errors = np.maximum(errors, abs(actual - expected) / np.maximum(abs(expected), [1e-18, 1e-18, 1e-18, 1e-30]))
        incident = np.array([0., 0., 1.])
        cosine = random.uniform(-.95, .95)
        scattered = np.array([math.sqrt(1 - cosine ** 2), 0., cosine])
        channels, recoil = grid.prior.rest_channels(theta * 3, incident, scattered)
        first_energy, second_energy = 3., 3. * float(recoil)
        electron_ratio = math.exp(second_energy - first_energy)
        densities = []
        for repeat in range(2):
            raw = random.normal(size=(2, 2)) + 1j * random.normal(size=(2, 2))
            densities.append(raw @ raw.conj().T + .2 * np.eye(2))
        first_density, second_density = densities
        collision_i, collision_j = matrix_pair(first_density, second_density, channels, 1., electron_ratio)
        production = float(np.real(np.trace(entropy_derivative(first_density) @ collision_i
                                            + entropy_derivative(second_density) @ collision_j)
                                   + (first_energy - second_energy) * np.trace(collision_j)))
        eigen_i, rotate_i = linalg.eigh(first_density)
        eigen_j, rotate_j = linalg.eigh(second_density)
        nonnegative = 0.
        for channel in channels:
            amplitudes = rotate_j.conj().T @ channel @ rotate_i
            positive = eigen_i[None, :] * (1 + eigen_j[:, None])
            negative = electron_ratio * eigen_j[:, None] * (1 + eigen_i[None, :])
            nonnegative += float(np.sum(abs(amplitudes) ** 2 * (positive - negative) * np.log(positive / negative)))
        minimum_entropy = min(minimum_entropy, production)
        entropy_error = max(entropy_error, abs(production - nonnegative) / max(nonnegative, 1e-100))
    for name, error in zip(['incoming occupation', 'outgoing occupation', 'electron temperature', 'nonlinear background residual'], errors):
        checks.append(dict(name='65-digit reference for stable ' + name + ' coefficient', passed=bool(error < 1e-7), value=float(error)))
    checks.append(dict(name='Non-equilibrium polarized entropy production equals a positive transition sum',
                       passed=entropy_error < 1e-9 and minimum_entropy >= 0, relative_error=entropy_error,
                       minimum_production=minimum_entropy))
    folder.mkdir(parents=True, exist_ok=False)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        exact_formula_not_fitted=True, entropy_test_does_not_assume_symmetric_Jacobian=True),
           __file__, [ROOT / 'stable_pair.py', ROOT / 'derive_matrix_pair.py', SPIN / 'kernel_common.py'])
    print(json.dumps(dict(checks=checks)), flush=True)


if __name__ == '__main__':
    main()
