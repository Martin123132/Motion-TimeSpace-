import argparse
from grid_common import *


def frequency_mass(nodes):
    mass = np.zeros((len(nodes), len(nodes)))
    quadrature, weights = np.polynomial.legendre.leggauss(10)
    for cell in range(len(nodes) - 1):
        left, right = nodes[cell:cell + 2]
        width = right - left
        frequency = (right + left) / 2 + quadrature * width / 2
        basis = np.array([(1 - quadrature) / 2, (1 + quadrature) / 2])
        occupation = 1 / np.expm1(frequency)
        measure = frequency ** 2 * occupation * (1 + occupation) * weights * width / 2 / (2 * I3)
        mass[cell:cell + 2, cell:cell + 2] += (basis * measure) @ basis.T
    return mass


def block(nodes, theta, events, degree, cell_order=4):
    first, second, names = angular_correlations(events, degree)
    modes, points = len(names), len(nodes)
    stiffness = np.zeros((modes * points, modes * points))
    base = np.zeros((points, points))
    quadrature, weights = np.polynomial.legendre.leggauss(cell_order)
    discarded, total = 0., 0.
    pairs = [(left, right) for left in range(modes) for right in range(modes)
             if max(np.max(abs(first[left, right])), np.max(abs(second[left, right]))) > 1e-14]
    for cell in range(points - 1):
        left, right = nodes[cell:cell + 2]
        width = right - left
        for node, weight in zip(quadrature, weights):
            frequency = (right + left) / 2 + node * width / 2
            initial_basis = np.array([(1 - node) / 2, (1 + node) / 2])
            ratio = 1 / (1 + theta * frequency * events['incident'] * (1 - events['cosine']))
            extra = (1 - ratio) ** 2 / ratio
            final = frequency * events['incident'] * ratio * events['outgoing']
            occupation = 1 / np.expm1(frequency)
            bose = (1 + 1 / np.expm1(final)) / (1 + occupation)
            measure = frequency ** 2 * occupation * (1 + occupation) * weight * width / 2 / (2 * I3)
            probability = measure * events['weight'] * 1.5 * ratio ** 2 * bose
            trace = 1 + events['cosine'] ** 2 + extra
            inside = (final >= nodes[0]) & (final <= nodes[-1])
            discarded += float(np.sum((probability * trace)[~inside]))
            total += float(np.sum(probability * trace))
            final, probability, trace, extra = final[inside], probability[inside], trace[inside], extra[inside]
            indices = np.clip(np.searchsorted(nodes, final) - 1, 0, points - 2)
            fraction = (final - nodes[indices]) / (nodes[indices + 1] - nodes[indices])
            final_basis = np.array([1 - fraction, fraction])
            conductance = probability * trace / (2 * degree + 1)
            base[cell:cell + 2, cell:cell + 2] -= .5 * conductance.sum() * np.outer(initial_basis, initial_basis)
            for first_side in range(2):
                for second_side in range(2):
                    contribution = np.bincount(indices, weights=-.5 * conductance * final_basis[first_side] * final_basis[second_side], minlength=points)
                    diagonal_indices = np.arange(points - 1)
                    base[diagonal_indices + first_side, diagonal_indices + second_side] += contribution[:-1]
            for initial_mode, final_mode in pairs:
                cross = .5 * probability * (first[initial_mode, final_mode, inside] + extra * second[initial_mode, final_mode, inside])
                for final_side in range(2):
                    contribution = np.bincount(indices + final_side, weights=cross * final_basis[final_side], minlength=points)
                    target = slice(final_mode * points, (final_mode + 1) * points)
                    for initial_side in range(2):
                        row = initial_mode * points + cell + initial_side
                        stiffness[row, target] += initial_basis[initial_side] * contribution
                        stiffness[target, row] += initial_basis[initial_side] * contribution
    for mode in range(modes):
        target = slice(mode * points, (mode + 1) * points)
        stiffness[target, target] += base
    mass = frequency_mass(nodes) * 2 / (2 * degree + 1)
    return stiffness, mass, names, dict(boundary_discarded_weight_fraction=discarded / total,
                                       numerically_zero_cross_channel_pairs_skipped=modes ** 2 - len(pairs),
                                       omitted_cross_pair_threshold=1e-14)


def main(arguments):
    modest()
    folder = ROOT / 'banks' / arguments.name
    assert not folder.exists()
    folder.mkdir(parents=True, exist_ok=False)
    source = STEP / 'runs/heavy-warm-angular/status.json'
    parent = json.loads(source.read_text())
    theta = parent['theta']
    nodes = np.geomspace(arguments.minimum, arguments.maximum_frequency, arguments.points)
    events = event_geometry(theta, arguments.order)
    started = time.perf_counter()
    checks, rows = [], []
    for degree in range(arguments.maximum_degree + 1):
        stiffness, mass, names, details = block(nodes, theta, events, degree, arguments.cell_order)
        full_mass = linalg.block_diag(*([mass] * len(names)))
        eigenvalues = linalg.eigh(stiffness, full_mass, eigvals_only=True)
        largest = float(max(eigenvalues))
        checks.append(dict(name='Physical full-polarization collision block dissipates degree' + str(degree), passed=largest < 1e-9,
                           largest_eigenvalue=largest, smallest_eigenvalue=float(min(eigenvalues))))
        if degree == 0:
            chemical = np.r_[np.ones(len(nodes)), np.zeros(len(nodes))]
            error = float(np.linalg.norm(stiffness @ chemical) / max(np.linalg.norm(stiffness) * np.linalg.norm(chemical), 1e-100))
            checks.append(dict(name='Chemical photon-number null vector from physical pair assembly', passed=error < 1e-10, value=error))
        np.savez_compressed(folder / ('block-' + str(degree) + '.npz'), nodes=nodes, mass=mass, stiffness=stiffness,
                            eigenvalues=eigenvalues, theta=theta, degree=degree)
        rows.append(dict(degree=degree, names=names, **details))
        progress = dict(state='running', degree=degree, target_degree=arguments.maximum_degree,
                        elapsed_seconds=time.perf_counter() - started)
        write_json(folder / 'progress.json', progress)
        print(json.dumps(progress), flush=True)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        points=arguments.points, maximum_degree=arguments.maximum_degree, theta=theta,
                        event_order=arguments.order, cell_order=arguments.cell_order,
                        minimum_frequency=arguments.minimum, maximum_frequency=arguments.maximum_frequency,
                        rows=rows, independent_m_values_degenerate_by_rotational_invariance=True,
                        reciprocal_physical_Galerkin_not_an_angular_moment_closure=True,
                        elapsed_seconds=time.perf_counter() - started), __file__, [source])
    print(json.dumps(dict(checks=checks, elapsed=time.perf_counter() - started)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--points', type=int, default=96)
    parser.add_argument('--maximum-degree', type=int, default=8)
    parser.add_argument('--order', type=int, default=6)
    parser.add_argument('--cell-order', type=int, default=4)
    parser.add_argument('--minimum', type=float, default=.001)
    parser.add_argument('--maximum-frequency', type=float, default=30.)
    main(parser.parse_args())
