from polarized_soft_pole import *
from gould_angles import marginal_eigenvalue


def main():
    modest()
    folder = ROOT / 'banks/polarized-singular104'
    folder.mkdir(parents=True, exist_ok=False)
    specification = dict(count=104, quadrature=700, minimum=1e-5, maximum=60., pivot=.1)
    basis = ConsistentBasis(**specification)
    frequency_mass = (basis.values.T * (basis.measure * basis.nodes ** 2)) @ basis.values
    checks, rows = [], []
    for degree in range(5):
        angular, names, normalization = weighted_angular(degree, 8)
        refined, _, _ = weighted_angular(degree, 12)
        checks.append(check('Scattering direction measure unit normalization l=' + str(degree), abs(normalization - 1), 1e-13))
        checks.append(check('Polarized soft angular quadrature l=' + str(degree), linalg.norm(angular - refined), 1e-12))
        eigenvalues = linalg.eigvalsh(refined)
        checks.append(check('Resolved soft angular pole dissipates l=' + str(degree), max(0., max(eigenvalues)), 1e-12))
        expected = (float(marginal_eigenvalue(1., degree)) - 1) / (2 * degree + 1)
        checks.append(check('Independent eikonal/Thomson intensity pole equals Gould l=' + str(degree), abs(refined[0, 0] - expected), 1e-13))
        coefficient = 2 * np.kron(refined, frequency_mass)
        template = np.r_[basis.temperature, np.zeros((len(names) - 1) * basis.count)]
        mass = linalg.block_diag(*([basis.mass / (2 * degree + 1)] * len(names)))
        rayleigh = float(-template @ coefficient @ template / (template @ mass @ template))
        predicted = 40 * math.pi ** 2 / 7 * (1 - float(marginal_eigenvalue(1., degree)))
        checks.append(check('Full coefficient matches Stage81 temperature moment l=' + str(degree), abs(rayleigh - predicted) / max(1., abs(predicted)), 1e-11))
        np.savez_compressed(folder / ('pole-' + str(degree) + '.npz'), angular=refined, frequency_mass=frequency_mass,
            real_coefficient=coefficient, virtual_coefficient=-coefficient, names=np.array(names), mass=mass)
        rows.append(dict(degree=degree, names=names, angular=refined.tolist(), temperature_rayleigh=rayleigh))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
        basis_spec=specification, formula='C_real,pole = [4alpha/(3pi)] theta_star^2/xmin * 2 A_l tensor M_x2; C_virtual,pole=-C_real,pole.',
        normalization_fitted=False, scalar_14_16_factor_not_part_of_exact_soft_theorem=True,
        complete_finite_radiative_operator=False), __file__,
        [ROOT / 'polarized_soft_pole.py', ROOT / 'sources/hep-ph-9308249.html', PARENT / 'gould_angles.py',
         BRANCH / 'polarized-heat-momentum-grid-20261007/grid_common.py', PARENT / 'results/resolved-infrared-asymptotic/status.json'])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']], rows=rows)), flush=True)


if __name__ == '__main__':
    main()
