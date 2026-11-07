from step_common import *
import sympy as sp


def redistribution(initial, final, cosine, theta):
    transfer_squared = initial ** 2 + final ** 2 - 2 * initial * final * cosine
    difference = final - initial
    return np.exp(-(difference + theta * transfer_squared / 2) ** 2 / (2 * theta * transfer_squared)) / np.sqrt(2 * np.pi * theta * transfer_squared)


def screen(direction):
    reference = np.array([0., 0., 1.]) if abs(direction[2]) < .8 else np.array([1., 0., 0.])
    first = np.cross(direction, reference)
    first /= np.linalg.norm(first)
    return np.column_stack([first, np.cross(direction, first)])


def scalar_candidate(frequency, power, degree, theta, order=128):
    cosine, angular_weights = np.polynomial.legendre.leggauss(48)
    nodes, weights = np.polynomial.legendre.leggauss(order)
    nodes, weights = nodes * 10, weights * 10
    cosine = cosine[:, None]
    width = frequency * np.sqrt(2 * theta * (1 - cosine))
    final = frequency + width * nodes[None, :]
    assert np.min(final) > 0
    probability = redistribution(frequency, final, cosine, theta)
    initial_occupation = 1 / np.expm1(frequency)
    final_occupation = 1 / np.expm1(final)
    rate = .75 * (1 + cosine ** 2) * final / frequency * probability
    detailed_balance_weight = (1 + final_occupation) / (1 + initial_occupation)
    difference = special.eval_legendre(degree, cosine) * final ** power - frequency ** power
    return float(np.sum(angular_weights[:, None] / 2 * weights[None, :] * width * rate * detailed_balance_weight * difference))


