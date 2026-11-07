import argparse
from kernel_common import *


def event_rule(theta, order):
    speeds, radial_weights = juttner_rule(theta, order)
    electron_cosine, electron_weights = np.polynomial.legendre.leggauss(order)
    scattering_cosine, scattering_weights = np.polynomial.legendre.leggauss(order)
    azimuth = 2 * np.pi * (np.arange(2 * order) + .5) / (2 * order)
    cosine = scattering_cosine[:, None]
    incoming = np.array([0., 0., 1.])
    result = {key: [] for key in ['incident', 'outgoing', 'cosine', 'lab_cosine', 'weight']}
    for speed, radial_weight in zip(speeds, radial_weights):
        for electron_node, electron_weight in zip(electron_cosine, electron_weights / 2):
            beta = speed * np.array([np.sqrt(1 - electron_node ** 2), 0., electron_node])
            rest_initial, incident, _ = boost(incoming, beta)
            transverse = np.array([rest_initial[2], 0., -rest_initial[0]])
            second = np.cross(rest_initial, transverse)
            final_rest = cosine[..., None] * rest_initial + np.sqrt(1 - cosine ** 2)[..., None] * (
                np.cos(azimuth)[None, :, None] * transverse + np.sin(azimuth)[None, :, None] * second)
            final_lab, outgoing, _ = boost(final_rest, -beta)
            count = len(scattering_cosine) * len(azimuth)
            result['incident'].extend(np.full(count, incident))
            result['outgoing'].extend(outgoing.ravel())
            result['cosine'].extend(np.broadcast_to(cosine, outgoing.shape).ravel())
            result['lab_cosine'].extend(final_lab[..., 2].ravel())
            weights = radial_weight * electron_weight * (1 - beta[2]) * scattering_weights[:, None] / len(azimuth)
            result['weight'].extend(np.broadcast_to(weights, outgoing.shape).ravel())
    return {key: np.array(values) for key, values in result.items()}


def assemble(points, theta, order=8, cell_order=4, minimum=.001, maximum=30.):
    nodes = np.geomspace(minimum, maximum, points)
    mass = np.zeros((points, points))
    stiffness = np.zeros_like(mass)
    events = event_rule(theta, order)
    quadrature, weights = np.polynomial.legendre.leggauss(cell_order)
    mass_quadrature, mass_weights = np.polynomial.legendre.leggauss(10)
    discarded, total, strong_work = 0., 0., 0.
    for cell in range(points - 1):
        left, right = nodes[cell], nodes[cell + 1]
        width = right - left
        sample = (right + left) / 2 + mass_quadrature * width / 2
        basis = np.array([(right - sample) / width, (sample - left) / width])
        occupation = 1 / np.expm1(sample)
        measure = sample ** 2 * occupation * (1 + occupation) * mass_weights * width / 2 / 3 / previous.I3_PLANCK
        mass[cell:cell + 2, cell:cell + 2] += (basis * measure) @ basis.T
        for node, weight in zip(quadrature, weights):
            frequency = (right + left) / 2 + node * width / 2
            initial_basis = np.array([(1 - node) / 2, (1 + node) / 2])
            rest_frequency = frequency * events['incident']
            ratio = 1 / (1 + theta * rest_frequency * (1 - events['cosine']))
            final = rest_frequency * ratio * events['outgoing']
            occupation = 1 / np.expm1(frequency)
            bose = (1 + 1 / np.expm1(final)) / (1 + occupation)
            rate = events['weight'] * 3 / 8 * ratio ** 2 * (ratio + 1 / ratio - 1 + events['cosine'] ** 2) * bose
            node_measure = frequency ** 2 * occupation * (1 + occupation) * weight * width / 2 / 3 / previous.I3_PLANCK
            full = node_measure * rate
            inside = (final >= minimum) & (final <= maximum)
            discarded += float(np.sum(full[~inside]))
            total += float(np.sum(full))
            final = final[inside]
            angular = events['lab_cosine'][inside]
            conductance = full[inside]
            index = np.clip(np.searchsorted(nodes, final) - 1, 0, points - 2)
            fraction = (final - nodes[index]) / (nodes[index + 1] - nodes[index])
            final_basis = np.array([1 - fraction, fraction])
            strong_work += float(np.sum(conductance * frequency * (angular * final - frequency)))
            for initial_side in range(2):
                for final_side in range(2):
                    stiffness[cell + initial_side, cell + final_side] -= .5 * np.sum(conductance) * initial_basis[initial_side] * initial_basis[final_side]
                    np.add.at(stiffness, (index + initial_side, index + final_side), -.5 * conductance * final_basis[initial_side] * final_basis[final_side])
                    cross = .5 * conductance * angular * initial_basis[initial_side] * final_basis[final_side]
                    np.add.at(stiffness, (np.full(len(index), cell + initial_side), index + final_side), cross)
                    np.add.at(stiffness, (index + final_side, np.full(len(index), cell + initial_side)), cross)
    return nodes, mass, stiffness, dict(discarded_event_measure_fraction=discarded / total,
        independently_integrated_strong_work=strong_work,
        weak_work=float(nodes @ stiffness @ nodes), events_per_frequency=len(events['weight']))


