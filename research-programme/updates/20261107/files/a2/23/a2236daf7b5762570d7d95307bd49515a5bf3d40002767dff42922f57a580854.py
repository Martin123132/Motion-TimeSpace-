from grid_common import *
from build_bank import block as unsplit_block
from build_partitioned_bank import block as split_block
from cold_control import exact_cold


def main():
    modest()
    folder = ROOT / 'results/quadrature-repair'
    assert not folder.exists()
    theta = json.loads((ROOT / 'banks/main-96/status.json').read_text())['theta']
    nodes = np.geomspace(.001, 30., 64)
    events = event_geometry(theta, 4)
    rows, checks = [], []
    for degree in [0, 1, 2]:
        reference, mass, names, _ = split_block(nodes, theta, events, degree, 6)
        factor = linalg.cholesky(linalg.block_diag(*([mass] * len(names))), lower=True)
        initial = np.kron(np.eye(len(names)), nodes[:, None])
        cold = np.kron(exact_cold(degree), mass)
        response = linalg.solve_triangular(factor, (reference - cold) @ initial, lower=True)
        scale = float(np.linalg.norm(response))
        errors = []
        for label, builder, order in [('unsplit4', unsplit_block, 4), ('unsplit12', unsplit_block, 12),
                                       ('unsplit32', unsplit_block, 32), ('split4', split_block, 4)]:
            trial, _, _, _ = builder(nodes, theta, events, degree, order)
            difference = linalg.solve_triangular(factor, (trial - reference) @ initial, lower=True)
            error = float(np.linalg.norm(difference) / scale)
            errors.append(error)
            rows.append(dict(degree=degree, quadrature=label, relative_small_source_error=error,
                             reference='Split incoming and inverse-outgoing knots, six-point positive rule.',
                             same_nodes_events_and_physics=True))
        checks.append(dict(name='degree' + str(degree) + ': split quadrature resolves small source at unchanged gate',
                           passed=errors[-1] < .002, value=errors[-1]))
        checks.append(dict(name='degree' + str(degree) + ': finer unsplit quadrature approaches split reference',
                           passed=errors[2] < errors[0], original=errors[0], refined=errors[2]))
        checks.append(dict(name='degree' + str(degree) + ': resolving outgoing knots improves over original quadrature',
                           passed=errors[-1] < errors[0], original=errors[0], split=errors[-1]))
    folder.mkdir(parents=True, exist_ok=False)
    inputs = [ROOT / 'banks/main-96/status.json', ROOT / 'build_bank.py',
              ROOT / 'build_partitioned_bank.py', ROOT / 'cold_control.py']
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        rows=rows, only_quadrature_changed=True,
                        coarse_spectral_space_not_claimed_converged=True), __file__, inputs)
    print(json.dumps(dict(checks=checks, rows=rows)), flush=True)


if __name__ == '__main__':
    main()
