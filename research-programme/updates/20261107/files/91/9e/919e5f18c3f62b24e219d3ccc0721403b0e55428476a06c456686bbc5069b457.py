import argparse
from grid_common import *
from build_bank import frequency_mass


def partition(nodes, theta, events, first, last, order):
    incident = events['incident'][first:last, None]
    outgoing = events['outgoing'][first:last, None]
    shift = theta * incident * (1 - events['cosine'][first:last, None])
    dilation = incident * outgoing
    denominator = dilation - shift * nodes[None, :]
    inverse = np.divide(nodes[None, :], denominator, out=np.full_like(denominator, nodes[-1]), where=denominator > 0)
    inverse = np.clip(inverse, nodes[0], nodes[-1])
    breaks = np.sort(np.concatenate([np.broadcast_to(nodes, inverse.shape), inverse], axis=1), axis=1)
    abscissa, weights = np.polynomial.legendre.leggauss(order)
    widths = np.diff(breaks, axis=1)
    frequency = breaks[:, :-1, None] + .5 * widths[:, :, None] * (1 + abscissa)
    quadrature = .5 * widths[:, :, None] * weights
    ratio = 1 / (1 + shift[:, :, None] * frequency)
    final = dilation[:, :, None] * ratio * frequency
    occupation = 1 / np.expm1(frequency)
    bose = (1 + 1 / np.expm1(final)) / (1 + occupation)
    probability = frequency ** 2 * occupation * (1 + occupation) * quadrature / (2 * I3)
    probability *= events['weight'][first:last, None, None] * 1.5 * ratio ** 2 * bose
    extra = (1 - ratio) ** 2 / ratio
    trace = 1 + events['cosine'][first:last, None, None] ** 2 + extra
    inside = (final >= nodes[0]) & (final <= nodes[-1]) & (quadrature > 0)
    discarded = float(np.sum((probability * trace)[~inside]))
    total = float(np.sum(probability * trace))
    source_indices = np.clip(np.searchsorted(nodes, frequency) - 1, 0, len(nodes) - 2)
    target_indices = np.clip(np.searchsorted(nodes, final) - 1, 0, len(nodes) - 2)
    source_fraction = (frequency - nodes[source_indices]) / (nodes[source_indices + 1] - nodes[source_indices])
    target_fraction = (final - nodes[target_indices]) / (nodes[target_indices + 1] - nodes[target_indices])
    event_indices = np.broadcast_to(np.arange(first, last)[:, None, None], frequency.shape)[inside]
    return dict(source=source_indices[inside], target=target_indices[inside],
                source_basis=np.array([1 - source_fraction[inside], source_fraction[inside]]),
                target_basis=np.array([1 - target_fraction[inside], target_fraction[inside]]),
                probability=probability[inside], extra=extra[inside], trace=trace[inside],
                event_indices=event_indices, discarded=discarded, total=total)


