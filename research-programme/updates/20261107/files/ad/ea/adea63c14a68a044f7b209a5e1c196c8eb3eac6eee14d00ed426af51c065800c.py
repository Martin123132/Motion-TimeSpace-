import argparse
from grid_common import *


def parent_coefficients(label, maximum):
    source = WAVES / 'runs' / (label + '-sixteenth') / 'evolution.npz'
    with np.load(source, allow_pickle=False) as saved:
        state = saved['final_state'][0]
        own_maximum = int(saved['angular_maximum'])
    kernel = angular.AngularKernel(own_maximum + 4, 2 * (own_maximum + 4))
    photon = state[26:26 + 9 * kernel.count].reshape(kernel.count, 3, 3)
    axis = np.array([1., 0., 0.])
    coefficients, reconstructed = [], np.zeros_like(photon)
    for degree in range(maximum + 1):
        tensors, names = modal_tensors(kernel.directions, axis, degree)
        values = (2 * degree + 1) / 2 * np.einsum('n,anij,nji->a', kernel.weights, tensors, photon)
        coefficients.append(values / 2)
        reconstructed += np.einsum('a,anij->nij', values, tensors)
    error = float(np.linalg.norm(reconstructed - photon) / np.linalg.norm(photon))
    return coefficients, state[23], source, error


def system(stiffness, mass, nodes, degree, capacity):
    modes = stiffness.shape[0] // len(nodes)
    metric = linalg.block_diag(*([mass] * modes))
    columns = []
    if degree in [0, 1]:
        field_equilibrium = np.r_[nodes, np.zeros((modes - 1) * len(nodes))]
        coupling = np.column_stack([np.eye(len(metric)), -field_equilibrium])
        full_stiffness = coupling.T @ stiffness @ coupling
        metric = linalg.block_diag(metric, capacity)
        columns.append(np.r_[field_equilibrium, 1.])
        if degree == 0:
            columns.insert(0, np.r_[np.ones(len(nodes)), np.zeros((modes - 1) * len(nodes) + 1)])
    else:
        full_stiffness = stiffness
    factor = linalg.cholesky(metric, lower=True)
    symmetric = linalg.solve_triangular(factor, full_stiffness, lower=True)
    symmetric = linalg.solve_triangular(factor, symmetric.T, lower=True).T
    symmetric = (symmetric + symmetric.T) / 2
    if columns:
        exact_nulls = np.column_stack(columns)
        transformed = factor.T @ exact_nulls
        orthogonal, _ = np.linalg.qr(transformed, mode='complete')
        nulls, complement = orthogonal[:, :len(columns)], orthogonal[:, len(columns):]
        null_error = float(np.linalg.norm(symmetric @ nulls) / max(np.linalg.norm(symmetric), 1e-100))
        invariants = exact_nulls.T @ metric
    else:
        nulls, complement = np.zeros((len(metric), 0)), np.eye(len(metric))
        null_error, invariants = 0., np.zeros((0, len(metric)))
    reduced = complement.T @ symmetric @ complement
    eigenvalues, vectors = linalg.eigh((reduced + reduced.T) / 2)
    assert max(eigenvalues) < 1e-8, (degree, max(eigenvalues))
    basis = complement @ vectors
    return metric, factor, nulls, basis, eigenvalues, invariants, full_stiffness, null_error


