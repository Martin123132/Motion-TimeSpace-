import urllib.request
import sympy as symbolic
from mixed_common import *
from pair_coefficients import coefficients, thermal_weights


def anticommutator(left, right):
    return (left @ right + right @ left) / 2


def matrix_pair(first, second, channels, rate_forward, rate_reverse):
    identity = np.eye(2)
    gain = lambda value: sum(channel @ value @ channel.conj().T for channel in channels)
    adjoint = lambda value: sum(channel.conj().T @ value @ channel for channel in channels)
    incoming = (rate_reverse * anticommutator(identity + first, adjoint(second))
                - rate_forward * anticommutator(first, adjoint(identity + second)))
    outgoing = (rate_forward * anticommutator(identity + second, gain(first))
                - rate_reverse * anticommutator(second, gain(identity + first)))
    return incoming, outgoing


def main():
    modest()
    folder = ROOT / 'results/matrix-pair'
    assert not folder.exists()
    source_folder = ROOT / 'sources'
    source_folder.mkdir(parents=True, exist_ok=True)
    source = source_folder / 'nagirner-poutanen-0108357.html'
    url = 'https://arxiv.org/html/astro-ph/0108357'
    if not source.exists():
        request = urllib.request.Request(url, headers={'User-Agent': 'Research-source-archive/1.0'})
        with urllib.request.urlopen(request, timeout=60) as response:
            data = response.read()
        assert b'Kinetic Equation' in data and len(data) > 10000
        source.write_bytes(data)
    checks = []
    first, second, ref_first, ref_second, forward, reverse = symbolic.symbols('N_i N_j n_i n_j a b', positive=True)
    potential_first, potential_second = symbolic.symbols('X_i X_j')
    rate_forward = forward / (ref_first * (1 + ref_second))
    rate_reverse = reverse / (ref_second * (1 + ref_first))
    left = (rate_forward * (1 + second) - rate_reverse * second) * ref_first * (1 + ref_first)
    right = (rate_reverse * (1 + first) - rate_forward * first) * ref_second * (1 + ref_second)
    scalar_left = forward * (1 + ref_first) * (1 + second) / (1 + ref_second) - reverse * ref_first * second / ref_second
    scalar_right = reverse * (1 + ref_second) * (1 + first) / (1 + ref_first) - forward * ref_second * first / ref_first
    checks.append(dict(name='Polarized loss coefficient equals derived scalar incoming derivative', passed=symbolic.simplify(left - scalar_left) == 0))
    checks.append(dict(name='Polarized gain coefficient equals derived scalar outgoing derivative', passed=symbolic.simplify(right - scalar_right) == 0))
    generator = np.random.default_rng(7601)
    errors = dict(trace=0., hermitian=0., derivative=0., boundary=0., equilibrium=0., temperature=0.)
    for index in range(40):
        channels = (generator.normal(size=(4, 2, 2)) + 1j * generator.normal(size=(4, 2, 2))) / 4
        incoming, outgoing = generator.uniform(.1, 2., size=2)
        first_planck, second_planck = generator.uniform(.2, 3., size=2)
        weight_first, weight_second = first_planck * (1 + first_planck), second_planck * (1 + second_planck)
        first_electron, second_electron = generator.uniform(.5, 1.5, size=2)
        rate_first = first_electron / (first_planck * (1 + second_planck))
        rate_second = second_electron / (second_planck * (1 + first_planck))
        first_raw = generator.normal(size=(2, 2)) + 1j * generator.normal(size=(2, 2))
        second_raw = generator.normal(size=(2, 2)) + 1j * generator.normal(size=(2, 2))
        first_perturbation = (first_raw + first_raw.conj().T) / 2
        second_perturbation = (second_raw + second_raw.conj().T) / 2
        first_density, second_density = incoming * np.eye(2), outgoing * np.eye(2)
        exact = matrix_pair(first_density, second_density, channels, rate_first, rate_second)
        norm = max(np.linalg.norm(exact), 1e-100)
        errors['trace'] = max(errors['trace'], abs(np.trace(exact[0] + exact[1])) / norm)
        errors['hermitian'] = max(errors['hermitian'], max(np.linalg.norm(value - value.conj().T) for value in exact) / norm)
        gain = lambda value: sum(channel @ value @ channel.conj().T for channel in channels)
        adjoint = lambda value: sum(channel.conj().T @ value @ channel for channel in channels)
        left_value = weight_first * (rate_first * (1 + outgoing) - rate_second * outgoing)
        right_value = weight_second * (rate_second * (1 + incoming) - rate_first * incoming)
        analytic = np.array([right_value * adjoint(second_perturbation) - left_value * anticommutator(first_perturbation, adjoint(np.eye(2))),
                             left_value * gain(first_perturbation) - right_value * anticommutator(second_perturbation, gain(np.eye(2)))])
        step = 1e-4
        plus = np.array(matrix_pair(first_density + step * weight_first * first_perturbation,
                                    second_density + step * weight_second * second_perturbation, channels, rate_first, rate_second))
        minus = np.array(matrix_pair(first_density - step * weight_first * first_perturbation,
                                     second_density - step * weight_second * second_perturbation, channels, rate_first, rate_second))
        errors['derivative'] = max(errors['derivative'], np.linalg.norm((plus - minus) / (2 * step) - analytic) / np.linalg.norm(analytic))
        pure = first_raw @ first_raw.conj().T
        pure = np.linalg.eigh(pure)[1][:, :1]
        boundary = pure @ pure.conj().T
        null = np.linalg.eigh(boundary)[1][:, 0]
        boundary_rate = matrix_pair(boundary, second_density, channels, rate_first, rate_second)[0]
        errors['boundary'] = min(errors['boundary'], float(np.real(null.conj() @ boundary_rate @ null)))
        equilibrium = matrix_pair(first_planck * np.eye(2), second_planck * np.eye(2), channels,
                                  1 / (first_planck * (1 + second_planck)), 1 / (second_planck * (1 + first_planck)))
        errors['equilibrium'] = max(errors['equilibrium'], float(np.linalg.norm(equilibrium)))
        photon_first, photon_second = generator.uniform(.2, 10., size=2)
        theta = 2e-4
        gamma = 1 + generator.uniform(0., 10.) * theta
        shift = 1e-4
        heat = 1e-5
        initial, final = generator.uniform(-.1, .1, size=2)
        values = coefficients(photon_first, photon_second, initial, final, heat, shift, theta, gamma)
        temperature_step = 2e-6
        flux_plus = coefficients(photon_first, photon_second, initial, final, heat, shift + temperature_step, theta, gamma)[3]
        flux_minus = coefficients(photon_first, photon_second, initial, final, heat, shift - temperature_step, theta, gamma)[3]
        expected = values[2] - (photon_first - photon_second)
        error = abs((flux_plus - flux_minus) / (2 * temperature_step) - expected) / max(abs(expected), 1e-3)
        errors['temperature'] = max(errors['temperature'], float(error))
    for name in ['trace', 'hermitian', 'derivative', 'equilibrium']:
        checks.append(dict(name='Matrix pair independent ' + name + ' check', passed=errors[name] < 1e-9, value=errors[name]))
    checks.append(dict(name='Occupation positivity cone has inward collision direction at zero eigenvalue', passed=errors['boundary'] > -1e-12, value=errors['boundary']))
    checks.append(dict(name='Stable electron-temperature derivative agrees with independent finite difference', passed=errors['temperature'] < 1e-7, value=errors['temperature']))
    folder.mkdir(parents=True, exist_ok=False)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        source_url=url, source_sha256=digest(source), primary_scope='Equation99 with nondegenerate unpolarized electrons; primary paper2001, not HTML conversion date.',
                        approximation='Binary scattering, molecular chaos, unpolarized nondegenerate thermalized electrons, arbitrary photon polarization perturbations about scalar occupations.',
                        equilibrium_symmetry_not_imposed_off_equilibrium=True), __file__,
           [ROOT / 'pair_coefficients.py', source, SPIN / 'DERIVATION.md', GRID / 'grid_common.py'])
    print(json.dumps(dict(checks=checks)), flush=True)


if __name__ == '__main__':
    main()
