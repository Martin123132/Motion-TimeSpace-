import argparse
from observer_common import *
from build_mixed_bank import physical_mixed, background_profile
from build_spectral_kernel import physical_block


def main(arguments):
    modest()
    folder = ROOT / 'banks' / ('basis' + str(arguments.count))
    folder.mkdir(parents=True, exist_ok=False)
    basis = StableBasis(arguments.count)
    systems = [MixedSystem(model, 24, 8, 'event8') for model in ['heavy', 'cold']]
    checks = [dict(name='Refined basis mass orthogonality', passed=basis.qr_orthogonality < 1e-10, value=basis.qr_orthogonality)]
    evaluation_error = float(np.max(abs(basis.evaluate(basis.nodes) - basis.values)))
    checks.append(dict(name='Unchanged absolute recurrence re-evaluation gate', passed=evaluation_error < 1e-7, value=evaluation_error))
    assert all(row['passed'] for row in checks)
    started = time.perf_counter()
    temperatures = systems[0].ladder.temperatures
    for index, theta in enumerate(temperatures):
        contents = dict(theta=theta)
        for order in [6, 8]:
            events = previous.grid.event_geometry(theta, order)
            for degree in range(9):
                if order != (8 if degree == 8 else 6):
                    continue
                block, names, tail = physical_block(basis, theta, events, degree)
                mass = linalg.block_diag(*([basis.mass / (2 * degree + 1)] * len(names)))
                highest = float(max(linalg.eigh(block, mass, eigvals_only=True)))
                checks.append(dict(name='Refined Planck block dissipates theta' + str(index) + ' degree' + str(degree), passed=highest < 1e-9, value=highest))
                contents['block_' + str(degree)] = block
        np.savez_compressed(folder / ('planck-' + str(index) + '.npz'), **contents)
        print(json.dumps(dict(planck=index, elapsed=time.perf_counter() - started)), flush=True)
    prior_bank = json.loads((PARENT / 'banks/fine16/status.json').read_text())
    knots = prior_bank['knots']
    for index, expansion in enumerate(knots):
        theta = systems[0].background(expansion)['theta']
        backgrounds = []
        for system in systems:
            profile, shift, heat = background_profile(system, expansion)
            backgrounds.append((np.pad(profile, (0, arguments.count - 24)), shift, heat))
        contents = dict(expansion=expansion, theta=theta)
        for order in [6, 8]:
            events = previous.grid.event_geometry(theta, order)
            speeds, _ = previous.grid.prior.juttner_rule(theta, order)
            gamma = np.repeat(1 / np.sqrt(1 - speeds ** 2), 2 * order ** 3)
            for degree in range(9):
                if order != (8 if degree == 8 else 6):
                    continue
                angular = previous.grid.angular_correlations(events, degree)
                blocks, temperature, residual, tail = physical_mixed(basis, theta, events, gamma, angular, degree, backgrounds)
                contents['block_' + str(degree)] = blocks
                if degree == 0:
                    contents.update(temperature=temperature, residual=residual)
                    error = max(float(linalg.norm(basis.chemical @ block[:basis.count]) / max(linalg.norm(block), 1e-100)) for block in blocks)
                    checks.append(dict(name='Refined mixed left number null knot' + str(index), passed=error < 1e-10, value=error))
        np.savez_compressed(folder / ('mixed-' + str(index) + '.npz'), **contents)
        print(json.dumps(dict(mixed=index, elapsed=time.perf_counter() - started)), flush=True)
        write_json(folder / 'progress.json', dict(state='running', mixed_knots_done=index + 1, elapsed=time.perf_counter() - started))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        basis_count=arguments.count, quadrature=300, temperatures=temperatures.tolist(), knots=knots,
                        background_is_same_retained_24_function_trajectory=True,
                        event_orders='6 for degree0..7;8 for degree8', elapsed=time.perf_counter() - started), __file__,
           [PARENT / 'build_mixed_bank.py', PARENT / 'stable_pair.py',
            THERMAL_PARENT / 'build_spectral_kernel.py', THERMAL_PARENT / 'stable_spectral_basis.py',
            *[system.geometry.source for system in systems]])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', type=int, default=28)
    main(parser.parse_args())