def main():
    modest()
    folder = ROOT / 'results/finite-shift'
    assert not folder.exists()
    checks = []
    def check(name, passed, **details):
        checks.append(dict(name=name, passed=bool(passed), **details))
    cosine_symbol = sp.symbols('cosine', real=True)
    phase = sp.Rational(3, 4) * (1 + cosine_symbol ** 2)
    moments = [sp.integrate(phase * (1 - cosine_symbol) ** degree / 2, (cosine_symbol, -1, 1)) for degree in range(3)]
    check('Normalized Thomson angular probability and exact first two shift moments', moments == [1, 1, sp.Rational(7, 5)])
    dipole_first = -sp.integrate(phase * cosine_symbol * (1 - cosine_symbol) / 2, (cosine_symbol, -1, 1))
    check('Gaussian finite-shift Taylor coefficient reproduces unstable dipole principal part', dipole_first == sp.Rational(2, 5))
    theta = 4.596201578526332e-4
    omega = np.r_[np.linspace(0, 5, 101), np.linspace(6, 400, 395)]
    angular, angular_weights = np.polynomial.legendre.leggauss(256)
    probability = angular_weights * .75 * (1 + angular ** 2) / 2
    characteristic = np.exp(-theta * omega[:, None] ** 2 * (1 - angular[None, :]))
    symbols = np.array([characteristic @ (probability * special.eval_legendre(degree, angular)) - 1 for degree in range(9)])
    check('All nine finite-shift angular symbols are nonpositive on resolved sample', np.max(symbols) < 1e-13, largest=float(np.max(symbols)))
    truncated = -1 + .4 * theta * omega ** 2
    check('Finite-shift dipole remains damped where truncation grows', truncated[-1] > 0 and symbols[1, -1] < 0,
          truncated_at_400=float(truncated[-1]), finite_shift_at_400=float(symbols[1, -1]))
    remainder_bound = .7 * theta ** 2 * omega ** 4
    check('Rigorous exponential remainder bound contains dipole error', np.all(abs(symbols[1] - truncated) <= remainder_bound + 1e-13),
          bound_at_omega5=float(.7 * theta ** 2 * 5 ** 4))
    hermite, hermite_weights = np.polynomial.hermite.hermgauss(64)
    velocity_errors = []
    for scattering_cosine in [-.8, -.1, .6]:
        for frequency_wavenumber in [.1, 2., 8., 20.]:
            shift = np.sqrt(4 * theta * (1 - scattering_cosine)) * hermite
            actual = np.dot(hermite_weights, np.exp(1j * frequency_wavenumber * shift)) / np.sqrt(np.pi)
            exact = np.exp(-theta * (1 - scattering_cosine) * frequency_wavenumber ** 2)
            velocity_errors.append(abs(actual - exact))
    check('Independent Maxwell velocity quadrature recovers finite-shift characteristic', max(velocity_errors) < 1e-12, value=float(max(velocity_errors)))
    directions = np.array([[0., 0., 1.], [.6, 0., .8], [0., .8, -.6], [-.8, -.6, 0.], [.3, -.4, np.sqrt(.75)]])
    frequencies = np.array([1., 1.013, .997, 1.026, 1.041])
    widths = np.array([.009, .010, .011, .008, .012])
    occupations = 1 / np.expm1(frequencies)
    measure = frequencies ** 2 * widths * occupations * (1 + occupations)
    frames = [screen(direction) for direction in directions]
    pairs, reciprocity = [], []
    for initial in range(len(frequencies)):
        for final in range(initial + 1, len(frequencies)):
            cosine = directions[initial] @ directions[final]
            forward = redistribution(frequencies[initial], frequencies[final], cosine, theta)
            reverse = redistribution(frequencies[final], frequencies[initial], cosine, theta)
            prefactor = frequencies[initial] * frequencies[final] * widths[initial] * widths[final]
            conductance = prefactor * occupations[initial] * (1 + occupations[final]) * forward
            reverse_conductance = prefactor * occupations[final] * (1 + occupations[initial]) * reverse
            reciprocity.append(abs(conductance - reverse_conductance) / conductance)
            pairs.append((initial, final, conductance, frames[initial].T @ frames[final]))
    check('Maxwell recoil phase-space rate obeys exact Bose detailed balance', max(reciprocity) < 1e-12, value=float(max(reciprocity)))
    identity = np.eye(2)
    def collision(values):
        output = np.zeros_like(values, dtype=complex)
        for initial, final, conductance, jones in pairs:
            left = jones @ jones.conj().T
            right = jones.conj().T @ jones
            output[initial] += conductance / measure[initial] * (jones @ values[final] @ jones.conj().T - (left @ values[initial] + values[initial] @ left) / 2)
            output[final] += conductance / measure[final] * (jones.conj().T @ values[initial] @ jones - (right @ values[final] + values[final] @ right) / 2)
        return output
    def pairing(left, right):
        return float(np.sum(measure * np.einsum('nij,nij->n', left.conj(), right)).real)
    generator = np.random.default_rng(72071)
    for trial in range(4):
        values = generator.normal(size=(5, 2, 2)) + 1j * generator.normal(size=(5, 2, 2))
        values = (values + values.swapaxes(-1, -2).conj()) / 2
        temperature = .03 * generator.normal()
        velocity = .02 * generator.normal(size=3)
        relative = values - (frequencies * (temperature + directions @ velocity))[:, None, None] * identity
        response = collision(relative)
        trace = np.trace(response, axis1=-2, axis2=-1).real
        energy = np.dot(measure * frequencies, trace)
        momentum = np.einsum('n,ni,n->i', measure * frequencies, directions, trace)
        capacity, inertia = .03, .07
        temperature_rate, velocity_rate = -energy / capacity, -momentum / inertia
        entropy_rate = pairing(values, response) + capacity * temperature * temperature_rate + inertia * np.dot(velocity, velocity_rate)
        exact_rate = -sum(conductance * np.linalg.norm(relative[initial] @ jones - jones @ relative[final]) ** 2 for initial, final, conductance, jones in pairs)
        error = abs(entropy_rate - exact_rate) / max(abs(exact_rate), 1e-100)
        check('Polarized jump plus plasma exact square dissipation ' + str(trial), error < 1e-12 and exact_rate <= 0, value=error)
        check('Polarized jump number and total energy/momentum balance ' + str(trial),
              abs(np.dot(measure, trace)) < 1e-12 and abs(energy + capacity * temperature_rate) < 1e-12
              and np.max(abs(momentum + inertia * velocity_rate)) < 1e-12)
    chemical = np.ones((5, 1, 1)) * identity
    check('Chemical equilibrium is an exact polarized jump null vector', np.max(abs(collision(chemical))) < 1e-13)
    difference, recoil = sp.symbols('difference recoil', real=True)
    balance = sp.expand(-(difference + recoil / 2) ** 2 / (2 * recoil) + (-difference + recoil / 2) ** 2 / (2 * recoil))
    check('Exact recoil Maxwell forward/reverse log-ratio', sp.simplify(balance + difference) == 0)
    rows = []
    for frequency in [1., 3., 8.]:
        occupation = 1 / np.expm1(frequency)
        local = 2 * frequency * (1 + 2 * occupation) - 2 * frequency ** 2 * occupation * (1 + occupation)
        diffusion = 4 * frequency - frequency ** 2 * (1 + 2 * occupation)
        target = -.4 * diffusion - .4 * frequency + 1.4 * local * frequency
        coefficients = []
        for test_theta in [2e-4, 1e-4, 5e-5]:
            value = scalar_candidate(frequency, 1, 1, test_theta)
            coefficients.append((value + frequency) / test_theta)
        extrapolated = 2 * coefficients[-1] - coefficients[-2]
        refined = scalar_candidate(frequency, 1, 1, 5e-5, 192)
        quadrature_error = abs(refined - scalar_candidate(frequency, 1, 1, 5e-5)) / 5e-5
        rows.append(dict(frequency=frequency, parent_coefficient=float(target), raw_candidate_coefficients=coefficients,
                         extrapolated_candidate_coefficient=float(extrapolated), mismatch=float(extrapolated - target),
                         quadrature_coefficient_error=float(quadrature_error)))
    check('Simple phase-space candidate has resolved quadrature', max(row['quadrature_coefficient_error'] for row in rows) < 1e-7)
    matched = all(abs(row['mismatch']) < 1e-3 for row in rows)
    check('Complete-kernel claim is gated by independent parent matching, not by positivity alone', not matched,
          candidate_status='rejected_as_complete_kernel' if not matched else 'requires_further_validation')
    folder.mkdir(parents=True, exist_ok=False)
    np.savez_compressed(folder / 'symbols.npz', omega=omega, theta=theta, finite_shift=symbols,
                        truncated_dipole=truncated, rigorous_remainder_bound=remainder_bound)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        scalar_candidate_matching=rows, simple_phase_space_candidate_matches_parent=matched,
                        gaussian_principal_part_stable=True, full_polarized_Compton_kernel_completed=False,
                        polarized_detailed_balance_square_identity_derived=True,
                        physical_rate_not_inferred_from_entropy_identity_alone=True,
                        leading_Doppler_shift_not_full_recoil_or_relativistic_amplitude=True,
                        candidate_rejection_does_not_invalidate_abstract_pair_dissipation_identity=True), __file__)
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']], matching=rows)), flush=True)


if __name__ == '__main__':
    main()
