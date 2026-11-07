import argparse
from mandl_skyrme import *
from gould_angles import correlations


def main(arguments):
    modest()
    mp.mp.dps = 70
    folder = ROOT / 'results' / arguments.name
    folder.mkdir(parents=True, exist_ok=False)
    nodes, weights = np.polynomial.legendre.leggauss(arguments.order)
    azimuth = 2 * math.pi * (np.arange(2 * arguments.order) + .5) / (2 * arguments.order)
    geometry = []
    for incident, incident_weight in zip(nodes, weights / 2):
        for companion, companion_weight in zip(nodes, weights / 2):
            for angle in azimuth:
                cosine_01 = incident * companion + math.sqrt((1 - incident ** 2) * (1 - companion ** 2)) * math.cos(angle)
                geometry.append((cosine_01, incident, companion, incident_weight * companion_weight / len(azimuth)))
    geometry = np.array(geometry)
    projections = np.array([[special.eval_legendre(degree, geometry[:, index]) for degree in range(7)] for index in range(3)])
    checks, rows = [], []
    started = time.perf_counter()
    for fraction in [.001, .01, .1, .25, .5]:
        expected = np.array([correlations(fraction, degree) for degree in range(7)]).T
        for energy in [1e-4, 1e-6]:
            kernel = np.array([differential_weight(energy, fraction, *angles[:3]) for angles in geometry])
            weighted = geometry[:, 3] * kernel
            actual = np.einsum('pln,n->pl', projections, weighted) / sum(weighted)
            error = float(np.max(abs(actual - expected)))
            checks.append(check('Full squared matrix element tends to all three analytic angular marginals share=' + str(fraction) + ' energy=' + str(energy), error, 5 * energy))
            rows.append(dict(fraction=fraction, energy=energy, maximum_absolute_moment_error=error,
                             incoming_soft=actual[1].tolist(), companion_soft=actual[2].tolist(), hard_pair=actual[0].tolist()))
            np.savez_compressed(folder / ('sample-' + str(fraction) + '-' + str(energy) + '.npz'),
                                geometry=geometry, kernel=kernel, actual=actual, expected=expected)
            print(json.dumps(dict(fraction=fraction, energy=energy, error=error, elapsed=time.perf_counter() - started)), flush=True)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
        order=arguments.order, arithmetic_decimal_places=70, rows=rows, elapsed=time.perf_counter() - started,
        normalization_fitted=False, comparison='Normalized angular moments; overall differential normalization tested separately.'), __file__,
        [ROOT / 'mandl_skyrme.py', ROOT / 'gould_angles.py', PARENT / 'sources/astro-ph-0611172.html',
         BRANCH / 'scaled-spectral-evolution-20261007/sources/2005.06941v1.html'])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--order', type=int, default=8)
    parser.add_argument('--name', default='full-matrix-marginals')
    main(parser.parse_args())
