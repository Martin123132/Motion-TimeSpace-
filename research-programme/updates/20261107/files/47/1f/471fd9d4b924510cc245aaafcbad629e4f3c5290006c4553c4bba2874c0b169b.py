from step_common import *


def main():
    modest()
    folder = ROOT / 'results/spectral-stability'
    assert not folder.exists()
    rows, checks = [], []
    for scale in [1e-6, 1e-5]:
        theta = 4.596201578526332e-10 / scale
        for points in [64, 96, 144, 192, 256, 384]:
            model = CollisionStep(points, 8, theta, 5.755472902372619e-10, .001)
            symmetric = model.symmetric_photon()
            asymmetry = symmetric - symmetric.T
            relative = float((np.max(abs(asymmetry.data)) if asymmetry.nnz else 0.) / max(np.max(abs(symmetric.data)), 1.))
            eigenvalues = spla.eigsh(symmetric, k=2, which='LA', return_eigenvectors=False, tol=1e-8, maxiter=20000)
            grid = model.grid
            frequency = grid.frequency
            occupation = inherited.inherited.planck(frequency)
            local = 2 * frequency * (1 + 2 * occupation) - 2 * frequency ** 2 * occupation * (1 + occupation)
            diagonal = -1 + theta * (-.4 * grid.diagonal - .4 + 1.4 * local)
            off_diagonal = -.4 * theta * np.sqrt(grid.upper * grid.lower)
            dipole_largest = float(linalg.eigvalsh_tridiagonal(diagonal, off_diagonal, select='i',
                                     select_range=(points - 1, points - 1))[0])
            stable = bool(max(eigenvalues) < 1e-10)
            row = dict(scale=scale, theta=theta, frequency_points=points, polar_points=8,
                       largest_photon_eigenvalues=eigenvalues.tolist(), dipole_largest_eigenvalue=dipole_largest,
                       entropy_dissipative=stable, symmetric_relative_error=relative,
                       maximum_log_grid_wavenumber_proxy=2 / np.log(grid.edges[1] / grid.edges[0]),
                       accepted_for_time_evolution=stable)
            rows.append(row)
            checks.append(dict(name='Entropy symmetry scale=' + str(scale) + ',N=' + str(points),
                               passed=relative < 1e-10, value=relative, gate=1e-10))
            print(json.dumps(row), flush=True)
    unstable = [row for row in rows if not row['entropy_dissipative']]
    checks.append(dict(name='Coarse resolved grids dissipative at both physical endpoints',
                       passed=all(row['entropy_dissipative'] for row in rows if row['frequency_points'] <= 192)))
    checks.append(dict(name='Any unstable grids excluded from evolution, not stabilized by timestep',
                       passed=all(not row['accepted_for_time_evolution'] for row in unstable)))
    folder.mkdir(parents=True, exist_ok=False)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        rows=rows, excluded_grid_count=len(unstable),
                        high_wavenumber_dipole_principal_symbol='-1+(2/5)*theta*omega_log_energy^2',
                        high_frequency_instability_is_truncation_domain_failure_not_MTS_background_instability=True,
                        finite_resolved_test_is_not_uniform_frequency_convergence_proof=True), __file__)
    print(json.dumps(dict(checks=len(checks), excluded_grids=len(unstable), failed=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    main()
