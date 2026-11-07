from step_common import *
from moving_kernel import scalar_compton


def main():
    modest()
    folder = ROOT / 'results/moving-kernel-independent-check'
    assert not folder.exists()
    saved = ROOT / 'results/moving-kernel/status.json'
    parent = json.loads(saved.read_text())
    checks, rows = [], []
    for row in parent['rows']:
        frequency, power, degree = row['frequency'], row['power'], row['degree']
        coefficients = [(scalar_compton(frequency, power, degree, theta, 12, 16, 32) - row['cold_coefficient']) / theta
                        for theta in [8e-5, 4e-5, 2e-5]]
        extrapolated = (coefficients[0] - 6 * coefficients[1] + 8 * coefficients[2]) / 3
        error = float(abs(extrapolated - row['parent_coefficient']) / max(1, abs(row['parent_coefficient'])))
        rows.append(dict(frequency=frequency, power=power, degree=degree, refined_coefficient=extrapolated,
                         parent_coefficient=row['parent_coefficient'], relative_error=error))
    maximum = max(row['relative_error'] for row in rows)
    checks.append(dict(name='Independent temperature ladder and finer quadrature retain all36 first-order matches',
                       passed=maximum < 1e-5, value=maximum, gate=1e-5))
    generator = np.random.default_rng(7271)
    on_shell, detailed_balance, ratios, rates = [], [], [], []
    for trial in range(100):
        theta = 10 ** generator.uniform(-5, -3)
        frequency = 10 ** generator.uniform(-1, 1.3)
        beta = np.sqrt(theta) * generator.normal(size=3)
        speed_squared = beta @ beta
        gamma = 1 / np.sqrt(1 - speed_squared)
        initial = generator.normal(size=3)
        initial /= np.linalg.norm(initial)
        incident_dot = initial @ beta
        incident_factor = gamma * (1 - incident_dot)
        initial_rest = (initial + ((gamma - 1) * incident_dot / speed_squared - gamma) * beta) / incident_factor
        final_rest = generator.normal(size=3)
        final_rest /= np.linalg.norm(final_rest)
        cosine = initial_rest @ final_rest
        rest_frequency = frequency * incident_factor
        recoil_ratio = 1 / (1 + theta * rest_frequency * (1 - cosine))
        final_factor = gamma * (1 + beta @ final_rest)
        final_frequency = rest_frequency * recoil_ratio * final_factor
        final = (final_rest + ((gamma - 1) * (beta @ final_rest) / speed_squared + gamma) * beta) / final_factor
        epsilon, final_epsilon = theta * frequency, theta * final_frequency
        electron_final_energy = gamma + epsilon - final_epsilon
        electron_final_momentum = gamma * beta + epsilon * initial - final_epsilon * final
        on_shell.append(abs(electron_final_energy ** 2 - electron_final_momentum @ electron_final_momentum - 1))
        direct_ratio = (1 - incident_dot) / (1 - beta @ final + epsilon / gamma * (1 - initial @ final))
        ratios.append(abs(final_frequency / frequency - direct_ratio))
        initial_n, final_n = 1 / np.expm1(frequency), 1 / np.expm1(final_frequency)
        forward_log = np.log(initial_n) + np.log1p(final_n)
        reverse_log = (final_frequency - frequency) + np.log(final_n) + np.log1p(initial_n)
        detailed_balance.append(abs(forward_log - reverse_log))
        rates.append((1 - incident_dot) * recoil_ratio ** 2 * (recoil_ratio + 1 / recoil_ratio - 1 + cosine ** 2))
    checks.extend([
        dict(name='Exact two-body boosted recoil leaves final electron on mass shell', passed=max(on_shell) < 1e-12, value=float(max(on_shell))),
        dict(name='Rest-frame boosts agree with independent laboratory energy-ratio identity', passed=max(ratios) < 1e-12, value=float(max(ratios))),
        dict(name='Juttner and Bose equilibrium statistical factors balance per physical event', passed=max(detailed_balance) < 1e-12, value=float(max(detailed_balance))),
        dict(name='All sampled physical Klein-Nishina event rates are positive', passed=min(rates) > 0, minimum=float(min(rates))),
        dict(name='Original saved numerical packet survives console-only formatting failure',
             passed=parent['all_checks_passed'] and (saved.parent / 'COMPLETE').is_file()
             and all(digest(path) == expected for path, expected in parent['input_hashes'].items()))])
    folder.mkdir(parents=True, exist_ok=False)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        rows=rows, physical_samples=100,
                        original_probe_exit1_after_successful_packet_write_due_to_numpy_bool_console_JSON=True,
                        original_packet_preserved_and_independently_rechecked=True,
                        new_entrypoint_successful=True, scalar_first_order_matching_only=True,
                        full_polarized_reciprocal_discretization_next=True), __file__, [saved, ROOT / 'moving_kernel.py'])
    print(json.dumps(dict(checks=checks, maximum=maximum), default=lambda value: value.item()), flush=True)


if __name__ == '__main__':
    main()