def evolve(nodes, mass, stiffness, inertia):
    count = len(nodes)
    metric = linalg.block_diag(mass, inertia)
    coupling = np.column_stack([np.eye(count), -nodes])
    full = coupling.T @ stiffness @ coupling
    factor = linalg.cholesky(metric, lower=True)
    symmetric = linalg.solve_triangular(factor, full, lower=True)
    symmetric = linalg.solve_triangular(factor, symmetric.T, lower=True).T
    eigenvalues, eigenvectors = linalg.eigh((symmetric + symmetric.T) / 2)
    times = np.array([0., .001, .01, .1, 1., 6.])
    histories, checks = {}, []
    for fixture_name in ['smooth', 'oscillatory']:
        potential = .003 * nodes * np.exp(-np.log(nodes / 3) ** 2 / 8)
        if fixture_name == 'oscillatory':
            potential *= np.sin(80 * np.log(nodes))
        initial = np.r_[potential, 0.]
        transformed = factor.T @ initial
        coordinates = eigenvectors.T @ transformed
        reference_momentum = nodes @ mass @ potential
        invariant_row = np.r_[mass @ nodes, inertia]
        reference_entropy = transformed @ transformed / 2
        exact = np.array([linalg.solve_triangular(factor.T, eigenvectors @ (np.exp(eigenvalues * depth) * coordinates), lower=False) for depth in times])
        entropy = np.einsum('ti,ij,tj->t', exact, metric, exact) / 2
        error = max(abs(exact @ invariant_row - reference_momentum)) / max(np.sqrt(reference_entropy), 1e-30)
        checks.append(dict(name=fixture_name + ': combined photon/plasma momentum conserved', passed=float(error) < 1e-9, value=float(error)))
        checks.append(dict(name=fixture_name + ': coupled quadratic entropy does not increase',
                           passed=bool(np.max(np.diff(entropy)) <= 1e-10 * reference_entropy),
                           final_entropy_ratio=float(entropy[-1] / reference_entropy)))
        time_errors = []
        for step in [1e-4, 5e-5]:
            multiplier = (1 + step * eigenvalues / 2) / (1 - step * eigenvalues / 2)
            approximations = []
            for depth in times:
                steps = int(round(depth / step))
                evolved = eigenvectors @ (multiplier ** steps * coordinates)
                approximations.append(linalg.solve_triangular(factor.T, evolved, lower=False))
            residual = np.array(approximations) - exact
            errors = np.sqrt(np.maximum(np.einsum('ti,ij,tj->t', residual, metric, residual), 0)) / np.linalg.norm(transformed)
            time_errors.append(float(max(errors)))
        checks.append(dict(name=fixture_name + ': midpoint agrees with independent semidiscrete exponential',
                           passed=max(time_errors) < .002 and time_errors[-1] < .4 * time_errors[0],
                           errors=time_errors, gate=.002))
        histories[fixture_name] = exact
    return eigenvalues, times, histories, checks


def main(arguments):
    modest()
    folder = ROOT / 'runs' / arguments.name
    assert not folder.exists()
    folder.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter()
    source = PARENT / 'runs/synthetic-fine/status.json'
    parent = json.loads(source.read_text())
    theta, inertia = parent['theta'], parent['inertia']
    nodes, mass, stiffness, details = assemble(arguments.points, theta, arguments.order, arguments.cell_order)
    symmetric = linalg.eigh(stiffness, mass, eigvals_only=True)
    eigenvalues, times, histories, checks = evolve(nodes, mass, stiffness, inertia)
    weak_error = abs(details['weak_work'] - details['independently_integrated_strong_work']) / abs(details['weak_work'])
    checks.extend([
        dict(name='Finite-shift photon spectrum strictly damped on tested dipole grid', passed=float(max(symmetric)) < 0, largest=float(max(symmetric)), smallest=float(min(symmetric))),
        dict(name='Coupled generator negative semidefinite with common-velocity null mode', passed=float(max(eigenvalues)) < 1e-9 and abs(float(max(eigenvalues))) < 1e-9,
             largest=float(max(eigenvalues)), smallest=float(min(eigenvalues))),
        dict(name='Reciprocal weak work agrees with independently integrated strong form', passed=weak_error < .002, value=weak_error, gate=.002),
        dict(name='Boundary-discarded event measure explicitly bounded', passed=details['discarded_event_measure_fraction'] < 1e-4,
             value=details['discarded_event_measure_fraction'], gate=1e-4)])
    np.savez_compressed(folder / 'operator.npz', nodes=nodes, mass=mass, stiffness=stiffness, eigenvalues=symmetric,
                        coupled_eigenvalues=eigenvalues, theta=theta, inertia=inertia, times=times, **histories)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        points=arguments.points, event_order=arguments.order, cell_order=arguments.cell_order,
                        theta=theta, inertia=inertia, details=details,
                        dipole_only_time_evolution_full_tensor_matching_separate=True,
                        reciprocal_Galerkin_form_from_physical_event_integral_not_fitted_damping=True,
                        piecewise_linear_frequency_potential_no_moment_closure=True,
                        elapsed_seconds=time.perf_counter() - started), __file__, [source])
    print(json.dumps(dict(run=arguments.name, checks=checks, details=details, elapsed=time.perf_counter() - started)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--points', type=int, default=384)
    parser.add_argument('--order', type=int, default=8)
    parser.add_argument('--cell-order', type=int, default=4)
    main(parser.parse_args())
