import argparse
from thermal_wave_common import *


def physical_block(basis, theta, events, degree):
    first, second, names = prior.angular_correlations(events, degree)
    count, modes = basis.count, len(names)
    stiffness = np.zeros((modes * count, modes * count))
    base = np.zeros((count, count))
    number_block = np.zeros_like(base)
    discarded, total = 0., 0.
    pairs = [(left, right) for left in range(modes) for right in range(modes)
             if max(np.max(abs(first[left, right])), np.max(abs(second[left, right]))) > 1e-14
             and not (degree == 0 and left == right == 0)]
    for frequency, measure, initial in zip(basis.nodes, basis.measure / 2, basis.values):
        ratio = 1 / (1 + theta * frequency * events['incident'] * (1 - events['cosine']))
        extra = (1 - ratio) ** 2 / ratio
        final = frequency * events['incident'] * ratio * events['outgoing']
        bose = (1 + 1 / np.expm1(final)) / (1 + 1 / np.expm1(frequency))
        probability = measure * events['weight'] * 1.5 * ratio ** 2 * bose
        trace = (1 + events['cosine'] ** 2 + extra) / (2 * degree + 1)
        inside = (final >= basis.minimum) & (final <= basis.maximum)
        discarded += float(np.sum((probability * trace)[~inside]))
        total += float(np.sum(probability * trace))
        target = basis.evaluate(final[inside])
        probability, trace, extra = probability[inside], trace[inside], extra[inside]
        conductance = probability * trace
        base -= .5 * (conductance.sum() * np.outer(initial, initial) + (target.T * conductance) @ target)
        if degree == 0:
            difference = initial[None, :] - target
            number_block -= .5 * (difference.T * conductance) @ difference
        for left, right in pairs:
            coefficient = .5 * probability * (first[left, right, inside] + extra * second[left, right, inside])
            cross = np.outer(initial, coefficient @ target)
            left_slice = slice(left * count, (left + 1) * count)
            right_slice = slice(right * count, (right + 1) * count)
            stiffness[left_slice, right_slice] += cross
            stiffness[right_slice, left_slice] += cross.T
    for mode in range(modes):
        target = slice(mode * count, (mode + 1) * count)
        stiffness[target, target] += number_block if degree == 0 and mode == 0 else base
    return stiffness, names, discarded / total


def main(arguments):
    modest()
    folder = ROOT / 'banks' / arguments.name
    assert not folder.exists()
    folder.mkdir(parents=True, exist_ok=False)
    basis = SpectralBasis(arguments.count, arguments.quadrature, arguments.minimum, arguments.maximum, arguments.pivot)
    theta = arguments.theta
    events = prior.event_geometry(theta, arguments.event_order)
    checks = [dict(name='Weighted spectral basis orthogonality', passed=basis.qr_orthogonality < 1e-8,
                   value=basis.qr_orthogonality, raw_condition=basis.raw_condition)]
    started = time.perf_counter()
    rows = []
    for degree in range(arguments.maximum_degree + 1):
        stiffness, names, discarded = physical_block(basis, theta, events, degree)
        mass = basis.mass / (2 * degree + 1)
        full_mass = linalg.block_diag(*([mass] * len(names)))
        eigenvalues = linalg.eigh(stiffness, full_mass, eigvals_only=True)
        checks.append(dict(name='Physical spectral block dissipates degree' + str(degree),
                           passed=float(max(eigenvalues)) < 1e-9, largest=float(max(eigenvalues)), smallest=float(min(eigenvalues))))
        if degree == 0:
            chemical = np.r_[basis.chemical, np.zeros(basis.count)]
            error = float(np.linalg.norm(stiffness @ chemical) / (np.linalg.norm(stiffness) * np.linalg.norm(chemical)))
            checks.append(dict(name='Exact constant-basis pair difference conserves photon number',
                               passed=error < 1e-10, value=error))
        np.savez_compressed(folder / ('block-' + str(degree) + '.npz'), stiffness=stiffness, mass=mass,
                            eigenvalues=eigenvalues, theta=theta, degree=degree, temperature=basis.temperature,
                            chemical=basis.chemical, transform=basis.transform, pivot=basis.pivot,
                            nodes=basis.nodes, quadrature_measure=basis.measure)
        rows.append(dict(degree=degree, names=names, discarded_weight_fraction=discarded))
        write_json(folder / 'progress.json', dict(state='running', degree=degree, elapsed=time.perf_counter() - started))
        print(json.dumps(dict(degree=degree, elapsed=time.perf_counter() - started)), flush=True)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        theta=theta, basis_count=arguments.count, quadrature_count=arguments.quadrature,
                        event_order=arguments.event_order, minimum=arguments.minimum, maximum=arguments.maximum,
                        pivot=arguments.pivot, maximum_degree=arguments.maximum_degree, rows=rows,
                        no_small_shift_expansion=True, no_eigenvalue_clipping=True,
                        basis_parameters_are_numerical_not_fitted_physical_coefficients=True,
                        elapsed=time.perf_counter() - started), __file__, [PARENT / 'grid_common.py'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--count', type=int, default=16)
    parser.add_argument('--quadrature', type=int, default=240)
    parser.add_argument('--event-order', type=int, default=6)
    parser.add_argument('--theta', type=float, default=4.596201578526332e-5)
    parser.add_argument('--maximum-degree', type=int, default=8)
    parser.add_argument('--minimum', type=float, default=1e-5)
    parser.add_argument('--maximum', type=float, default=60.)
    parser.add_argument('--pivot', type=float, default=3.)
    main(parser.parse_args())
