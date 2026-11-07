import argparse
from infrared_ladder import *
from build_spectral_kernel import physical_block


def main(arguments):
    modest()
    folder = ROOT / 'banks' / arguments.name
    folder.mkdir(parents=True, exist_ok=False)
    specification = dict(count=arguments.count, quadrature=arguments.quadrature, minimum=arguments.minimum, maximum=60., pivot=arguments.pivot)
    basis = ConsistentBasis(**specification)
    temperatures = np.array(json.loads((OBSERVER / 'banks/basis36/status.json').read_text())['temperatures'])
    checks = [dict(name='Infrared-aware basis mass orthogonality', passed=basis.qr_orthogonality < 1e-10, value=basis.qr_orthogonality),
        dict(name='Two-pass evaluation preserves unchanged absolute gate', passed=float(np.max(abs(basis.evaluate(basis.nodes) - basis.values))) < 1e-7)]
    assert all(row['passed'] for row in checks)
    started = time.perf_counter()
    for index, theta in enumerate(temperatures):
        events = thermal_wave.prior.event_geometry(theta, arguments.event_order)
        block, discarded = scalar_physical_block(basis, theta, events)
        values = linalg.eigh(block, basis.mass, eigvals_only=True)
        number_error = float(linalg.norm(block @ basis.chemical) / (linalg.norm(block) * linalg.norm(basis.chemical)))
        checks.extend([
            dict(name='Physical finite-shift dissipation at theta' + str(index), passed=float(max(values)) < 1e-9, value=float(max(values))),
            dict(name='Compton number null before adding emission at theta' + str(index), passed=number_error < 1e-10, value=number_error)])
        if index == 0:
            original, names, tail = physical_block(basis, theta, events, 0)
            difference = float(linalg.norm(block - original[:basis.count, :basis.count]) / linalg.norm(block))
            checks.append(dict(name='Scalar specialization equals original polarized intensity block', passed=difference < 1e-13, value=difference))
        np.savez_compressed(folder / ('planck-' + str(index) + '.npz'), stiffness=block, mass=basis.mass,
                            theta=theta, discarded_pair_weight=discarded, eigenvalues=values)
        write_json(folder / 'progress.json', dict(state='running', temperatures_done=index + 1, elapsed=time.perf_counter() - started))
        print(json.dumps(dict(temperature=index, elapsed=time.perf_counter() - started)), flush=True)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
        basis_spec=specification, temperatures=temperatures.tolist(), event_order=arguments.event_order,
        no_diffusion_substitution=True, numerical_pivot_not_physical_parameter=True,
        elapsed=time.perf_counter() - started), __file__,
        [ROOT / 'infrared_ladder.py', OBSERVER / 'consistent_spectral_basis.py', OBSERVER / 'banks/basis36/status.json',
         THERMAL_STAGE / 'build_spectral_kernel.py', THERMAL_STAGE.parent / 'polarized-heat-momentum-grid-20261007/grid_common.py'])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--count', type=int, default=36)
    parser.add_argument('--quadrature', type=int, default=420)
    parser.add_argument('--event-order', type=int, default=6)
    parser.add_argument('--minimum', type=float, default=1e-5)
    parser.add_argument('--pivot', type=float, default=.1)
    main(parser.parse_args())
