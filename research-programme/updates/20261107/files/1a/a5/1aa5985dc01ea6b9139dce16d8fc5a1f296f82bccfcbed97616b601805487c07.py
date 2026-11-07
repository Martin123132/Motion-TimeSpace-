import argparse
from thermal_wave_common import *
from kernel_ladder import KernelLadder
from build_spectral_kernel import physical_block


def main(arguments):
    modest()
    folder = ROOT / 'banks' / arguments.name
    assert not folder.exists()
    folder.mkdir(parents=True, exist_ok=False)
    ladder = KernelLadder(arguments.count)
    temperatures = np.r_[ladder.temperatures, math.sqrt(ladder.temperatures[-2] * ladder.temperatures[-1])]
    checks, rows = [], []
    started = time.perf_counter()
    mass = ladder.basis.mass / 17
    full_mass = linalg.block_diag(*([mass] * 4))
    for index, theta in enumerate(temperatures):
        events = prior.event_geometry(float(theta), arguments.event_order)
        stiffness, names, discarded = physical_block(ladder.basis, float(theta), events, 8)
        eigenvalues = linalg.eigh(stiffness, full_mass, eigvals_only=True)
        checks.append(dict(name='Refined physical degree8 dissipates at temperature index' + str(index),
                           passed=float(max(eigenvalues)) < 1e-9, value=float(max(eigenvalues))))
        np.savez_compressed(folder / ('theta-' + str(index) + '.npz'), theta=theta, stiffness=stiffness,
                            mass=mass, eigenvalues=eigenvalues)
        rows.append(dict(index=index, theta=float(theta), names=names, discarded_weight_fraction=discarded))
        write_json(folder / 'progress.json', dict(state='running', index=index, elapsed=time.perf_counter() - started))
        print(json.dumps(dict(index=index, elapsed=time.perf_counter() - started)), flush=True)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        basis_count=arguments.count, event_order=arguments.event_order, degree=8, rows=rows,
                        scope='Independent event-quadrature refinement of highest retained angular block, including hot midpoint.',
                        elapsed=time.perf_counter() - started), __file__,
           [ROOT / 'kernel_ladder.py', ROOT / 'stable_spectral_basis.py', ROOT / 'build_spectral_kernel.py',
            PARENT / 'grid_common.py', *ladder.inputs])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--count', type=int, default=16)
    parser.add_argument('--event-order', type=int, default=8)
    main(parser.parse_args())
