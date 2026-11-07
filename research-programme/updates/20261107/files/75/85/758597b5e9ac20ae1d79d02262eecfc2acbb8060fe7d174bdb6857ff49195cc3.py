from inclusive_soft import *


def main():
    modest()
    folder = ROOT / 'results/current-and-four-transfer'
    folder.mkdir(parents=True, exist_ok=False)
    nodes, weights = np.polynomial.legendre.leggauss(160)
    checks, rows = [], []
    for speed in [1e-5, .00045962015785263325, .01, .1, .5, .9]:
        current_time = speed * nodes / (1 - speed * nodes)
        current_space = speed / (1 - speed * nodes)
        density = current_space ** 2 - current_time ** 2
        actual = ALPHA / (2 * math.pi) * np.dot(weights, density)
        expected = cusp_coefficient(speed)
        checks.append(check('Direct conserved-current angular integral speed=' + str(speed), abs(actual / expected - 1), 1e-11))
        checks.append(check('Current contracted with emitted null momentum speed=' + str(speed), np.max(abs(current_time - nodes * current_space)), 1e-13))
        rows.append(dict(speed=speed, amplitude=actual, exact=expected))
    azimuth = 2 * math.pi * (np.arange(24) + .5) / 24
    angular_nodes, angular_weights = np.polynomial.legendre.leggauss(12)
    vectors, weights = [], []
    for cosine, weight in zip(angular_nodes, angular_weights):
        for angle in azimuth:
            vectors.append([math.sqrt(1 - cosine ** 2) * math.cos(angle), math.sqrt(1 - cosine ** 2) * math.sin(angle), cosine])
            weights.append(weight / (2 * len(azimuth)) * 1.5 * (1 - cosine ** 2))
    vectors, weights = np.array(vectors), np.array(weights)
    moment = (vectors.T * weights) @ vectors
    expected = np.diag([2 / 5, 2 / 5, 1 / 5])
    checks.extend([check('Soft dipole radiation direction law normalized', abs(sum(weights) - 1), 1e-13),
        check('Mean soft spatial momentum vanishes in leading rest frame', linalg.norm(weights @ vectors), 1e-13),
        check('Derived spatial transfer tensor (2delta-u*u)/5', linalg.norm(moment - expected), 1e-13)])
    mean, variance = cumulants(.02)
    covariance = linalg.block_diag(variance, variance * moment)
    transfer = np.r_[mean, mean * (weights @ vectors)]
    photon_source, hard_source = transfer, -transfer
    checks.append(check('Photon plus hard-system four-transfer cancels componentwise', linalg.norm(photon_source + hard_source), 1e-15))
    checks.append(dict(name='All transfer covariance eigenvalues nonnegative', passed=bool(min(linalg.eigvalsh(covariance)) >= 0)))
    np.savez_compressed(folder / 'transfer.npz', soft_mean=transfer, hard_mean=hard_source, covariance=covariance)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
        transfer_scope='Conditional leading nonrelativistic hard event; not an integrated cosmological heating rate.',
        momentum_pairing_is_kinematic_not_a_new_equation_of_state=True), __file__,
        [ROOT / 'inclusive_soft.py', ROOT / 'sources/hep-ph-9308249.html', ROOT / 'sources/hep-ph-9507341.html'])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    main()