def block(nodes, theta, events, degree, cell_order):
    first, second, names = angular_correlations(events, degree)
    modes, points = len(names), len(nodes)
    stiffness = np.zeros((modes * points, modes * points))
    base = np.zeros((points, points))
    pairs = [(left, right) for left in range(modes) for right in range(modes)
             if max(np.max(abs(first[left, right])), np.max(abs(second[left, right]))) > 1e-14]
    discarded, total = 0., 0.
    diagonal = np.arange(points - 1)
    for chunk in range(0, len(events['weight']), 32):
        data = partition(nodes, theta, events, chunk, min(chunk + 32, len(events['weight'])), cell_order)
        discarded += data['discarded']
        total += data['total']
        conductance = -.5 * data['probability'] * data['trace'] / (2 * degree + 1)
        for side in ['source', 'target']:
            indices, basis = data[side], data[side + '_basis']
            for left in range(2):
                for right in range(2):
                    values = np.bincount(indices, weights=conductance * basis[left] * basis[right], minlength=points)
                    base[diagonal + left, diagonal + right] += values[:-1]
        for source_mode, target_mode in pairs:
            correlation = first[source_mode, target_mode, data['event_indices']]
            correlation += data['extra'] * second[source_mode, target_mode, data['event_indices']]
            probability = .5 * data['probability'] * correlation
            source_slice = slice(source_mode * points, (source_mode + 1) * points)
            target_slice = slice(target_mode * points, (target_mode + 1) * points)
            for left in range(2):
                for right in range(2):
                    indices = (data['source'] + left) * points + data['target'] + right
                    values = probability * data['source_basis'][left] * data['target_basis'][right]
                    contribution = np.bincount(indices, weights=values, minlength=points ** 2).reshape(points, points)
                    stiffness[source_slice, target_slice] += contribution
                    stiffness[target_slice, source_slice] += contribution.T
    for mode in range(modes):
        target = slice(mode * points, (mode + 1) * points)
        stiffness[target, target] += base
    return stiffness, 2 * frequency_mass(nodes) / (2 * degree + 1), names, dict(
        boundary_discarded_weight_fraction=discarded / total,
        numerically_zero_cross_channel_pairs_skipped=modes ** 2 - len(pairs),
        omitted_cross_pair_threshold=1e-14)


def main(arguments):
    modest()
    folder = ROOT / 'banks' / arguments.name
    assert not folder.exists()
    folder.mkdir(parents=True, exist_ok=False)
    source = STEP / 'runs/heavy-warm-angular/status.json'
    theta = json.loads(source.read_text())['theta']
    nodes = np.geomspace(arguments.minimum, arguments.maximum_frequency, arguments.points)
    events = event_geometry(theta, arguments.order)
    started = time.perf_counter()
    rows, checks = [], []
    for degree in range(arguments.maximum_degree + 1):
        stiffness, mass, names, details = block(nodes, theta, events, degree, arguments.cell_order)
        full_mass = linalg.block_diag(*([mass] * len(names)))
        eigenvalues = linalg.eigh(stiffness, full_mass, eigvals_only=True)
        checks.append(dict(name='Split-cell physical block dissipates degree' + str(degree),
                           passed=float(max(eigenvalues)) < 1e-9, largest_eigenvalue=float(max(eigenvalues))))
        if degree == 0:
            chemical = np.r_[np.ones(len(nodes)), np.zeros(len(nodes))]
            error = float(np.linalg.norm(stiffness @ chemical) / (np.linalg.norm(stiffness) * np.linalg.norm(chemical)))
            checks.append(dict(name='Split-cell chemical null remains exact', passed=error < 1e-10, value=error))
        np.savez_compressed(folder / ('block-' + str(degree) + '.npz'), nodes=nodes, mass=mass,
                            stiffness=stiffness, eigenvalues=eigenvalues, theta=theta, degree=degree)
        rows.append(dict(degree=degree, names=names, **details))
        progress = dict(state='running', degree=degree, target_degree=arguments.maximum_degree,
                        elapsed_seconds=time.perf_counter() - started)
        write_json(folder / 'progress.json', progress)
        print(json.dumps(progress), flush=True)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        points=arguments.points, maximum_degree=arguments.maximum_degree, theta=theta,
                        event_order=arguments.order, cell_order=arguments.cell_order,
                        minimum_frequency=arguments.minimum, maximum_frequency=arguments.maximum_frequency,
                        rows=rows, incoming_and_inverse_outgoing_knots_both_split=True,
                        positive_quadrature_reciprocal_pair_form_preserved=True,
                        elapsed_seconds=time.perf_counter() - started), __file__, [source, ROOT / 'build_bank.py'])
    print(json.dumps(dict(checks=checks, elapsed=time.perf_counter() - started)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--points', type=int, default=256)
    parser.add_argument('--maximum-degree', type=int, default=8)
    parser.add_argument('--order', type=int, default=8)
    parser.add_argument('--cell-order', type=int, default=4)
    parser.add_argument('--minimum', type=float, default=1e-5)
    parser.add_argument('--maximum-frequency', type=float, default=60.)
    main(parser.parse_args())
