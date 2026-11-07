import argparse
from thermal_wave_common import *
from stable_spectral_basis import StableBasis
from build_spectral_kernel import physical_block


def main(arguments):
    modest()
    folder = ROOT / 'banks' / arguments.name
    assert not folder.exists()
    folder.mkdir(parents=True, exist_ok=False)
    basis = StableBasis(arguments.count, arguments.quadrature, arguments.minimum, arguments.maximum, arguments.pivot)
    events = prior.event_geometry(arguments.theta, arguments.event_order)
    checks = [dict(name='Recurrence basis mass orthogonality', passed=basis.qr_orthogonality < 1e-10,
                   value=basis.qr_orthogonality),
              dict(name='Evaluated recurrence equals orthogonalized basis', passed=bool(np.max(abs(basis.evaluate(basis.nodes) - basis.values)) < 1e-7))]
    started = time.perf_counter()
    rows = []
    for degree in range(arguments.maximum_degree + 1):
        stiffness, names, discarded = physical_block(basis, arguments.theta, events, degree)
        mass = basis.mass / (2 * degree + 1)
        full_mass = linalg.block_diag(*([mass] * len(names)))
        eigenvalues = linalg.eigh(stiffness, full_mass, eigvals_only=True)
        checks.append(dict(name='Physical stable-basis block dissipates degree' + str(degree),
                           passed=float(max(eigenvalues)) < 1e-9, largest=float(max(eigenvalues)), smallest=float(min(eigenvalues))))
        if degree == 0:
            chemical = np.r_[basis.chemical, np.zeros(basis.count)]
            error = float(np.linalg.norm(stiffness @ chemical) / (np.linalg.norm(stiffness) * np.linalg.norm(chemical)))
            checks.append(dict(name='Chemical null retained without imposing an eigenvalue', passed=error < 1e-10, value=error))
        np.savez_compressed(folder / ('block-' + str(degree) + '.npz'), stiffness=stiffness, mass=mass,
                            eigenvalues=eigenvalues, theta=arguments.theta, degree=degree,
                            temperature=basis.temperature, chemical=basis.chemical, nodes=basis.nodes,
                            quadrature_measure=basis.measure, recurrence=basis.coefficients, norms=basis.norms,
                            mean=basis.mean, pivot=basis.pivot)
        rows.append(dict(degree=degree, names=names, discarded_weight_fraction=discarded))
        write_json(folder / 'progress.json', dict(state='running', degree=degree, elapsed=time.perf_counter() - started))
        print(json.dumps(dict(degree=degree, elapsed=time.perf_counter() - started)), flush=True)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        theta=arguments.theta, basis_count=arguments.count, quadrature_count=arguments.quadrature,
                        event_order=arguments.event_order, minimum=arguments.minimum, maximum=arguments.maximum,
                        pivot=arguments.pivot, maximum_degree=arguments.maximum_degree, rows=rows,
                        basis='Reorthogonalized rational recurrence retaining exact constant and x',
                        positive_physical_pair_Galerkin=True, no_small_shift_expansion=True,
                        elapsed=time.perf_counter() - started), __file__,
           [ROOT / 'stable_spectral_basis.py', ROOT / 'build_spectral_kernel.py', PARENT / 'grid_common.py'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--count', type=int, default=24)
    parser.add_argument('--quadrature', type=int, default=300)
    parser.add_argument('--event-order', type=int, default=6)
    parser.add_argument('--theta', type=float, default=4.596201578526332e-5)
    parser.add_argument('--maximum-degree', type=int, default=8)
    parser.add_argument('--minimum', type=float, default=1e-5)
    parser.add_argument('--maximum', type=float, default=60.)
    parser.add_argument('--pivot', type=float, default=3.)
    main(parser.parse_args())