def main(arguments):
    modest()
    bank = ROOT / 'banks' / arguments.bank
    metadata = json.loads((bank / 'status.json').read_text())
    assert metadata['all_checks_passed']
    folder = ROOT / 'runs' / arguments.name
    assert not folder.exists()
    folder.mkdir(parents=True, exist_ok=False)
    source = STEP / 'runs' / (arguments.model + '-warm-angular') / 'status.json'
    plasma = json.loads(source.read_text())
    heat_capacity, inertia = plasma['heat_capacity'], plasma['inertia']
    maximum = metadata['maximum_degree']
    coefficients, velocity, mode_source, reconstruction = parent_coefficients(arguments.model, maximum)
    heat_time = heat_capacity / (4 * metadata['theta'])
    times = np.unique(np.r_[0., np.geomspace(heat_time / 50, .001, 25), .01, .03, .1, .3, 1., 3., 6.])
    checks, rows, inputs = [], [], [bank / 'status.json', source, mode_source]
    started = time.perf_counter()
    for degree in range(maximum + 1):
        path = bank / ('block-' + str(degree) + '.npz')
        with np.load(path, allow_pickle=False) as saved:
            nodes, mass, stiffness = saved['nodes'], saved['mass'], saved['stiffness']
        names = metadata['rows'][degree]['names']
        capacity = heat_capacity if degree == 0 else inertia
        metric, factor, nulls, basis, eigenvalues, invariants, full_stiffness, null_error = system(stiffness, mass, nodes, degree, capacity)
        if arguments.fixture == 'saved':
            potential = (coefficients[degree][:, None] * nodes).ravel()
            matter = coefficients[0][0] if degree == 0 else velocity
        else:
            values = []
            for mode, name in enumerate(names):
                if degree == 0 and name == 'I':
                    value = nodes * (.02 + .003 * np.exp(-nodes / 3) * np.sin(np.log(nodes + .2)))
                else:
                    value = nodes * .001 * np.exp(-nodes / 4) / (degree + 1) / (mode + 1)
                values.append(value)
            potential = np.concatenate(values).astype(complex)
            matter = .01 if degree == 0 else .0001
        initial = np.r_[potential, matter] if degree in [0, 1] else potential
        whitened = factor.T @ initial
        reference = nulls @ (nulls.T @ whitened)
        initial_coordinates = basis.T @ whitened
        equilibrium = linalg.solve_triangular(factor.T, reference, lower=False)
        states, defects = [], []
        for depth in times:
            defect = linalg.solve_triangular(factor.T, basis @ (np.exp(eigenvalues * depth) * initial_coordinates), lower=False)
            defects.append(defect)
            states.append(equilibrium + defect)
        states, defects = np.array(states), np.array(defects)
        scale = float(np.linalg.norm(initial_coordinates))
        entropy = .5 * np.einsum('ti,ij,tj->t', defects.conj(), metric, defects).real
        if len(invariants):
            invariant_error = float(np.max(abs(defects @ invariants.T)) / max(scale, 1e-30))
        else:
            invariant_error = 0.
        source_defect = full_stiffness @ defects[0]
        source_norm = float(np.linalg.norm(source_defect))
        source_balance = float(np.max(abs(invariants @ linalg.cho_solve((factor, True), source_defect)))) if len(invariants) else 0.
        check_scale = max(scale, np.linalg.norm(whitened) * 1e-10, 1e-30)
        checks.append(dict(name='degree' + str(degree) + ': analytic nulls agree with unmodified physical assembly', passed=null_error < 1e-9, value=null_error))
        checks.append(dict(name='degree' + str(degree) + ': conserved moments of evolving defect', passed=invariant_error < 1e-9, value=invariant_error))
        checks.append(dict(name='degree' + str(degree) + ': quadratic defect entropy nonincreasing',
                           passed=bool(np.max(np.diff(entropy)) < 1e-9 * check_scale ** 2)))
        checks.append(dict(name='degree' + str(degree) + ': opposite source moments',
                           passed=source_balance < 1e-9 * max(source_norm, 1e-20), value=source_balance,
                           source_norm=source_norm))
        details = dict(degree=degree, names=names, initial_entropy_defect=float(entropy[0]),
                       final_entropy_defect=float(entropy[-1]), minimum_reduced_eigenvalue=float(min(eigenvalues)),
                       maximum_reduced_eigenvalue=float(max(eigenvalues)),
                       analytic_equilibrium_coordinates_kept_not_fitted=True)
        if degree in [0, 1]:
            moments = invariants[-1, :-1]
            delta_photon = (defects[:, :-1] - defects[0, :-1]) @ moments
            delta_matter = capacity * (defects[:, -1] - defects[0, -1])
            transfer_scale = float(max(abs(delta_matter)))
            residual = float(max(abs(delta_photon + delta_matter)))
            details.update(plasma_initial_real=float(states[0, -1].real), plasma_final_real=float(states[-1, -1].real),
                           exchanged_matter_energy_or_momentum_scale=transfer_scale,
                           independent_photon_matter_transfer_residual=residual,
                           transfer_relative_error=residual / max(transfer_scale, 1e-30))
            if arguments.fixture == 'synthetic':
                checks.append(dict(name='degree' + str(degree) + ': transfer-size-normalized species exchange',
                                   passed=residual < .002 * transfer_scale, value=residual / transfer_scale, gate=.002))
        np.savez_compressed(folder / ('evolution-' + str(degree) + '.npz'), nodes=nodes, mass=mass, metric=metric,
                            initial=initial, equilibrium=equilibrium, times=times, states=states, defects=defects,
                            eigenvalues=eigenvalues, entropy=entropy, capacity=capacity,
                            initial_collision_covector=source_defect, invariants=invariants)
        inputs.append(path)
        rows.append(details)
    if arguments.fixture == 'saved':
        checks.append(dict(name='Saved parent tensor reconstructed in retained angular modes', passed=reconstruction < 1e-7, value=reconstruction))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        bank=arguments.bank, model=arguments.model, fixture=arguments.fixture, rows=rows,
                        chi=heat_capacity, inertia=inertia, duration_optical_depth=6.,
                        full_retained_polarization_blocks_evolved=True,
                        finite_heat_capacity_and_plasma_velocity_evolved=True,
                        thermal_background_frozen_local_patch_not_full_cosmological_evolution=True,
                        elapsed_seconds=time.perf_counter() - started), __file__, inputs)
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']],
                         heat_and_momentum=rows[:2], elapsed=time.perf_counter() - started)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--bank', required=True)
    parser.add_argument('--name', required=True)
    parser.add_argument('--model', choices=['heavy', 'cold'], default='heavy')
    parser.add_argument('--fixture', choices=['saved', 'synthetic'], default='saved')
    main(parser.parse_args())
